# -*- coding:utf-8 -*-


import os
import yaml
from iclouder.commands import Command
from iclouder.utils import color_print
import fire


class CMDExecutor(object):


    def __init__(self):
        user_home = os.path.expanduser('~')
        settings_file = os.path.join(user_home, '.iclouder_config')
        self._settings = {}
        if not os.path.exists(settings_file):
            color_print("Not Configure settings, please configureit first",\
                    "red")
        else:
            with open(settings_file) as f:
                self._settings = yaml.load(f)


    def run(self, cmd, *params, **kwparams):
        # If one assigns --with-config or --with_config with a file name,
        # then it would read configurations from the new file or
        # write configuration  to the new file.
        config_file = kwparams.get("with_config") or kwparams.get("with-config")
        if config_file:
            try:
                with open(config_file) as f:
                    self._settings = yaml.load(f)
            except FileNotFoundError:
                if cmd != 'config':
                    color_print("Not Found %s file!" % config_file)
        Command.get_cmd_class(cmd)(self._settings).execute(*params, **kwparams)


def execute():
    fire.Fire(CMDExecutor().run)


if __name__ == '__main__':
    execute()
