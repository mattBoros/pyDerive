
def surround_with_parenthesis(s):
    if s[0] == '(' and s[-1] == ')':
        return s
    return "({0})".format(s)


def arithmetic_wrapper_convert_to_constants(arith_func):
    def wrapper(self, other):
        if type(other) == int or type(other) == float:
            other = Constant.Constant(other)
        return arith_func(self, other)
    return wrapper


def is_empty(given_term):
    if type(given_term) == MultipliedTerm.MultipliedTerm \
            or type(given_term) == AddedTerm.AddedTerm:
        return len(given_term.terms) == 0
    return False


def simplify(term):

    if type(term) == AddedTerm.AddedTerm:
        term.terms = [simplify(term_current) for term_current in term.terms
                      if simplify(term_current) != 0 and not is_empty(term_current)]
        return term

    elif type(term) == MultipliedTerm.MultipliedTerm:
        term.terms = [simplify(term_current) for term_current in term.terms
                      if simplify(term_current) != 1 and not is_empty(term_current)]
        if 0 in term.terms:
            return Constant.Constant(0)
        return term

    elif type(term) == NaturalLog.NaturalLog:
        inner_term_simple = simplify(term.inner_term)
        if inner_term_simple == Terms.MathConstants.E:
            return Constant.Constant(1)
        if inner_term_simple == 1:
            return Constant.Constant(0)
        return NaturalLog.NaturalLog(inner_term_simple)

    elif type(term) == ExponentTerm:
        base_simple = simplify(term.base)
        power_simple = simplify(term.power)
        if power_simple == 0:
            return Constant.Constant(1)
        if power_simple == 1:
            return base_simple
        return base_simple ** power_simple

    return term

from Terms import Constant
from Terms import AddedTerm, MultipliedTerm, ExponentTerm, NaturalLog
import Terms




