Change Log
==========

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`__.

[Unreleased]
------------

[2.0] - 2016-08-15
------------------

- Using ``topic`` instead of ``direct`` RabbitMQ exchanger for improved
  flexibility in message receiving (breaking change! all services must use this
  new version of ``hms_base`` in order to speak together)
- Added ``listen_all`` option to client and made listening topics optional

[1.0] - 2016-06-19
------------------

- First prototype from existing HMS services
