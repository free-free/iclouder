# -*- coding:utf-8 -*-


import re
import abc
import os
import qiniu
from qiniu import put_file
import yaml
import hashlib
import time
import functools
from base64 import urlsafe_b64encode
from urllib import parse 


# Just match ascii character based path name
IMG_REG = "(([C-H]:)|[.\\\/]+)[a-z0-9A-Z.\/\\-_=]+.(jpg|png|jpeg|gif)"
# Fix IMG_REG, support any kind of character as a path name 
FULL_IMG_REG = "(([C-H]:)|[.\\\/]+)(.*?).(jpg|png|jpeg|gif)\??([a-zA-Z0-9_-]+=[\u4e00-\u9fa5a-zA-Z0-9-_@\/\\.:#]+&?)*"


def b64encode(string, encode='utf-8'):
    return urlsafe_b64encode(string.encode(encode)).decode(encode)


def image_operation(func):
    @functools.wraps(func)
    def _wrapper(self, path):
        splited_parts = path.split("?")
        img_url = func(self, splited_parts[0])
        if len(splited_parts) == 1:
            return img_url
        opera_dict = parse.parse_qs(splited_parts[-1])
        return self.process_image(img_url, opera_dict)
    return _wrapper


class Uploader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def upload(self, img_path):
        ...

    
    @abc.abstractmethod
    def process_image(self, img_url, opera_dict):
        ...


class DummyUploader(Uploader):


    def __init__(self, **kwargs):
        pass


    @image_operation
    def upload(self, img_path):
        print("matched_path: " + img_path)
        return img_path


    def process_image(self, img_url, opera_dict):
        return img_url



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


    @image_operation
    def upload(self, path):
        key = hashlib.sha256(
            (path + str(time.time())).encode("utf-8")).hexdigest()
        key = key + os.path.splitext(path)[1]
        ret, _ = put_file(self._token, key, path)
        img_url = parse.urljoin(self._config.get('bucket_domain'), ret['key'])
        return img_url


    def process_image(self, img_url, opera_dict):
        opera_str = ''
        if 'water_text' in opera_dict and 'water_image' in opera_dict:
            opera_str = '?watermark/3'
        elif 'water_image' in opera_dict:
            opera_str = '?watermark/1'
        elif 'water_text' in opera_dict:
            opera_str = '?watermark/2'
        else:
            opera_str = ''
        if 'water_text' in opera_dict:
            opera_str += '/text'
            opera_str += '/' + b64encode(opera_dict.get('water_text', ['@iclouder'])[0])
            opera_str += '/font'
            opera_str += '/' + b64encode(opera_dict.get('font', ['宋体'])[0])
            opera_str += '/fill'
            opera_str += '/' + b64encode(opera_dict.get('color', ['white'])[0])
            opera_str += '/fontsize/' + opera_dict.get('fontsize', ['500'])[0]
            opera_str += '/dissolve/' + opera_dict.get('t_dissolve', ['100'])[0]
            opera_str += '/dx/' + opera_dict.get('t_dx', ['10'])[0]
            opera_str += '/dy/' + opera_dict.get('t_dy', ['10'])[0]
            opera_str += '/gravity/' + opera_dict.get('t_gravity', ['SouthEast'])[0]
        if 'water_image' in opera_dict:
            water_image_url = opera_dict.get('water_image',[''])[0]
            if not water_image_url:
                return img_url + opera_str
            if not water_image_url.startswith("http://") \
                    and not water_image_url.startswith("https://"):
                water_image_url = self.upload(water_image_url)
            opera_str += '/image'
            opera_str += '/' + b64encode(water_image_url)
            opera_str += '/dissolve/' + opera_dict.get('i_dissolve', ['100'])[0]
            opera_str += '/dx/' + opera_dict.get('i_dx', ['10'])[0]
            opera_str += '/dy/' + opera_dict.get('i_dy', ['10'])[0]
            opera_str += '/gravity/' + opera_dict.get('i_gravity', ['SouthEast'])[0]
            opera_str += '/ws/' + opera_dict.get('ws', ['1'])[0]
            opera_str += '/wst/' + opera_dict.get('wst', ['0'])[0]
        return img_url + opera_str


class MDImageReplacer(object):


    def __init__(self, reg, uploader):
        self._img_reg = reg
        self._md_img_reg = re.compile('(!\[(.*)\]\(' + self._img_reg + '\))' + '|' + \
            '(<img\s+src="' + self._img_reg + '"\/?>)')
        self._img_reg = re.compile(self._img_reg)
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
