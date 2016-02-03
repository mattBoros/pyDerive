import util
import term
import constant, naturallog


class ExponentTerm(term.Term):

    def __init__(self, base, power):
        assert issubclass(type(base), term.Term)
        assert issubclass(type(power), term.Term)
        self.base = base
        self.power = power

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
        base_string = str(self.base)
        power_string = util.surround_with_parenthesis(str(self.power))
        return "{0}^{1}".format(base_string, power_string)

    def __eq__(self, other):
        if type(other) == ExponentTerm and other.base == self.base and other.power == self.power:
            return True
        return False

    def derivative(self, respect_to=None):
        if self.base.contains_variable(respect_to) and self.power.contains_variable(respect_to):
            # (u^v)' = (u^v)*(v'*ln(u) + u'v/u)
            #            ^this is equivalent to 'self'
            added_term_1 = self.power.derivative(respect_to) * naturallog.NaturalLog(self.base)
            added_term_2 = (self.base.derivative(respect_to) * self.power) / self.base
            return self * (added_term_1 + added_term_2)
        elif self.base.contains_variable(respect_to):
            # (u^v)' with respect to u
            # is v*u'*u^(v-1)
            return self.power * self.base.derivative(respect_to) * self.base ** (self.power - 1)
        elif self.power.contains_variable(respect_to):
            # (u^v)' with respect to u
            # is ln(u)*v'*u^v
            #              ^with is equivalent to 'self'
            return self * naturallog.NaturalLog(self.base) * self.power.derivative(respect_to)
        else:
            return constant.Constant(0)

    def evaluate(self, values=None):
        try:
            result = self.base.evaluate(values) ** self.power.evaluate(values)
        except TypeError:
            result = constant.Constant(self.base.evaluate(values)) ** self.power.evaluate(values)
        return result

    def contains_variable(self, var):
        return self.base.contains_variable(var) or self.power.contains_variable(var)

    def to_number(self, values=None):
        try:
            result = self.base.to_number(values) ** self.power.to_number(values)
        except TypeError:
            result = constant.Constant(self.base.to_number(values)) ** self.power.to_number(values)
        return result






