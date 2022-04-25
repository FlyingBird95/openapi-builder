"""Halogen route fixtures."""

import pytest
from flask import jsonify
from halogen import Schema, types, Attr

from openapi_builder import add_documentation


@pytest.fixture
def halogen_fields():
    return {"field": Attr(types.String())}


@pytest.fixture
def halogen_example_object():
    return {"field": "value"}


@pytest.fixture
def halogen_schema(halogen_fields):
    return Schema(**halogen_fields)


@pytest.fixture
def second_halogen_fields():
    return {"field": Attr(types.Int())}


@pytest.fixture
def second_halogen_example_object():
    return {"field": 42}


@pytest.fixture
def second_halogen_schema(second_halogen_fields):
    return Schema(**second_halogen_fields)


@pytest.fixture
def get_with_halogen_schema(app, halogen_schema, halogen_example_object):
    @app.route("/get_with_halogen_schema")
    @add_documentation(response=halogen_schema)
    def get_with_halogen_schema_func():
        return jsonify(halogen_schema.serialize(halogen_example_object))

    return get_with_halogen_schema_func


@pytest.fixture
def post_with_halogen_request_data(app, halogen_schema, halogen_example_object):
    @app.route("/post_with_halogen_request_data", methods=["POST"])
    @add_documentation(request_data=halogen_schema)
    def post_with_halogen_request_data_func():
        return jsonify({"status": "OK"})

    return post_with_halogen_request_data_func


@pytest.fixture
def put_with_halogen_request_query(app, halogen_schema, halogen_example_object):
    @app.route("/put_with_halogen_request_query", methods=["PUT"])
    @add_documentation(request_query=halogen_schema)
    def put_with_halogen_request_query():
        return jsonify({"status": "OK"})

    return put_with_halogen_request_query
