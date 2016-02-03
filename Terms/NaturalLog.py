import math

import term
import util
import constant, mathconstants


class NaturalLog(term.Term):

    @util.arithmetic_wrapper_convert_to_constants
    def __init__(self, inner_term):
        assert issubclass(type(inner_term), term.Term)
        self.inner_term = inner_term

    @util.arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        return term.Term.__add__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        return term.Term.__mul__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return term.Term.__pow__(self, power)

    def __str__(self):
        return 'ln({0})'.format(str(self.inner_term))

    def __eq__(self, other):
        if other == 0 and self.inner_term == 1:
            return True
        if other == 1 and self.inner_term == mathconstants.E:
            return True
        if type(other) == NaturalLog:
            return util.simplify(other.inner_term) == util.simplify(self.inner_term)
        return False

    def derivative(self, respect_to=None):
        if self.contains_variable(respect_to):
            return self.inner_term.derivative(respect_to) / self.inner_term
        return constant.Constant(0)

    def evaluate(self, values=None):
        evaluated_inner_term = self.inner_term.evaluate(values)
        if issubclass(type(evaluated_inner_term), term):
            return NaturalLog(evaluated_inner_term)
        return NaturalLog(constant.Constant(evaluated_inner_term))

    def contains_variable(self, var):
        return self.inner_term.contains_variable(var)

    def to_number(self, values=None):
        evaluated_inner_term = self.inner_term.to_number(values)
        if type(evaluated_inner_term) == float or type(evaluated_inner_term) == int:
            return math.log(evaluated_inner_term)
        # otherwise it is a type of term
        return NaturalLog(evaluated_inner_term)







