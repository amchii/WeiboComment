import requests
import config


def login_for_session():
    session = requests.Session()
    login_data = {
        'username': config.USERNAME,
        'password': config.PASSWORD,
        'savestate': '1',
        'r': 'https://weibo.cn/',
        'ec': '0',
        'pagerefer': 'https://weibo.cn/pub/',
        'entry': 'mweibo',
        'mainpageflag': '1',
    }
    print(config.USERNAME, config.PASSWORD)

    r = session.post(config.LOGIN_URL, data=login_data, headers=config.LOGIN_HEADERS)
    # print(r.text)
    # print(r.headers)
    # print(r.cookies.get_dict())
    # resp = session.get(config.url)
    # print(resp.text)
    if b'errline' in r.content:
        print('登陆失败.')
        print('Login data: \n', login_data)
    else:
        return session
