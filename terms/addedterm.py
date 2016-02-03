import util
import Term


class AddedTerm(Term.Term):

    def __init__(self, terms):
        for current_term in terms:
            assert issubclass(type(current_term), Term.Term)
        self.terms = terms

    @util.arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if type(other) == AddedTerm:
            return AddedTerm(self.terms + other.terms)
        return Term.Term.__add__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        return Term.Term.__mul__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return Term.Term.__pow__(self, power)

    def __str__(self):
        if len(self.terms) == 0:
            return ""
        if len(self.terms) == 1:
            return str(self.terms[0])
        s = ""
        for i in xrange(len(self.terms) - 1):
            term = self.terms[i]
            s = s + "{0} + ".format(term)
        return s + "{0}".format(self.terms[-1])

    def __eq__(self, other):
        if type(other) == AddedTerm:
            if len(self.terms) != len(other.terms):
                return False
            self.terms = sorted(self.terms, key=type)
            other.terms = sorted(other.terms, key=type)
            for (self_term, other_term) in zip(self.terms, other.terms):
                if util.simplify(self_term) != util.simplify(other_term):
                    return False
            return True
        return False

    def derivative(self, respect_to=None):
        # (u + v)' = u' + v'
        return AddedTerm([term.derivative(respect_to) for term in self.terms])

    def evaluate(self, values=None):
        s = 0
        for term in self.terms:
            try:
                s = term.evaluate(values) + s
            except TypeError:
                s = s + term.evaluate(values)
        return s

    def contains_variable(self, var):
        return any(term.contains_variable(var) for term in self.terms)

    def to_number(self, values=None):
        s = 0
        for term in self.terms:
            try:
                s = term.to_number(values) + s
            except TypeError:
                s = s + term.to_number(values)
        return s



