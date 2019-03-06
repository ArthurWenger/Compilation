#!/usr/bin/python
# -*- coding: utf-8 -*-
from sys import argv, stderr

from misc import *
from symbtab import *
from scanner import *


class Parser(object):

    '''Analyse syntaxique.'''

    def __init__(self, scanner, symbtab):
        self.scanner = scanner
        self.symbtab = symbtab

    def match(self, token):
        if self.lookahead == token:
            (self.lookahead, self.attribut) = self.scanner.nexttoken()
        else:
            raise SyntaxError( str(token) + ' attendu, lookahead lu: ' + self.lookahead)

    def parse(self):
        (self.lookahead, self.attribut) = self.scanner.nexttoken()
        self.S()
        if self.lookahead != DONE:
            raise SyntaxError
        else:
            print('OK')

    def S(self):
        '''S -> (S+F) | F'''

        if self.lookahead == '(':
            self.match('(')
            self.S()
            self.match('+')
            self.F()
            self.match(')')
        else:
            self.F()

    def F(self):
        '''F -> num | id'''

        if self.lookahead in [NUM, ID]:
            self.match(self.lookahead)
        else:
            raise SyntaxError('num ou id attendu !')


## Programme principal :

if __name__ == '__main__':
    if len(argv) != 2:
        stderr.write('usage: parser-simple <file>\n')
    else:
        f = open(argv[1],  'br+')
        symbtab = Symbtab()
        scanner = Scanner(symbtab, f)
        parser = Parser(scanner, symbtab)
        try:
            parser.parse()
        finally:
            f.close()
