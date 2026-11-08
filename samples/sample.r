# R sample — functions, vectors, infix operators, strings, backticks, comments.
# Targets the R lexer.

# --- Comments ---
# Single-line comment.

# --- Variables and vectors ---
pi <- 3.14159
name <- "Ada"
numbers <- c(1, 2, 3, 4, 5)
chars <- c("a", "b", "c")

# --- Functions ---
add <- function(a, b) {
  return(a + b)
}

factorial <- function(n) {
  if (n == 0) return(1)
  return(n * factorial(n - 1))
}

# --- Infix operators and pipes ---
result <- add(10, 20)
squared <- numbers ^ 2
filtered <- numbers[numbers > 2]

# --- Strings and backticks ---
normal <- "Hello, world!"
raw <- 'raw string'
`backtick var` <- 42

# --- Data frame and list ---
df <- data.frame(x = 1:3, y = c("a", "b", "c"))
lst <- list(name = "Ada", age = 30, active = TRUE)

# --- Edge cases: NULL, NA, Inf, NaN, comments with # inside strings ---
empty <- NULL
missing <- NA
infinite <- Inf
not_a_number <- NaN

# Function call with named args
add(a = 5, b = 7)

# Print results
print(result)
print(squared)
print(filtered)
