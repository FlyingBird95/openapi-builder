Configuration
=============
Once you have successfully installed the :code:`openapi_builder` package, it's time to properly configure it such
that it suits your needs. The configuration consist of the following two steps:

- :ref:`Configuring the extension`
- :ref:`Adding resources`

Configuring the extension
~~~~~~~~~~~~~~~~~~~~~~~~~
The extension can be added to the Flask app using the following snippet.

.. code:: python

    from flask import Flask
    from openapi_builder import OpenApiDocumentation

    app = Flask(__name__)

    documentation = OpenApiDocumentation(app=app)


It is also possible to bind the :code:`app` in a later stage. This can be achieved using the following snippet.

.. code:: python

    from flask import Flask
    from openapi_builder import OpenApiDocumentation

    documentation = OpenApiDocumentation()

    app = Flask(__name__)
    documentation.init_app(app)

The following configuration options are applicable for passing to :code:`OpenApiDocumentation`.

.. list-table::
   :widths: 15 15 15 55
   :header-rows: 1

   * - Argument
     - Type
     - Default value
     - Explanation
   * - :code:`app`
     - :code:`Optional[Flask]`
     - :code:`None`
     - The Flask application for iterating the endpoints to find out the documentation. It not passed directly, it must
       be passed via the :code:`init_app` function.
   * - :code:`title`
     - :code:`str`
     - :code:`"Open API REST documentation"`
     - The title of the API.
   * - :code:`version`
     - :code:`str`
     - :code:`"1.0.0"`
     - The version of the OpenAPI document (which is distinct from the
       `OpenAPI Specification version <openapi_specification_version_>`_ or the API implementation version).
   * - :code:`options`
     - :code:`Optional[DocumentationOptions]`
     - :code:`None`
     - Additional optional documentation options that are global for the entire app. If not specified, a new
       :code:`DocumentationOptions()` will be created and used. For all possible values, see the :ref:`Documentation options` section.

.. _openapi_specification_version: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#oasVersion

Documentation options
*********************
The following options are applicable for passing to :code:`DocumentationOptions`. This class can be imported using the
following line:

.. code:: python

    from openapi_builder import DocumentationOptions


.. list-table::
   :widths: 15 15 15 55
   :header-rows: 1

   * - Argument
     - Type
     - Default value
     - Explanation
   * - :code:`include_head_response`
     - :code:`bool`
     - :code:`True`
     - Whether the HEAD operation is included in the documentation. By default, a Flask endpoint automatically exposes
       the HEAD operation. Since this is often not very useful, it is advised to remove it from the documentation.
   * - :code:`include_options_response`
     - :code:`bool`
     - :code:`True`
     - Whether the OPTIONS operation is included in the documentation. By default, a Flask endpoint automatically
       exposes the OPTIONS operation. Since this is often not very useful, it is advised to remove it from the
       documentation.
   * - :code:`server_url`
     - :code:`str`
     - :code:`"/"`
     - A URL to the target host. This URL supports Server Variables and MAY be relative, to indicate that the host
       location is relative to the location where the OpenAPI document is being served. Variable substitutions will be
       made when a variable is named in {brackets}.
   * - :code:`include_marshmallow_converters`
     - :code:`bool`
     - :code:`True`
     - Whether default marshmallow converters are included in the :code:`OpenAPIBuilder`. In case a different
       serialization library than marshmallow_ is used, this value must be set to :code:`False`.
   * - :code:`include_halogen_converters`
     - :code:`bool`
     - :code:`False`
     - Whether default halogen converters are included in the :code:`OpenAPIBuilder`. In case a different
       serialization library than halogen_ is used, this value must be set to :code:`False`.
   * - :code:`include_documentation_blueprint`
     - :code:`bool`
     - :code:`True`
     - Whether a documentation blueprint is exposed in the Flask application. This blueprint contains two endpoints.
       One for exposing the documentation UI, and one for exposing the documentation configuration (data collected by
       inspecting all endpoints). If a custom documentation UI is used, the value must be set to :code:`False`.
   * - :code:`strict_mode`
     - :code:`DocumentationOptions.StrictMode`
     - :code:`DocumentationOptions.StrictMode.SHOW_WARNINGS`
     - Whether something unforeseen happened, should the extension crash (preferred in testing), using
       :code:`DocumentationOptions.StrictMode.FAIL_ON_ERROR` or only print out warnings, using
       :code:`DocumentationOptions.StrictMode.SHOW_WARNINGS`.

.. _marshmallow: https://github.com/marshmallow-code/marshmallow
.. _halogen: https://halogen.readthedocs.io/en/latest/

Adding resources
~~~~~~~~~~~~~~~~
Resources can be exposed by adding the :code:`add_documentation` decorator to the corresponding endpoint. The following
options are applicable for passing to the function. This decorator can be imported using the following line:

.. code:: python

    from openapi_builder import add_documentation


.. list-table::
   :widths: 15 15 15 55
   :header-rows: 1

   * - Argument
     - Type
     - Default value
     - Explanation
   * - :code:`responses`
     - :code:`Optional[Dict[Union[HTTPStatus, int], Any]]`
     - :code:`None`
     - A dictionary from :code:`HTTPStatus` (passing the status code as an :code:`int` is also supported) to the class
       that is serialized. A converter must be registered in the :code:`OpenAPIBuilder` for all values of the
       dictionary, including the attributes of the schemas that it serializes. Otherwise a :code:`MissingConverter`
       exception is raised. An example of this argument is:
       :code:`{HTTPStatus.OK: UserSchema(many=True), HTTPStatus.NOT_FOUND: ErrorSchema()}`
   * - :code:`input_schema`
     - :code:`Optional[Any]`
     - :code:`None`
     - This argument is similar to the :code:`responses`, except that this class/value is used for deserializing data
       as the input of the endpoint. A converter must be registered in the :code:`OpenAPIBuilder` for the specified
       value, including the attributes of the schemas that it deserializes. Otherwise a :code:`MissingConverter`
       exception is raised.
   * - :code:`parameters`
     - :code:`Optional[List[Parameter]]`
     - :code:`None`
     - A list of parameters that the endpoint uses. Parameters can be query-arguments,
       header-values, path-values or cookies. See the parameter_ documentation for more info about the
       :code:`Parameter`. This class can be imported using:
       :code:`from openapi_builder.specification import Parameter`.
   * - :code:`summary`
     - :code:`Optional[str]`
     - :code:`None`
     - A short summary of what the operation does.
   * - :code:`description`
     - :code:`Optional[str]`
     - :code:`None`
     - A verbose explanation of the operation behavior. CommonMark syntax MAY be used for rich text representation.
   * - :code:`custom_converters`
     - :code:`Optional[Dict[str, Schema]]`
     - :code:`None`
     - A dictionary for describing custom attributes within a serialization class. This is illustrated in example 2.
       Note that the value of the dictionary must be a :code:`Schema` class. See the schema_ documentation for more info
       about :code:`Schema`. This class can be imported using:
       :code:`from openapi_builder.specification import Schema`.
   * - :code:`tags`
     - :code:`Optional[List[str]]`
     - :code:`None`
     - Optional list of strings that represent the endpoint. A typical value for this argument is the name of the
       resource where this endpoint belongs to. Tags are also used by the documentation UI to group related endpoints
       (with the same tags) together.


.. _parameter: https://flyingbird95.github.io/openapi_builder/source/packages/openapi_builder.specification.html#openapi_builder.specification.Parameter
.. _schema: https://flyingbird95.github.io/openapi_builder/source/packages/openapi_builder.specification.html#openapi_builder.specification.Schema
