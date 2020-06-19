import re
import time
import logging
from datetime import datetime
from pyquery import PyQuery
from weibo.login import login_for_session

import config

logging.basicConfig(level=logging.INFO)


class LoginError(Exception):
    pass


class WeiboUser(object):
    def __init__(self, url, headers=None, url_prefix=None, **kwargs):
        self.url = url
        self.headers = headers
        if url_prefix is None:
            url_prefix = 'https://weibo.cn'
        self.url_prefix = url_prefix
        self.session = self.get_session()

    @staticmethod
    def get_session():
        session = login_for_session()
        if session is None:
            raise LoginError('Login Failed.')
        return session

    def refresh_session(self):
        self.session = self.get_session()

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.session.post(url, data=data, **kwargs)

    def parse_post_in_time(self, minutes=1):
        """
        Get the comment's url.
        """
        resp = self.get(self.url)
        data = resp.content
        if b'refresh' in data or b'errorDialog' in data:
            logging.warning('Cookie已失效.')
            return False
        # print(data)
        doc = PyQuery(data)
        posts = doc.find('div.c[id^=M]')
        for post in posts.items():
            post_time = post.find('span.ct').text().strip()
            logging.info('本条微博发布于' + post_time)
            if re.match(r'\s*%s分钟.*' % minutes, post_time):
                comment = post.find('a.cc')
                comment_url = comment.attr('href') if len(
                    comment) == 1 else comment[-1].attrib['href']
                logging.info("Comment's url: " + comment_url)
                return comment_url
        return None

    def parse_comment(self, url):
        resp = self.get(url)
        doc = PyQuery(resp.content)
        form = doc.find('#cmtfrm form')
        post_comment_url = self.url_prefix + form.attr('action')
        data = {
            'srcuid': form.find('input[name=srcuid]').attr('value'),
            'id': form.find('input[name=id]').attr('value'),
            'rl': form.find('input[name=rl]').attr('value'),
        }
        logging.info("Post-comment's url:" + post_comment_url)
        return post_comment_url, data

    def post_comment(self, url, data, message):
        data['content'] = message
        self.post(url, data=data)
        logging.info('Comment:"%s" post success!' % message)

    def run_comment(self, minutes=1, interval=30, times=1):
        """

        :param minutes: Int. Define the satisfied time of post. eg: 2 minutes ago.
        :type minutes: int
        :param interval: Refresh interval(seconds).
        :param times: Int. The numbers of satisfied posts, if achieve this, the funtion will stop.
        :type times: int
        """
        logging.info('开始轮询url:%s' % self.url)
        flag = 0
        while flag < times:
            comment_url = self.parse_post_in_time(minutes)
            if comment_url:
                post_comment_url, data = self.parse_comment(comment_url)
                self.post_comment(post_comment_url, data=data, message=config.COMMENT)
                flag += 1
                time.sleep(minutes * 60)
                continue
            elif comment_url is False:
                logging.info('尝试重新登录...')
                self.refresh_session()
            logging.info('%s: 未发布新内容' % str(datetime.now()))
            time.sleep(interval)

#
# if __name__ == '__main__':
#     user = WeiboUser(url=config.URL)
#     user.run_comment()
