"""Marshmallow route fixtures."""

import pytest
from flask import jsonify
from marshmallow import Schema, fields

from openapi_builder import add_documentation


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
    @add_documentation(response=marshmallow_schema())
    def get_with_marshmallow_schema_func():
        return jsonify(marshmallow_schema().dump(marshmallow_example_object))

    return get_with_marshmallow_schema_func


@pytest.fixture
def post_with_marshmallow_request_data(
    app, marshmallow_schema, marshmallow_example_object
):
    @app.route("/post_with_marshmallow_request_data", methods=["POST"])
    @add_documentation(request_data=marshmallow_schema)
    def post_with_marshmallow_request_data_func():
        return jsonify({"status": "OK"})

    return post_with_marshmallow_request_data_func


@pytest.fixture
def put_with_marshmallow_request_query(
    app, marshmallow_schema, marshmallow_example_object
):
    @app.route("/put_with_marshmallow_request_query", methods=["PUT"])
    @add_documentation(request_query=marshmallow_schema)
    def put_with_marshmallow_request_query():
        return jsonify({"status": "OK"})

    return put_with_marshmallow_request_query
