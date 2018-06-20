# -*- coding:utf-8 -*-


import os
import re
import yaml



def run():
    config = {}
    print("欢迎使用mdimguploader配置器....")
    
    def simple_request(var, prompt, filter_input=None):
        text = input(prompt + ' : ')
        if text:
            if filter_input:
                text=filter_input(text)
            config[var] = text

    simple_request('backend', '请输入图片储存服务(qiniu)')
    if config['backend'].strip() == 'qiniu':
        simple_request('bucket', '请输入bucket name')
        simple_request('bucket_url', '请输入bucket url')
        simple_request('access_key', '请输入access key')
        simple_request('secret_key', '请输入secret key')
        config['qiniu'] = {}
        config['qiniu']['bucket'] = config['bucket']
        config['qiniu']['access_key'] = config['access_key']
        config['qiniu']['secret_key'] = config['secret_key']
        config['qiniu']['bucket_url'] = config['bucket_url']
        del config['bucket']
        del config['access_key']
        del config['secret_key']
        del config['bucket_url']
    user_home = os.path.expanduser('~')
    config_file = os.path.join(user_home, '.mdiup_config')
    with open(config_file,'w') as f:
        yaml.dump(config, f, default_flow_style=False)


if __name__ == '__main__':
    run()

                

