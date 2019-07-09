'''

'''
import os

import pathlib
from luaparser import ast

from . import lua_code
from . import ast_to_string as ats
from . import call_lua as cl


def read_content(main_path, src_dir, file_list, content_list):
    '''
        Function reads content of all required modules.
          main_path    - relative path inside source directory
          src_dir      - path of source directory
          file_list    - list to add requireed files
          content_list - list to add file content (ast tree)

        Returns files list, contents list including the module.
    '''

    # Read file.
    full_src_path = os.path.join(src_dir, main_path)
    with open(full_src_path, 'r') as file:
        module = file.read()
    tree = ast.parse(module)

    file_list.append(main_path)
    content_list.append(tree)
    # Searching depencies.
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and ats.node_to_str(node.func) == 'require':
            if len(node.args) != 1 or not isinstance(node.args[0], ast.String):
                print('Error: require function can have only one constant string argument.')
                raise SystemExit

            # Prepare depency.
            path = ats.name_to_module_path(node.args[0].s)
            if path in file_list:
                continue
            read_content(path, src_dir, file_list, content_list)


def get_contents(main_path, src_dir):
    file_list = []
    content_list = []
    read_content(main_path, src_dir, file_list, content_list)
    file_list.reverse()
    content_list.reverse()
    return file_list, content_list


def fix_content_return(file_path, content):
    module_name = ats.path_to_module_name(file_path)
    for pos, node in enumerate(content.body.body):
        if isinstance(node, ast.Return):
            func = ast.Function(ast.Name(str(module_name) + '_return'), [], ast.Block([node]))
            content.body.body.pop(pos)
            #content.body.body[pos] = func
            content.body.body.append(func)


def compiletime_execution(module_tree):
    # Run module to get compiletime results list.
    cl.clear_enviroment()
    cl.init_code(lua_code.LUA_COMPILETIME)
    cl.load_enviroment(ats.node_to_str(module_tree))

    # Get compiletime results.
    cur = 0
    for node in ast.walk(module_tree):
        if not isinstance(node, (ast.Assign, ast.LocalAssign)):
            continue

        new_vals = []
        for val in node.values:
            if isinstance(val, ast.Call) and ats.node_to_str(val.func, 0) == 'compiletime':
                cur += 1
                if len(val.args) > 1:
                    s_args = ''
                    for arg in node.args:
                        s_args += ats.node_to_str(arg) + ', '
                    s_args = s_args[:-2]
                    print('Error in compiletime(' + s_args + ').')
                    print('Require function needs only one argument.')
                    return
                val = cl.get_compiletime_result(cur)
                #print(ats.node_to_str(val))
            new_vals.append(val)
        node.values = new_vals


def link_content(content_list):
    require_tree = ast.parse(lua_code.LUA_REQUIRE)
    content_list.insert(0, require_tree)
    block = ast.Block(content_list)
    return block

