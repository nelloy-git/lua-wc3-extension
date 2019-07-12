'''
    Lua code lib.
'''


LUA_COMPILETIME = \
'''
is_compiletime = true
__compile_data = {
    count = 0,
    result = {}
}

function compiletime(body, ...)
    if not is_compiletime then
        print('Compiletime function is trying run in runtime')
        return
    end
    
    if type(body) == \'function\' then
        __compile_data.result[compiletime_count + 1] = body(...)
    else
        __compile_data.result[compiletime_count + 1] = body
    end
    compiletime_count = compiletime_count + 1
end
'''


LUA_REQUIRE = \
'''
__require_data = {
    loaded = {},
    module = {},
    result = {}
}

function require(name)
    if __require_data.loaded[name] == false then
        __require_data.result[name] = __require_data.module[name]()
        __require_data.loaded[name] = true
    end
    return __require_data.result[name]
end
'''


LUA_REQUIRE_FUNC = \
    '''
    __require_data.module['name'] = function()
    end
    '''