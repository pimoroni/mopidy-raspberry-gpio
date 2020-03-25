****************************
Mopidy-Raspberry-GPIO
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Raspberry-GPIO.svg
    :target: https://pypi.org/project/Mopidy-Raspberry-GPIO/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/circleci/build/gh/pimoroni/mopidy-raspberry-gpio
    :target: https://circleci.com/gh/pimoroni/mopidy-raspberry-gpio
    :alt: CircleCI build status

.. image:: https://img.shields.io/codecov/c/gh/pimoroni/mopidy-raspberry-gpio
    :target: https://codecov.io/gh/pimoroni/mopidy-raspberry-gpio
    :alt: Test coverage

Mopidy extension for GPIO input on a Raspberry Pi


Installation
============

Install by running::

    python3 -m pip install Mopidy-Raspberry-GPIO

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<https://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Raspberry-GPIO to your Mopidy configuration file::

    [raspberry-gpio]
    enabled = true
    bcm5 = play_pause,active_low,250
    bcm6 = volume_down,active_low,250
    bcm16 = next,active_low,250
    bcm20 = volume_up,active_low,250

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

Events volume_up and volume_down both support an (optional) "step" option, which controls the amount (in percent) that the volume is adjusted with each button press.

Eg::

    [raspberry-gpio]
    enabled = true
    bcm5 = play_pause,active_low,250
    bcm6 = volume_down,active_low,250,step=1
    bcm16 = next,active_low,250
    bcm20 = volume_up,active_low,250,step=1


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
