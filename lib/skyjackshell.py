import cmd, shlex
from tabulate import tabulate
from lib.parser import ArgumentParserError
from termcolor import colored

class SkyjackShell(cmd.Cmd):
    intro = "\n--------------------------------------------------\nSkyjack ready. Type help or ? to list commands.\n"
    prompt = colored("skyjack> ", "red")

    _cmds = {}

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            return

    # prints list of commands + documentation
    def do_help(self, arg):
        'List available commands with "help"'
        names = self.get_names()
        docs = []
        # There can be duplicates if routines overridden
        prevname = ''

        # get docs for built in commands
        for name in names:
            if name[:3] == 'do_':
                if name == prevname:
                    continue
                prevname = name
                cmd=name[3:]
                doc = getattr(self, name).__doc__

                if doc:
                    docs.append([cmd, doc])

        # get docs for external commands
        for cmd in self._cmds.values():
            doc = getattr(cmd, "execute").__doc__
            docs.append([cmd.cmd, doc])

        # sort docs by command name
        docs.sort(key=lambda x: x[0])

        print(tabulate(docs, headers=['command', 'info']))

    def completenames(self, text, *ignored):
        arr = cmd.Cmd.completenames(self, text, None)
        arr.remove('EOF')
        return arr + [k for k in self._cmds.keys() if k.lower().startswith(text)]

    # registers a new command, see documentation for requirements regarding "command"
    def register_command(self, command):
        self._cmds[command.cmd] = command

    # this method is called if cmd does not recognize the command
    # we use this to do our own dispatching
    def default(self, arg):

        args = shlex.split(arg)
        command = self._cmds.get(args[0], None)
        if command:
            name = args.pop(0)
            parser = command.parser
            # if the command supplies a parser, use it
            if parser:
                try:
                    args = parser.parse_args(args)
                except SystemExit: # argparse tries to exit the program on -h and --help, we don't want that
                    return
                except ArgumentParserError as e:
                    print("%s: error: %s " % (name, e))
                    return

            command.execute(args)
        else:
            print("unknown command '%s'" % args[0])

    # this handles CTRL+D
    def do_EOF(self, args):
        print()
        return self.do_exit(args)

    def do_exit(self, args):
        'quits the program'
        print("stopping skyjack...")
        
        # do cleanup here
        
        return True
