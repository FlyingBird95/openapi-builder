##########
Exceptions
##########

The following exceptions can be encountered during the configuration of the :code:`openapi_builder` package:


- :ref:`missing_converter`
- :ref:`missing_parameter_converter`
- :ref:`missing_default_converter`
- :ref:`missing_config_context`

.. _missing_converter:

****************
MissingConverter
****************
A converter is missing for the field or schema that needs to be serialized. You can either solve this error using
:code:`DocumentationOptions.strict_mode`, or by registering your `custom converter <custom_converter_>`_. You can use the following
snippet as an example:

.. _custom_converter: configuration.html#schema-converters

.. code:: python

    from openapi_builder import DocumentationOptions, OpenApiDocumentation
    from openapi_builder.converters.schema.base import SchemaConverter
    from openapi_builder.specification import Schema


    class YourFieldConverter(SchemaConverter):
        converts_class = YourFieldClass

        def convert(self, value) -> Schema:
            return Schema(type="string", format="email")


    OpenApiDocumentation(
        ...,
        options=DocumentationOptions(
            schema_converter_classes=[YourFieldConverter],
        ),
    )

.. _missing_parameter_converter:

*************************
MissingParameterConverter
*************************
A converter is missing for the parameter. This might be because you added a custom parameter validator using the following snippet:

.. code:: python

    app.url_map.converters["uid"] = validators.UUIDValidator

You can solve this error by registering your custom `parameter converter <parameter_converter_>`_. You can use the following snippet as an example:

.. _parameter_converter: configuration.html#parameter-converters

.. code:: python

    from openapi_builder import DocumentationOptions, OpenApiDocumentation
    from openapi_builder.converters.parameters.base import ParameterConverter
    from openapi_builder.specification import Schema


    class UUIDConverter(ParameterConverter):
        converts_class = validators.UUIDValidator

        @property
        def schema(self) -> Schema:
            return Schema(type="string", format="hex")


    OpenApiDocumentation(
        ...,
        options=DocumentationOptions(
            schema_converter_classes=[YourFieldConverter],
        ),
    )

.. _missing_default_converter:

***********************
MissingDefaultConverter
***********************
A converter is missing for a default type. This might be because you return a default that is not JSON serializable.

You can solve this error by registering your custom `defaults converter <defaults_converter_>`_. You can use the following snippet as an example:

.. _defaults_converter: configuration.html#defaults-converters

.. code:: python

    import datetime

    from openapi_builder import DocumentationOptions, OpenApiDocumentation
    from openapi_builder.converters.defaults.base import DefaultsConverter
    from openapi_builder.specification import Schema


    class TimeDeltaConverter(DefaultsConverter):
        converts_class = datetime.timedelta

        def convert(self, value) -> Any:
            return value.isoformat()


    OpenApiDocumentation(
        ...,
        options=DocumentationOptions(
            schema_converter_classes=[YourFieldConverter],
        ),
    )

.. _missing_config_context:

********************
MissingConfigContext
********************
A function is called that requires a proper value for the :code:`documentation` variable.
This variable is used by the :code:`OpenAPIBuilder`. You can only encounter this exception when
overriding the :code:`OpenAPIBuilder`-class itself. Decorate your function according to the following snippet:

.. code:: python

    def process():
        config = Documentation(...)
        with builder.config_manager.use_documentation_context(config):
            ...
