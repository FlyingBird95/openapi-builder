"""Contains all Open API specifications.

This is described on this page:
https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md
"""
from typing import Any, Dict, List, Optional, Union


class OpenAPI:
    """Root document object of the OpenAPI document.

    Open API root object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#openapi-object
    """

    def __init__(
        self,
        info: "Info",
        paths: "Paths",
        openapi: str = "3.0.3",
        servers: Optional[List["Server"]] = None,
        components: Optional["Components"] = None,
        security: Optional[List["SecurityRequirement"]] = None,
        tags: Optional[List["Tag"]] = None,
        external_docs: Optional["ExternalDocumentation"] = None,
    ):
        self.openapi: str = openapi
        """REQUIRED. This string MUST be the semantic version number of the OpenAPI
        Specification version that the OpenAPI document uses. The openapi field SHOULD
        be used by tooling specifications and clients to interpret the OpenAPI document.
        This is not related to the API info.version string."""

        self.info: Info = info
        """REQUIRED. Provides metadata about the API. The metadata MAY be used by
        tooling as required."""

        self.servers: List[Server] = servers if servers is not None else []
        """An array of Server Objects, which provide connectivity information to a
        target server. If the servers property is not provided, or is an empty array,
        the default value would be a Server Object with a url value of /."""

        self.paths: Paths = paths
        """REQUIRED. The available paths and operations for the API."""

        self.components: Components = (
            components if components is not None else Components()
        )
        """An element to hold various schemas for the specification."""

        self.security: List[SecurityRequirement] = (
            security if security is not None else []
        )
        """A declaration of which security mechanisms can be used across the API. The
        list of values includes alternative security requirement objects that can be
        used. Only one of the security requirement objects need to be satisfied to
        authorize a request. Individual operations can override this definition. To make
        security optional, an empty security requirement ({}) can be included in the
        array."""

        self.tags: List[Tag] = tags if tags is not None else []
        """A list of tags used by the specification with additional metadata. The order
        of the tags can be used to reflect on their order by the parsing tools. Not all
        tags that are used by the Operation Object must be declared. The tags that are
        not declared MAY be organized randomly or based on the tools' logic. Each tag
        name in the list MUST be unique."""

        self.external_docs: Optional[ExternalDocumentation] = external_docs
        """Additional external documentation."""

    def get_value(self):
        value = {
            "openapi": self.openapi,
            "info": self.info.get_value(),
            "servers": [server.get_value() for server in self.servers],
            "paths": self.paths.get_value(),
            "components": self.components.get_value(),
        }
        return value


class Info:
    """The object provides metadata about the API.

    The metadata MAY be used by the clients if needed, and MAY be presented in editing
    or documentation generation tools for convenience.

    Open API info object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#infoObject

    Example object:
    {
        "title": "Sample Pet Store App",
        "description": "This is a sample server for a pet store.",
        "termsOfService": "https://example.com/terms/",
        "contact": {
            "name": "API Support",
            "url": "https://www.example.com/support",
            "email": "support@example.com"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
        },
        "version": "1.0.1"
    }
    """

    def __init__(
        self,
        title: str,
        version: str,
        description: Optional[str] = None,
        terms_of_service: Optional[str] = None,
        contact: Optional["Contact"] = None,
        license: Optional["License"] = None,
    ):
        self.title: str = title
        """REQUIRED. The title of the API."""

        self.description: Optional[str] = description
        """A short description of the API. CommonMark syntax MAY be used for rich
        text representation."""

        self.terms_of_service: Optional[str] = terms_of_service
        """A URL to the Terms of Service for the API. MUST be in the format of a URL."""

        self.contact: Optional[Contact] = contact
        """The contact information for the exposed API."""

        self.license: Optional[License] = license
        """The license information for the exposed API."""

        self.version: str = version
        """REQUIRED. The version of the OpenAPI document (which is distinct from the
        OpenAPI Specification version or the API implementation version)."""

    def get_value(self):
        value = {
            "title": self.title,
            "version": self.version,
        }

        if self.description is not None:
            value["description"] = self.description
        if self.terms_of_service is not None:
            value["termsOfService"] = self.terms_of_service
        if self.contact is not None:
            value["contact"] = self.contact.get_value()
        if self.license is not None:
            value["license"] = self.license.get_value()

        return value


class Contact:
    """Contact information for the exposed API.

    Open API contact object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#contactObject

    Example object:
    {
        "name": "API Support",
        "url": "https://www.example.com/support",
        "email": "support@example.com"
    }
    """

    def __init__(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        email: Optional[str] = None,
    ):
        self.name: Optional[str] = name
        """The identifying name of the contact person/organization."""

        self.url: Optional[str] = url
        """The URL pointing to the contact information. MUST be in the format of a
        URL."""

        self.email: Optional[str] = email
        """The email address of the contact person/organization. MUST be in the format
        of an email address."""

    def get_value(self):
        value = {}

        if self.name is not None:
            value["name"] = self.name
        if self.url is not None:
            value["url"] = self.url
        if self.email is not None:
            value["email"] = self.email

        return value


class License:
    """License information for the exposed API.

    Open API license object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#licenseObject

    Example object:
    {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }
    """

    def __init__(self, name: str, url: Optional[str] = None):
        self.name: str = name
        """REQUIRED. The license name used for the API."""

        self.url: str = url
        """A URL to the license used for the API. MUST be in the format of a URL."""

    def get_value(self):
        value = {"name": self.name}

        if self.url is not None:
            value["url"] = self.url

        return value


class Server:
    """An object representing a Server.

    Open API server object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#serverObject

    Example object:
    {
        "url": "https://{username}.gigantic-server.com:{port}/{basePath}",
        "description": "The production API server",
        "variables": {
            "username": {
                "default": "demo",
                "description": "this value is assigned by the service provider, in this
                example `gigantic-server.com`"
            },
            "port": {
                "enum": [
                    "8443",
                    "443"
                ],
                "default": "8443"
            },
            "basePath": {
                "default": "v2"
            }
        }
    }
    """

    def __init__(
        self,
        url: str,
        description: Optional[str] = None,
        variables: Optional[Dict[str, "ServerVariable"]] = None,
    ):
        self.url: str = url
        """REQUIRED. A URL to the target host. This URL supports Server Variables and
        MAY be relative, to indicate that the host location is relative to the location
        where the OpenAPI document is being served. Variable substitutions will be made
        when a variable is named in {brackets}."""

        self.description: Optional[str] = description
        """An optional string describing the host designated by the URL. CommonMark
        syntax MAY be used for rich text representation."""

        self.variables: Dict[str, ServerVariable] = (
            variables if variables is not None else {}
        )
        """A map between a variable name and its value. The value is used for
        substitution in the server's URL template."""

    def get_value(self):
        value = {"url": self.url}

        if self.description is not None:
            value["description"] = self.description
        if self.variables:
            value["variables"] = {
                key: server_variable.get_value()
                for key, server_variable in self.variables.items()
            }

        return value


class ServerVariable:
    """An object representing a Server Variable for server URL template substitution.

    Open API server variable object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#serverVariableObject
    """

    def __init__(
        self, default: str, enum: List[str] = None, description: Optional[str] = None
    ):
        self.enum: List[str] = enum if enum is not None else []
        """An enumeration of string values to be used if the substitution options are
        from a limited set. The array SHOULD NOT be empty."""

        self.default: str = default
        """REQUIRED. The default value to use for substitution, which SHALL be sent
        if an alternate value is not supplied. Note this behavior is different than the
        Schema Object's treatment of default values, because in those cases parameter
        values are optional. If the enum is defined, the value SHOULD exist in the
        enum's values."""

        self.description: Optional[str] = description
        """An optional description for the server variable. CommonMark syntax MAY be
        used for rich text representation."""

    def get_value(self):
        value = {"default": self.default}

        if self.enum:
            value["enum"] = self.enum
        if self.description is not None:
            value["description"] = self.description

        return value


class Components:
    """Holds a set of reusable objects for different aspects of the OAS.

    All objects defined within the components object will have no effect on the API
    unless they are explicitly referenced from properties outside the components object.

    Open API components object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#componentsObject
    """

    def __init__(
        self,
        schemas: Optional[Dict[str, Union["Schema", "Reference"]]] = None,
        responses: Optional[Dict[str, Union["Response", "Reference"]]] = None,
        parameters: Optional[Dict[str, Union["Parameter", "Reference"]]] = None,
        examples: Optional[Dict[str, Union["Example", "Reference"]]] = None,
        request_bodies: Optional[Dict[str, Union["RequestBody", "Reference"]]] = None,
        headers: Optional[Dict[str, Union["Header", "Reference"]]] = None,
        security_schemes: Optional[
            Dict[str, Union["SecurityScheme", "Reference"]]
        ] = None,
        links: Optional[Dict[str, Union["Link", "Reference"]]] = None,
        callbacks: Optional[Dict[str, Union["Callback", "Reference"]]] = None,
    ):
        self.schemas: Dict[str, Union[Schema, Reference]] = (
            schemas if schemas is not None else {}
        )
        """An object to hold reusable Schema Objects."""

        self.responses: Dict[str, Union[Response, Reference]] = (
            responses if responses is not None else {}
        )
        """An object to hold reusable Response Objects."""

        self.parameters: Dict[str, Union[Parameter, Reference]] = (
            parameters if parameters is not None else {}
        )
        """An object to hold reusable Parameter Objects."""

        self.examples: Dict[str, Union[Example, Reference]] = (
            examples if examples is not None else {}
        )
        """An object to hold reusable Example Objects."""

        self.request_bodies: Dict[str, Union[RequestBody, Reference]] = (
            request_bodies if request_bodies is not None else {}
        )
        """An object to hold reusable Request Body Objects."""

        self.headers: Dict[str, Union[Header, Reference]] = (
            headers if headers is not None else {}
        )
        """An object to hold reusable Header Objects."""

        self.security_schemes: Dict[str, Union[SecurityScheme, Reference]] = (
            security_schemes if security_schemes is not None else {}
        )
        """An object to hold reusable Security Scheme Objects."""

        self.links: Dict[str, Union[Link, Reference]] = (
            links if links is not None else {}
        )
        """An object to hold reusable Link Objects."""

        self.callbacks: Dict[str, Union[Callback, Reference]] = (
            callbacks if callbacks is not None else {}
        )
        """An object to hold reusable Callback Objects."""

    def get_value(self):
        value = {}

        if self.schemas:
            value["schemas"] = {
                key: value.get_value() for key, value in self.schemas.items()
            }
        if self.responses:
            value["responses"] = {
                key: value.get_value() for key, value in self.responses.items()
            }
        if self.parameters:
            value["parameters"] = {
                key: value.get_value() for key, value in self.parameters.items()
            }
        if self.examples:
            value["examples"] = {
                key: value.get_value() for key, value in self.examples.items()
            }
        if self.request_bodies:
            value["request_bodies"] = {
                key: value.get_value() for key, value in self.request_bodies.items()
            }
        if self.headers:
            value["headers"] = {
                key: value.get_value() for key, value in self.headers.items()
            }
        if self.security_schemes:
            value["security_schemes"] = {
                key: value.get_value() for key, value in self.security_schemes.items()
            }
        if self.links:
            value["links"] = {
                key: value.get_value() for key, value in self.links.items()
            }
        if self.callbacks:
            value["callbacks"] = {
                key: value.get_value() for key, value in self.callbacks.items()
            }

        return value


class Paths:
    """Holds the relative paths to the individual endpoints and their operations.

    The path is appended to the URL from the Server Object in order to construct the
    full URL. The Paths MAY be empty, due to ACL constraints.

    Open API path object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#pathsObject

    Example object:
    {
        "/pets": {
            "get": {
                "description": "Returns all pets from the system that the user has access to",
                "responses": {
                    "200": {
                        "description": "A list of pets.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/pet"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """

    def __init__(self, values: Optional[Dict[str, "PathItem"]] = None):
        self.values = values if values is not None else {}
        """A relative path to an individual endpoint. The field name MUST begin with a
        forward slash (/). The path is appended (no relative URL resolution) to the
        expanded URL from the Server Object's url field in order to construct the full
        URL. Paths templating is allowed. When matching URLs, concrete (non-templated)
        paths would be matched before their templated counterparts. Templated paths
        with the same hierarchy but different templated names MUST NOT exist as they
        are identical. In case of ambiguous matching, it's up to the tooling to decide
        which one to use."""

    def get_value(self):
        value = {key: value.get_value() for key, value in self.values.items()}
        return value


class PathItem:
    """Describes the operations available on a single path.

    A Paths Item MAY be empty, due to ACL constraints. The path itself is still
    exposed to the documentation viewer but they will not know which operations and
    parameters are available.

    Open API path item as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#pathItemObject
    """

    def __init__(
        self,
        ref: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        get: Optional["Operation"] = None,
        put: Optional["Operation"] = None,
        post: Optional["Operation"] = None,
        delete: Optional["Operation"] = None,
        options: Optional["Operation"] = None,
        head: Optional["Operation"] = None,
        patch: Optional["Operation"] = None,
        trace: Optional["Operation"] = None,
        servers: Optional[List["Server"]] = None,
        parameters: Optional[List[Union["Parameter", "Reference"]]] = None,
    ):
        self.ref: str = ref
        """Allows for an external definition of this path item. The referenced structure
        MUST be in the format of a Paths Item Object. In case a Paths Item Object field
        appears both in the defined object and the referenced object, the behavior is
        undefined."""

        self.summary: str = summary
        """An optional, string summary, intended to apply to all operations in this
        path."""

        self.description: str = description
        """An optional, string description, intended to apply to all operations in this
        path. CommonMark syntax MAY be used for rich text representation."""

        self.get: Optional[Operation] = get
        """A definition of a GET operation on this path."""

        self.put: Optional[Operation] = put
        """A definition of a PUT operation on this path."""

        self.post: Optional[Operation] = post
        """A definition of a POST operation on this path."""

        self.delete: Optional[Operation] = delete
        """A definition of a DELETE operation on this path."""

        self.options: Optional[Operation] = options
        """A definition of a OPTIONS operation on this path."""

        self.head: Optional[Operation] = head
        """A definition of a HEAD operation on this path."""

        self.patch: Optional[Operation] = patch
        """A definition of a PATCH operation on this path."""

        self.trace: Optional[Operation] = trace
        """A definition of a TRACE operation on this path."""

        self.servers: List[Server] = servers if servers is not None else []
        """An alternative server array to service all operations in this path."""

        self.parameters: List[Union[Parameter, Reference]] = (
            parameters if parameters is not None else []
        )
        """A list of parameters that are applicable for all the operations described
        under this path. These parameters can be overridden at the operation level, but
        cannot be removed there. The list MUST NOT include duplicated parameters. A
        unique parameter is defined by a combination of a name and location. The list
        can use the Reference Object to link to parameters that are defined at the
        OpenAPI Object's components/parameters."""

    def get_value(self):
        value = {}

        if self.ref is not None:
            value["$ref"] = self.ref
        if self.summary is not None:
            value["summary"] = self.summary
        if self.description is not None:
            value["description"] = self.description
        if self.get is not None:
            value["get"] = self.get.get_value()
        if self.put is not None:
            value["put"] = self.put.get_value()
        if self.post is not None:
            value["post"] = self.post.get_value()
        if self.delete is not None:
            value["delete"] = self.delete.get_value()
        if self.options is not None:
            value["options"] = self.options.get_value()
        if self.head is not None:
            value["head"] = self.head.get_value()
        if self.patch is not None:
            value["patch"] = self.patch.get_value()
        if self.trace is not None:
            value["trace"] = self.trace.get_value()
        if self.servers:
            value["servers"] = [server.get_value() for server in self.servers]
        if self.parameters:
            value["parameters"] = [
                parameter.get_value() for parameter in self.parameters
            ]

        return value


class Operation:
    """Describes a single API operation on a path.

    Open API operation object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#operationObject
    """

    def __init__(
        self,
        tags: Optional[List[str]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        external_docs: Optional["ExternalDocumentation"] = None,
        operation_id: Optional[str] = None,
        parameters: Optional[Union["Parameter", "Reference"]] = None,
        request_body: Optional[Union["RequestBody", "Reference"]] = None,
        responses: Optional["Responses"] = None,
        callbacks: Optional[Dict[str, Union["Callback", "Reference"]]] = None,
        deprecated: bool = False,
        security: Optional[List["SecurityRequirement"]] = None,
        servers: Optional[List["Server"]] = None,
    ):
        self.tags: List[Tag] = tags if tags is not None else []
        """A list of tags for API documentation control. Tags can be used for logical
        grouping of operations by resources or any other qualifier."""

        self.summary: Optional[str] = summary
        """A short summary of what the operation does."""

        self.description: Optional[str] = description
        """A verbose explanation of the operation behavior. CommonMark syntax MAY be
        used for rich text representation."""

        self.external_docs: ExternalDocumentation = external_docs
        """Additional external documentation for this operation."""

        self.operation_id: Optional[str] = operation_id
        """Unique string used to identify the operation. The id MUST be unique among
        all operations described in the API. The operationId value is case-sensitive.
        Tools and libraries MAY use the operationId to uniquely identify an operation,
        therefore, it is RECOMMENDED to follow common programming naming conventions."""

        self.parameters: List[Union[Parameter, Reference]] = (
            parameters if parameters is not None else []
        )
        """A list of parameters that are applicable for this operation. If a parameter
        is already defined at the Paths Item, the new definition will override it but
        can never remove it. The list MUST NOT include duplicated parameters. A unique
        parameter is defined by a combination of a name and location. The list can use
        the Reference Object to link to parameters that are defined at the OpenAPI
        Object's components/parameters."""

        self.request_body: Optional[Union[RequestBody, Reference]] = request_body
        """The request body applicable for this operation. The requestBody is only
        supported in HTTP methods where the HTTP 1.1 specification RFC7231 has
        explicitly  defined semantics for request bodies. In other cases where the HTTP
        spec is vague, requestBody SHALL be ignored by consumers."""

        self.responses: Responses = responses
        """REQUIRED. The list of possible responses as they are returned from executing
        this operation."""

        self.callbacks: Dict[str, Union[Callback, Reference]] = (
            callbacks if callbacks is not None else {}
        )
        """A map of possible out-of band callbacks related to the parent operation. The
        key is a unique identifier for the Callback Object. Each value in the map is a
        Callback Object that describes a request that may be initiated by the API
        provider and the expected responses."""

        self.deprecated: bool = deprecated
        """Declares this operation to be deprecated. Consumers SHOULD refrain from
        usage of the declared operation. Default value is false."""

        self.security: List[SecurityRequirement] = (
            security if security is not None else []
        )
        """A declaration of which security mechanisms can be used for this operation.
        The list of values includes alternative security requirement objects that can
        be used. Only one of the security requirement objects need to be satisfied to
        authorize a request. To make security optional, an empty security requirement
        ({}) can be included in the array. This definition overrides any declared
        top-level security. To remove a top-level security declaration, an empty array
        can be used."""

        self.servers: List[Server] = servers if servers is not None else []
        """An alternative server array to service this operation. If an alternative
        server object is specified at the Paths Item Object or Root level, it will be
        overridden by this value."""

    def get_value(self):
        value = {}

        if self.tags:
            value["tags"] = self.tags
        if self.summary is not None:
            value["summary"] = self.summary
        if self.description is not None:
            value["description"] = self.description
        if self.external_docs is not None:
            value["externalDocs"] = self.external_docs.get_value()
        if self.operation_id is not None:
            value["operationId"] = self.operation_id
        if self.parameters:
            value["parameters"] = [
                parameter.get_value() for parameter in self.parameters
            ]
        if self.request_body is not None:
            value["requestBody"] = self.request_body.get_value()
        if self.responses is not None:
            value["responses"] = self.responses.get_value()
        if self.callbacks:
            value["callbacks"] = {
                key: callback.get_value() for key, callback in self.callbacks.items()
            }
        if self.deprecated is True:
            value["deprecated"] = True
        if self.security:
            value["security"] = [
                security_requirement.get_value()
                for security_requirement in self.security
            ]
        if self.servers:
            value["servers"] = [server.get_value() for server in self.servers]

        return value


class ExternalDocumentation:
    """Allows referencing an external resource for extended documentation.

    Open API external docs object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#externalDocumentationObject

    Example object:
    {
      "description": "Find more info here",
      "url": "https://example.com"
    }
    """

    def __init__(self, url: str, description: Optional[str] = None):
        self.description = description
        """A short description of the target documentation. CommonMark syntax MAY be
        used for rich text representation."""

        self.url = url
        """REQUIRED. The URL for the target documentation. Value MUST be in the format
        of a URL."""

    def get_value(self):
        value = {"url": self.url}

        if self.description is not None:
            value["description"] = self.description

        return value


class Parameter:
    """Describes a single operation parameter.

    A unique parameter is defined by a combination of a name and location (in_).

    Open API parameter object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#parameterObject

    Example object:
    {
        "name": "token",
        "in": "header",
        "description": "token to be passed as a header",
        "required": true,
        "schema": {
            "type": "array",
            "items": {
                "type": "integer",
                "format": "int64"
            }
        },
        "style": "simple"
    }
    """

    def __init__(
        self,
        in_: str,
        name: str,
        description: Optional[str] = None,
        schema: Optional[Union["Schema", "Reference"]] = None,
        required=True,
        deprecated=False,
        allow_empty_value=False,
    ):
        self.name: str = name
        """REQUIRED. The name of the parameter. Parameter names are case sensitive.
            - If in is "path", the name field MUST correspond to a template expression
              occurring within the path field in the Paths Object. See Paths Templating
              for further information.
            - If in is "header" and the name field is "Accept", "Content-Type" or
              "Authorization", the parameter definition SHALL be ignored.
            - For all other cases, the name corresponds to the parameter name used by
              the in property.
        """

        self.in_: str = in_
        """REQUIRED. The location of the parameter. Possible values are "query",
        "header", "path" or "cookie"."""

        self.description: Optional[str] = description
        """A brief description of the parameter. This could contain examples of use.
        CommonMark syntax MAY be used for rich text representation."""

        self.schema: Optional[Union["Schema", "Reference"]] = schema
        """The schema defining the type used for the parameter."""

        self.required: bool = required
        """Determines whether this parameter is mandatory. If the parameter location
        is "path", this property is REQUIRED and its value MUST be true. Otherwise, the
        property MAY be included and its default value is false."""

        self.deprecated: bool = deprecated
        """Specifies that a parameter is deprecated and SHOULD be transitioned out of
        usage. Default value is false."""

        self.allow_empty_value: bool = allow_empty_value
        """Sets the ability to pass empty-valued parameters. This is valid only for
        query parameters and allows sending a parameter with an empty value. Default
        value is false. If style is used, and if behavior is n/a (cannot be serialized),
        the value of allowEmptyValue SHALL be ignored. Use of this property is NOT
        RECOMMENDED, as it is likely to be removed in a later revision."""

    def get_value(self):
        value = {"in": self.in_, "name": self.name}

        if self.description is not None:
            value["description"] = self.description
        if self.schema is not None:
            value["schema"] = self.schema.get_value()
        if self.required is True:
            value["required"] = self.required
        if self.deprecated is True:
            value["deprecated"] = self.deprecated
        if self.allow_empty_value is True:
            value["allowEmptyValue"] = self.allow_empty_value

        return value


class RequestBody:
    """Describes a single request body.

    Open API request body object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#requestBodyObject
    """

    def __init__(
        self,
        description: Optional[str] = None,
        content: Optional[Dict[str, "MediaType"]] = None,
        required: bool = False,
    ):
        self.description: Optional[str] = description
        """A brief description of the request body. This could contain examples of use.
        CommonMark syntax MAY be used for rich text representation."""

        self.content: Dict[str, MediaType] = content if content is not None else {}
        """REQUIRED. The content of the request body. The key is a media type or media
        type range and the value describes it. For requests that match multiple keys,
        only the most specific key is applicable. e.g. text/plain overrides text/*"""

        self.required: bool = required
        """Determines if the request body is required in the request. Defaults to
        false."""

    def get_value(self):
        value = {
            "content": {
                key: media_type.get_value() for key, media_type in self.content.items()
            }
        }

        if self.description is not None:
            value["description"] = self.description
        if self.required is True:
            value["required"] = self.required

        return value


class MediaType:
    """Provides schema and examples for the media type identified by its key.

    Open API media type object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#mediaTypeObject
    """

    def __init__(
        self,
        schema: Optional[Union["Schema", "Reference"]] = None,
        example: Any = None,
        examples: Optional[Dict[str, Union["Example", "Reference"]]] = None,
        encoding: Optional[Dict[str, "Encoding"]] = None,
    ):
        self.schema: Optional[Union["Schema", "Reference"]] = schema
        """The schema defining the content of the request, response, or parameter."""

        self.example: Any = example
        """Example of the media type. The example object SHOULD be in the correct
        format as specified by the media type. The example field is mutually exclusive
        of the examples field. Furthermore, if referencing a schema which contains an
        example, the example value SHALL override the example provided by the schema."""

        self.examples: Dict[str, Union[Example, Reference]] = (
            examples if examples is not None else {}
        )
        """Examples of the media type. Each example object SHOULD match the media type
        and specified schema if present. The examples field is mutually exclusive of the
        example field. Furthermore, if referencing a schema which contains an example,
        the examples value SHALL override the example provided by the schema."""

        self.encoding: Dict[str, "Encoding"] = encoding if encoding is not None else {}
        """A map between a property name and its encoding information. The key, being
        the property name, MUST exist in the schema as a property. The encoding object
        SHALL only apply to requestBody objects when the media type is multipart or
        application/x-www-form-urlencoded."""

    def get_value(self):
        value = {}

        if self.schema:
            value["schema"] = self.schema.get_value()
        if self.example is not None:
            value["example"] = self.example
        elif self.examples:
            value["examples"] = {
                key: example.get_value() for key, example in self.examples.items()
            }
        elif self.encoding:
            value["encoding"] = {
                key: encoding_obj.get_value()
                for key, encoding_obj in self.encoding.items()
            }

        return value


class Encoding:
    """A single encoding definition applied to a single schema property.

    Open API encoding object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#encodingObject
    """

    def __init__(
        self,
        content_type: Optional[str] = None,
        headers: Optional[Dict[str, Union["Header", "Reference"]]] = None,
        style: Optional[str] = None,
        explode: bool = True,
        allow_reserved: bool = False,
    ):
        self.content_type: Optional[str] = content_type
        """The Content-Type for encoding a specific property. Default value depends on
        the property type: for string with format being binary –
        application/octet-stream; for other primitive types – text/plain; for object -
        application/json; for array – the default is defined based on the inner type.
        The value can be a specific media type (e.g. application/json), a wildcard media
        type (e.g. image/*), or a comma-separated list of the two types."""

        self.headers: Dict[str, Union[Header, Reference]] = (
            headers if headers is not None else {}
        )
        """A map allowing additional information to be provided as headers, for example
        Content-Disposition. Content-Type is described separately and SHALL be ignored
        in this section. This property SHALL be ignored if the request body media type
        is not a multipart."""

        self.style: Optional[str] = style
        """Describes how a specific property value will be serialized depending on its
        type. See Parameter Object for details on the style property. The behavior
        follows the same values as query parameters, including default values. This
        property SHALL be ignored if the request body media type is not
        application/x-www-form-urlencoded."""

        self.explode: bool = explode
        """When this is true, property values of type array or object generate separate
        parameters for each value of the array, or key-value-pair of the map. For other
        types of properties this property has no effect. When style is form, the default
        value is true. For all other styles, the default value is false. This property
        SHALL be ignored if the request body media type is not
        application/x-www-form-urlencoded."""

        self.allow_reserved: bool = allow_reserved
        """Determines whether the parameter value SHOULD allow reserved characters, as
        defined by RFC3986 :/?#[]@!$&'()*+,;= to be included without percent-encoding.
        The default value is false. This property SHALL be ignored if the request body
        media type is not application/x-www-form-urlencoded."""

    def get_value(self):
        value = {}

        if self.content_type is not None:
            value["contentType"] = self.content_type
        if self.headers:
            value["headers"] = {
                key: header.get_value() for key, header in self.headers.items()
            }
        if self.style is not None:
            value["style"] = self.style
        if self.explode is True:
            value["explode"] = self.explode
        if self.allow_reserved is True:
            value["allowReserved"] = self.allow_reserved

        return value


class Responses:
    """A container for the expected responses of an operation.

    The container maps a HTTP response code to the expected response. The documentation
    is not necessarily expected to cover all possible HTTP response codes because they
    may not be known in advance. However, documentation is expected to cover a
    successful operation response and any known errors.

    Open API responses object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#responsesObject

    Example object:
    {
        "200": {
            "description": "a pet to be returned",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/Pet"
                    }
                }
            }
        },
        "default": {
            "description": "Unexpected error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ErrorModel"
                    }
                }
            }
        }
    }
    """

    def __init__(
        self, values: Optional[Dict[str, Union["Response", "Reference"]]] = None
    ):
        self.values: Dict[str, Union[Response, Reference]] = (
            values if values is not None else {}
        )
        """The documentation of responses other than the ones declared for specific
        HTTP response codes. Use this field to cover undeclared responses. A Reference
        Object can link to a response that the OpenAPI Object's components/responses
        section defines."""

    def get_value(self):
        value = {key: value.get_value() for key, value in self.values.items()}
        return value


class Response:
    """Describes a single response from an API Operation.

    This response is including design-time, static links to operations based on the
    response.

    Open API response object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#responseObject

    Example object:
    {
        "description": "A complex object array response",
        "content": {
            "application/json": {
                "schema": {
                    "type": "array",
                    "items": {
                        "$ref": "#/components/schemas/VeryComplexType"
                    }
                }
            }
        }
    }
    """

    def __init__(
        self,
        description: str,
        headers: Optional[Dict[str, Union["Header", "Reference"]]] = None,
        content: Optional[Dict[str, "MediaType"]] = None,
        links: Optional[Dict[str, Union["Link", "Reference"]]] = None,
    ):
        self.description = description
        """REQUIRED. A short description of the response. CommonMark syntax MAY be used
        for rich text representation."""

        self.headers: Dict[str, Union[Header, Reference]] = (
            headers if headers is not None else {}
        )
        """Maps a header name to its definition. RFC7230 states header names are case
        insensitive. If a response header is defined with the name "Content-Type", it
        SHALL be ignored."""

        self.content: Dict[str, MediaType] = content if content is not None else {}
        """A map containing descriptions of potential response payloads. The key is a
        media type or media type range and the value describes it. For responses that
        match multiple keys, only the most specific key is applicable. e.g. text/plain
        overrides text/*"""

        self.links: Dict[str, Union[Link, Reference]] = (
            links if links is not None else {}
        )
        """A map of operations links that can be followed from the response. The key of
        the map is a short name for the link, following the naming constraints of the
        names for Component Objects."""

    def get_value(self):
        value = {"description": self.description}

        if self.headers:
            value["headers"] = {
                key: header.get_value() for key, header in self.headers.items()
            }
        if self.content:
            value["content"] = {
                key: media_type.get_value() for key, media_type in self.content.items()
            }
        if self.links:
            value["links"] = {key: link.get_value() for key, link in self.links.items()}

        return value


class Callback:
    """A map of possible out-of band callbacks related to the parent operation.

    Each value in the map is a Paths Item Object that describes a set of requests that
    may be initiated by the API provider and the expected responses. The key value used
    to identify the path item object is an expression, evaluated at runtime, that
    identifies a URL to use for the callback operation.

    Open API callback object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#callbackObject
    """

    def __init__(self, values: Optional[Dict[str, PathItem]] = None):
        self.values = values if values is not None else {}
        """A Paths Item Object used to define a callback request and expected
        responses."""

    def get_value(self):
        value = {key: path_item.get_value() for key, path_item in self.values.items()}
        return value


class Example:
    """Open API example object.

     As described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#exampleObject
    """

    def __init__(
        self,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        value: Any = None,
        external_value: str = None,
    ):
        self.summary: str = summary
        """Short description for the example."""

        self.description: str = description
        """Long description for the example. CommonMark syntax MAY be used for rich
        text representation."""

        self.value: Any = value
        """Embedded literal example. The value field and externalValue field are
        mutually exclusive. To represent examples of media types that cannot naturally
        represented in JSON or YAML, use a string value to contain the example,
        escaping where necessary."""

        self.external_value: str = external_value
        """A URL that points to the literal example. This provides the capability to
        reference examples that cannot easily be included in JSON or YAML documents.
        The value field and externalValue field are mutually exclusive."""

    def get_value(self):
        value = {}

        if self.summary is not None:
            value["summary"] = self.summary
        if self.description is not None:
            value["description"] = self.description
        if self.value is not None:
            value["value"] = self.value
        if self.external_value is not None:
            value["externalValue"] = self.external_value

        return value


class Link:
    """The Link object represents a possible design-time link for a response.

    The presence of a link does not guarantee the caller's ability to successfully
    invoke it, rather it provides a known relationship and traversal mechanism between
    responses and other operations.

    Open API link object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#linkObject
    """

    def __init__(
        self,
        operation_ref: Optional[str] = None,
        operation_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        request_body: Any = None,
        description: Optional[str] = None,
        server: Optional["Server"] = None,
    ):
        self.operation_ref: str = operation_ref
        """A relative or absolute URI reference to an OAS operation. This field is
        mutually exclusive of the operationId field, and MUST point to an Operation
        Object. Relative operationRef values MAY be used to locate an existing
        Operation Object in the OpenAPI definition."""

        self.operation_id: str = operation_id
        """The name of an existing, resolvable OAS operation, as defined with a unique
        operationId. This field is mutually exclusive of the operationRef field."""

        self.parameters: Dict[str, Any] = parameters if parameters is not None else {}
        """A map representing parameters to pass to an operation as specified with
        operationId or identified via operationRef. The key is the parameter name to be
        used, whereas the value can be a constant or an expression to be evaluated and
        passed to the linked operation. The parameter name can be qualified using the
        parameter location [{in}.]{name} for operations that use the same parameter
        name in different locations (e.g. path.id)."""

        self.request_body: Any = request_body
        """A literal value or {expression} to use as a request body when calling the
        target operation."""

        self.description: str = description
        """A description of the link. CommonMark syntax MAY be used for rich text
        representation."""

        self.server: Server = server
        """A server object to be used by the target operation."""

    def get_value(self):
        value = {}

        if self.operation_ref is not None:
            value["operationRef"] = self.operation_ref
        if self.operation_id is not None:
            value["operationId"] = self.operation_id
        if self.parameters:
            value["parameters"] = {key: value for key, value in self.parameters.items()}
        if self.request_body:
            value["requestBody"] = self.request_body
        if self.description is not None:
            value["description"] = self.description
        if self.server is not None:
            value["server"] = self.server.get_value()

        return value


class Header:
    """The Header Object.

    It follows the structure of the Parameter Object with the following changes:
    1. name MUST NOT be specified, it is given in the corresponding headers map.
    2. in MUST NOT be specified, it is implicitly in header.
    3. All traits that are affected by the location MUST be applicable to a location of
      header (for example, style).

    Open API header object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#headerObject

    Example object:
    {
        "description": "The number of allowed requests in the current period",
        "schema": {
            "type": "integer"
        }
    }
    """

    def __init__(
        self,
        description: Optional[str] = None,
        required=True,
        deprecated=False,
        allow_empty_value=False,
    ):
        self.description: Optional[str] = description
        """A brief description of the header. This could contain examples of use.
        CommonMark syntax MAY be used for rich text representation."""

        self.required: bool = required
        """Determines whether this header is mandatory. If the header location is
        "path", this property is REQUIRED and its value MUST be true. Otherwise, the
        property MAY be included and its default value is false."""

        self.deprecated: bool = deprecated
        """Specifies that a header is deprecated and SHOULD be transitioned out of
        usage. Default value is false."""

        self.allow_empty_value: bool = allow_empty_value
        """Sets the ability to pass empty-valued headers. This is valid only for query
        headers and allows sending a header with an empty value. Default value is false.
        If style is used, and if behavior is n/a (cannot be serialized), the value of
        allowEmptyValue SHALL be ignored. Use of this property is NOT RECOMMENDED, as
        it is likely to be removed in a later revision."""

    def get_value(self):
        value = {}

        if self.description is not None:
            value["description"] = self.description
        if self.required is True:
            value["required"] = self.required
        if self.deprecated is True:
            value["deprecated"] = self.deprecated
        if self.allow_empty_value is True:
            value["allowEmptyValue"] = self.allow_empty_value

        return value


class Tag:
    """Adds metadata to a single tag that is used by the Operation Object.

    It is not mandatory to have a Tag Object per tag defined in the Operation Object
    instances.

    Open API tag object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#tagObject

    Example object:
    {
        "name": "pet",
        "description": "Pets operations"
    }
    """

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        external_docs: Optional[ExternalDocumentation] = None,
    ):
        self.name: str = name
        """REQUIRED. The name of the tag."""

        self.description: Optional[str] = description
        """A short description for the tag. CommonMark syntax MAY be used for rich
        text representation."""

        self.external_docs: Optional[ExternalDocumentation] = external_docs
        """Additional external documentation for this tag."""

    def get_value(self):
        value = {"name": self.name}

        if self.description is not None:
            value["description"] = self.description
        if self.external_docs is not None:
            value["externalDocs"] = self.external_docs.get_value()

        return value


class Reference:
    """A simple object to allow referencing other components in the specification.

    The Reference may refer to something internally and externally. The Reference
    Object is defined by JSON Reference and follows the same structure, behavior and
    rules. For this specification, reference resolution is accomplished as defined by
    the JSON Reference specification and not by the JSON Schema specification.

    Open API reference object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#referenceObject

    Example object:
    {
        "$ref": "#/components/schemas/Pet"
    }
    """

    def __init__(self, ref: str):
        self.ref: str = ref
        """REQUIRED. The reference string."""

    @classmethod
    def from_schema(cls, schema_name):
        return cls(ref=f"#/components/schemas/{schema_name}")

    @classmethod
    def from_response(cls, response_name):
        return cls(ref=f"#/components/responses/{response_name}")

    @classmethod
    def from_parameter(cls, parameter_name):
        return cls(ref=f"#/components/parameters/{parameter_name}")

    @classmethod
    def from_example(cls, example_name):
        return cls(ref=f"#/components/examples/{example_name}")

    @classmethod
    def from_security_scheme(cls, security_scheme_name):
        return cls(ref=f"#/components/securitySchemes/{security_scheme_name}")

    def get_value(self):
        value = {"$ref": self.ref}

        return value


class Schema:
    """The Schema Object allows the definition of input and output data types.

    These types can be objects, but also primitives and arrays.

    Open API schema object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#schemaObject
    """

    def __init__(
        self,
        title: Optional[str] = None,
        multiple_of: Optional[int] = None,
        maximum: Optional[int] = None,
        exclusive_maximum: Optional[bool] = None,
        minimum: Optional[int] = None,
        exclusive_minimum: Optional[bool] = None,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        pattern: Optional[str] = None,
        max_items: Optional[int] = None,
        min_items: Optional[int] = None,
        unique_items: Optional[int] = None,
        max_properties: Optional[int] = None,
        min_properties: Optional[int] = None,
        required: Optional[bool] = None,
        enum: Optional[List["Schema"]] = None,
        type: Optional[Union[str, List[str]]] = None,
        all_of: Optional[List["Schema"]] = None,
        any_of: Optional[List["Schema"]] = None,
        one_of: Optional[List["Schema"]] = None,
        not_: Optional["Schema"] = None,
        items: Optional["Schema"] = None,
        properties: Optional[Dict[str, Union["Schema", Reference]]] = None,
        additional_properties: Union[bool, "Schema", Reference] = True,
        description: Optional[str] = None,
        format: Optional[str] = None,
        default: Optional[Any] = None,
    ):
        self.title: Optional[str] = title
        self.multiple_of: Optional[int] = multiple_of
        self.maximum: Optional[int] = maximum
        self.exclusive_maximum: Optional[bool] = exclusive_maximum
        self.minimum: Optional[int] = minimum
        self.exclusive_minimum: Optional[bool] = exclusive_minimum
        self.max_length: Optional[int] = max_length
        self.min_length: Optional[int] = min_length
        self.pattern: Optional[str] = pattern
        self.max_items: Optional[int] = max_items
        self.min_items: Optional[int] = min_items
        self.unique_items: Optional[int] = unique_items
        self.max_properties: Optional[int] = max_properties
        self.min_properties: Optional[int] = min_properties
        self.required: Optional[bool] = required
        self.enum: List[Schema] = enum if enum is not None else []
        self.type: Optional[Union[str, List[str]]] = type
        self.all_of: List[Schema] = all_of if all_of is not None else []
        self.any_of: List[Schema] = any_of if any_of is not None else []
        self.one_of: List[Schema] = one_of if one_of is not None else []
        self.not_: Optional[Schema] = not_
        self.items: Optional[Schema] = items
        self.properties: Dict[str, Union[Schema, Reference]] = (
            properties if properties is not None else {}
        )
        self.additional_properties: Union[
            bool, "Schema", Reference
        ] = additional_properties
        self.description: Optional[str] = description
        self.format: Optional[str] = format
        self.default: Optional[Any] = default

    def get_value(self):
        value = {}

        if self.title is not None:
            value["title"] = self.title
        if self.multiple_of is not None:
            value["multipleOf"] = self.multiple_of
        if self.maximum is not None:
            value["maximum"] = self.maximum
        if self.exclusive_maximum is not None:
            value["exclusiveMaximum"] = self.exclusive_maximum
        if self.minimum is not None:
            value["minimum"] = self.minimum
        if self.exclusive_minimum is not None:
            value["exclusiveMinimum"] = self.exclusive_minimum
        if self.max_length is not None:
            value["maxLength"] = self.max_length
        if self.min_length is not None:
            value["minLength"] = self.min_length
        if self.pattern is not None:
            value["pattern"] = self.pattern
        if self.max_items is not None:
            value["maxItems"] = self.max_items
        if self.min_items is not None:
            value["minItems"] = self.min_items
        if self.unique_items is not None:
            value["uniqueItems"] = self.unique_items
        if self.max_properties is not None:
            value["maxProperties"] = self.max_properties
        if self.min_properties is not None:
            value["minProperties"] = self.min_properties
        if self.required is not None:
            value["required"] = self.required
        if self.enum:
            value["enum"] = self.enum
        if self.type is not None:
            value["type"] = self.type
        if self.all_of:
            value["allOf"] = [item.get_value() for item in self.all_of]
        if self.any_of:
            value["anyOf"] = [item.get_value() for item in self.any_of]
        if self.one_of:
            value["oneOf"] = [item.get_value() for item in self.one_of]
        if self.not_ is not None:
            value["not"] = self.not_
        if self.items is not None:
            value["items"] = self.items.get_value()
        if self.properties:
            value["properties"] = {
                key: prop.get_value() for key, prop in self.properties.items()
            }
        if self.additional_properties is not True:
            value["additionalProperties"] = self.additional_properties.get_value()
        if self.description is not None:
            value["description"] = self.description
        if self.format is not None:
            value["format"] = self.format
        if self.default is not None:
            value["default"] = self.default

        return value


class Discriminator:
    """The Descriminator object.

    When request bodies or response payloads may be one of a number of different
    schemas, a discriminator object can be used to aid in serialization,
    deserialization, and validation. The discriminator is a specific object in a schema
    which is used to inform the consumer of the specification of an alternative schema
    based on the value associated with it.

    Open API discriminator object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#discriminatorObject
    """

    def __init__(self, property_name: str, mapping: Optional[Dict[str, str]] = None):
        self.property_name: str = property_name
        """REQUIRED. The name of the property in the payload that will hold the
        discriminator value."""

        self.mapping: Dict[str, str] = mapping if mapping is not None else {}
        """An object to hold mappings between payload values and schema names or
        references."""

    def get_value(self):
        value = {"propertyName": self.property_name}

        if self.mapping:
            value["mapping"] = {key: value for key, value in self.mapping.items()}

        return value


class SecurityScheme:
    """Defines a security scheme that can be used by the operations.

    Supported schemes are HTTP authentication, an API key (either as a header, a cookie
    parameter or as a query parameter), OAuth2's common flows (implicit, password,
    client credentials and authorization code) as defined in RFC6749, and OpenID Connect
    Discovery.

    Open API security scheme object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#securitySchemeObject
    """

    def __init__(
        self,
        type: str,
        name: str,
        in_: str,
        scheme: str,
        open_id_connect_url: str,
        description: Optional[str] = None,
        bearer_format: Optional[str] = None,
        flows: Optional["OAuthFlows"] = None,
    ):
        self.type: str = type
        """REQUIRED. The type of the security scheme. Valid values are "apiKey",
        "http", "oauth2", "openIdConnect"."""

        self.description: str = description
        """A short description for security scheme. CommonMark syntax MAY be used for
        rich text representation."""

        self.name: str = name
        """REQUIRED. The name of the header, query or cookie parameter to be used."""

        self.in_: str = in_
        """REQUIRED. The location of the API key. Valid values are "query", "header" or
        "cookie"."""

        self.scheme: str = scheme
        """REQUIRED. The name of the HTTP Authorization scheme to be used in the
        Authorization header as defined in RFC7235. The values used SHOULD be registered
        in the IANA Authentication Scheme registry."""

        self.bearer_format: str = bearer_format
        """A hint to the client to identify how the bearer token is formatted. Bearer
        tokens are usually generated by an authorization server, so this information is
        primarily for documentation purposes."""

        self.flows: List[OAuthFlows] = flows if flows is not None else []
        """REQUIRED. An object containing configuration information for the flow types
        supported."""

        self.open_id_connect_url: str = open_id_connect_url
        """REQUIRED. OpenId Connect URL to discover OAuth2 configuration values. This
        MUST be in the form of a URL."""

    def get_value(self):
        value = {
            "type": self.type,
            "name": self.name,
            "in": self.in_,
            "scheme": self.scheme,
            "flows": [flow.get_value() for flow in self.flows],
            "openIdConnectUrl": self.open_id_connect_url,
        }

        if self.description:
            value["description"] = self.description
        if self.bearer_format:
            value["bearerFormat"] = self.bearer_format

        return value


class OAuthFlows:
    """Allows configuration of the supported OAuth Flows.

    Open API OAuth flows object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#oauthFlowsObject
    """

    def __init__(
        self,
        implicit: Optional["OAuthFlow"] = None,
        password: Optional["OAuthFlow"] = None,
        client_credentials: Optional["OAuthFlow"] = None,
        authorization_code: Optional["OAuthFlow"] = None,
    ):
        self.implicit = implicit
        """Configuration for the OAuth Implicit flow"""

        self.password = password
        """Configuration for the OAuth Resource Owner Password flow"""

        self.client_credentials = client_credentials
        """Configuration for the OAuth Client Credentials flow. Previously called
        application in OpenAPI 2.0."""

        self.authorization_code = authorization_code
        """Configuration for the OAuth Authorization Code flow. Previously called
        accessCode in OpenAPI 2.0."""

    def get_value(self):
        value = {}

        if self.implicit is not None:
            value["implicit"] = self.implicit.get_value()
        if self.password is not None:
            value["password"] = self.password.get_value()
        if self.client_credentials is not None:
            value["clientCredentials"] = self.client_credentials.get_value()
        if self.authorization_code is not None:
            value["authorizationCoee"] = self.authorization_code.get_value()

        return value


class OAuthFlow:
    """Configuration details for a supported OAuth Flow.

    Open API OAuth flow object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#oauthFlowObject
    """

    def __init__(
        self,
        authorization_url: str,
        token_url: str,
        refresh_url: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
    ):
        self.authorization_url = authorization_url
        """REQUIRED. The authorization URL to be used for this flow. This MUST be in the
        form of a URL."""

        self.token_url = token_url
        """REQUIRED. The token URL to be used for this flow. This MUST be in the form
        of a URL."""

        self.refresh_url = refresh_url
        """The URL to be used for obtaining refresh tokens. This MUST be in the form
        of a URL."""

        self.scopes: Dict[str, str] = scopes if scopes is not None else {}
        """REQUIRED. The available scopes for the OAuth2 security scheme. A map between
        the scope name and a short description for it. The map MAY be empty."""

    def get_value(self):
        value = {
            "authorizationUrl": self.authorization_url,
            "tokenUrl": self.token_url,
            "scopes": self.scopes,
        }

        if self.refresh_url is not None:
            value["refreshUrl"] = self.refresh_url

        return value


class SecurityRequirement:
    """Lists the required security schemes to execute this operation.

    The name used for each property MUST correspond to a security scheme declared in
    the Security Schemes under the Components Object.

    Open API security requirement object as described here:
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md#securityRequirementObject
    """

    def __init__(self, values: Dict[str, List[str]] = None):
        self.values: Dict[str, List[str]] = values if values is not None else {}
        """Each name MUST correspond to a security scheme which is declared in the
        Security Schemes under the Components Object. If the security scheme is of
        type "oauth2" or "openIdConnect", then the value is a list of scope names
        required for the execution, and the list MAY be empty if authorization does
        not require a specified scope. For other security scheme types, the array MUST
        be empty."""

    def get_value(self):
        return self.values
