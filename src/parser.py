from sys import argv, stderr

from misc import *
from symbtab import *
from scanner import *

class Parser(object):
    "Analyse syntaxique."

    def __init__(self, scanner, symbtab):
        self.scanner = scanner
        self.symbtab = symbtab

    def match(self, token):
        if self.lookahead == token:
            (self.lookahead, self.tokenat) = self.scanner.nexttoken()
        else:
            error_msg = "line " + str(self.scanner.lineno) + ", " + str(token) + " expected" + " lexeme lu: " + self.lookahead
            raise SyntaxError( error_msg)

    def parse(self):
        (self.lookahead, self.tokenat) = self.scanner.nexttoken()
        self.E()
        if self.lookahead != DONE:
            error_msg = "line " + str(self.scanner.lineno) + ", DONE expected"
            raise SyntaxError( error_msg)
        else:
            print( "OK")

    def E(self):
        "E -> T+E | T-E | T"
        self.T()
        if self.lookahead in ['+','-']:
            self.match(self.lookahead)
            self.E()

    def T(self):
        "T -> F*T | F/T | F"
        self.F()
        if self.lookahead in ['*','/']:
            self.match(self.lookahead)
            self.T()

    def F(self):
        "F -> (E) | num | id"
        if self.lookahead == '(':
            self.match('(')
            self.E()
            self.match(')')
        elif self.lookahead in [NUM,ID]:
            self.match(self.lookahead)
        else:
            error_msg = "line " + str(self.scanner.lineno) + ", '(', NUM or ID expected"
            raise SyntaxError( error_msg)


## Programme principal :
if __name__ == "__main__":
    if len(argv) != 2:
        stderr.write("usage: parser <file>\n")
    else:
        with open(argv[1], 'br+') as f:
            symbtab = Symbtab()
            scanner = Scanner(symbtab, f)
            parser  = Parser(scanner, symbtab)
            parser.parse()

