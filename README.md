
### 简介

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;实现markdown文档中的本地图片自动上传并自动替换图片链接。

### 支持说明

`图片存储支持` : qiuiu(暂时)

`python` : >=3.4


### 安装

```sh
$ pip install iclouder
```

### 使用

##### 1. 创建配置

```sh
$ iclouder config create
```
执行上面命令后，按照提示输入相关配置信息

##### 2. 上传并替换图片路径

```sh
$ iclouder replace --in-file input.md --out-file out.md
```
或者
```sh
$ iclouder replace --in-file input.md % 在原文件上进行修改
```

例如：

替换前

```markdown
图像上传

示例图像，示例图像
![a2c8deca0561cdc6dbdca555d2d3825e](/home/xxx/Pictures/upgrade-from-ubuntu-17.04-to-ubuntu-17.10-07.png

![a2c8deca0561cdc6dbdca555d2d3825e](/home/xxx/Pictures/a2c8deca0561cdc6dbdca555d2d3825e.jpg)

<img src="/home/xxx/Pictures/code1.png" />

```

替换后

```markdown
图像上传

示例图像，示例图像
![a2c8deca0561cdc6dbdca555d2d3825e](http://oz7mpt8xg.bkt.clouddn.com/dd47be5df027d12c82bad5a65bd9d4081d581b1ebbc792fb6510a38c894ef259.png)

![a2c8deca0561cdc6dbdca555d2d3825e](http://oz7mpt8xg.bkt.clouddn.com/d082ad3209a1ed9544f2462c0a9a1568d1ce4ec0ee26d5bfbff5f2cf4a2db531.jpg)  

<img src="http://oz7mpt8xg.bkt.clouddn.com/e6524ccb0455b98200f9efa29de7209ebc5cb13c5d00507ca5d56733757b2b93.png" />

```


### LICENSE
[MIT](LICENSE.md)
