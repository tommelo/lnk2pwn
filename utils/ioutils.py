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

import sys

class IOUtils(object):
    """
    The IOUtils class.

    This is an utility class to make it easier to
    perform io actions such as detecting piped input, 
    piped output and piped input read/parse.
    """

    @staticmethod
    def is_piped_input():
        """
        Checks the piped input.

        This function checks if the script
        is being executed with a piped input.

        E.g.: echo "input" | python scrypt.py

        Returns
        -------
        bool
            True if the is a piped input, False otherwise.
        """

        return not sys.stdin.isatty()
    
    @staticmethod
    def is_piped_output():
        """
        Checks the piped output.

        This function checks if the script
        is being executed with a piped output.

        E.g.: python scrypt.py -c caesar -e "plaintext" > result.txt

        Returns
        -------
        bool
            True if the is a piped output, False otherwise.
        """

        return not sys.stdout.isatty()
   
    @staticmethod
    def read_piped_input():
        """
        Reads the content of the piped input.

        Returns
        -------
        str
            The striped string content
        """

        return sys.stdin.read().strip()

