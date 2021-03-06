import math
import util
import term
import constant, sine


class Cosine(term.Term):

    @util.arithmetic_wrapper_convert_to_constants
    def __init__(self, inner_term):
        assert issubclass(type(inner_term), term.Term)
        self.inner_term = inner_term

    def __str__(self):
        return 'cos({0})'.format(str(self.inner_term))

    def __eq__(self, other):
        if type(other) == Cosine and util.simplify(self.inner_term) == util.simplify(other.inner_term):
            return True
        # TODO: Add other ways to check for sine equality
        return False

    def derivative(self, respect_to=None):
        if self.contains_variable(respect_to):
            # (cos(u))' = sin(u)*u'*-1
            return sine.Sine(self.inner_term) * self.inner_term.derivative() * (-1)
        return constant.Constant(0)

    def evaluate(self, values=None):
        evaluated_inner_term = self.inner_term.evaluate(values)
        if issubclass(type(evaluated_inner_term), term):
            return Cosine(evaluated_inner_term)
        return Cosine(constant.Constant(evaluated_inner_term))

    def contains_variable(self, var):
        return self.inner_term.contains_variable(var)

    def to_number(self, values=None):
        evaluated_inner_term = self.inner_term.to_number(values)
        if type(evaluated_inner_term) == float or type(evaluated_inner_term) == int:
            return math.cos(evaluated_inner_term)
        # otherwise it is a type of term
        return Cosine(evaluated_inner_term)










