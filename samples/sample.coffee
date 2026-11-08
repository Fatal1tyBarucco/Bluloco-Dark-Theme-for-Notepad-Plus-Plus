# CoffeeScript sample — exercises functions, classes, strings, regex, comments, interpolation.
# This file targets the coffeescript lexer.

# --- Comments ---
# Single-line comment.
###
Multi-line comment block.
###

# --- Variables and constants ---
pi = 3.14159
greeting = "Hello, world!"
multiline = """
This is a
multi-line string
with interpolation #{pi}.
"""
name = 'Baruloco'

# --- Functions (named and anonymous) ---
square = (x) -> x * x
add = (a, b) ->
  result = a + b
  return result

# --- Class with constructor and methods ---
class Animal
  constructor: (@name, @species) ->
  speak: ->
    console.log "#{@name} says hello"

class Dog extends Animal
  speak: ->
    console.log "#{@name} barks!"

dog = new Dog("Rex", "Canine")
dog.speak()

# --- Regular expression ---
email_re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

# --- Edge cases: empty string, interpolation with expression, chained calls ---
empty = ""
chained = [1, 2, 3].map (x) -> x * 2. filter (n) -> n > 2

# --- Conditional and loop ---
if dog.speak()
  console.log "It works!"
for item in [1..5] by 2
  console.log item
