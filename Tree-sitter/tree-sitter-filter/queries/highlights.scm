; Kata kunci
["and" "or" "not" "in" "contains"] @keyword

; Operator perbandingan
["=" "!=" ">" "<" ">=" "<="] @operator

; Nilai literal
(string) @string
(number) @number
(boolean) @constant.builtin

; Nama field di sisi kiri perbandingan / in / contains
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)

; Tanda baca
["(" ")"] @punctuation.bracket
"," @punctuation.delimiter
