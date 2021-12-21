Exceptions
==========

The following exceptions can be encountered during the configuration of the :code:`openapi_builder` package:


- :ref:`MissingConverter`
- :ref:`MissingConfigContext`

MissingConverter
~~~~~~~~~~~~~~~~
A converter is missing for the field or schema that needs to be serialized. You can either solve this error using
:code:`DocumentationOptions.strict_mode`, or by registering your custom converter. You can use the following
snippet as an example:

.. code:: python

    from openapi_builder.converters import Converter, register_converter
    from openapi_builder.specification import Schema


    @register_converter
    class YourFieldConverter(Converter):
        converts_class = YourFieldClass

        def convert(self, value) -> Schema:
            return Schema(type="string", format="email")


MissingConfigContext
~~~~~~~~~~~~~~~~~~~~
A function is called that requires a proper value for the :code:`documentation` variable.
This variable is used by the :code:`OpenAPIBuilder`. You can only encounter this exception when
overriding the :code:`OpenAPIBuilder`-class itself. Decorate your function according to the following snippet:

.. code:: python

    @documentation_context.verify_context
    def process():
        ...