# pyDerive
Note that not everything in this module works yet. It is still a work in progress.

## Variables

After importing the Variable class from primitive_terms, you can declare a variable like this:
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

Equations can be declared like this:
```
from primitive_terms import Variable, E
x = Variable('x')
y = Variable('y')
equation = x**2 + y - E
```

You can obtain the derivative of any term or equation by calling `equation.derivative()`, which produces another equation or term. If you have an equation with more than one variable, and would like to take a partial derivative or a derivative with respect to only one variable, call `equation.derivative(x)` or `equation.derivative('x')`.

There are two ways to plug numbers into your equation. There is `equation.evaluate(values)` and `equation.to_number(values)`, where values is a dictionary that assigns the variable name or string to the value. `evaluate` will give you an exact representation of the equation, while `to_number` will give you an approximation.

For example:
```
from primitive_terms import Variable, E

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

Be careful how you declare and assign your equations, because a term must always come first. If you do something like `5**x`, an error will occur because the integer and float arithmetic operators have not been overloaded. An alternative method to this would be to declare 5 as a constant, and then perform the exponentiation on it. For example:
```
from primitive_terms import Variable, Constant
x = Variable('x')
five_to_the_x = Constant(5)**x
```

Any of these equations will print with the proper parenthesis. For example:
```
print Variable('x') + Variable('y') + 5 - E**(Variable('z') + 2 + Variable('y'))
# prints "x + y + 5 + (-1)*(e^(z + 2 + y))"
```

TODO:

-Fix the operators (they were changed and broken)

-Add simplification of expressions to get rid of things like x^(2) + 0

-Add more functions such as sin, cos, logarithms with different bases.
