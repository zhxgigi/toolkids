def func():
    a = 10
    print a

co = func.func_code
modified_consts = list(co.co_consts)
for idx, val in enumerate(modified_consts):
    if modified_consts[idx] == 10: 
        modified_consts[idx] = 15

modified_consts = tuple(modified_consts)

import types
modified_code = types.CodeType(co.co_argcount, co.co_nlocals, co.co_stacksize, co.co_flags, co.co_code, modified_consts, co.co_names, co.co_varnames, co.co_filename, co.co_name, co.co_firstlineno, co.co_lnotab)
modified_func = types.FunctionType(modified_code, func.func_globals)
# 15:
modified_func()
