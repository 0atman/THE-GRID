```python

>>> from lis import eval_string

>>> eval_string('(list "one" "two")')
'(one two)'

>>> eval_string('(list 0 1 2 3 0 0)')
'(0 1 2 3 0 0)'

>>> eval_string('"string"')
"string"

>>> eval_string('"a string with spaces"')
"a string with spaces"

```