from lib.parser import SkyjackArgumentParser


class TemplateCommand():

    def __init__(self):
        self.cmd = "" 
        
        self.parser = SkyjackArgumentParser(prog=self.cmd, description="")

    def execute(self, args):
        ""
