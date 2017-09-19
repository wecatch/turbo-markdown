# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import os
import codecs

from pygments.lexers import get_lexer_for_filename
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.styles import get_style_by_name
import markdown
from turbo import app, register
from turbo.conf import app_config
import tornado.template

from util import get_tree, generate_html_tree
from temp import template_html

app_config.app_name = 'turbo-markdown'
app_config.web_application_setting = {
    'xsrf_cookies': False,
    'cookie_secret': 'abcdefg',
    'static_path': os.path.join('.', "static"),
}

DOC_DICT = None
HTML_TREE = None


class DocsInfo(object):

    docs_path = '/Users/zhyq0826/workspace/zhyq0826/note'

    def __init__(self, docs_path=None):
        if docs_path:
            self.docs_path = '/home/dev/worlspace/tornado/tornado'


def parse_markdown(path):
    current_file = os.path.join(DocsInfo.docs_path, path)
    if path.endswith('.md') or path.endswith('.markdown'):
        with codecs.open(current_file, mode='r', encoding='utf-8') as f:
            html = markdown.markdown(f.read())

        return html
    else:
        basename = os.path.basename(current_file)
        with codecs.open(current_file, mode='r', encoding='utf-8') as f:
            return highlight(
                f.read(),
                get_lexer_for_filename(basename),
                HtmlFormatter(style=get_style_by_name('colorful')))


class HomeHandler(app.BaseHandler):

    def get(self, *path):
        self.template_path = ''
        global DOC_DICT
        global HTML_TREE
        html = ''
        if path and path[0]:
            html = parse_markdown(path[0])

        if 'X-Requested-With' in self.request.headers:
            return self.write(html)

        if not DOC_DICT:
            DOC_DICT = get_tree(DocsInfo.docs_path)

        if not HTML_TREE:
            HTML_TREE = generate_html_tree(DocsInfo.docs_path, DOC_DICT)
        t = tornado.template.Template(template_html)
        self.write(t.generate(html_tree=HTML_TREE, html=html))


def run_server():
    register.register_url('/', HomeHandler)
    register.register_url('', HomeHandler)
    app.start(8888)


if __name__ == '__main__':
    run_server()
