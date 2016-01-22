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

    def derivative(self, respect_to=None):
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

    def evaluate(self, values):
        print "There is a subclass of Term which does not override."

# -----------------------------------------------------------


class Constant(Term):

    def __init__(self, number):
        assert type(number) == int or type(number) == float
        self.number = number

    @staticmethod
    def derivative(self, respect_to=None):
        return Constant(0)

    def __str__(self):
        return str(self.number)

    def __eq__(self, other):
        if type(other) == Constant and self.number == other.number:
            return True
        if (type(other) == int or type(other) == float) and self.number == other:
            return True
        return False

    def evaluate(self, values):
        return self.number

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

    def derivative(self, respect_to=None):
        return self.term.derivative(respect_to) / self.term

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

    def evaluate(self, values):
        return math.log(self.term.evaluate(values))


# -----------------------------------------------------------


class AddedTerm(Term):

    def __init__(self, terms):
        for term in terms:
            assert issubclass(type(term), Term)
        self.terms = terms

    def derivative(self, respect_to=None):
        # (u + v)' = u' + v'
        return AddedTerm([term.derivative(respect_to) for term in self.terms])

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

    def evaluate(self, values):
        s = 0
        for term in self.terms:
            s = term.evaluate(values) + s
        return s


# -----------------------------------------------------------


class MultipliedTerm(Term):

    def __init__(self, terms):
        for term in terms:
            assert issubclass(type(term), Term)
        self.terms = terms

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

    def __str__(self):
        if len(self.terms) == 1:
            return str(self.terms[0])
        s = ""
        for term in self.terms[:-1]:
            term_string = str(term)
            if len(term_string) > 1:
                term_string = surround_with_parenthesis(term_string)
            s = s + "{0}*".format(term_string)
        if len(self.terms) > 0:
            last_term_string = str(self.terms[-1])
            if len(last_term_string) > 1:
                last_term_string = surround_with_parenthesis(last_term_string)
            s = s + "{0}".format(last_term_string)
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

    def evaluate(self, values):
        p = 1
        for term in self.terms:
            p = term.evaluate(values) * p
        return p


# -----------------------------------------------------------


class ExponentTerm(Term):

    def __init__(self, base, power):
        assert issubclass(type(base), Term)
        assert issubclass(type(power), Term)
        self.base = base
        self.power = power

    def derivative(self, respect_to=None):
        # (u^v)' = (u^v)*(v'ln(u) + u'v/u)
        #            ^this is the same as 'self'
        added_term_1 = self.power.derivative(respect_to) * NaturalLog(self.base)
        added_term_2 = (self.base.derivative(respect_to) * self.power) / self.base
        return self * (added_term_1 + added_term_2)

    def __str__(self):
        base_string = str(self.base)
        power_string = str(self.power)
        return "{0}^({1})".format(base_string, power_string)

    def __eq__(self, other):
        if type(other) == ExponentTerm and other.base == self.base and other.power == self.power:
            return True
        return False

    def evaluate(self, values):
        return self.base.evaluate(values) ** self.power.evaluate(values)


# -----------------------------------------------------------


class Variable(Term):

    def __init__(self, symbol):
        assert type(symbol) == str
        assert len(symbol) > 0
        self.symbol = symbol

    def derivative(self, respect_to=None):
        if self == respect_to or respect_to is None:
            return Constant(1)
        return self

    def to_string(self):
        if len(self.symbol) > 1:
            return surround_with_parenthesis(self.symbol)
        return self.symbol

    def __eq__(self, other):
        # Variable('x') == Variable('x') and Variable('x') == 'x'
        if type(other) == Variable and other.symbol == self.symbol:
            return True
        return self.symbol == other

    def __str__(self):
        return self.to_string()

    def can_combine(self, other):
        if type(other) == Variable:
            if self == other:
                return True
        if type(other) == MultipliedTerm or type(other) == AddedTerm:
            if self in other.terms:
                return True
        return False

    def evaluate(self, values):
        if self in values.keys():
            # running values[self] doesn't work because the objects have to be the same
            # not equivalent
            index_of_self_equivalent = values.keys().index(self)
            key = values.keys()[index_of_self_equivalent]
            return values[key]
        return self















