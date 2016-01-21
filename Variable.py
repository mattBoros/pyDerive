from PrimitiveTerms import Term, Constant
from util import surround_with_parenthesis

class Variable(Term):
    def __init__(self, symbol):
        assert type(symbol) == str
        assert len(symbol) > 0
        self.symbol = symbol

    def derivative(self):
        return Constant(1)

    def to_string(self):
        if len(self.symbol) > 1:
            return surround_with_parenthesis(self.symbol)
        return self.symbol

    def __eq__(self, other):
        if type(other) == Variable and other.symbol == self.symbol:
            return True
        return False

    def __str__(self):
        return self.to_string()









