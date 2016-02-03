from util import simplify



# constant showcase (lol)
from terms.mathconstants import PI, E

for constant in E, PI:
    print "{0} ~~ {1}".format(constant, constant.to_number())



# variable creation
from terms.variable import Variable

x = Variable('x')
y = Variable('y')
z = Variable('z')
print ""



# derivative showcase
equation = x ** 2 + x + 1
derivative = simplify(equation.derivative())

print 'The derivative of "{0}" is "{1}"'\
        .format(equation, derivative)
print ""



# partial derivative showcase
equation = x ** 2 + x * y + y ** 2
partial_derivative = simplify(equation.derivative('x'))

print 'The derivative of "{0}" with respect to "x" is "{1}"'\
        .format(equation, partial_derivative)
print ""



# string -> equation showcase
from string_to_equation import string_to_equation

string = "x^2 - 2 + y"
equation = string_to_equation(string)

print 'It evaluated to "{0}"'.format(equation)
print ""



# sine, cosine, natural log showcase
from terms.sine import Sine
from terms.cosine import Cosine
from terms.naturallog import NaturalLog

equation = Sine(x) + Cosine(y) + NaturalLog(z)
derivative = simplify(equation.derivative())

print 'The derivative of "{0}" is "{1}"'\
        .format(equation, derivative)
print ""



# evaluate showcase
equation = x**2 + x + PI + E
values = {x: 2}
approx_value = simplify(equation.evaluate(values))

print '"{0}" evaluated at x = 2 is "{1}"'\
        .format(equation, approx_value)
print ""



# to_number showcase
equation = x**2 + x + PI + E
values = {x: 2}
approx_value = simplify(equation.to_number(values))

print '"{0}" at x = 2 is about "{1}"'\
        .format(equation, approx_value)








