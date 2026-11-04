#!/usr/bin/env python3
"""Exercise the built nginx image against disposable DNS and HTTP/TLS servers."""
import argparse
import http.client
import http.server
import json
import os
from pathlib import Path
import socket
import ssl
import struct
import subprocess
import sys
import tempfile
import threading
import time
import uuid

HOST = "backend.railway.internal"


def fixture(mode):
    if mode == "dns":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 53))
        while True:
            request, peer = sock.recvfrom(4096)
            end = 12
            labels = []
            while request[end]:
                size = request[end]
                labels.append(request[end + 1:end + 1 + size].decode())
                end += size + 1
            end += 1
            kind, _ = struct.unpack("!HH", request[end:end + 4])
            question = request[12:end + 4]
            address = json.loads(Path("/fixture/dns.json").read_text()).get("address")
            found = ".".join(labels) == HOST and address is not None
            answer = b""
            if found and kind == 1:
                answer = b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 1, 4) + socket.inet_aton(address)
            flags = 0x8180 if found else 0x8183
            header = request[:2] + struct.pack("!HHHHH", flags, 1, int(bool(answer)), 0, 0)
            sock.sendto(header + question + answer, peer)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            body = json.dumps({
                "backend": os.environ["BACKEND_ID"],
                "path": self.path,
                "host": self.headers.get("Host"),
                "sni": getattr(self.connection, "sni", None),
                "origin": self.headers.get("Origin"),
                "referer": self.headers.get("Referer"),
                "cookie": self.headers.get("Cookie"),
            }).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Set-Cookie", "fixture=ok; Path=/; HttpOnly; SameSite=Lax")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_args):
            pass

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("/fixture/cert.pem", "/fixture/key.pem")
    context.set_servername_callback(lambda sock, name, _context: setattr(sock, "sni", name))
    for port in (80, 8080, 443, 8443):
        server = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
        if port in (443, 8443):
            server.socket = context.wrap_socket(server.socket, server_side=True)
        threading.Thread(target=server.serve_forever, daemon=True).start()
    threading.Event().wait()


def check_image(image, fixture_image):
    prefix = "ronnia-dns-" + uuid.uuid4().hex[:10]
    containers = []

    def docker(*args):
        return subprocess.check_output(["docker", *args], text=True).strip()

    def inspect(name, expression):
        return docker("inspect", "--format", expression, name)

    with tempfile.TemporaryDirectory(prefix=prefix) as directory:
        work = Path(directory)
        script = Path(__file__).resolve()

        def dns(address):
            target = work / "dns.json"
            temporary = work / "dns.next"
            temporary.write_text(json.dumps({"address": address}))
            temporary.replace(target)

        def run(name, target_image, *args, command=()):
            containers.append(name)
            docker("run", "--detach", "--name", name, "--network", prefix,
                   *args, target_image, *command)
            return name

        def fixture_args():
            return ("--volume", f"{work}:/fixture:ro", "--volume", f"{script}:/test.py:ro")

        def address(name):
            return inspect(name, "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}")

        def request(port, path, headers=None):
            connection = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
            try:
                connection.request("GET", path, headers=headers or {})
                response = connection.getresponse()
                return response.status, dict(response.getheaders()), response.read()
            finally:
                connection.close()

        def eventually(description, operation, predicate, seconds=25):
            deadline = time.monotonic() + seconds
            last = None
            while time.monotonic() < deadline:
                try:
                    last = operation()
                    if predicate(last):
                        return last
                except (OSError, http.client.HTTPException, json.JSONDecodeError) as error:
                    last = str(error)
                time.sleep(0.25)
            raise AssertionError(f"{description}: {last!r}")

        docker("image", "inspect", image)
        docker("pull", fixture_image)
        subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                        "-keyout", str(work / "key.pem"), "-out", str(work / "cert.pem"),
                        "-days", "1", "-subj", f"/CN={HOST}"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dns(None)
        docker("network", "create", prefix)
        try:
            backends = [run(f"{prefix}-{label}", fixture_image, *fixture_args(),
                            "--env", f"BACKEND_ID={label}", command=("python", "/test.py", "fixture", "upstream"))
                        for label in ("a", "b")]
            dns_server = run(f"{prefix}-dns", fixture_image, *fixture_args(),
                             command=("python", "/test.py", "fixture", "dns"))
            dns_ip = address(dns_server)
            for index, (scheme, suffix) in enumerate((
                ("http", ""), ("http", ":8080"),
                ("https", ""), ("https", ":8443"),
            )):
                dns(None)
                frontend = run(f"{prefix}-web-{index}", image,
                               "--dns", dns_ip, "--publish", "127.0.0.1::80",
                               "--env", f"API_UPSTREAM={scheme}://{HOST}{suffix}")
                local_port = int(json.loads(inspect(frontend, "{{json .NetworkSettings.Ports}}"))["80/tcp"][0]["HostPort"])
                started = inspect(frontend, "{{.State.StartedAt}}")
                eventually("frontend serves static content despite NXDOMAIN", lambda: request(local_port, "/"),
                           lambda result: result[0] == 200)
                assert request(local_port, "/api/probe")[0] == 502
                for path in ("/api/internal/", "/api/internal/secret?x=1", "/api/%69nternal/secret"):
                    assert request(local_port, path)[0] == 404, path
                dns(address(backends[0]))
                headers = {"Origin": "https://dashboard.example", "Referer": "https://dashboard.example/settings",
                           "Cookie": "session=synthetic"}
                path = "/api/echo/a%20b?x=one%2Ftwo&x=3"

                def echo():
                    status, response_headers, body = request(local_port, path, headers)
                    return status, response_headers, json.loads(body) if status == 200 else body.decode()

                def is_backend(result, backend):
                    return result[0] == 200 and result[2]["backend"] == backend

                first = eventually("DNS recovery without restart", echo, lambda result: is_backend(result, "a"))
                assert first[2] == {"backend": "a", "path": path.removeprefix("/api"),
                                    "host": HOST + suffix, "sni": HOST if scheme == "https" else None,
                                    "origin": headers["Origin"], "referer": headers["Referer"],
                                    "cookie": headers["Cookie"]}, first
                assert first[1]["Set-Cookie"] == "fixture=ok; Path=/; HttpOnly; SameSite=Lax"
                dns(address(backends[1]))
                second = eventually("DNS address change without restart", echo, lambda result: is_backend(result, "b"))
                assert second[2] == {**first[2], "backend": "b"}, second
                # Stop the old address, proving continued traffic is not accidentally using it.
                docker("stop", backends[0])
                assert is_backend(echo(), "b")
                docker("start", backends[0])
                root = request(local_port, "/api/?root=1")
                assert root[0] == 200 and json.loads(root[2])["path"] == "/?root=1", root
                if index == 0:
                    dns(None)
                    docker("stop", backends[1])
                    eventually("runtime DNS/backend outage", lambda: request(local_port, "/api/probe"),
                               lambda result: result[0] == 502)
                    assert request(local_port, "/")[0] == 200
                    docker("start", backends[1])
                    dns(address(backends[1]))
                    eventually("runtime DNS/backend recovery", echo, lambda result: is_backend(result, "b"))
                assert inspect(frontend, "{{.State.StartedAt}}") == started
                assert inspect(frontend, "{{.RestartCount}}") == "0"
                print(f"PASS {scheme}://{HOST}{suffix}: NXDOMAIN startup/recovery, DNS a→b, Host/SNI, URI/query, cookies/origins, internal block; no restart", flush=True)
                docker("rm", "--force", frontend)
                containers.remove(frontend)

            for value in (f"http://{HOST}:80", f"https://{HOST}:443", "http://127.0.0.1:0080", "https://[::1]", "http://[::1]:8080"):
                docker("run", "--rm", "--env", f"API_UPSTREAM={value}", image, "nginx", "-t")
            for value in ("ftp://backend", "http://backend/path", "https://user:pass@backend", "http://backend?x=1", "http://backend:0", "http://backend:65536", "http://backend:", "http://backend;", "http://backend:80:90"):
                result = subprocess.run(["docker", "run", "--rm", "--env", f"API_UPSTREAM={value}", image, "nginx", "-t"], capture_output=True)
                assert result.returncode != 0, value
                assert b"API_UPSTREAM must be" in result.stderr, (value, result.stderr)
            print("PASS explicit default ports, IPv4/bracketed IPv6, invalid upstream rejection", flush=True)
        except BaseException:
            for container in containers:
                subprocess.run(["docker", "logs", "--tail", "40", container], check=False)
            raise
        finally:
            if containers:
                docker("rm", "--force", *containers)
            docker("network", "rm", prefix)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fixture":
        fixture(sys.argv[2])
    else:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--image", default="ronnia-web:ci")
        parser.add_argument("--fixture-image", default="python:3.13-alpine")
        args = parser.parse_args()
        check_image(args.image, args.fixture_image)
