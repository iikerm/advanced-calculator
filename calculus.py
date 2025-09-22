from sympy import *


def preCalc(expr: str):
    synonymsDict = {"sen": "sin", "arcsin": "asin",
                    "arcos": "acos", "arccos": "acos",
                    "tg": "tan", "arctan": "atan", "∞": "oo"}

    for key in synonymsDict:
        expr = expr.replace(key, synonymsDict[key])
    return expr

def cleanExpr(expr: str):
    # superIndexList = [f'^0', f'\u00b9', f'\u00b2', f'\u00b3', f'^4',
    #                   f'^5', f'^6', f'^7', f'^8', f'^9']

    subDict = {"sqrt": "√", "**": "^", "*": "·"}
    superIndexDict = {"^1 ": f'\u00b9 ', "^2 ": f'\u00b2 ', "^3 ": f'\u00b3 '}

    expr = str(expr)
    expr += " "

    expr = expr.replace("**", "^")
    # Only 3 exponents that I managed to represent properly in utf-8 (or any other encoding)
    for key in superIndexDict.keys():
        if expr.__contains__(key):
            try:
                int(expr[expr.index(key) + 1])
            except ValueError:
                print(f"Value error in: '{expr[expr.index(key) + 1]}'")
            else:
                expr = expr.replace(key, superIndexDict[key])

    expr = expr.replace("*", "·")
    return expr.strip()


def calcDiff(func: str, inTermsOf=None, nth=1, partial=False):
    d = preCalc(func)
    count = 0

    if inTermsOf is None:
        if partial:
            return None, "An error occurred | For a partial derivative, the variable\nto derive with respect to must be entered"

        try:
            diff(d)
        except ValueError as e:      # This happens when an unknown expression is entered (e.g. multiplication without *)
            return None, "An error occurred | Invalid expression was entered for the function\n" \
                         "so the differential could not be calculated"

        else:   # inTermsOf is None and there is no error
            while count < nth and d != 0:
                d = diff(d)
                count += 1

    else:   # inTermsOf is not None
        while count < nth and d != 0:
            d = diff(d, inTermsOf)
            count += 1

    # print("CLEANEXPR RESULT:\n" + cleanExpr(d))
    return d, "Differential calculated successfully"


def calcInteg(func: str, inTermsOf=None, uBound: str="0", lBound: str="0"):
    r = preCalc(func)
    uBound = preCalc(uBound)
    lBound = preCalc(lBound)

    try:
        if lBound.__contains__("oo") or uBound.__contains__("oo"):
            # Indefinite integral
            r = integrate(r, Symbol(inTermsOf))
        else:
            # Definite integral
            r = integrate(r, (inTermsOf, lBound, uBound))

    except ValueError as e:
        return None, "An error occurred | Invalid expression was entered for the function\n" \
                     f"so the differential could not be calculated.\n{e}"

    return r, "Integral calculated successfully"


if __name__ == '__main__':
    # For debug
    print(calcDiff("x**2+y**2", "x", nth=1))
    print(cleanExpr("x**4"))
    print(calcInteg("x**2", "x", "-oo", "oo"))
