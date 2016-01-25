"""
 --- primitive_terms in pyDerive ---


 -- Term --
The most basic class in this module is the Term class. Every
other class inherits from Term. Term overloads the arithmetic
operators, and also overrides equal, not equal, and string
operators. It also sets up basic derivative, contains_variable,
evaluate, and to_number for subclasses of Term to override.

Unfortunately since each Term subclass relies on each other and
on other Term subclasses, they cannot be split into different
files because of cyclic importing.


 - arithmetic_wrapper_convert_to_constants -
This is a wrapper for arithmetic operators to ensure that any
float or integer arguments are converted into Constants.


 -- Constant --
The Constant class holds any number whose string representation
is the same as the number itself. For example, the number 10 is
represented as "10", so it is a constant. Pi is represented as
"pi," even though it is equal to 3.14159... Therefore pi is not
a Constant.

A Constant is equal to any other Constant that holds the same
number, or any float or integer that is the same number as the
number that the Constant holds. For example:

Constant(1.5) == Constant(1.5) -> True
Constant(1.5) == 1.5 -> True


 -- SpecialConstant --
SpecialConstant class is for any constant which cannot be
represented by a Constant. Examples of these are pi, e, c,
and others.


 -- Variable --
The Variable class is meant to represent a mathematical
variable. It holds a symbol, which is normally one letter
long like 'x' or 'y'. Variables are equal to their symbols
and any other variable which has the same symbol.

When running the derivative function on a variable, it
returns Constant(1) only if the respect_to argument is equal
to the variable itself or is equal to None.


NaturalLog
AddedTerm
MultipliedTerm
ExponentTerm
Sine
Cosine



"""

import math
from util import surround_with_parenthesis


def arithmetic_wrapper_convert_to_constants(arith_func):
    def wrapper(self, other):
        if type(other) == int or type(other) == float:
            other = Constant(other)
        return arith_func(self, other)
    return wrapper


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
        inner_term_simple = simplify(term.inner_term)
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


class Term(object):

    @arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if type(other) == AddedTerm:
            for term in other.terms:
                if type(term) == MultipliedTerm and self in term.terms:
                    # x + (a + b + x*y*z) = a + b + x + x*y*z = a + b + x(1 + y*z)
                    term.terms.remove(self)
                    replacement_term = self * (term + 1)
                    other.terms.remove(term)
                    other.terms.append(replacement_term)
                    return other
            return AddedTerm([self] + other.terms)
        return AddedTerm([self, other])

    @arithmetic_wrapper_convert_to_constants
    def __sub__(self, other):
        return self + (Constant(-1) * other)

    @arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        if type(other) == MultipliedTerm:
            if self in other.terms:
                other.terms.remove(self)
                return self * (other + 1)
            return MultipliedTerm([self] + other.terms)
        return MultipliedTerm([self, other])

    @arithmetic_wrapper_convert_to_constants
    def __div__(self, other):
        return self * (other**-1)

    @arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return ExponentTerm(self, power)

    def __str__(self):
        return "There is a type which is a subclass of Term, but doesn't override __str__."

    def __eq__(self, other):
        print "There is a subclass of Term which does not override equals."

    def __ne__(self, other):
        return not self.__eq__(other)

    def derivative(self, respect_to=None):
        print "There is a subclass of Term which does not override derivative."

    def contains_variable(self, var):
        print "There is a subclass of Term which does not override contains_variable."

    def evaluate(self, values=None):
        print "There is a subclass of Term which does not override evaluate."

    def to_number(self, values=None):
        print "There is a subclass of Term which does not override to_number."


# -----------------------------------------------------------


class Constant(Term):

    def __init__(self, number):
        assert type(number) == int or type(number) == float
        self.number = number

    @arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if type(other) == Constant:
            return Constant(self.number + other.number)
        return Term.__add__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        if type(other) == Constant:
            return Constant(self.number * other.number)
        return Term.__mul__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        if type(power) == Constant:
            return Constant(self.number ** power.number)
        return Term.__pow__(self, power)

    def __eq__(self, other):
        if type(other) == Constant and self.number == other.number:
            return True
        if (type(other) == int or type(other) == float) and self.number == other:
            return True
        return False

    def __str__(self):
        return str(self.number)

    @staticmethod
    def derivative(self, respect_to=None):
        return Constant(0)

    def evaluate(self, values=None):
        return self.number

    def contains_variable(self, var):
        return True

    def to_number(self, values=None):
        return self.number


# -----------------------------------------------------------


class SpecialConstant(Term):

    def __init__(self, number, string_representation=None):
        assert type(number) == int or type(number) == float
        self.number = number
        self.string_representation = string_representation

    @arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if self == other:
            return Constant(2) * self
        return Term.__add__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        # do thing here
        return Term.__mul__(self, other)

    def __eq__(self, other):
        if type(other) == SpecialConstant:
            if other.string_representation == self.string_representation \
                    or other.number == self.number:
                return True
        if type(other) == Constant and other.number == self.number:
            return True
        return False

    def __str__(self):
        return self.string_representation

    @staticmethod
    def derivative(self, respect_to=None):
        return Constant(0)

    def evaluate(self, values=None):
        return self

    def contains_variable(self, var):
        return True

    def to_number(self, values=None):
        return self.number


# -----------------------------------------------------------


class Variable(Term):

    def __init__(self, symbol):
        assert type(symbol) == str
        assert len(symbol) > 0
        self.symbol = symbol

    @arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if type(other) == MultipliedTerm:
            if self in other.terms:
                # x + x*y*z = x*(1 + y*z)
                other.terms.remove(self)
                return self*(other + 1)
        elif type(other) == AddedTerm:
            if self in other.terms:
                # x + y + z + x = 2*x + y + z
                other.terms.remove(self)
                return self*2 + other
        elif type(other) == ExponentTerm:
            if other.base == self:
                return self ** (other.power + 1)
        return Term.__add__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        return Term.__mul__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return Term.__pow__(self, power)

    def __eq__(self, other):
        # Variable('x') == Variable('x') and Variable('x') == 'x'
        if type(other) == Variable and other.symbol == self.symbol:
            return True
        return self.symbol == other

    def __str__(self):
        if len(self.symbol) > 1:
            return surround_with_parenthesis(self.symbol)
        return self.symbol

    def derivative(self, respect_to=None):
        if self == respect_to or respect_to is None:
            return Constant(1)
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


# -----------------------------------------------------------


class NaturalLog(Term):

    @arithmetic_wrapper_convert_to_constants
    def __init__(self, inner_term):
        assert issubclass(type(inner_term), Term)
        self.inner_term = inner_term

    @arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        return Term.__add__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        return Term.__mul__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return Term.__pow__(self, power)

    def __str__(self):
        return 'ln({0})'.format(str(self.inner_term))

    def __eq__(self, other):
        if other == 0 and self.inner_term == 1:
            return True
        if other == 1 and self.inner_term == E:
            return True
        if type(other) == NaturalLog:
            return simplify(other.inner_term) == simplify(self.inner_term)
        return False

    def derivative(self, respect_to=None):
        if self.contains_variable(respect_to):
            return self.inner_term.derivative(respect_to) / self.inner_term
        return Constant(0)

    def evaluate(self, values=None):
        evaluated_inner_term = self.inner_term.evaluate(values)
        if issubclass(type(evaluated_inner_term), Term):
            return NaturalLog(evaluated_inner_term)
        return NaturalLog(Constant(evaluated_inner_term))

    def contains_variable(self, var):
        return self.inner_term.contains_variable(var)

    def to_number(self, values=None):
        evaluated_inner_term = self.inner_term.to_number(values)
        if type(evaluated_inner_term) == float or type(evaluated_inner_term) == int:
            return math.log(evaluated_inner_term)
        # otherwise it is a type of term
        return NaturalLog(evaluated_inner_term)


# -----------------------------------------------------------


class AddedTerm(Term):

    def __init__(self, terms):
        for term in terms:
            assert issubclass(type(term), Term)
        self.terms = terms

    @arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if type(other) == AddedTerm:
            return AddedTerm(self.terms + other.terms)
        return Term.__add__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        return Term.__mul__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return Term.__pow__(self, power)

    def __str__(self):
        if len(self.terms) == 1:
            return str(self.terms[0])
        s = ""
        for term in self.terms[:-1]:
            s = s + "{0} + ".format(term)
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


# -----------------------------------------------------------


class MultipliedTerm(Term):

    def __init__(self, terms):
        for term in terms:
            assert issubclass(type(term), Term)
        self.terms = terms

    @arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        return Term.__add__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        return Term.__mul__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return Term.__pow__(self, power)

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


# -----------------------------------------------------------


class ExponentTerm(Term):

    def __init__(self, base, power):
        assert issubclass(type(base), Term)
        assert issubclass(type(power), Term)
        self.base = base
        self.power = power

    @arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        return Term.__add__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        return Term.__mul__(self, other)

    @arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return Term.__pow__(self, power)

    def __str__(self):
        base_string = str(self.base)
        power_string = str(self.power)
        return "{0}^({1})".format(base_string, power_string)

    def __eq__(self, other):
        if type(other) == ExponentTerm and other.base == self.base and other.power == self.power:
            return True
        return False

    def derivative(self, respect_to=None):
        if self.base.contains_variable(respect_to) and self.power.contains_variable(respect_to):
            # (u^v)' = (u^v)*(v'*ln(u) + u'v/u)
            #            ^this is equivalent to 'self'
            added_term_1 = self.power.derivative(respect_to) * NaturalLog(self.base)
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
            return self * NaturalLog(self.base) * self.power.derivative(respect_to)
        else:
            return Constant(0)

    def evaluate(self, values=None):
        try:
            result = self.base.evaluate(values) ** self.power.evaluate(values)
        except TypeError:
            result = Constant(self.base.evaluate(values)) ** self.power.evaluate(values)
        return result

    def contains_variable(self, var):
        return self.base.contains_variable(var) or self.power.contains_variable(var)

    def to_number(self, values=None):
        try:
            result = self.base.to_number(values) ** self.power.to_number(values)
        except TypeError:
            result = Constant(self.base.to_number(values)) ** self.power.to_number(values)
        return result


# -----------------------------------------------------------


class Sine(Term):

    @arithmetic_wrapper_convert_to_constants
    def __init__(self, inner_term):
        assert issubclass(type(inner_term), Term)
        self.inner_term = inner_term

    def __str__(self):
        return 'sin({0})'.format(str(self.inner_term))

    def __eq__(self, other):
        if type(other) == Sine and simplify(self.inner_term) == simplify(other.inner_term):
            return True
        # TODO: Add other ways to check for sine equality
        return False

    def derivative(self, respect_to=None):
        if self.contains_variable(respect_to):
            # (sin(u))' = cos(u)*u'
            return Cosine(self.inner_term) * self.inner_term.derivative()
        return Constant(0)

    def evaluate(self, values=None):
        evaluated_inner_term = self.inner_term.evaluate(values)
        if issubclass(type(evaluated_inner_term), Term):
            return Sine(evaluated_inner_term)
        return Sine(Constant(evaluated_inner_term))

    def contains_variable(self, var):
        return self.inner_term.contains_variable(var)

    def to_number(self, values=None):
        evaluated_inner_term = self.inner_term.to_number(values)
        if type(evaluated_inner_term) == float or type(evaluated_inner_term) == int:
            return math.sin(evaluated_inner_term)
        # otherwise it is a type of term
        return Sine(evaluated_inner_term)


class Cosine(Term):

    @arithmetic_wrapper_convert_to_constants
    def __init__(self, inner_term):
        assert issubclass(type(inner_term), Term)
        self.inner_term = inner_term

    def __str__(self):
        return 'cos({0})'.format(str(self.inner_term))

    def __eq__(self, other):
        if type(other) == Cosine and simplify(self.inner_term) == simplify(other.inner_term):
            return True
        # TODO: Add other ways to check for sine equality
        return False

    def derivative(self, respect_to=None):
        if self.contains_variable(respect_to):
            # (cos(u))' = sin(u)*u'*-1
            return Sine(self.inner_term) * self.inner_term.derivative() * (-1)
        return Constant(0)

    def evaluate(self, values=None):
        evaluated_inner_term = self.inner_term.evaluate(values)
        if issubclass(type(evaluated_inner_term), Term):
            return Cosine(evaluated_inner_term)
        return Cosine(Constant(evaluated_inner_term))

    def contains_variable(self, var):
        return self.inner_term.contains_variable(var)

    def to_number(self, values=None):
        evaluated_inner_term = self.inner_term.to_number(values)
        if type(evaluated_inner_term) == float or type(evaluated_inner_term) == int:
            return math.cos(evaluated_inner_term)
        # otherwise it is a type of term
        return Cosine(evaluated_inner_term)


# -----------------------------------------------------------
# CONSTANTS


E = SpecialConstant(math.e, 'e')
PI = SpecialConstant(math.pi, 'pi')








