'''
This work is licensed under the
Creative Commons Attribution-Share Alike 3.0 License.
To view a copy of this license,
visit http://creativecommons.org/licenses/by-sa/3.0

Written by Abd Allah Diab (mpcabd)
Email: mpcabd ^at^ gmail ^dot^ com
Website: http://magicpc.wordpress.com
'''
import ply.lex as lex


t_GoLeft = r'\<'
t_GoRight = r'\>'
t_Print = r'\.'
t_Read = r','
t_Increase = r'\+'
t_Decrease = r'\-'
t_WhileStart = r'\['
t_WhileEnd = r'\]'


def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__":
    lex.runmain()
