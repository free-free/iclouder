# -*- coding:utf-8 -*-


import sys
import subprocess
import shlex
import datetime
import functools
from colorama import init as colorama_init
from termcolor import colored, cprint



COLORAMA_INITIATION_FLG = False


def execute_shell_cmd(cmd, timeout=60, bufsize=4096):
    assert isinstance(cmd, str)
    cmd = shlex.split(cmd)
    sub = subprocess.Popen(cmd, stdin=subprocess.PIPE, \
            bufsize=bufsize)
    end_time = datetime.datetime.now() + \
            datetime.timedelta(seconds=timeout)
    while sub.poll() is None:
        if timeout:
            if end_time < datetime.datetime.now():
                raise Exception("failed to exceute `%s`"\
                        % (cmd))
    return sub.returncode


def _chk_platform(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        """
            Cause the module `colorama` is required to call 
            `init` function when it's running windows, the 
            purpose of code here is to check platform and so as to 
            avoid repeatedly calling `init` function.
        """
        if sys.platform == 'win32':
            global COLORAMA_INITATION_FLG
            if not COLORAMA_INITIATION_FLG:
                colorama_init()
                COLORAMA_INITIATION_FLG = True
        return func(*args, **kwargs)
    return _wrapper
        

@_chk_platform
def color_input(prompt, color, highlight_color=None):
    if isinstance(highlight_color, str):
        highlight_color = 'on_' + highlight_color 
    return input(colored(prompt, color, highlight_color))


@_chk_platform
def color_print(text,color, highlight_color=None):
    if isinstance(highlight_color, str):
        highlight_color = 'on_' + highlight_color 
    return cprint(text, color, highlight_color)


