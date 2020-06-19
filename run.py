from weibo import WeiboUser
import config

if __name__ == '__main__':
    user = WeiboUser(url=config.URL)
    user.run_comment()
