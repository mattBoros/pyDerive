from primitive_terms import Variable, E, PI

x = Variable('x')

equation = x**2 + x + 1
values = {x: 5}
print '"{0}" evaluated at x = 5 is {1}'.format(equation, equation.to_number(values))

# EDIT in how add/multiplication/exponentiation works
# so this is broken!!
derivative_of_equation = x.derivative('x')
print 'The derivative of "{0}" is "{1}"\n'.format(equation, derivative_of_equation)


y = Variable('y')

equation2 = x**2 + x*y + y**2
values2 = {'x': 1}
print 'When x = 1, "{0}" evaluates to "{1}"\n'.format(equation2, equation2.evaluate(values2))


equation3 = x**2 + E + PI
values3 = {'x': 5}
print 'When x = 5, "{0}" evaluates to {1}'.format(equation3, equation3.evaluate(values3))
print '...this is approximately {0}'.format(equation3.to_number(values3))















