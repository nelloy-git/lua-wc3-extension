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
    require_data = {
        loaded = {},
        module = {},
        return = {},
    }
    
    function require(name)
        if not require_data.loaded[name] then
            require_data.return[name] = require_data.module[name]()
            require_data.loaded[name] = true
        end
        return require_data.return[name]
    end
    '''


LUA_REQUIRE_FUNC = \
    '''
    require_data.module['name'] = function()
    end
    '''