%% Erlang sample — module, functions, atoms, variables (uppercase), macros, records, comments.
%% Targets the erlang lexer.

-module(sample).
-export([start/0, add/2, factorial/1]).

%% Macros
-define(PI, 3.14159).
-define(MAX_RETRY, 5).

%% Records
-record(person, {name, age}).

%% Comments: single-line above.

%% Atoms (lowercase names)
ok_atom = ok.
error_atom = error.

%% Variables are UPPERCASE (or start with _)
Add = fun(A, B) -> A + B end.
Result = add(2, 3).

%% Functions with pattern matching
start() ->
    io:format("Hello Erlang~n"),
    Person = #person{name = "Ada", age = 30},
    io:format("Name: ~s~n", [Person#person.name]).

add(A, B) ->
    A + B.

factorial(0) ->
    1;
factorial(N) when N > 0 ->
    N * factorial(N - 1).

%% Edge cases: empty list, tuple, binary, anonymous function, case
edge_cases() ->
    Empty = [],
    Tuple = {foo, bar, baz},
    Bin = <<"binary">>,
    Anon = fun(X) -> X * 2 end,
    Case = case 1 of
        1 -> one;
        2 -> two;
        _ -> other
    end,
    {Empty, Tuple, Bin, Anon, Case}.
