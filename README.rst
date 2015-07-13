|build| |version|

Python OBD Library
== == == == == == == == ==

OBD Lib provides easy access to ELM327 OBD - II Interfaces in Python.
It's been successfully used with ELM327 OBD - II bluetooth scanners and the Raspberry Pi to create portable automotive
OBD - II logging devices.  Data can be captured during test drives for later analysis.  It may also be used as part of
routine driving to gather information to determine an optimal vehicle maintenance schedule.  Continuous logging may
also help with vehicle troubleshooting when problems occur.

The library is still under development. Initial work focused on reading from and writing to ELM327 OBD - II interfaces.

Installation
------------

Install using pip_

.. code - block:: bash

    $ pip install obdlib

Quick start
-----------

.. code - block:: python

    from obdlib.obd.scanner import OBDScanner

    with OBDScanner() as obd:
        print('ELM version'.format(obd.elm_version))
        print('Vehicle Identification Number (VIN): {0}'.format(
            obd.vehicle_id_number()))
        print('Engine Control Unit (ECU) Name: {0}'.format(obd.ecu_name()))
        print('Battery voltage: {0}'.format(obd.battery_voltage()))
        print('Fuel type: {0}'.format(obd.fuel_type()))
        print('Coolant temp: {0}'.format(
            obd.current_engine_coolant_temperature()))
        print('Oil temp: {0}'.format(obd.current_engine_oil_temperature()))
        print('Engine RPM: {0}'.format(obd.current_engine_rpm()))

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
.. |build| image:: https://travis-ci.org/s-s-boika/obdlib.svg
       :target: https://travis-ci.org/s-s-boika/obdlib

.. _pip:
    https:
        //pypi.python.org / pypi / pip

.. _LICENSE:
    LICENSE.txt

.. | version | image:: https://badge.fury.io/py/obdlib.svg
    :target: https://pypi.python.org/pypi/obdlib/
