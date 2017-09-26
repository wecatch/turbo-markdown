# -*- coding: utf-8 -*-

import socket
import platform
import os

import os.path
import click
from turbo_markdown import run_server


def port_is_used(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(('localhost', port)) == 0:
        return True

    return False


@click.command()
def main(args=None):
    """Console script for turbo_markdown"""
    abspath = os.path.abspath('.')
    port = 8888
    while True:
        if not port_is_used(port):
            break
        port += 1
    url = 'http://localhost:%s' % port
    if platform.system() == 'Darwin':
        os.system('open %s' % url)
    else:
        click.echo("Open your brower visit %s" % url)
    run_server(abspath, port)


if __name__ == "__main__":
    main()
