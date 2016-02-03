"""
 --- primitive_terms in pyDerive ---


 -- Term --
The most basic class in this module is the Term class. Every
other class inherits from Term. Term overloads the arithmetic
operators, and also overrides equal, not equal, and string
operators. It also sets up basic derivative, contains_variable,
evaluate, and to_number for subclasses of Term to override.

Unfortunately since each Term subclass relies on each other and
on other Term subclasses, they cannot be split into different
files because of cyclic importing.


 - arithmetic_wrapper_convert_to_constants -
This is a wrapper for arithmetic operators to ensure that any
float or integer arguments are converted into Constants.


 -- Constant --
The Constant class holds any number whose string representation
is the same as the number itself. For example, the number 10 is
represented as "10", so it is a constant. Pi is represented as
"pi," even though it is equal to 3.14159... Therefore pi is not
a Constant.

A Constant is equal to any other Constant that holds the same
number, or any float or integer that is the same number as the
number that the Constant holds. For example:

Constant(1.5) == Constant(1.5) -> True
Constant(1.5) == 1.5 -> True


 -- SpecialConstant --
SpecialConstant class is for any constant which cannot be
represented by a Constant. Examples of these are pi, e, c,
and others.


 -- Variable --
The Variable class is meant to represent a mathematical
variable. It holds a symbol, which is normally one letter
long like 'x' or 'y'. Variables are equal to their symbols
and any other variable which has the same symbol.

When running the derivative function on a variable, it
returns Constant(1) only if the respect_to argument is equal
to the variable itself or is equal to None.


NaturalLog
AddedTerm
MultipliedTerm
ExponentTerm
Sine
Cosine



"""