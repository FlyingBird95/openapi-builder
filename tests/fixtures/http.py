import json

import pytest
from flask import Flask, Response, url_for
from flask.testing import FlaskClient


class CustomResponse(Response):
    """Response object used by default in the API tests."""

    @property
    def parsed_data(self):
        """Parsed the response data."""
        data = self.get_data().decode(self.mimetype_params.get("charset", "utf-8"))
        if data == "" or data is None:
            return

        if self.mimetype == "application/json":
            return json.loads(data)

        raise ValueError("Mimetype is not supported")


class TestClient(FlaskClient):
    """App test client."""

    def make_uri(self, *args, **kwargs):
        """Reverse the URL in the application context.

        :note: Requires SERVER_NAME to be defined in the configuration.
        """
        with self.application.app_context():
            return url_for(*args, _external=False, **kwargs)


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SERVER_NAME"] = "127.0.0.1"
    app.config["DEBUG"] = True
    app.test_client_class = TestClient
    app.response_class = CustomResponse
    return app


@pytest.fixture
def http(app):
    """Flask test client."""
    with app.test_client() as client:
        yield client
