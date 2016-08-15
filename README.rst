=============================
hms_base, base module for HMS
=============================

This Python module is very simple and allow you to connect to the HMS network
with the protocol already implemented.

Features
========

A basic HMS microservice can do the following:

- Connect to the messaging server
- Publish a message with a topic key
- Receive and handle messages from various topic keys

And that's it. All these functions are provided by this Python module.

Installing
==========

hms_base is `available on PyPI <https://pypi.python.org/pypi/hms_base>`_ so
you can register it as a dependency for microservices your create.

Be sure to respect semantic versioning for non-breaking changes:

::

    hms_base>=2.0,<3

License
-------

This project is brought to you under MIT license. For further information,
please read the provided ``LICENSE.txt`` file.
