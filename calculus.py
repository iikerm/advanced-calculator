from sympy import *


def preCalc(expr: str) -> str:
    """
    Parses the expression received in order for sympy to understand expressions in other languages or other ways of
    writing some mathematical functions (e.g. sen (seno) is the spanish way to write sin (sine) and sympy only
    understands sin).
    :param expr: expression to parse
    :return: parsed expression
    """
    synonymsDict = {"sen": "sin", "arcsin": "asin",
                    "arcos": "acos", "arccos": "acos",
                    "tg": "tan", "arctan": "atan", "∞": "oo"}

    for key in synonymsDict:
        expr = expr.replace(key, synonymsDict[key])
    return expr

def cleanExpr(expr: str) -> str:
    """
    Improves readability of the functions that result of integral or differential calculations by parsing to substitute
    certain expressions, for example by substituting expressions like '^exponent' by superscript characters to represent
    exponents, or swapping the python exponent representation (**) for an easier to read representation (^).
    :param expr: function to be parsed
    :return: 'clean' parsed function
    """
    substituteDict = {"**": "^", "*": "·"}

    # Only 3 exponents that I managed to represent properly in utf-8
    superIndexDict = {"^1 ": f'\u00b9 ', "^2 ": f'\u00b2 ', "^3 ": f'\u00b3 '}

    expr = str(expr)
    expr += " "

    for key in substituteDict.keys():
        if expr.__contains__(key):
            expr = expr.replace(key, substituteDict[key])

    for key in superIndexDict.keys():
        if expr.__contains__(key):
            try:
                int(expr[expr.index(key) + 1])
            except ValueError:
                print(f"Value error in: '{expr[expr.index(key) + 1]}'")
            else:
                expr = expr.replace(key, superIndexDict[key])

    return expr.strip()


def calculateDifferential(func: str, inTermsOf=None, nth=1, partial=False) -> (Derivative, str):
    """
    Computes the nth differential (partial or whole) of the received function.
    :param func: function whose differential will be calculated
    :param inTermsOf: variable in terms of which the differential will be calculated
    :param nth: the differential to be calculated (i.e. nth=2 means the 2nd derivative of the function
    will be calculated)
    :param partial: indicates if the differential should be partial (True), or whole (False)
    :return: The calculated derivative (if possible), along with a message, which will be the error message produced if
    the derivative was not computable.
    """
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

    return d, "Differential calculated successfully"

def calculateIntegral(func: str, inTermsOf=None, uBound: str= "0", lBound: str= "0") -> (Integral, str):
    """
    Computes the integral (definite or indefinite) of the received function.
    :param func: function whose integral will be computed
    :param inTermsOf: variable to integrate
    :param uBound: upper bound of the integral (as a string so that things like sin(x), x, x**2, etc. can be used)
    :param lBound: lower bound of the integral (as a string so that things like sin(x), x, x**2, etc. can be used)
    :return: The calculated integral (if possible), along with a message, which will be the error message produced if
    the integral was not computable.
    """
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

