"""
 -- Variable --
The Variable class is meant to represent a mathematical
variable. It holds a symbol, which is normally one letter
long like 'x' or 'y'. Variables are equal to their symbols
and any other variable which has the same symbol.

When running the derivative function on a variable, it
returns Constant(1) only if the respect_to argument is equal
to the variable itself or is equal to None.

"""
import util
import Term
import Constant, AddedTerm, MultipliedTerm, ExponentTerm


class Variable(Term.Term):

    def __init__(self, symbol):
        assert type(symbol) == str
        assert len(symbol) > 0
        self.symbol = symbol

    @util.arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if type(other) == MultipliedTerm.MultipliedTerm:
            if self in other.terms:
                # x + x*y*z = x*(1 + y*z)
                other.terms.remove(self)
                return self*(other + 1)
        elif type(other) == AddedTerm.AddedTerm:
            if self in other.terms:
                # x + y + z + x = 2*x + y + z
                other.terms.remove(self)
                return self*2 + other
        elif type(other) == ExponentTerm:
            if other.base == self:
                return self ** (other.power + 1)
        return Term.Term.__add__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        return Term.Term.__mul__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return Term.Term.__pow__(self, power)

    def __eq__(self, other):
        # Variable('x') == Variable('x') and Variable('x') == 'x'
        if type(other) == Variable and other.symbol == self.symbol:
            return True
        return self.symbol == other

    def __str__(self):
        if len(self.symbol) > 1:
            return util.surround_with_parenthesis(self.symbol)
        return self.symbol

    def derivative(self, respect_to=None):
        if self == respect_to or respect_to is None:
            return Constant.Constant(1)
        return self

    def evaluate(self, values=None):
        if self in values.keys():
            # running values[self] doesn't work because the objects have to be the same
            # not equivalent
            index_of_self_equivalent = values.keys().index(self)
            key = values.keys()[index_of_self_equivalent]
            return values[key]
        return self

    def contains_variable(self, var):
        if self == var or var is None:
            return True
        return False

    def to_number(self, values=None):
        return self.evaluate(values)




