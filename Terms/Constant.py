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














