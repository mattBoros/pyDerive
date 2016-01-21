from Variable import Variable
from PrimitiveTerms import simplify
from PrimitiveTerms import *

x = Variable('x')
y = ((x**50)*x*5)*(x + 5)
print simplify(y.derivative())
print simplify((x+x*1*1).derivative())






















