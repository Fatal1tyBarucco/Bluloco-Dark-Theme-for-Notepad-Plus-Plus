-- Sample Lua code to test Bluloco Dark
-- Includes tables, functions and local variables

local theme = {
    name = "Bluloco Dark",
    version = "1.0",
    colors = { "282C34", "ABB2BF" }
}

function describe(t)
    print("Theme: " .. t.name .. " v" .. t.version)
end

-- User keyword test: custom_init
custom_init(theme)

describe(theme)
