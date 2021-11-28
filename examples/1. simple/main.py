"""Simple Flask REST API that uses the OpenAPI builder to generate the documentation.

Run using the following command:

    $ python main.py
"""


if __name__ == "__main__":
    from server.app import app

    app.run()
