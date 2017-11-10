# -*- coding: utf-8 -*-
import os


def main():
    print 'hello, {}!'.format(os.environ['COMPUTERNAME'])


if __name__ == '__main__':
    main()
