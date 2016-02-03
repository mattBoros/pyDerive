
def surround_with_parenthesis(s):
    if s[0] == '(' and s[-1] == ')':
        return s
    return "({0})".format(s)


def arithmetic_wrapper_convert_to_constants(arith_func):
    """
    This is a wrapper for arithmetic operators to ensure that any
    float or integer arguments are converted into Constants.
    """
    def wrapper(self, other):
        if type(other) == int or type(other) == float:
            other = constant.Constant(other)
        return arith_func(self, other)
    return wrapper


def is_empty(given_term):
    if type(given_term) == multipliedterm.MultipliedTerm \
            or type(given_term) == addedterm.AddedTerm:
        return len(given_term.terms) == 0
    return False


def simplify(term):

    if type(term) == addedterm.AddedTerm:
        term.terms = [simplify(term_current) for term_current in term.terms
                      if simplify(term_current) != 0 and not is_empty(term_current)]
        return term

    elif type(term) == multipliedterm.MultipliedTerm:
        term.terms = [simplify(term_current) for term_current in term.terms
                      if simplify(term_current) != 1 and not is_empty(term_current)]
        if 0 in term.terms:
            return constant.Constant(0)
        return term

    elif type(term) == naturallog.NaturalLog:
        inner_term_simple = simplify(term.inner_term)
        if inner_term_simple == terms.MathConstants.E:
            return constant.Constant(1)
        if inner_term_simple == 1:
            return constant.Constant(0)
        return naturallog.NaturalLog(inner_term_simple)

    elif type(term) == exponentterm:
        base_simple = simplify(term.base)
        power_simple = simplify(term.power)
        if power_simple == 0:
            return constant.Constant(1)
        if power_simple == 1:
            return base_simple
        return base_simple ** power_simple

    return term

from terms import constant
from terms import addedterm, multipliedterm, exponentterm, naturallog
import terms




