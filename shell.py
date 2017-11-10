"""This module is used to run a cmd-like shell.

Attributes
----------
MYPATH: str
    custom path to the folder which is added to the %PATH% environmental variable each run.

"""

import os
import subprocess


MYPATH = os.path.join(os.getcwd(), 'test')


class CMD(object):
    """This class offers the basic functionality of a shell.
    It is used for parsing input and running commands.
    """
    def __init__(self, handler):
        """The class constructor

        Parameters
        ----------
        handler: CmdHandler
            used to handle and execute the commands.
            the handler must have a pre_run_operations method, which will be called before running the shell.
            to handle a command, there has to be a method named 'do_command-name'.

        """
        self.handler = handler

    def get_input(self):
        """Gets input from the user.

        Returns
        -------
        str
            stripped input.

        """
        return raw_input(os.getcwd() + '>').strip()

    def parse_input(self, input):
        """Parses the input into command components.

        Parameters
        ----------
        input: str
            the string to parse.

        Returns
        -------
        tuple(str, str)
            the command name and the arguments.

        """
        components = input.split()
        return components[0], ' '.join(components[1:])

    def run_command(self, input):
        """Executes the wanted command.

        Parameters
        ----------
        input: str
            the input from the user.

        Returns
        -------
        str
            the output returned from the command's execution.

        """
        cmd, args = self.parse_input(input)
        method_name = 'do_' + cmd
        if hasattr(self.handler, method_name):
            method = getattr(self.handler, method_name)
            return method(args)
        else:
            try:
                return subprocess.check_output([cmd, args], shell=True)
            except subprocess.CalledProcessError:
                return ''

    def pipe_cmd(self, cmds, args=''):
        """Pipes multiple commands recursively.

        Parameters
        ----------
        cmds: Union[str]
            series of commands to pipe.
        args: Union[str]
            arguments to pass to the first command in `cmds`.

        Returns
        -------
        str
            the output returned from the commands' execution.

        """
        if len(cmds) == 1:
            return self.run_command(' '.join([cmds[0], args]))
        if not args:
            return self.pipe_cmd(cmds[1:], self.run_command(cmds[0]))
        return self.pipe_cmd(cmds[1:], self.run_command(' '.join([cmds[0], args])))

    def run(self):
        """Starts the shell running loop."""
        self.handler.pre_run_operations()
        while True:
            input = self.get_input()
            if not input:
                continue
            cmds = filter(None, input.split(' | '))
            if len(cmds) == 1:
                print self.run_command(input)
            else:
                print self.pipe_cmd(cmds)


class CmdHandler(object):
    """This class is used to handle and execute custom shell commands."""

    def pre_run_operations(self):
        """Executes operations before the shell runs.
        This method must exist at any time, as it is run by `CMD` before running.
        Use `pass` if no operations are needed, but do not remove this method.
        """
        os.environ['PATH'] += MYPATH + ';'

    def do_set(self, args):
        """Handles a 'set' command.
        Changes, Adds or removes a value of an environmental variable.

        Parameters
        ----------
        args: str
            the arguments sent to the command.

        Returns
        -------
        str
            if `args` is None, the names and values of all environmental variables.
            if `args` is (or part of) a name, the names and values of all environmental variables
            which names' start with `args`.

        """
        args = args.strip()
        separator = '='
        sep_index = args.find(separator)
        argsv = args
        if sep_index > 0:
            argsv = filter(None, (args[:sep_index], args[sep_index + 1:]))
        if separator in args:
            if len(argsv) == 2:
                os.environ[argsv[0]] = argsv[1]
                return ''
            del os.environ[argsv[0]]
            return ''
        if not args:
            return '\n'.join([separator.join([key, val]) for key, val in os.environ.iteritems()])
        return '\n'.join(['{}={}'.format(key, val) for key, val in os.environ.iteritems() if key.startswith(argsv)])

    def do_exit(self, *args):
        """Handles the 'exit' command.
        Ends the program.
        """
        print 'Goodbye!'
        exit()

    def do_cd(self, newdir):
        """Handles the 'cd' command.
        Changes the current working directory to `newdir`.

        Parameters
        ----------
        newdir: str
            path of the new working directory.

        Returns
        -------
        str
            if `newdir` is an empty string, the path of the current working directory, otherwise an empty string.

        """
        if not os.path.isdir(newdir):
            return newdir + ' is not a valid directory.'
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
