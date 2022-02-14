Changelog
=========

All notable changes to openapi_builder will be documented here.

The format is based on `Keep a Changelog`_, and this project adheres to `Semantic Versioning`_.

.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html

Categories for changes are: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security**.

Unreleased
----------
Release date:

Version `0.2.7 <https://github.com/FlyingBird95/openapi-builder/tree/v0.2.7>`__
--------------------------------------------------------------------------------
Release date: 2022-02-15

- **Updated** :code:`add_documentation` arguments:

  - :code:`responses` is now :code:`response`, and accepts either a :code:`dict` or any value.
    In case any value is passed, it's converted into :code:`{200: <value>}`.
  - :code:`input_schema` renamed into :code:`request_data`.
  - :code:`query_schema` renamed into :code:`request_query`.


Version `0.2.6 <https://github.com/FlyingBird95/openapi-builder/tree/v0.2.6>`__
--------------------------------------------------------------------------------
Release date: 2022-02-12

- **Updated** converters, and how to register them. This can now be done via the :code:`Options`.

Version `0.2.5 <https://github.com/FlyingBird95/openapi-builder/tree/v0.2.5>`__
--------------------------------------------------------------------------------
Release date: 2022-02-06

- **Added** default converters: :code:`openapi_builder.converters.defaults`.
- **Added** :code:`set_resource_options` and :code:`set_schema_options`.
- **Changed** specification to use :code:`dataclass()`.

Version `0.2.4 <https://github.com/FlyingBird95/openapi-builder/tree/v0.2.4>`__
--------------------------------------------------------------------------------
Release date: 2022-01-09

- **Added** tag support per endpoint
- **Added** configuration page
- **Added** support for halogen_ (including example).
- **Added** class decorator for registering converters: :code:`openapi_builder.converters.base.register_converter`.
- **Removed** :code:`custom_converters` option to :code:`add_documentation`.
- **Changed** loading converters lazily.
- **Added** url parameter converters: :code:`openapi_builder.converters.parameter`.

.. _halogen: https://halogen.readthedocs.io/en/latest/


Version `0.2.0 <https://github.com/FlyingBird95/openapi-builder/tree/v0.2.0>`__
--------------------------------------------------------------------------------
Release date: 2021-12-09

- **Changed** interface to support the standard :code:`init_app` notation.
- **Fixed** broken marshmallow support.
- **Added** :code:`custom_converters` option to :code:`add_documentation`.
- **Added** example.
- **Added** documentation.

Version `0.1.0 <https://github.com/FlyingBird95/openapi-builder/tree/v0.1.0>`__
--------------------------------------------------------------------------------
Release date: 2021-11-17

- **Added** Continuous integration (automated tests)
- **Added** Continuous delivery (publishing to PyPI)
- **Added** Automatically formatting (black and isort)
- **Added** Checking formatting errors (flake8)
- **Added** Automatic documentation integration and delivery
- **Added** Initial code
