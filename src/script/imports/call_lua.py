'''
    Functions for calling lua content.
'''

from luaparser import ast
import os
import lupa

lua = None

def init_lua(path):
    os.chdir(path)
    return lupa.LuaRuntime(unpack_returned_tuples=True)


def init_code(lua, code):
    lua.execute(code)


def load_enviroment(lua, content):
    try:
        lua.execute(content)
    except RuntimeError as err:
        print('RuntimeError: ', err)


def lua_to_ast(val, val_type):
    if val_type == 'nil':
        return ast.Nil()
    if val_type == 'number':
        return ast.Number(val)
    if val_type == 'string':
        return ast.String(val)
    if val_type == 'table':
        fields = []
        for field_name in val:
            field_val = lua_to_ast(val[field_name], lua.globals().type(val[field_name]))
            field = ast.Field(ast.Name(field_name), field_val)
            fields.append(field)
        return ast.Table(fields)

    print('Error: compiletime function can return only nil, number, \
           string or table (with nils, numbers, strings and tables etc.).')
    return False


def get_compiletime_result(lua, pos):
    lg = lua.globals()
    res = lg.compiletime_results[pos]
    res_type = lg.type(lg.compiletime_results[pos])
    return lua_to_ast(res, res_type)


def clear_enviroment(lua):
    lua.execute('for k, v in pairs(_G) do v = nil end')