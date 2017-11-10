"""This module is used to display the hexadecimal representation of a file's data."""

import sys
import os
import binascii


def load_file(src_file, size=64):
    """Loads a file's data.

    Parameters
    ----------
    src_file: open file object
        the file to load.
    size: int
        the maximum amount of bytes to read from the file at once.

    Yields
    ------
    str
        the loaded file's data

    """
    while True:
        data = src_file.read(size)
        if not data:
            raise StopIteration
        yield data


def main(args):
    """The main function.

    Parameters
    ----------
    args: Union(str)
        arguments passed to the script.

    """
    path = args[0]
    if not os.path.isfile(path):
        sys.stdout.write('{} is not a file.'.format(path))
    else:
        with open(path, 'rb') as src_file:
            sys.stdout.write('\n'.join([binascii.hexlify(data) for data in load_file(src_file)]))


if __name__ == '__main__':
    main(sys.argv[1:])
    exit(0)
