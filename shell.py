# -*- coding: utf-8 -*-

import os
import subprocess


MYPATH = os.path.join(os.getcwd(), 'test')


class CMD(object):
    def __init__(self, handler):
        self.handler = handler

    def get_input(self):
        return raw_input(os.getcwd() + '>').strip()

    def run(self):
        self.handler.pre_run_operations()
        while True:
            input = self.get_input()
            if not input:
                continue
            components = input.split()
            cmd, args = components[0], ' '.join(components[1:])
            method_name = 'do_' + cmd
            if hasattr(self.handler, method_name):
                method = getattr(self.handler, method_name)
                output = method(args)
                print output
            else:
                try:
                    exit_code = subprocess.check_call([cmd, args], shell=True)
                except:
                    pass


class CmdHandler(object):

    def pre_run_operations(self):
        os.environ['PATH'] += MYPATH + ';'

    def do_set(self, args):
        args = args.strip()
        separator = '='
        sep_index = args.find(separator)
        argsv = filter(None, (args[:sep_index], args[sep_index + 1:]))
        if separator in args:
            if len(argsv) == 2:
                os.environ[argsv[0]] = argsv[1]
                return ''
            del os.environ[argsv[0]]
            return ''
        if not args:
            return '\n'.join([separator.join([key, val]) for key, val in os.environ.iteritems()])
        return '{}={}'.format(args, os.environ[args])

    def do_exit(self, *args):
        print 'Goodbye!'
        exit()

    def do_cd(self, newdir):
        if newdir:
            os.chdir(newdir)
            return ''
        return os.getcwd()


def main():
    handler = CmdHandler()
    cmd = CMD(handler)
    cmd.run()


if __name__ == '__main__':
    main()