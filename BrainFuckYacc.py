'''
This work is licensed under the
Creative Commons Attribution-Share Alike 3.0 License.
To view a copy of this license,
visit http://creativecommons.org/licenses/by-sa/3.0

Written by Abd Allah Diab (mpcabd)
Email: mpcabd ^at^ gmail ^dot^ com
Website: http://magicpc.wordpress.com
'''

from __future__ import print_function
import ply.yacc as yacc

tokens = [
    'GoLeft',
    'GoRight',
    'Print',
    'Read',
    'Increase',
    'Decrease',
    'WhileStart',
    'WhileEnd'
]


class sparseMatrix(object):
    def __init__(self):
        self.dict = {}

    def __getitem__(self, index):
        if self.dict.get(index):
            return self.dict[index]
        else:
            return 0

    def __setitem__(self, index, value):
        self.dict[index] = value

MAX_INDEX = 30000


def executeStatements(tuplesList):
    global matrix
    global index
    global MAX_INDEX

    for node in tuplesList:
        if node[0] == 'GoLeft':
            if index > 0:
                index -= 1
            else:
                raise Exception("Index out of array bounds!")
        elif node[0] == 'GoRight':
            if index < MAX_INDEX:
                index += 1
            else:
                raise Exception("Index out of array bounds!")
        elif node[0] == 'Print':
            print(chr(matrix[index]), sep='', end='')
        elif node[0] == 'Read':
            matrix[index] = ord(input()[0])
        elif node[0] == 'Increase':
            matrix[index] += 1
        elif node[0] == 'Decrease':
            matrix[index] -= 1
        elif node[0] == 'While':
            while matrix[index] != 0:
                executeStatements(node[1])


def p_start(p):
    """
    start : code
            | empty
    """
    if p[1]:
        executeStatements(p[1])


def p_empty(p):
    'empty : '
    pass


def p_code(p):
    """
    code : code statement
            | code whilestatement
            | statement
            | whilestatement
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1][:]
        p[0].extend([p[2]])


def p_statement(p):
    """
    statement : GoLeft
                   | GoRight
                   | Print
                   | Read
                   | Increase
                   | Decrease
    """
    if p[1] == '<':
        p[0] = ('GoLeft', None)
    elif p[1] == '>':
        p[0] = ('GoRight', None)
    elif p[1] == '.':
        p[0] = ('Print', None)
    elif p[1] == ',':
        p[0] = ('Read', None)
    elif p[1] == '+':
        p[0] = ('Increase', None)
    elif p[1] == '-':
        p[0] = ('Decrease', None)


def p_whilestatement(p):
    'whilestatement : WhileStart code WhileEnd'
    p[0] = ('While', p[2])

index = 0
matrix = sparseMatrix()
parser = yacc.yacc()
while True:
    try:
        s = input('BrainFuck> ')
    except EOFError:
        break
    if not s:
        continue
    parser.parse(s)
    print()
