import util
import Term


class MultipliedTerm(Term.Term):

    def __init__(self, terms):
        for term in terms:
            assert issubclass(type(term), Term.Term)
        self.terms = terms

    @util.arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        return Term.Term.__add__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        return Term.Term.__mul__(self, other)

    @util.arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return Term.Term.__pow__(self, power)

    def __str__(self):
        if len(self.terms) == 1:
            return str(self.terms[0])
        s = ""
        for term in self.terms[:-1]:
            term_string = str(term)
            if len(term_string) > 1:
                term_string = util.surround_with_parenthesis(term_string)
            s = s + "{0}*".format(term_string)
        if len(self.terms) > 0:
            last_term_string = str(self.terms[-1])
            if len(last_term_string) > 1:
                last_term_string = util.surround_with_parenthesis(last_term_string)
            s = s + "{0}".format(last_term_string)
        return s

    def __eq__(self, other):
        if type(other) == MultipliedTerm:
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
        # (uv)' = u'v + uv'
        if len(self.terms) == 1:
            return self.terms[0].derivative(respect_to)
        if len(self.terms) == 2:
            u = self.terms[0]
            v = self.terms[1]
            return u.derivative(respect_to) * v + u * v.derivative(respect_to)
        halfway_point = len(self.terms)/2
        u = MultipliedTerm(self.terms[:halfway_point])
        v = MultipliedTerm(self.terms[halfway_point:])
        return u.derivative(respect_to) * v + u * v.derivative(respect_to)

    def evaluate(self, values=None):
        p = 1
        for term in self.terms:
            try:
                p = term.evaluate(values) * p
            except TypeError:
                p = p * term.evaluate(values)
        return p

    def contains_variable(self, var):
        return any(term.contains_variable(var) for term in self.terms)

    def to_number(self, values=None):
        p = 1
        for term in self.terms:
            try:
                p = term.to_number(values) * p
            except TypeError:
                p = p * term.to_number(values)
        return p