import json

import pytest
from flask import Flask, Response


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


@pytest.fixture
def app():
    app = Flask(__name__)
    app.response_class = CustomResponse
    return app


@pytest.fixture
def http(app):
    """Flask test client."""
    with app.test_client() as client:
        yield client
