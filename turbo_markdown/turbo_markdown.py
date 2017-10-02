# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import os
import codecs

from pygments.lexers import get_lexer_for_filename
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.styles import get_style_by_name
import mistune
from turbo import app, register
from turbo.conf import app_config
import tornado.template

from turbo_markdown.util import get_tree, generate_html_tree
from turbo_markdown.template import template_html

app_config.app_name = 'turbo-markdown'
app_config.web_application_setting = {
    'xsrf_cookies': False,
    'cookie_secret': 'abcdefg',
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
}

DOC_DICT = None
DOCS_PATH = ''
HTML_TREE = None


def parse_markdown(path):
    current_file = os.path.join(DOCS_PATH, path)
    if path.endswith('.md') or path.endswith('.markdown'):
        with codecs.open(current_file, mode='r', encoding='utf-8') as f:
            html = mistune.markdown(f.read())

        return html
    else:
        return ''
        # basename = os.path.basename(current_file)
        # with codecs.open(current_file, mode='r', encoding='utf-8') as f:
        #     return highlight(
        #         f.read(),
        #         get_lexer_for_filename(basename),
        #         HtmlFormatter(style=get_style_by_name('colorful')))


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
            DOC_DICT = get_tree(DOCS_PATH)

        if not HTML_TREE:
            HTML_TREE = generate_html_tree(DOCS_PATH, DOC_DICT)
        t = tornado.template.Template(template_html)
        self.write(t.generate(
            html_tree=HTML_TREE, html=html, title=os.path.basename(DOCS_PATH)))


def run_server(docs_path='', port=None):
    if not docs_path:
        print('No Path Found')
        return
    global DOCS_PATH
    DOCS_PATH = docs_path
    register.register_url('/', HomeHandler)
    register.register_url('/(.*)', HomeHandler)
    app.start(port)


if __name__ == '__main__':
    run_server()
