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

# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4
# pylint: disable=C0103,C0301,W1202,W0212

import os
import abc
import subprocess
from utils.log import Log

class Command(object):
    """
    The abstract Command class.

    All command handlers should inherit this class.
    This class has a default command execution based on the given cli arguments. 
    It also handlesthe piped/output option.
    """

    __metaclass__ = abc.ABCMeta

    BANNER = """
                 ,-*
                (_).lnk
           -----------------           
               <lnk2pwn>

    Malicious Shortcut(.lnk) Generator

                             [tommelo]
                                v1.0.0
    """

    def __init__(self, handler):
        """
        Initiates the class.

        Parameters
        ----------
        handler: func
            The command handler to be executed based on the given cli args.
        """

        self.handler = handler

    def __which(self, name):
        """
        Checks if an application is installed.

        Parameters
        ----------
        name: str
            The application name

        Returns
        ----------
        is_installed: Bool
            True if is installed, false otherwise
        """

        try:

            devnull = open(os.devnull)
            subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()

        except OSError as e:

            if e.errno == os.errno.ENOENT:
                return False
        
        return True

    def delegate(self, args, **kwargs):
        """
        Executes the command based on the given cli args.

        Parameters
        ----------
        args: Namespace
            The argparse cli arguments
        kwargs: dict
            The arguments to be passed to the handler
        """

        Log.raw_info(self.BANNER)        

        Log.info("Checking wine installation")
        if not self.__which("wine"):
            raise ValueError("Unable to continue: wine NOT FOUND")            
        
        Log.info("wine status: OK")
        self.handler(args, kwargs)

    @abc.abstractmethod
    def execute(self, args):
        """
        Handles the command execution.

        Parameters
        ----------
        args: Namespace
            The argparse cli arguments
        """

        raise NotImplementedError('The execute method must be implemented')