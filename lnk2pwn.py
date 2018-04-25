# MIT License
#
# Copyright (c) 2018 tommelo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
# pylint: disable=C0103,C0301,W1202,W0212

"""
lnk2pwn.py
Malicious Shortcut(.lnk) Generator
"""

__author__ = "tommelo"
__license__ = "MIT"
__version__ = "v1.0.0"

import os
import sys
import argparse
from utils.log import Log
from utils.ioutils import IOUtils
from cmd.cmdstrategy import CommandStrategy
from utils.clihelpformatter import CliHelpFormatter

parser = argparse.ArgumentParser(
    prog="lnk2pwn.py",
    usage="python lnk2pwn.py <options>",
    formatter_class=CliHelpFormatter
)

parser.add_argument(
    "json_config",
    nargs="?",
    help="the shortcut json config"
)

parser.add_argument(
    "-g",
    "--generate",
    action="store_true",
    help="generates a malicious shortcut file(default is True)"
)

parser.add_argument(
    "-c",
    "--config-file",
    metavar="",
    type=argparse.FileType('r'),   
    help="the shortcut config file"
)

parser.add_argument(
    "-o",
    "--output-path",
    metavar="",    
    help="the output path"
)

parser.add_argument(
    "--version",
    action="version",
    version=__version__
)

parser.set_defaults(generate=True)
parser.set_defaults(config_file="config.json")

def main(args):
    """
    Executes the lnk2pwn cli tool

    Parameters
    ----------
    args: Namespace
        The cli arguments
    """

    try:

        executor = CommandStrategy.resolve(args)
        executor.execute(args)

        sys.stdout.close()
        sys.stderr.close()

    except KeyError:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    except ValueError as error:
        Log.error(str(error))        
        sys.exit(1)

if __name__ == "__main__":

    try:

        json_config = None

        if IOUtils.is_piped_input():
            json_config = IOUtils.read_piped_input()

        cli_args = parser.parse_args()
        cli_args.json_config = cli_args.json_config or json_config

        main(cli_args)
    
    except KeyboardInterrupt:
        sys.exit(1)