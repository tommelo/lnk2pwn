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

from generatecmd import GenerateCommand

class CommandStrategy(object):
    """
    The CommandStrategy class.
    This class contains all the command handlers.
    
    The current supported handlers are:

        * generate for the option -g, --generate        
    """

    COMMANDS = {
        "generate": GenerateCommand()
    }

    @staticmethod
    def resolve(args):
        """
        Resolves the command handler strategy.
        
        Parameters
        ----------
        args: Namespace
            The cli arguments.
        
        Returns
        -------
        strategy: Command
            The command handler
        """

        cmd = "".join([key for key in vars(args) if getattr(args, key) is True])
        return CommandStrategy.COMMANDS[cmd]
