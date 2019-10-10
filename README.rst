****************************
Mopidy-Raspberry-GPIO
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Raspberry-GPIO.svg?style=flat
    :target: https://pypi.org/project/Mopidy-Raspberry-GPIO/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/pimoroni/mopidy-raspberry-gpio/master.svg?style=flat
    :target: https://travis-ci.org/pimoroni/mopidy-raspberry-gpio
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/pimoroni/mopidy-raspberry-gpio/master.svg?style=flat
   :target: https://coveralls.io/r/pimoroni/mopidy-raspberry-gpio
   :alt: Test coverage

Mopidy extension for GPIO input on a Raspberry Pi


Installation
============

Install by running::

    pip install Mopidy-Raspberry-GPIO

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<https://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Raspberry-GPIO to your Mopidy configuration file::

    [raspberry-gpio]
    enabled = true
    bcm0 = 
    bcm1 =
    bcm2 =
    bcm3 =
    bcm4 = play_pause,active_low,30
    bcm5 = volume_up,active_low,30
    bcm6 = volume_down,active_low,30
    bcm7 =
    bcm8 =
    bcm9 =
    bcm10 =
    bcm11 =
    bcm12 =
    bcm13 =
    bcm14 =
    bcm15 =
    bcm16 =
    bcm17 =
    bcm18 =
    bcm19 =
    bcm20 =
    bcm21 =
    bcm22 =
    bcm23 =
    bcm24 =
    bcm25 =
    bcm26 =
    bcm27 =

Each bcmN entry corresponds to the BCM pin of that number.

You must assign an event, mode and bouncetime (ms) to your desired pins.

Supported events:

- play_pause
- volume_up
- volume_down
- next
- prev

Supported modes:

- active_low - configures the pin with a pull-up and triggers when it reads 0/low (RECOMMENDED)
- active_high - configures the pin as a pull-down and triggers when it reads 1/high


Project resources
=================

- `Source code <https://github.com/pimoroni/mopidy-raspberry-gpio>`_
- `Issue tracker <https://github.com/pimoroni/mopidy-raspberry-gpio/issues>`_
- `Changelog <https://github.com/pimoroni/mopidy-raspberry-gpio/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `Phil Howard <https://github.com/pimoroni>`__
- Current maintainer: `Phil Howard <https://github.com/pimoroni>`__
- `Contributors <https://github.com/pimoroni/mopidy-raspberry-gpio/graphs/contributors>`_
