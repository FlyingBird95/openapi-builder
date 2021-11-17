from openapi_builder.specification import Contact


def test_contact_serialization():
    """Test how a Contact-object is serialized."""
    assert Contact().get_value() == {}
    assert Contact(name="name").get_value() == {"name": "name"}
    assert Contact(url="url").get_value() == {"url": "url"}
    assert Contact(email="email").get_value() == {"email": "email"}
