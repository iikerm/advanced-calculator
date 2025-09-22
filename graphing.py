from sympy.core.sympify import SympifyError
from sympy.plotting import plot3d
from sympy.plotting import plot as plot2d
from sympy.plotting.pygletplot import PygletPlot as Plot


def makeGraph2d(func: str, inTermsOf: str, visionRange: tuple, funcHue: str) -> (Plot, str):
    """
    Creates and returns a sympy.Plot object that represents the received function in 2D.
    :param func: mathematical function to draw
    :param inTermsOf: variable used by the function
    :param visionRange: range (min, max) where the function will be represented.
    :param funcHue: hue (color) in which the function will be drawn
    :return: a tuple containing the generated sympy.Plot object (if possible), and a string that will contain the error
    message produced if said Plot object could not be created.
    """
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
            return None, \
                "An error occurred | The function should be\nin terms of a variable, not a number"

        try:
            p = plot2d(func, (inTermsOf, visionRange[0], visionRange[1]), show=False, line_color=funcHue)
        except SympifyError:
            return None, "An error occurred | Multiplications should be\ndenoted by '*' (i.e. 5*x, not 5x)"

        return p, "Graph created successfully"


def makeGraph3d(func: str, inTermsOfX: str, inTermsOfY: str, visionRangeX: tuple, visionRangeY: tuple) -> (Plot, str):
    """
    Creates and returns a sympy.Plot object that represents the received function in 2D.
    :param func: mathematical function to draw
    :param inTermsOfX: variable used by the function in the first axis
    :param inTermsOfY: variable used by the function in the second axis
    :param visionRangeX: range (min, max) where the function will be represented for the first variable's axis.
    :param visionRangeY: range (min, max) where the function will be represented for the second variable's axis.
    :return: a tuple containing the generated sympy.Plot object (if possible), and a string that will contain the error
    message produced if said Plot object could not be created.
    """

    if not func.__contains__(inTermsOfX) and not func.__contains__(inTermsOfY):
        return None, "An error occurred | " \
                     "An error occurred, the function doesn't\ncontain the variable specified for X or Y"
    else:
        try:
            float(inTermsOfX)
            float(inTermsOfY)
        except ValueError:
            pass
        else:
            return None, \
                "An error occurred | An error occurred, the function should be\nin terms of a variable, not a number"

    p = plot3d(func, (inTermsOfX, visionRangeX[0], visionRangeX[1]), (inTermsOfY, visionRangeY[0], visionRangeY[1]),
               show=False)

    return p, "Graph created successfully"

