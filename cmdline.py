# -*- coding:utf-8 -*-

import os
import yaml
from commands import Command
import fire


class CMDExecutor(object):


    def __init__(self):
        user_home = os.path.expanduser('~')
        settings_file = os.path.join(user_home,'.mdimguploader')
        self._settings = {}
        if not os.path.exists(settings_file):
            raise Exception("Not Configure settings, please configure\
                    it first")
        with open(settings_file) as f:
            self._settings = yaml.load(f)


    def run(self, cmd, *params, **kwparams):
        Command.get_cmd_class(cmd)(self._settings).execute(*params, **kwparams)


if __name__ == '__main__':
    fire.Fire(CMDExecutor().run)
