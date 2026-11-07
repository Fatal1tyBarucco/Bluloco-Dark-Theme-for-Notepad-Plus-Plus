#!/bin/bash
# Sample Bash code to test Bluloco Dark
# Includes functions, loops and expansions

function greet() {
    local name=$1
    echo "Hello, ${name}!"
}

# Array test
fruits=("apple" "banana" "cherry")

for fruit in "${fruits[@]}"; do
    echo "I like ${fruit}"
done

if [[ -f "BlulocoDark.xml" ]]; then
    echo "Theme file exists."
else
    echo "Theme file missing!"
fi

greet "Developer"
