# Nim sample — procs, types, decorators, strings raw/triple, comments, operators.
# Targets the nim lexer.

# --- Comments ---
# Single-line comment.
#[ Multi-line comment block. ]#

# --- Imports ---
import strutils, sequtils

# --- Types and constants ---
const
  Pi = 3.14159
  MaxRetry = 5

type
  Person = object
    name: string
    age: int

  Shape = ref object
    name: string

# --- Decorators / templates ---
template withLog(body: untyped): untyped =
  echo "Entering"
  body
  echo "Leaving"

# --- Procs ---
proc add(a: int, b: int): int =
  return a + b

proc factorial(n: int): int =
  if n == 0: return 1
  return n * factorial(n - 1)

proc draw(s: Shape) =
  echo "Drawing ", s.name

# --- Variables ---
var p = Person(name: "Ada", age: 30)
var s = Shape(name: "Circle")

# --- Strings ---
let normal = "Hello, world!"
let raw = r"raw \n string"
let triple = """This is a
triple-quoted string
with interpolation: $#{}."""

# --- Edge cases: operators, seq, option, callbacks ---
let nums = @[1, 2, 3, 4, 5]
let doubled = nums.map(it => it * 2)
let filtered = nums.filter(it => it > 2)

withLog:
  echo add(10, 20)
  draw(s)
  echo factorial(5)

# Operators
let sum = 1 + 2 - 3 * 4 / 5
let cmp = 10 == 10 and 5 != 3
