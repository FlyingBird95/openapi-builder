#############
Configuration
#############
Once you have successfully installed the :code:`openapi_builder` package, it's time to properly configure it such
that it suits your needs. The configuration consist of the following two steps:

1. :ref:`configuring`
2. :ref:`adding_resources`

In case you are using blueprints in your application, we recommend you to read the :ref:`resource_defaults` section. If
you are using custom marshmallow_ attributes, then we recommend you to read the :ref:`processing_resources` section.

.. _configuring:

*************************
Configuring the extension
*************************
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
       :code:`DocumentationOptions()` will be created and used. For all possible values, see the :ref:`documentation_options` section.

.. _openapi_specification_version: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#oasVersion

.. _documentation_options:

Documentation options
=====================
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
   * - :code:`request_content_type`
     - :code:`str`
     - :code:`"application/json"`
     - The content type used for requests throughout the entire application.
   * - :code:`response_content_type`
     - :code:`str`
     - :code:`"application/json"`
     - The content type used for responses throughout the entire application.
   * - :code:`schema_converter_classes`
     - :code:`List[Type[SchemaConverter]]`
     - :code:`[]`
     - See :ref:`schema_converters` for more info about this option.
   * - :code:`defaults_converter_classes`
     - :code:`List[Type[DefaultsConverter]]`
     - :code:`[]`
     - See :ref:`defaults_converters` for more info about this option.
   * - :code:`parameter_converter_classes`
     - :code:`List[Type[ParameterConverter]]`
     - :code:`[]`
     - See :ref:`parameter_converters` for more info about this option.

.. _marshmallow: https://github.com/marshmallow-code/marshmallow
.. _halogen: https://halogen.readthedocs.io/en/latest/

.. _adding_resources:

****************
Adding resources
****************
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
   * - :code:`tags`
     - :code:`Optional[List[str]]`
     - :code:`None`
     - Optional list of strings that represent the endpoint. A typical value for this argument is the name of the
       resource where this endpoint belongs to. Tags are also used by the documentation UI to group related endpoints
       (with the same tags) together.


.. _parameter: https://flyingbird95.github.io/openapi-builder/source/packages/openapi_builder.specification.html#openapi_builder.specification.Parameter
.. _schema: https://flyingbird95.github.io/openapi-builder/source/packages/openapi_builder.specification.html#openapi_builder.specification.Schema


.. _processing_resources:

********************
Processing resources
********************
An important feature that the openapi_builder offers it to ability to process custom attributes for your schema. Custom
attributes can be processed by custom converters. There are three types of custom converters:

- :ref:`schema_converters`
- :ref:`defaults_converters`
- :ref:`parameter_converters`


.. _schema_converters:

Schema converters
=================
Schema converters can be used to convert custom fields in your schema to SchemaObjects_. Suppose you have the
following custom field (taken from the `Marshmallow doc <marshmallow_doc_>`_):

.. _SchemaObjects: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#schemaObject
.. _marshmallow_doc: https://marshmallow.readthedocs.io/en/stable/custom_fields.html

.. code:: python

    from marshmallow import fields, Schema, ValidationError


    class PinCode(fields.Field):
        """Field that serializes to a string of numbers and deserializes
        to a list of numbers.
        """

        def _serialize(self, value, attr, obj, **kwargs):
            if value is None:
                return ""
            return "".join(str(d) for d in value)

        def _deserialize(self, value, attr, data, **kwargs):
            try:
                return [int(c) for c in value]
            except ValueError as error:
                raise ValidationError("Pin codes must contain only digits.") from error


    class UserSchema(Schema):
        name = fields.String()
        email = fields.String()
        created_at = fields.DateTime()
        pin_code = PinCode()


When :code:`OpenAPIBuilder` is trying to generate the documentation for your :code:`UserSchema`-class, it doesn't know
how to generate the documentation for the :code:`PinCode` class. In order to configure a schema converter for the
:code:`OpenAPIBuilder`, you'll need to create a custom converter class:

.. code:: python

    from openapi_builder.converters.schema.base import SchemaConverter
    from openapi_builder.specification import Schema


    class PinCodeConverter(SchemaConverter):
        converts_class = PinCode

        def convert(self, value, name) -> Schema:
            return Schema(type="int", format="pincode", example=1234)


This :code:`PinCodeConverter` can be passed to the :code:`OpenAPIBuilder` via the :code:`DocumentationOptions`:

.. code:: python

    from flask import Flask
    from openapi_builder import OpenApiDocumentation, DocumentationOptions

    app = Flask(__name__)

    documentation = OpenApiDocumentation(
        app=app,
        options=DocumentationOptions(
            schema_converter_classes=[PinCodeConverter],
        ),
    )

Note that the class should be passed, and not an instance.


.. _defaults_converters:

Defaults converters
===================
Suppose we have the following marshmallow_ schema:

.. code:: python

    from datetime import datetime

    from marshmallow import fields, Schema


    class RegisterSchema(Schema):
        name = fields.String()
        email = fields.String()
        created_at = fields.DateTime(dump_default=lambda: datetime.now())


This would be problematic for the :code:`OpenAPIBuilder`, since :code:`datetime` is not JSON-serializable.
As a consequence, the documentation can't be generated for this type.

By using a defaults converter, this issue can be overcome. A defaults converter for a :code:`datetime`  might look
like this:

.. code:: python

    from datetime import datetime

    from marshmallow import fields
    from openapi_builder.converters.defaults.base import DefaultsConverter


    class DateTimeConverter(DefaultsConverter):
        converts_class = datetime

        def convert(self, value) -> Any:
            return fields.DateTime()._serialize(value=value, attr="", obj={})


Thus, we are using the power of Marshmallow to serialize the default datetime value. This :code:`DateTimeConverter`
can be passed to the :code:`OpenAPIBuilder` via the :code:`DocumentationOptions`:

.. code:: python

    from flask import Flask
    from openapi_builder import OpenApiDocumentation, DocumentationOptions

    app = Flask(__name__)

    documentation = OpenApiDocumentation(
        app=app,
        options=DocumentationOptions(
            defaults_converter_classes=[DateTimeConverter],
        ),
    )

Note that the class should be passed, and not an instance.


.. _parameter_converters:

Parameter converters
====================
Flask allows custom validators to be passed for an endpoint_. This allows you to do the following:

.. _endpoint: https://stackoverflow.com/questions/19261833/what-is-an-endpoint-in-flask

.. code:: python

    from http import HTTPStatus

    from flask import abort, Flask
    from werkzeug.routing import BaseConverter


    class UUIDValidator(BaseConverter):
        """Validates the `UID` bit of the route."""

        def to_python(self, value):
            """Check if the value is a valid `UID`."""
            try:
                return uuid.UUID(value).hex
            except ValueError:
                abort(HTTPStatus.BAD_REQUEST, f"Invalid UID {value}")


    app = Flask(__name__)

    app.url_map.converters["uid"] = validators.UUIDValidator


    @app.get("/pet/<uid:uid>")
    @serialization.serialize(schema.Pet)
    def get(uid):
        ...

This would be problematic for the :code:`OpenAPIBuilder`, since it doesn't know how to generate documentation for
:code:`uid`: path params.  As a consequence, the documentation can't be generated for this type.

By using a parameter converter, this issue can be overcome. A parameter converter for a :code:`uid` might look like this:

.. code:: python

    import uuid

    from openapi_builder.converters.parameter.base import ParameterConverter
    from openapi_builder.specification import Schema


    class UUIDConverter(ParameterConverter):
        converts_class = UUIDValidator

        @property
        def schema(self) -> Schema:
            return Schema(type="string", format="hex", example=uuid.uuid4().hex)


This :code:`UUIDConverter` can be passed to the :code:`OpenAPIBuilder` via the :code:`DocumentationOptions`:

.. code:: python

    from flask import Flask
    from openapi_builder import OpenApiDocumentation, DocumentationOptions

    app = Flask(__name__)

    documentation = OpenApiDocumentation(
        app=app,
        options=DocumentationOptions(
            parameter_converter_classes=[UUIDConverter],
        ),
    )

Note that the class should be passed, and not an instance.

.. _resource_defaults:

******************************
Resource defaults (blueprints)
******************************
It is common practice to group several Flask related resources together in a Blueprint_. Blueprints can greatly
simplify how large applications work and provide a central means for Flask extensions to register operations on
applications. Take for example the petstore_ example, which is an API with three resources: :code:`pet`, :code:`store`
and :code:`user`. This API could be designed using three blueprints, one for each resource. The :code:`pet` resource
might look the following:

.. code:: python

    from flask import Blueprint

    blueprint = Blueprint(
        name="pet",
        import_name=__name__,
        url_prefix="/pet",
    )

    from . import upload_image, post, put, find_by_status, find_by_tags, get, post, delete

All these endpoints would use the same :code:`Tag`, which groups them under the :code:`pet` resource. It would bad
design to copy this tag for all endpoints, and therefore defaults can be configured on the :code:`blueprint` variable:

.. code:: python

    from openapi_builder import set_resource_options
    from openapi_builder.specification import Tag

    set_resource_options(
        resource=blueprint,
        tags=[Tag(name="Pet", description="A description for the pet resource.")],
    )

The following configuration options are applicable for passing to :code:`set_resource_options`:

.. list-table::
   :widths: 15 15 15 55
   :header-rows: 1

   * - Argument
     - Type
     - Default value
     - Explanation
   * - :code:`resource`
     - :code:`Blueprint`
     - :code:`<no-default>`
     - The resource for which defaults need to be configured.
   * - :code:`tags`
     - :code:`Optional[List[Union[str, Tag]]]`
     - :code:`None`
     - A list of :code:`openapi_builder.specification.Tag` objects to hold default tags for each endpoint in the
       resource.


.. _Blueprint: https://flask.palletsprojects.com/en/2.0.x/blueprints/
.. _petstore: https://petstore.swagger.io/
