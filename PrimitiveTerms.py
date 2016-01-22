import math
from util import surround_with_parenthesis


def replace_num_with_constant_if_constant(var):
    if type(var) == int or type(var) == float:
        return Constant(var)
    return var


def combine(term):
    assert issubclass(type(term), AddedTerm) or issubclass(type(term), MultipliedTerm)
    if type(term) == AddedTerm:
        nothing_found = True
        while nothing_found:
            nothing_found = False
            for i, term1 in enumerate(term.terms):
                for j, term2 in enumerate(term.terms):
                    if i != j:
                        pass

    if type(term) == MultipliedTerm:
        pass
    return term


def simplify(term):
    if type(term) == AddedTerm:
        term.terms = [simplify(term_current) for term_current in term.terms
                      if simplify(term_current) != 0]
        return term

    elif type(term) == MultipliedTerm:
        term.terms = [simplify(term_current) for term_current in term.terms
                      if simplify(term_current) != 1]
        if 0 in term.terms:
            return Constant(0)
        return term

    elif type(term) == NaturalLog:
        inner_term_simple = simplify(term.term)
        if inner_term_simple == E:
            return Constant(1)
        if inner_term_simple == 1:
            return Constant(0)
        return NaturalLog(inner_term_simple)

    elif type(term) == ExponentTerm:
        base_simple = simplify(term.base)
        power_simple = simplify(term.power)
        if power_simple == 0:
            return Constant(1)
        if power_simple == 1:
            return base_simple
        return base_simple ** power_simple

    return term


def constant_arithmetic(c1, c2, operation):
    if type(c1) == Constant and type(c2) == Constant and operation in ['+', '-', '*', '/', '**']:
        num = eval(str(c1.number) + operation + str(float(c2.number)))
        num = int(num) if int(num) == num else num
        return Constant(num)
    return None


class Term(object):

    def derivative(self):
        pass

    def integrate(self):
        pass

    def __mul__(self, other):
        other = replace_num_with_constant_if_constant(other)
        if constant_arithmetic(self, other, '*') is not None:
            return constant_arithmetic(self, other, '*')

        if type(self) == MultipliedTerm and type(other) == MultipliedTerm:
            return MultipliedTerm(self.terms + other.terms)
        if type(self) == MultipliedTerm:
            return MultipliedTerm(self.terms + [other])
        if type(other) == MultipliedTerm:
            return MultipliedTerm(other.terms + [self])
        return MultipliedTerm([self, other])

    def __div__(self, other):
        other = replace_num_with_constant_if_constant(other)
        if constant_arithmetic(self, other, '/') is not None:
            return constant_arithmetic(self, other, '/')
        return self * other**-1

    def __add__(self, other):
        other = replace_num_with_constant_if_constant(other)
        if constant_arithmetic(self, other, '+') is not None:
            return constant_arithmetic(self, other, '+')
        if type(self) == AddedTerm and type(other) == AddedTerm:
            return AddedTerm(self.terms + other.terms)
        if type(self) == AddedTerm:
            return AddedTerm(self.terms + [other])
        if type(other) == AddedTerm:
            return AddedTerm(other.terms + [self])
        return AddedTerm([self, other])

    def __sub__(self, other):
        return self + (Constant(-1) * other)

    def __pow__(self, power, modulo=None):
        power = replace_num_with_constant_if_constant(power)
        if constant_arithmetic(self, power, '**') is not None:
            return constant_arithmetic(self, power, '**')
        return ExponentTerm(self, power)

    def __str__(self):
        return "There is a type which is a subclass of Term, but doesn't override __str__"

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        return not self.__eq__(other)

# -----------------------------------------------------------


class Constant(Term):

    def __init__(self, number):
        assert type(number) == int or type(number) == float
        self.number = number

    @staticmethod
    def derivative():
        return Constant(0)

    def integral(self, with_respect_to):
        pass

    def __str__(self):
        return str(self.number)

    def __eq__(self, other):
        if type(other) == Constant and self.number == other.number:
            return True
        if (type(other) == int or type(other) == float) and self.number == other:
            return True
        return False

# -----------------------------------------------------------


class E(Constant):

    def __init__(self):
        super(E, self).__init__(math.e)

    def __str__(self):
        return 'e'

    def __eq__(self, other):
        if type(other) == E:
            return True
        return False

# -----------------------------------------------------------


class PI(Constant):

    def __init__(self):
        super(PI, self).__init__(math.pi)

    def __str__(self):
        return 'pi'

    def __eq__(self, other):
        if type(other) == PI:
            return True
        return False

# -----------------------------------------------------------


class NaturalLog(Term):

    def __init__(self, term):
        assert issubclass(type(term), Term)
        self.term = term

    def derivative(self):
        return self.term.derivative() / self.term

    def __str__(self):
        return 'ln({0})'.format(self.term.to_string())

    def __eq__(self, other):
        if other == 0 and self.term == 1:
            return True
        if other == 1 and self.term == E:
            return True
        if type(other) == NaturalLog:
            return simplify(other.term) == simplify(self.term)
        return False


# -----------------------------------------------------------


class AddedTerm(Term):

    def __init__(self, terms):
        for term in terms:
            assert issubclass(type(term), Term)
        self.terms = terms

    def derivative(self):
        # (u + v)' = u' + v'
        return AddedTerm([term.derivative() for term in self.terms])

    def __str__(self):
        if len(self.terms) == 1:
            return str(self.terms[0])
        s = ""
        for term in self.terms[:-1]:
            s = s + "{0}+".format(term)
        if len(self.terms) > 0:
            s = s + "{0}".format(self.terms[-1])
        return s

    def __eq__(self, other):
        if type(other) == AddedTerm:
            if len(self.terms) != len(other.terms):
                return False
            self.terms = sorted(self.terms, key=type)
            other.terms = sorted(other.terms, key=type)
            for (self_term, other_term) in zip(self.terms, other.terms):
                if simplify(self_term) != simplify(other_term):
                    return False
            return True
        return False


# -----------------------------------------------------------


class MultipliedTerm(Term):
    def __init__(self, terms):
        for term in terms:
            assert issubclass(type(term), Term)
        self.terms = terms

    def derivative(self):
        # (uv)' = u'v + uv'
        if len(self.terms) == 1:
            return self.terms[0].derivative()
        if len(self.terms) == 2:
            u = self.terms[0]
            v = self.terms[1]
            return u.derivative() * v + u * v.derivative()
        halfway_point = len(self.terms)/2
        u = MultipliedTerm(self.terms[:halfway_point])
        v = MultipliedTerm(self.terms[halfway_point:])
        return u.derivative() * v + u * v.derivative()

    def __str__(self):
        if len(self.terms) == 1:
            return str(self.terms[0])
        s = ""
        for term in self.terms[:-1]:
            s = s + "{0}*".format(term)
        if len(self.terms) > 0:
            s = s + "{0}".format(self.terms[-1])
        return s

    def __eq__(self, other):
        if type(other) == MultipliedTerm:
            if len(self.terms) != len(other.terms):
                return False
            self.terms = sorted(self.terms, key=type)
            other.terms = sorted(other.terms, key=type)
            for (self_term, other_term) in zip(self.terms, other.terms):
                if simplify(self_term) != simplify(other_term):
                    return False
            return True
        return False


# -----------------------------------------------------------


class ExponentTerm(Term):
    def __init__(self, base, power):
        assert issubclass(type(base), Term)
        assert issubclass(type(power), Term)
        self.base = base
        self.power = power

    def derivative(self):
        # (u^v)' = (u^v)*(v'ln(u) + u'v/u)
        #            ^this is the same as 'self'
        added_term_1 = self.power.derivative() * NaturalLog(self.base)
        added_term_2 = (self.base.derivative() * self.power) / self.base
        return self * (added_term_1 + added_term_2)

    def __str__(self):
        base_string = str(self.base)
        power_string = str(self.power)
        if len(power_string) > 1:
            power_string = surround_with_parenthesis(power_string)
        return "{0}^{1}".format(base_string, power_string)

    def __eq__(self, other):
        if type(other) == ExponentTerm and other.base == self.base and other.power == self.power:
            return True
        return False

# -----------------------------------------------------------

















