import os
import shutil
import unittest
import urllib.parse
from unittest.mock import patch

from fastapi.testclient import TestClient


class TestApi(unittest.TestCase):

    @classmethod
    @patch.dict(os.environ, {'DB_DIR': os.path.join(os.getcwd(), 'tests', 'data')})
    def setUpClass(cls) -> None:
        test_db_path = os.path.join(os.getcwd(), 'tests', 'data', 'users_test.db')
        db_path = os.path.join(os.getcwd(), 'tests', 'data', 'users.db')
        if os.path.exists(db_path):
            os.remove(db_path)
        shutil.copyfile(test_db_path, db_path)

        from backend.api import app
        cls.client = TestClient(app)

    def test_api_read_root_returns_200_status_code(self):
        expected_status_code = 200
        response = self.client.get("/")
        self.assertEqual(expected_status_code, response.status_code)

    def test_api_read_root_returns_307_status_code_when_redirects_are_not_allowed(self):
        expected_status_code = 307
        response = self.client.get("/", allow_redirects=False)
        self.assertEqual(expected_status_code, response.status_code)

    @patch.dict(os.environ, {'OSU_CLIENT_ID': 'test_client_id',
                             'OSU_REDIRECT_URI': 'test_redirect_uri',
                             })
    def test_api_osu_authorize_returns_307_status_code_when_redirects_are_not_allowed(self):
        expected_status_code = 307
        response = self.client.get("/osu_authorize", allow_redirects=False)
        self.assertEqual(expected_status_code, response.status_code)

    @patch.dict(os.environ, {'OSU_CLIENT_ID': 'test_client_id',
                             'OSU_REDIRECT_URI': 'test_redirect_uri',
                             })
    def test_api_osu_authorize_redirect_url_contains_required_parameters(self):
        expected_parameters = {'client_id': ['test_client_id'],
                               'redirect_uri': ['test_redirect_uri'],
                               'response_type': ['code'],
                               'scope': ['identify']}
        response = self.client.get("/osu_authorize", allow_redirects=False)
        redirect_url = response.headers["location"]
        parsed_url = urllib.parse.urlparse(redirect_url)
        returned_parameters = urllib.parse.parse_qs(parsed_url.query)

        self.assertDictEqual(expected_parameters, returned_parameters)

    @patch.dict(os.environ, {'TWITCH_CLIENT_ID': 'test_client_id',
                             'TWITCH_REDIRECT_URI': 'test_redirect_uri',
                             })
    def test_api_osu_authorize_returns_307_status_code_when_redirects_are_not_allowed(self):
        expected_status_code = 307
        response = self.client.get("/twitch_authorize", allow_redirects=False)
        self.assertEqual(expected_status_code, response.status_code)

    @patch.dict(os.environ, {'TWITCH_CLIENT_ID': 'test_client_id',
                             'TWITCH_REDIRECT_URI': 'test_redirect_uri',
                             })
    def test_api_osu_authorize_redirect_url_contains_required_parameters(self):
        expected_parameters = {'client_id': ['test_client_id'],
                               'redirect_uri': ['test_redirect_uri'],
                               'response_type': ['code'],
                               'scope': ['user:read:email']}
        response = self.client.get("/twitch_authorize", allow_redirects=False)
        redirect_url = response.headers["location"]
        parsed_url = urllib.parse.urlparse(redirect_url)
        returned_parameters = urllib.parse.parse_qs(parsed_url.query)

        self.assertDictEqual(expected_parameters, returned_parameters)
