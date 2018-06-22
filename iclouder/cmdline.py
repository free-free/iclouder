# -*- coding:utf-8 -*-


import os
import yaml
from iclouder.commands import Command
from iclouder.utils import shell_echo
import fire


class CMDExecutor(object):

    def __init__(self):
        user_home = os.path.expanduser('~')
        settings_file = os.path.join(user_home, '.iclouder_config')
        self._settings = {}
        if not os.path.exists(settings_file):
            shell_echo("Not Configure settings, please configureit first",\
                    "red")
        else:
            with open(settings_file) as f:
                self._settings = yaml.load(f)

    def run(self, cmd, *params, **kwparams):
        Command.get_cmd_class(cmd)(self._settings).execute(*params, **kwparams)


def execute():
    fire.Fire(CMDExecutor().run)


if __name__ == '__main__':
    execute()
