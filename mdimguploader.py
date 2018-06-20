# -*- coding:utf-8 -*-

import re
import abc
import os


IMG_REG = "(([C-H]:)|[.\\\/]+)[a-z0-9A-Z.\/\\-_=]+.(jpg|png|jpeg|gif)"


class Uploader(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        self._config = kwargs

    @abc.abstractmethod
    def upload(self, path):
        ...


class QiniuUploader(Uploader):

    def __init__(self, **kwargs):
        super(QiniuUploader, self).__init__(**kwargs)

    def upload(self, path):
        print(path)
        return os.path.relpath(path)


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


if __name__ == '__main__':
    ir = MDImageReplacer(IMG_REG, QiniuUploader())
    ir.replace_file("./image_uploading_example.md", "hello.md")
