'''
    Lua code lib.
'''

LUA_COMPILETIME = \
    '''
    is_compiletime = 1
    compiletime_count = 0
    compiletime_results = {}

    function compiletime(body)
        if type(body) == \'function\' then
            compiletime_results[compiletime_count + 1] = body()
        else
            compiletime_results[compiletime_count + 1] = body
        end
        compiletime_count = compiletime_count + 1
    end
    '''


LUA_REQUIRE = \
    '''
    function require(module)
        module = module:gsub(\'%.\', \'_\')
        local func = _G[module..\'_return\']
        if func == nil then
            return nil
        end
        return func()
    end
    '''