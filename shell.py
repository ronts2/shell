# -*- coding: utf-8 -*-

import os
import subprocess


class CMD(object):
    def __init__(self, handler):
        self.handler = handler

    def get_input(self):
        return raw_input(os.getcwd() + '>').strip()

    def run(self):
        while True:
            input = self.get_input()
            if not input:
                continue
            components = input.split()
            cmd, args = components[0], ' '.join(components[1:])
            method_name = 'do_' + cmd
            if hasattr(self.handler, method_name):
                method = getattr(self.handler, method_name)
                method(args)
            else:
                try:
                    exit_code = subprocess.check_call([cmd, args])
                except Exception as e:
                    print e


class CmdHandler(object):

    def set(self, ):
        pass

    def do_exit(self, *args):
        print 'Goodbye!'
        exit()

    def do_cd(self, newdir):
        if newdir:
            os.chdir(newdir)
        return os.getcwd()


def main():
    handler = CmdHandler()
    cmd = CMD(handler)
    cmd.run()


if __name__ == '__main__':
    main()