"""
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

"""
import util
import Term


class Constant(Term.Term):

    def __init__(self, number):
        assert type(number) == int or type(number) == float
        self.number = number

    @util.arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if type(other) == Constant:
            return Constant(self.number + other.number)
        return Term.Term.__add__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        if type(other) == Constant:
            return Constant(self.number * other.number)
        return Term.Term.__mul__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        if type(power) == Constant:
            return Constant(self.number ** power.number)
        return Term.Term.__pow__(self, power)

    def __eq__(self, other):
        if type(other) == Constant and self.number == other.number:
            return True
        if (type(other) == int or type(other) == float) and self.number == other:
            return True
        return False

    def __str__(self):
        if self.number < 0:
            return util.surround_with_parenthesis(str(self.number))
        return str(self.number)

    @staticmethod
    def derivative(self, respect_to=None):
        return Constant(0)

    def evaluate(self, values=None):
        return self.number

    def contains_variable(self, var):
        return True

    def to_number(self, values=None):
        return self.number














