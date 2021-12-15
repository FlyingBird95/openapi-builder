"""view_funcs are functions that return a Flask route."""

import pytest
from flask import jsonify

from openapi_builder import add_documentation


@pytest.fixture
def get_without_decorator(app):
    @app.route("/get_without_decorator")
    def get_without_decorator_func():
        return jsonify({"status": "OK"})

    return get_without_decorator_func


@pytest.fixture
def get_with_decorator(app):
    @app.route("/get_with_decorator")
    @add_documentation()
    def get_with_decorator_func():
        return jsonify({"status": "OK"})

    return get_with_decorator_func
