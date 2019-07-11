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
    result = {}
}

function require(name)
    if require_data.loaded[name] == false then
        require_data.result[name] = require_data.module[name]()
        require_data.loaded[name] = true
    end
    return require_data.result[name]
end
'''


LUA_REQUIRE_FUNC = \
    '''
    require_data.module['name'] = function()
    end
    '''