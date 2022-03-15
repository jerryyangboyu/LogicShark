# Defines methods functions for CNF, DNF and SIMPLIFY operations

from sympy.logic.boolalg import to_cnf
from sympy.logic.boolalg import to_dnf
from sympy.logic import simplify_logic
from sympy.abc import A, B, C, D, E, F, G, H, I, J, K, L, M, N, \
    O, P, Q, R, S, T, U, V, W, X, Y, Z


# cnf(String) -> String
def cnf(inputExpr):
    temp = inputExpr.replace('^', '&')
    return to_cnf(temp, simplify=True)


# dnf(String) -> String
def dnf(inputExpr):
    temp = inputExpr.replace('^', '&')
    return to_dnf(temp, simplify=True)


# simplify(String) -> String
def simplify(inputExpr):
    temp = inputExpr.replace('^', '&')
    return simplify_logic(temp)


# test
# print("1 : ", cnf('A ^ B | C'))
# print("2 : ", dnf('A ^ B | C'))
# print("3 : ", simplify('A ^ B | C'))
# print("4 : ", cnf('A ^ (A | C) | (C | ~B)'))
# print("5 : ", simplify('A ^ (A | C) | (C | ~B)'))
# print('6', cnf('((~A ^ B) | (C | D)) | ((D & ~C) | (~A | ~B))'))
# print('7', dnf('((~A ^ B) | (C | D)) | ((D & ~C) | (~A | ~B))'))
# print('8', simplify('((~A ^ B) | (C | D)) | ((D & ~C) | (~A | ~B))'))
# print('9', dnf('A ^ ~B | (B ^ (~C | A))'))
# print('10', cnf('A ^ ~B | (B ^ (~C | A))'))
# print('11', simplify('A ^ ~B | (B ^ (~C | A))'))
# print('12', cnf('W | ((X | ~Y) ^ (Z ^ Y))'))
# print('13', dnf('W | ((X | ~Y) ^ (Z ^ Y))'))
# print('14', simplify('W | ((X | ~Y) ^ (Z ^ Y))'))
