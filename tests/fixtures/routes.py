"""Route fixtures."""
from http import HTTPStatus

import pytest
from flask import jsonify
from marshmallow import Schema, fields

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
def marshmallow_fields():
    return {"field": fields.String()}


@pytest.fixture
def marshmallow_example_object():
    return {"field": "value"}


@pytest.fixture
def marshmallow_schema(marshmallow_fields):
    return Schema.from_dict(marshmallow_fields)


@pytest.fixture
def get_with_marshmallow_schema(app, marshmallow_schema, marshmallow_example_object):
    @app.route("/get_with_marshmallow_schema")
    @add_documentation(responses={HTTPStatus.OK: marshmallow_schema()})
    def get_with_marshmallow_schema_func():
        return jsonify(marshmallow_schema().dump(marshmallow_example_object))

    return get_with_marshmallow_schema_func


@pytest.fixture
def post_with_marshmallow_input_schema(
    app, marshmallow_schema, marshmallow_example_object
):
    @app.route("/post_with_marshmallow_input_schema", methods=["POST"])
    @add_documentation(input_schema=marshmallow_schema)
    def post_with_marshmallow_input_schema_func():
        return jsonify({"status": "OK"})

    return post_with_marshmallow_input_schema_func


@pytest.fixture
def put_with_marshmallow_query_schema(
    app, marshmallow_schema, marshmallow_example_object
):
    @app.route("/put_with_marshmallow_query_schema", methods=["PUT"])
    @add_documentation(query_schema=marshmallow_schema)
    def put_with_marshmallow_query_schema():
        return jsonify({"status": "OK"})

    return put_with_marshmallow_query_schema
