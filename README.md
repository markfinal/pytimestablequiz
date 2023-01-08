# Times table quiz
A quiz to practice your times tables up to 12.

Voice synthesizer support somewhat inspired by Joshua in [WarGames](https://war-games.fandom.com/wiki/Joshua).

# Prerequisites
* Python 3

## Windows
For the voice synthesizer, install https://github.com/espeak-ng/espeak-ng/releases/download/1.51/espeak-ng-X64.msi.
The command `espeak-ng.exe` is installed to your `PATH` by the installer.

## Ubuntu/Raspberry Pi
For the voice synthesizer
```
apt install espeak-ng
```

## MacOSX
For the voice synthesizer, untested support via MacPorts, https://ports.macports.org/port/espeak-ng/

# How to use
Run
```
python timestablequiz.py
```
To change the voice to male:
```
python timestablequiz.py -v male
```
To change the voice to female:
```
python timestablequiz.py -v female
```
