import os
from dotenv import load_dotenv

"""
用户名和密码可以在当前目录新建一个.env文本文件,内容如下:
    WEIBO_USERNAME=example
    WEIBO_PASSWORD=example
或者设置相应环境变量
"""

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

USERNAME = os.getenv('WEIBO_USERNAME')
PASSWORD = os.getenv('WEIBO_PASSWORD')

# 评论
COMMENT = 'test'

# 用户id或者个性后缀
USER_ID = os.getenv('WEIBO_USER_ID', None)

USER_URL_PREFIX = 'https://weibo.cn/u/'

URL = 'https://weibo.cn/%s' % USER_ID

LOGIN_HOME_URL = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
LOGIN_URL = 'https://passport.weibo.cn/sso/login'

HEADERS = {
    'Authority': 'weibo.cn',
    'Origin': 'https://weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

LOGIN_HEADERS = {
    'Origin': 'https://passport.weibo.cn',
    'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

ERROR_MSG = {"retcode": 50011015, "msg": "\u7528\u6237\u540d\u6216\u5bc6\u7801\u9519\u8bef",
             "data": {"username": "dacongming"", "errline": 659}}
