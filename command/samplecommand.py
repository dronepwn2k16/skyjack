from lib.parser import SkyjackArgumentParser
#
# This class is an example that demonstrates how to implement a command 
# for the Skyjack Shell. 
#
# The name of the class does not matter and it does not have to inherit 
# from a specific class. Just make sure to register it in skyjack.py
# by calling skyjack.register_command with  an instance of your 
# command class.
#
class SampleCommand():

    def __init__(self):
        # this is the name by which the command will be invoked
        self.cmd = "test" 
        
        # this ArgumentParser will automatically be invoked when your command is executed
        # see https://docs.python.org/3/library/argparse.html for documentation
        # please make sure to always include the help parameter
        # you do not have to add -h/--help, this gets gernated automatically
        # make sure to set prog to self.cmd, otherwise it will print the ARGV[0] as command name
        self.parser = SkyjackArgumentParser(prog=self.cmd, description="example command to demonstrate argument handling")

        # some examples:

        # mandatory argument with arbitrary value (--foo bar)
        self.parser.add_argument('-f', '--foo', help="something additional to print")

        # optional argument which takes only integer
        self.parser.add_argument('--favorite-number', help="your favorite number", type=int, default=42)

        # additional true/false switch
        self.parser.add_argument("-v", "--verbose", help="increase verbosity", action="store_true")

        # positional argument
        self.parser.add_argument("mytext", help="the text you want to print")
        


    # the execute method will be called when the command is invoked
    # args contains the results of your ArgumentParser.
    # the method will ONLY be executed if argument parsing was 
    # successful, so you do not have to care about that
    def execute(self, args):
        # the string below this line will be shown when the 'help' command is executed
        # it should be a short description of what it does
        'sample command that prints some information'

        # command logic goes here:
        print("you entered: %s" % args.mytext)
        if args.foo:
            print("you also wanted to print: %s" % args.foo)
        print("your favorite number is %d" % args.favorite_number) # note that - becomes _ in the argument name
        if args.verbose:
            print("you also wanted to print verbose")

# Sample Output:

# $ test something -f "something else" -v --favorite-number 1337
# you entered: something
# you also wanted to print: something else
# your favorite number is 1337
# you also wanted to print verbose
# $ test something
# you entered: something
# your favorite number is 42

