# -*- coding: utf-8 -*-

import os
from functools import partial
import subprocess


INPUT = partial(raw_input, os.getcwd() + '>')


class CMD(object):
    def __init__(self, handler):
        self.handler = handler

    def run(self):
        while True:
            input = INPUT()
            if not input:
                continue
            components = input.split()
            cmd, args = components[0], ' '.join(components[1:])
            if hasattr(self.handler, cmd):
                method = getattr(self.handler, cmd)
                method(cmd, args)
            else:
                try:
                    output = subprocess.check_call([cmd, args])
                except Exception as e:
                    output = str(e)
                print output


class CmdHandler(object):
    def __init__(self):
        pass

    def cd(self, newdir):
        os.chdir(newdir)

    def where(self, cmd):
        paths = os.environ['Path']
        for path in paths:



def main():
    handler = CmdHandler()
    cmd = CMD(handler)
    cmd.run()


if __name__ == '__main__':
    main()