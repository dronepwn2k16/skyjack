import argparse

class ArgumentParserError(Exception): pass

# simple subclass of argument parser that does not exit on error
class SkyjackArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)
