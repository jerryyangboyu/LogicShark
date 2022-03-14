# Defines methods functions for CNF, DNF and SIMPLIFY operations
from pyeda.inter import *


# cnf(String) -> String
def cnf(inputExpr):
    temp1 = inputExpr.replace('^', '&')
    expression = expr(temp1, simplify=False)
    temp = expression.to_cnf()
    if len(str(temp)) == 1:
        return str(temp)
    return string_replacement(temp.to_unicode())


# dnf(String) -> String
def dnf(inputExpr):
    temp1 = inputExpr.replace('^', '&')
    expression = expr(temp1, simplify=False)
    temp = expression.to_dnf()
    if len(str(temp)) == 1:
        return str(temp)
    return string_replacement(temp.to_unicode())


# simplify(String) -> String
def simplify(inputExpr):
    temp1 = inputExpr.replace('^', '&')
    temp = expr(temp1, simplify=True)
    if len(str(temp)) == 1:
        return str(temp)
    return string_replacement(temp.to_unicode())


def string_replacement(temp):
    temp = temp.replace('·', 'and')  # replace for AND
    temp = temp.replace('+', 'or')  # replace for OR

    # replace for NOT
    lst = list(temp)
    for i in range(0, len(lst)):
        if lst[i] == '′':
            lst[i], lst[i - 1] = lst[i - 1], lst[i]
    temp2 = ''.join(lst)
    result = temp2.replace('′', 'not ')
    return result


