Skyjack Shell
=============

## Setup

Made for Python2

Dependencies are listed in requirements.txt, install with:
```
pip install -r requirements.txt
```

It is recommended to make use of a python virtualenv for cleaner dependency management.
If you need help with that, virtualenvwrapper is a nice tool to manage your workflow.
See [here](https://virtualenvwrapper.readthedocs.org/en/latest/) for more information.

## Usage

###python skyjack \<WiFi interface\> [--autopwn , --mpwn]

```
--autopwn

intended to be used on a Raspberry Pi with WiFi dongle

* automatic scan for AR drone networks
* if one is found a connection is established
* the owner of the drone is deauthenticated
* the drone is kidnapped using a pre programmed flight routine
```

```
--mpwn

intended to be used on a laptop

* automatic scan for AR drone networks
* if one is found a connection is established
* the owner of the drone is deauthenticated
* dronepwn offers an interface for manual flight of the drone
```
<br>
###python skyjack \<WiFi interface\>

```
skyjack> auto

automatic flight routine
```
```
skyjack> backdoor

-a plant: plants a backdoor PoC on the drone
-a exec:  executes the backdoor
```
```
skyjack> blockothers

deauthenticates all connected users except the attacker
```
```
skyjack> connect <SSID>

connect to <SSID>
```
```
skyjack> manual

manual control of the drone
```
```
skyjack> scan

scans for AR drone networks
```
```
skyjack> shell

prompts a root shell on the drone
```
```
skyjack> help

list all commands
```


Hacking
-------

### Commands

If you want to add your own commands to the shell, check out commands/samplecommand.py.

* copy command/templatecommand.py
* change the class name to something meaningful
* set self.cmd to the name your command will be called with
* set self.parser to an instance of SkyjackArgumentParser and add arguments as [required](https://docs.python.org/3/library/argparse.html)
* execute will be automatically called when your command is invoked, arguments will already be parsed and passed in 'args'
* set the empty docstring in the first line of execute to a short description of your command, it will appear in the output of 'help'
* register your command in skyjack.py by calling skyjack.register_command(YourCommand())


Credits
-------
The dronepwn skyjack shell was made by students of the FH St. Poelten as a project PoC.


