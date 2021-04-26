![codeql-analysis](https://github.com/aticie/ronnia-web/actions/workflows/codeql-analysis.yml/badge.svg)
![docker-build](https://img.shields.io/docker/cloud/build/eatici/ronnia-web)
<div align="center">

# ronnia-web - A Dashboard Interface for ronnia

</div>

**[ronnia](https://github.com/aticie/ronnia)** is a Twitch/osu! bot that sends beatmap requests from Twitch chat to the streamer's in-game messages.

ronnia-web displays the ronnia dashboard for user settings.

## Usage

You can check out ronnia dashboard at https://ronnia.me/

## Setup

To build frontend:

```shell
> npm install
> npm run build
```

Requirements for backend can be installed with:

`pip install fastapi uvicorn[standard] aiohttp aiofiles python-jose[cryptography]`

Required environment variables for running:

```
OSU_CLIENT_SECRET=****
OSU_CLIENT_ID=2408
TWITCH_CLIENT_ID=****
TWITCH_CLIENT_SECRET=****
OSU_REDIRECT_URI=http://localhost:8000/identify
TWITCH_REDIRECT_URI=http://localhost:8000/twitch_identify
SECRET_KEY = "****"  # Secret key required for encoding JWT token
ALGORITHM = "HS256"  # Algorithm for encoding JWT token
DB_DIR=mount
```

### Docker 🐳

#### Docker Hub releases

Releases from 1.1.0 and onwards are published to Docker hub automatically. 
[You can find the repository here.](https://hub.docker.com/r/eatici/ronnia-web)

Use the release tag you want to use in docker-compose with the given template. 

```yaml
...
services:
  ronnia-web:
    build: .
    image: eatici/ronnia-web:release-v1.x.x <- change the tag here!
```

To host the website locally:

`docker-compose up -d`
