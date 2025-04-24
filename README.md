# Midimator
#### A automation tool to process midi messages, written in python 3

<p align="middle">
	<img src="res/midimator_128x128.png"/>
</p>

##

This python program automates your midi workflow.

For this very first version, the only features available are :
- MIDI devices enumeration function
- Transfer function : incoming MIDI messages from port#1 are sent to port#2 without any change
- Capture function : capture and print incoming MIDI messages
- Send message function

##
> **Note :**
> some commands offer the possibility to create a virtual midi device, but it does not work under Windows.
> If you need a virtual device under Windows, you must use a virtual midi driver, like :
> - LoopBe1 (https://www.nerds.de/en/download.html) : Works with Windows 7 - 11
> - LoopMidi (https://www.tobias-erichsen.de/software/loopmidi.html) : Works with Windows 7 - 10

## TODO
The next features will be :
- Reading MIDI translations from configuration file
- Message filtering
- Message transform / tailoring

## Installation
- Install python 3.8+
- Install python-rtmidi library :
```sh
python -m pip install python-rtmidi
```
If installation of python-rtmidi fails, it is likely because binaries have not yet been compiled for the version of python you are using. The solution is to install an older version of python.

## Usage
use '-h' parameter to get help :
```sh
python midimator.py -h
```

## Tech and dependencies
- [Python 3] - Required version is 3.7+
- [python-rtmidi] - a python library to receive and send MIDI messages


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

  [python 3]: <https://www.python.org/about/>
  [python-rtmidi]: <https://pypi.org/project/python-rtmidi/>
  