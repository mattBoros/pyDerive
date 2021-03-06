# pyDerive
Take symbolic derivatives with Python.

This project is still a work in progress.

## Variables

After importing the Variable class from terms.variable, you can declare a variable like this:
```
x = Variable('x')
```
Variables can have string representations longer than length one, but this could get confusing in situations with more than one variable in an equation.
Note that variables are equal to their string representations, for example
```
x == 'x'
# This is True
```

## Equations

Equations can be used like this:
```
from terms.variable import Variable
from terms.mathconstants import E

x = Variable('x')
y = Variable('y')

equation = x**2 + y - E
```

You can obtain the derivative of any term or equation by calling `equation.derivative()`, which produces another equation or term. If you have an equation with more than one variable, and would like to take a partial derivative or a derivative with respect to only one variable, call `equation.derivative(x)` or `equation.derivative('x')`.

There are two ways to plug numbers into your equation. There is `equation.evaluate(values)` and `equation.to_number(values)`, where values is a dictionary that assigns the variable name or string to the value. `evaluate` will give you an exact representation of the equation, while `to_number` will give you an approximation.

For example:
```
from terms.variable import Variable
from terms.mathconstants import E

x = Variable('x')
y = Variable('y')

equation = x**2 + y - E
values = {x: 2, 'y': 1}

equation.evaluate(values)
# This is "e*(-1) + 5" or an equivalent
# After simplification is implemented, it will just be "5 - e"

equation.to_number(values)
# This is 2.28171817154
```

Any of these equations will print with the proper parenthesis. For example:
```
print Variable('x') + Variable('y') + 5 - E**(Variable('z') + 2 + Variable('y'))
# prints "x + y + 5 + (-1)*(e^(z + 2 + y))"
```

## Evaluate strings to an equation

You can evaluate strings into an equation by using the string_to_equation function. For example:

```
from string_to_equation import string_to_equation

equation_from_string, variables = string_to_equation("x^2+1-y")
#The string_to_equation function returns the equation and the variables used in that equation.
print equation_from_string
# Prints "x^(2) + 1 + (-1)*y"

values = {'x': 4, 'y': 2}
print equation_from_string.to_number(values)
# Prints 15
```


**TODO:**

-Add simplification of expressions to get rid of things like "x^(2) + 0" and "x + (-1)*e"

-Add more functions such as sin, cos, logarithms with different bases.

-Create custom set of exceptions
