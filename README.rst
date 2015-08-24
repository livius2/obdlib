|build| |version| |scrutinizer| |coverage|

Python OBD Library
==================

OBD Lib provides easy access to ELM327 OBD - II Interfaces in Python.
It's been successfully used with ELM327 OBD - II bluetooth scanners and the Raspberry Pi to create portable automotive
OBD - II logging devices.  Data can be captured during test drives for later analysis.  It may also be used as part of
routine driving to gather information to determine an optimal vehicle maintenance schedule.  Continuous logging may
also help with vehicle troubleshooting when problems occur.

The library is still under development. Initial work focused on reading from and writing to ELM327 OBD - II interfaces.

Installation
------------

Install using pip_

.. code-block:: bash

    $ pip install obdlib


Installation for micropython
------------

For installing run:

.. code-block:: bash

    $ MICROPYPATH='path-to-pyboard' pip-micropython install obdlib

Quick start
-----------

.. code-block:: python

    import obdlib.scanner as scanner
    import time

    # Example 1
    # Retrieves value from one sensor
    with scanner.OBDScanner("/dev/pts/6") as scan:
        while True:
            if scan.sensor:
                if scan.sensor.is_pids():
                    # Engine coolant temperature
                    sensor = scan.sensor[1]('05')
                    # two or more ECU's respond to one request
                    # we should be prepared for it
                    for ecu, value in sensor.ecus:
                        print("ECU: {} Sensor {}: {} {}".format(ecu, sensor.title, value, sensor.unit))
                    time.sleep(0.5)
                else:
                    raise Exception("Pids are not supported")
            else:
                break

Supported Python Versions
-------------------------

OBDLib makes every effort to ensure smooth operation with these Python interpreters:

* 2.7+
* 3.4+
* PyPy
* micropython

License
-------

See LICENSE_ for details.


.. _pip:
    https://pypi.python.org/pypi/pip

.. _LICENSE:
    LICENSE.txt

.. |build| image:: https://travis-ci.org/s-s-boika/obdlib.svg
    :target: https://travis-ci.org/s-s-boika/obdlib

.. |version| image:: https://badge.fury.io/py/obdlib.svg
    :target: https://pypi.python.org/pypi/obdlib/

.. |scrutinizer| image:: https://scrutinizer-ci.com/g/s-s-boika/obdlib/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/s-s-boika/obdlib/

.. |coverage| image:: https://scrutinizer-ci.com/g/s-s-boika/obdlib/badges/coverage.png?b=master
    :target: https://scrutinizer-ci.com/g/s-s-boika/obdlib/
