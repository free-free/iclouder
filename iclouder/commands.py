# -*- coding:utf-8 -*-


import abc
import os
import yaml
from iclouder.replacer import MDImageReplacer
from iclouder.replacer import QiniuUploader
from iclouder.replacer import IMG_REG
from iclouder.utils import shell_echo

class Command(object, metaclass=abc.ABCMeta):


    CMD_CLASSES = {}
    CMD_NAME = ''


    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError


    @classmethod
    def get_cmd_class(cls, cmd_name=""):
        cmds = cls.__subclasses__()
        for klass in cmds:
            cls.CMD_CLASSES[klass.CMD_NAME] = klass
        if not cmd_name:
            return cls.CMD_CLASSES
        return cls.CMD_CLASSES.get(cmd_name)


class ReplaceUrlCommand(Command):


    CMD_NAME = 'replace'


    def __init__(self, settings, *args, **kwargs):
        assert isinstance(settings, dict)
        self._settings = settings


    def execute(self, in_file, out_file=""):
        if self._settings.get('backend') == 'qiniu':
            uploader = QiniuUploader(**self._settings['qiniu'])
        ir = MDImageReplacer(IMG_REG, uploader)
        ir.replace_file(in_file, out_file)


class ConfigCommand(Command):


    CMD_NAME = 'config'


    def __init__(self, *args, **kwargs):
        self._config = {}
        user_home = os.path.expanduser('~')
        self._cfile_path = os.path.join(user_home, '.iclouder_config')


    def _ask_input(self, var, prompt, _filter=None):
        text = input(prompt + ' : ')
        if text:
            if _filter:
                text = _filter(text)
            self._config[var] = text


    def _merge_dict(self, _dict, to_key, from_keys=tuple()):
        if to_key not in _dict:
            _dict[to_key] = {}
        for key in from_keys:
            _dict[to_key][key] = _dict[key]
            del _dict[key]
        return _dict


    def _dump_configuration(self):
        with open(self._cfile_path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)


    def _load_configuration(self):
        with open(self._cfile_path, 'r') as f:
            self._config = yaml.load(f)
        return self._config


    def execute(self, opera):
        if hasattr(self, opera):
            opera_fn = getattr(self, opera)
            return opera_fn()


    def create(self):
        shell_echo("Welcome to iclouder settings configer:","green")
        self._ask_input('backend', 'please input image storage(qiniu)')
        if self._config['backend'].strip() == 'qiniu':
            self._ask_input('bucket', 'please input bucket name')
            self._ask_input('bucket_domain', 'please input bucket domain')
            self._ask_input('access_key', 'please input access key')
            self._ask_input('secret_key', 'please input secret key')
            self._config = self._merge_dict(self._config, 'qiniu',
                                            ('bucket', 'bucket_domain', 'access_key',
                                             'secret_key'))
        self._dump_configuration()


