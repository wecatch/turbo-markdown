#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def get_tree(docs_path):
    doc_dict = {}
    # current relative path start from root path
    scan_file(docs_path, doc_dict, parent_relative_path='/')
    return doc_dict


def generate_html_tree(docs_path, doc_dict):
    html_tree = generate_html(docs_path, doc_dict)
    return html_tree


def generate_html(parent_path, doc_dict):
    html = '<ul class="nav-list" >'

    parent = doc_dict[parent_path]
    parent_content = parent['content']
    parent_relative_path = parent['relative_path']

    for current in parent_content:
        current_path = os.path.join(parent_path, current)
        current_content = doc_dict[current_path]['content']
        if isinstance(current_content, list):
            html += '<li class="has-sub" ><a class="js-has-sub"  href="javascript:void(0)" >%s</a>%s</li>' % (
                current, generate_html(current_path, doc_dict))
        else:
            if current.endswith('.md'):
                real_path = os.path.realpath(os.path.join(parent_relative_path, current))
                html += '''<li><a href="%s" >%s</a></li>''' % (real_path, current)

    html += '</ul>'

    return html


def scan_file(parent_path, doc_dict, parent_relative_path):
    all_docs = os.listdir(parent_path)
    doc_dict[parent_path] = {
        'content': all_docs,
        'relative_path': parent_relative_path,
    }
    for current in all_docs:
        current_path = os.path.join(parent_path, current)
        if os.path.isdir(current_path) and not os.path.basename(current_path).startswith('.'):
            scan_file(current_path, doc_dict, os.path.join(parent_relative_path, current))
        else:
            doc_dict[current_path] = {
                'content': current,
                'relative_path': parent_relative_path,
            }


def sort_path(c1, c2):
    """
    目录层级排序，
    如果目录层级一样，文件名或目录名排序
    """
    result = cmp(c1.count('/'), c2.count('/'))
    if result == 0:
        return cmp(c1, c2)
    else:
        return result


def print_fold_tree(doc_dict=None):
    if doc_dict:
        keys = doc_dict.keys()
        keys.sort(sort_path)
        for k in keys:
            if isinstance(doc_dict[k], list):
                print 'folder', '-->', k, '-->', doc_dict[k]
            else:
                print 'file', '-->', k, '-->', doc_dict[k]


if __name__ == '__main__':
    doc_dict = get_tree()
    print generate_html_tree(doc_dict)
