"""This module is used to display a hello message."""

import os


def main():
    print 'hello, {}!'.format(os.environ['COMPUTERNAME'])


if __name__ == '__main__':
    main()
