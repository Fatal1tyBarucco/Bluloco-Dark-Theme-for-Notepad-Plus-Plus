;; Scheme sample — define, lambda, lists, symbols, comments.
;; Targets the scheme lexer.

;; --- Comments ---
;; Single-line comment.
#| Multi-line comment block. |#

;; --- Imports / definitions ---
(define pi 3.14159)
(define name "Ada")

;; --- Lambda and functions ---
(define add (lambda (a b) (+ a b)))

(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

;; --- Lists and symbols ---
(define numbers '(1 2 3 4 5))
(define symbols '(a b c))
(define mixed '(1 "two" 3.0 #t))

;; --- Higher-order functions ---
(define doubled (map (lambda (x) (* x 2)) numbers))
(define filtered (filter (lambda (x) (> x 2)) numbers))

;; --- Edge cases: quoted lists, empty list, boolean, nested forms ---
(define empty '())
(define truthy #t)
(define falsy #f)
(define nested ((lambda (f) (f 10)) add))

;; --- Display results ---
(display (add 10 20))
(newline)
(display (factorial 5))
(newline)
(display doubled)
(newline)
(display filtered)
(newline)
