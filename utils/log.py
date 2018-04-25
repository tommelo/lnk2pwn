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

import logging

logging.basicConfig(format="%(message)s")
log = logging.getLogger("lnk2pwn")
log.setLevel(logging.INFO)

class Log(object):
    """
    The Log class.

    This is a helper class to make it easier
    to output content to the cli.
    """

    INFO_FORMAT = "\033[1m[+]\033[0m {}"
    WARN_FORMAT = "\033[1m[*]\033[0m {}"
    ERROR_FORMAT = "\033[1m[!]\033[0m {}"

    @staticmethod
    def raw_info(message):
        log.info(message)

    @staticmethod
    def info(message):
        text = Log.INFO_FORMAT.format(message)
        log.info(text)

    @staticmethod
    def warn(message):
        text = Log.WARN_FORMAT.format(message)
        log.info(text)

    @staticmethod
    def error(message):
        text = Log.ERROR_FORMAT.format(message)
        log.error(text)
