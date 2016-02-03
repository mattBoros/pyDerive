"""
 -- Term --
The most basic class in this module is the Term class. Every
other class inherits from Term. Term overloads the arithmetic
operators, and also overrides equal, not equal, and string
operators. It also sets up basic derivative, contains_variable,
evaluate, and to_number for subclasses of Term to override.

Unfortunately since each Term subclass relies on each other and
on other Term subclasses, they cannot be split into different
files because of cyclic importing.

"""
import util


class Term(object):

    @util.arithmetic_wrapper_convert_to_constants
    def __add__(self, other):
        if type(other) == AddedTerm.AddedTerm:
            for term in other.terms:
                if type(term) == MultipliedTerm.MultipliedTerm and self in term.terms:
                    # x + (a + b + x*y*z) = a + b + x + x*y*z = a + b + x(1 + y*z)
                    term.terms.remove(self)
                    replacement_term = self * (term + 1)
                    other.terms.remove(term)
                    other.terms.append(replacement_term)
                    return other
            return AddedTerm.AddedTerm([self] + other.terms)
        return AddedTerm.AddedTerm([self, other])

    @util.arithmetic_wrapper_convert_to_constants
    def __sub__(self, other):
        return self + (Constant.Constant(-1) * other)

    @util.arithmetic_wrapper_convert_to_constants
    def __mul__(self, other):
        if type(other) == MultipliedTerm:
            if self in other.terms:
                other.terms.remove(self)
                return self * (other + 1)
            return MultipliedTerm.MultipliedTerm([self] + other.terms)
        return MultipliedTerm.MultipliedTerm([self, other])

    @util.arithmetic_wrapper_convert_to_constants
    def __div__(self, other):
        return self * (other**-1)

    @util.arithmetic_wrapper_convert_to_constants
    def __pow__(self, power, modulo=None):
        return ExponentTerm.ExponentTerm(self, power)

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


import AddedTerm
import MultipliedTerm
import Constant
import ExponentTerm











