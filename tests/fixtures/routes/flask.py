import pytest
from flask import Blueprint, jsonify

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


@pytest.fixture
def user_blueprint():
    return Blueprint(
        name="users",
        import_name=__name__,
        url_prefix="/users",
    )


@pytest.fixture
def get_user_with_decorator(user_blueprint):
    @user_blueprint.route("/get_user")
    @add_documentation()
    def get_user_func():
        return jsonify({"user": "abc"})

    return get_user_func
