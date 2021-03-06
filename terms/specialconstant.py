"""
 -- SpecialConstant --
SpecialConstant class is for any constant which cannot be
represented by a Constant. Examples of these are pi, e, c,
and others.

"""
import util
import term
import constant
import exponentterm


class SpecialConstant(term.Term):

    def __init__(self, number, string_representation=None):
        assert type(number) == int or type(number) == float
        self.number = number
        self.string_representation = string_representation

    @util.arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if self == other:
            return constant.Constant(2) * self
        return term.Term.__add__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        if self == other:
            return exponentterm.ExponentTerm(self, constant.Constant(2))
        return term.Term.__mul__(self, other)

    def __eq__(self, other):
        if type(other) == SpecialConstant:
            if other.string_representation == self.string_representation \
                    or other.number == self.number:
                return True
        if type(other) == constant and other.number == self.number:
            return True
        return False

    def __str__(self):
        return self.string_representation

    @staticmethod
    def derivative(self, respect_to=None):
        return constant.Constant(0)

    def evaluate(self, values=None):
        return self

    @staticmethod
    def contains_variable(var):
        return True

    def to_number(self, values=None):
        return self.number








