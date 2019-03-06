from string import ascii_letters, digits

from misc import *

class LexicalError(SyntaxError): "Sert a indiquer une erreur lexicale"

class CompilerError(SyntaxError): "Sert a indiquer une erreur du compilateur"

## Analyse lexicale:
class Scanner(object):
    "Effectue l'analyse lexicale."

    def __init__(self, symbtab, f):
        self.symbtab = symbtab
        self.f = f  # fichier ou se trouve le code source
        self.lineno = 1

    def fail(self):
        "Branchement sur l'etat initial du prochain automate."
        if self.start == 0:
            self.start = 3
        elif self.start == 3:
            self.start = 6
        elif self.start == 6:
            self.start = 11
        elif self.start == 11:
            raise LexicalError( "line " + str(self.lineno))
        else:
            raise CompilerError( "line " + str(self.lineno))
        return self.start

    def nexttoken(self):
        "Simule les mouvements d'un automate."
        self.start = 0
        state = 0
        lexbuf = ""
        while 1:
            ## espaces:
            if state == 0:
                c = self.f.read(1).decode('utf-8')         # lecture d'un caractere dans f
                if c == '': return (DONE,None) # on est arrive a la fin de f
                elif c in ' \t': pass
                elif c in '\n': self.lineno = self.lineno + 1
                else: state = self.fail()
            ## id:
            elif state == 3:
                if c in ascii_letters:
                    lexbuf = lexbuf + c
                    state = 4
                else: state = self.fail()
            elif state == 4:
                c = self.f.read(1)
                if c in ascii_letters or c in digits:
                    lexbuf = lexbuf + c
                else: state = 5
            elif state == 5:
                self.f.seek(-1,1)  # recule la tete de lecture (remplacer 0 en -1)
                p = self.symbtab.insert(lexbuf, ID)
                return (self.symbtab.gettoken(p),p)
            ## num:
            elif state == 6:
                if c in digits:
                    lexbuf = lexbuf + c
                    state = 7
                else: state = self.fail()
            elif state == 7:
                c = self.f.read(1).decode('utf-8')
                if c in digits: lexbuf = lexbuf + c
                elif c == '.': state = 8
                else: state = 10
            elif state == 8:
                c = self.f.read(1).decode('utf-8')
                if c in digits:
                    lexbuf = lexbuf + '.' + c
                    state = 9
                else:
                    raise LexicalError( "line " + str(self.lineno))
            elif state == 9:
                c = self.f.read(1).decode('utf-8')
                if c in digits: lexbuf = lexbuf + c
                else: state = 10
            elif state == 10:
                self.f.seek(-1,1)
                return (NUM, lexbuf)
                ## autre:
            elif state == 11:
                if c in ';+-*/()':
                    return (c,None)
                else:
                    state = self.fail()
                    ## erreur:
            else:
                raise CompilerError( "line " + str(self.lineno))
