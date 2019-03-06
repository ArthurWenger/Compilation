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
        self.L()
        if self.lookahead != DONE:
            error_msg = "line " + str(self.scanner.lineno) + ", DONE expected"
            raise SyntaxError( error_msg)
        else:
            print( "OK")

    def L(self):
        "L -> E;L | eps"
        Eval=self.E()
        if self.lookahead in [';']:
            self.match(self.lookahead)
            print(Eval)
            self.L()
        else:
            pass
            
    def E(self):
        "E -> T+E|T"
        Tval=self.T()
        if self.lookahead in ['+']:
            self.match(self.lookahead)
            E1val=self.E()
            Eval=E1val+Tval
        else:
            Eval=Tval
        return Eval

    def T(self):
        "T -> F*T | F"
        Fval=self.F()
        if self.lookahead in ['*']:
            self.match(self.lookahead)
            T1val=self.T()
            Tval=T1val*Fval
        else:
            Tval=Fval
        return Tval

    def F(self):
        "F -> (E) | num"
        if self.lookahead == '(':
            self.match('(')
            Eval=self.E()
            self.match(')')
            Tval=Eval
        elif self.lookahead in [NUM]:
            Fval=int(self.lookahead)
            self.match(self.lookahead)
        else:
            error_msg = "line " + str(self.scanner.lineno) + ", '(', NUM expected"
            raise SyntaxError( error_msg)
        return Fval


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

