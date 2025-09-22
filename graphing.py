# from sympy import *
from sympy.core.sympify import SympifyError
from sympy.plotting import plot3d
from sympy.plotting import plot as plot2d
# from sympy.abc import x, y, h
from sympy.plotting.pygletplot import PygletPlot as Plot


def makeGraph2d(func: str, inTermsOf: str, visionRange: tuple, funcHue: str):
    if len(visionRange) > 2:
        raise Exception("Invalid tuple provided for function range,\n"
                        "must have 2 items maximum and they must be numbers")

    if not func.__contains__(inTermsOf):
        print("Func doesnt contain inTermsOf")
        return None, "An error occurred | Function doesn't contain specified variable"
        # show a tkinter messagebox with error, bc this error can be user's fault
    else:
        try:
            float(inTermsOf)
        except ValueError:
            pass
        else:
            print("Error inTermsOf")
            return None, \
                "An error occurred | The function should be\nin terms of a variable, not a number"

        try:
            p = plot2d(func, (inTermsOf, visionRange[0], visionRange[1]), show=False, line_color=funcHue)
        except SympifyError:
            return None, "An error occurred | Multiplications should be\ndenoted by '*' (i.e. 5*x, not 5x)"

        return p, "Graph created successfully"
    # Make it so that the endpoint checks if the return was none to see if the graph was generated or not


def showGraph2d(graph: Plot):
    graph.show()


def makeGraph3d(func: str, inTermsOfX: str, inTermsOfY: str, visionRangeX: tuple, visionRangeY: tuple):
    if not func.__contains__(inTermsOfX) and not func.__contains__(inTermsOfY):
        print("inTermsOf error")
        return None, "An error occurred | An error occurred, the function doesn't\ncontain the variable specified for X or Y"


    # if not func.__contains__(inTermsOfY):
    #     print("inTermsOfY error")
    #     return None, "An error occurred | An error occurred, the function doesn't\n contain the variable specified for Y"
    # Doesn't check for inTermsOfY because the function can also be a 3d single-variable function

    else:
        try:
            float(inTermsOfX)
            float(inTermsOfY)
        except ValueError:
            pass
        else:
            return None, \
                "An error occurred | An error occurred, the function should be\nin terms of a variable, not a number"

    p = plot3d(func, (inTermsOfX, visionRangeX[0], visionRangeX[1]), (inTermsOfY, visionRangeY[0], visionRangeY[1]), show=False)

    return p, "Graph created successfully"


# makeGraph3d("x**3", "x", "y", (-5, 5), (-5, 5))

# a = makeGraph("x**2", "x", (-5, 5))
# showGraph(a)
