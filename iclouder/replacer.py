# -*- coding:utf-8 -*-


import re
import abc
import os
import qiniu
from qiniu import put_file
import yaml
import hashlib
import time
from urllib import parse


IMG_REG = "(([C-H]:)|[.\\\/]+)[a-z0-9A-Z.\/\\-_=]+.(jpg|png|jpeg|gif)"


class Uploader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def upload(self, path):
        ...


class QiniuUploader(Uploader):

    def __init__(self, **kwargs):
        super(QiniuUploader, self).__init__()
        assert 'bucket' in kwargs
        assert 'access_key' in kwargs
        assert 'secret_key' in kwargs
        assert 'bucket_domain' in kwargs
        self._config = kwargs
        self._ins = qiniu.Auth(self._config.get('access_key'),
                               self._config.get('secret_key'))
        self._token = self._ins.upload_token(self._config.get('bucket'))

    def upload(self, path):
        key = hashlib.sha256(
            (path + str(time.time())).encode("utf-8")).hexdigest()
        key = key + os.path.splitext(path)[1]
        ret, _ = put_file(self._token, key, path)
        img_url = parse.urljoin(self._config.get('bucket_domain'), ret['key'])
        return img_url


class MDImageReplacer(object):

    def __init__(self, reg, uploader):
        self._img_reg = reg
        self._md_img_reg = '(!\[[a-z0-9A-Z-_=]+\]\(' + self._img_reg + '\))' + '|' + \
            '(<img\s+src="' + self._img_reg + '"\s+\/?>)'
        self._uploader = uploader

    def _replace_image(self, matched_img):
        img_path = matched_img.group()
        """
            if matched_img is a geniune image path, then
            just upload image to cloud and return image url
        """
        if re.match(self._img_reg, img_path):
            return self._uploader.upload(img_path)
        """
            if matched_img is an image path marked with markdown syntax,like
            ![](./hello/hello.jpg) or <img src="./hello/hello.jpg" />, matched_img
            need to continue extracting the geniune image path by repeatly calling
            re.sub() function.
        """
        return re.sub(self._img_reg, self._replace_image, img_path)

    def replace_text(self, text):
        return re.sub(self._md_img_reg, self._replace_image, text)

    def replace_file(self, in_file, out_file=""):
        if out_file:
            with open(in_file, "r") as fin, open(out_file, "w") as fout:
                fout.write(self.replace_text(fin.read()))
        else:
            with open(in_file, "r+") as fin:
                file_content = fin.read()
                fin.seek(0)
                fin.write(self.replace_text(file_content))
