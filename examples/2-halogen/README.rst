Open API Builder example with Halogen
=========================================

The purpose of this example is to show how the openapi_builder can be configured, and produces
the output that can be displayed at `/documentation <documentation>`_. This application mimics a simple webservice,
allowing to create, update, and read users. It uses an in-memory database, thus you need to add a new user every
time you (re)start the application. The data is serialized using the halogen_ serialization library.

Installation
------------
This example can be installed using the following command:

.. code:: bash

    pip install -r requirements.txt


Running the example
-------------------
To run the application, use the :code:`flask` command or :code:`python -m flask`. Before you can do that
you need to tell your terminal the application to work with by exporting the :code:`FLASK_APP` environment variable:

.. code:: bash

    export FLASK_APP=server.app:create_app
    flask run

Documentation
-------------
You can visit the documentation at `/documentation <documentation>`_.

.. _halogen: https://halogen.readthedocs.io/en/latest/
.. _documentation: http://localhost:5000/documentation
