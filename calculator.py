import tkinter as tk
from tkinter import messagebox

#  ⬇   M Y   O W N   M O D U L E S   ⬇
import graphing
import calculus
import uiElements as ui

def graph2dWindow() -> None:
    """
    Function that generates a window for introducing parameters to generate a representation of a 2D graph from a
    mathematical function.
    """
    def generate2dGraph(master: tk.Tk, params: list, forWhat="graph") -> None:
        """
        Reads a specific set of parameters in order to generate the graph
        :param master: tk.Tk object that contains the button that called this function.
        :param params: a list containing 3 ui.OperationTypeGroups: [graph, color, range]. The graph group contains
        things like the function to represent, the variable it is in terms of etc., the color group contains the color
        and the range group contains information about the range of the function that will be drawn.
        :param forWhat: Indicates if this function should create an ui.CodeInfoWindow ("code") or if it should
        generate a graph ("graph")
        """
        dataList = []

        for group in params:
            for widget in group.groupAll:
                if type(widget) == ui.UnderlinedEntry:
                    dataList.append(widget.get())
                elif type(widget) == ui.ColorButton:
                    dataList.append(widget.hue)

        # The loop above produces a list of strings: [func, inTermsOf, color, from, to]

        if dataList[0] == "":
            messagebox.showerror("Unfilled parameters", "Please fill in all of the parameters")
            window2d.focus_force()
            return

        # Sets unfilled parameters to default
        if dataList[3] == "from":
            dataList[3] = "-5"
        if dataList[4] == "to":
            dataList[4] = "5"

        if forWhat == "graph":
            master.title("Generating graph...")
            graph, errReport = graphing.makeGraph2d(func=dataList[0], inTermsOf=dataList[1],
                                               visionRange=(dataList[3], dataList[4]), funcHue=dataList[2])

            if graph is None:
                errReport = errReport.split(" | ")
                messagebox.showerror(errReport[0], errReport[1])
                window2d.focus_force()
                return
            else:
                master.after(1, lambda: graph.show())
                master.after(1000, lambda: master.title("Building a 2D graph (sympy)"))

        elif forWhat == "code":
            ui.CodeInfoWindow(code=f"plot({dataList[0]}, (inTermsOf={dataList[1]}, visionRangeMin={dataList[3]}, "
                               f"visionRangeMax={dataList[4]}), line_color={dataList[2]})",
                           labelTitleText="Code used for 2D graph", library="from sympy.plotting import plot")
        else:
            raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")


    window2d = tk.Tk()
    window2d.geometry("460x320")
    window2d.title("Building a 2D graph (sympy)")
    window2d.configure(bg=ui.WINDOW_BG)
    window2d.focus_force()

    labelTitle2d = ui.TitleLabel(window2d, text="Preparing the 2D graph:", relx=0.15, rely=0.1)

    graph2dGroup = ui.OperationTypeGroup(window2d, name="Enter parameters: ", relx=0.15, rely=0.3)
    funcLabel = graph2dGroup.add_label("Function:")
    funcEntry = graph2dGroup.add_entry(width=20, row=1)

    spaceLabel = graph2dGroup.add_label("       ")

    tofLabel = graph2dGroup.add_label("In terms of:")
    tofEntry = graph2dGroup.add_entry(width=5, placeholder="x")
    tofEntry.entryFrame.grid_configure(sticky=tk.W)

    color2dGroup = ui.OperationTypeGroup(window2d, name="Select color: ", relx=0.5, rely=0.3)
    colLabel = color2dGroup.add_label("Click me  ⬇")
    colButton = color2dGroup.add_button(text="", bg="blue", typ="color")

    vis2dGroup = ui.OperationTypeGroup(window2d, name="Visibility of the function: ", relx=0.5, rely=0.6)
    visFromEntry = vis2dGroup.add_entry(placeholder="from", width=5)
    visSpaceLabel = vis2dGroup.add_label("                         ")
    visSpaceLabel.grid_configure(row=0, column=1)
    visToEntry = vis2dGroup.add_entry(placeholder="to", width=5, column=2, row=0)

    button2dOk = ui.DefaultButton(window2d, text="Draw function", width=0)     # width 0 is default
    button2dOk.configure(command=lambda: generate2dGraph(window2d, [graph2dGroup, color2dGroup, vis2dGroup]))
    button2dOk.placeBt(relx=0.66, rely=0.8)

    button2dCode = ui.DefaultButton(window2d, text="See code", width=0)     # width 0 is default
    button2dCode.placeBt(relx=0.46, rely=0.8)
    button2dCode.configure(command=lambda: generate2dGraph(window2d, [graph2dGroup, color2dGroup, vis2dGroup], forWhat="code"))

    window2d.bind("<Escape>", lambda event: window2d.destroy())

    window2d.bind("<Return>", lambda event: generate2dGraph(window2d, [graph2dGroup, color2dGroup, vis2dGroup]))
    # Does the same as the button2dOk when you press enter (return key)

    window2d.resizable(False, False)
    window2d.mainloop()


def graph3dWindow():
    """
    Function that generates a window for introducing parameters to generate a representation of a 3D graph from a
    mathematical function.
    """
    def generate3dGraph(master: tk.Tk, params: list, forWhat="graph") -> None:
        """
        Reads a specific set of parameters in order to generate the graph
        :param master: tk.Tk object that contains the button that called this function.
        :param params: A list containing 2 ui.OperationTypeGroup objects in this order [graph, range]
        :param forWhat: Indicates if this function should create an ui.CodeInfoWindow ("code") or if it should
        generate a graph ("graph")
        :return:
        """
        dataList = []

        for group in params:
            for widget in group.groupAll:
                if type(widget) == ui.UnderlinedEntry:
                    dataList.append(widget.get())

        # The loop above produces a list of strings: [func, inTermsOfX, inTermsOfY, fromX, toX, fromY, toY]

        if dataList[0] == "":
            messagebox.showerror("Unfilled parameters", "Please fill in all of the parameters")
            window3d.focus_force()
            return

        for i in range(3, len(dataList)):
            if dataList[i] == "from":
                dataList[i] = "-10"      # Sets unfilled parameters to default
            if dataList[i] == "to":
                dataList[i] = "10"

        if forWhat == "graph":
            master.title("Generating graph...")
            graph, errReport = graphing.makeGraph3d(func=dataList[0], inTermsOfX=dataList[1], inTermsOfY=dataList[2],
                                                    visionRangeX=(dataList[3], dataList[4]),
                                                    visionRangeY=(dataList[5], dataList[6]))

            if graph is None:
                errReport = errReport.split(" | ")
                messagebox.showerror(errReport[0], errReport[1])
                window3d.focus_force()
                return
            else:
                master.after(1, lambda: graph.show())
                master.after(1000, lambda: master.title("Building a 3D graph (sympy)"))

        elif forWhat == "code":
            ui.CodeInfoWindow(code=f"plot3d({dataList[0]}, (inTermsOfX={dataList[1]}, visionRangeMinX={dataList[3]}, "
                               f"visionRangeMaxX={dataList[4]}), "
                               f"(inTermsOfY={dataList[2]}, visionRangeMinY={dataList[5]}, "
                               f"visionRangeMaxY={dataList[6]}))",
                           labelTitleText="Code used for 3D graph", library="from sympy.plotting import plot3d")

        else:
            raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")

    window3d = tk.Tk()
    window3d.geometry("460x320")
    window3d.title("Building a 3D graph (sympy)")
    window3d.configure(bg=ui.WINDOW_BG)
    window3d.focus_force()

    labelTitle3d = ui.TitleLabel(window3d, text="Preparing the 3D graph:", relx=0.1, rely=0.1)

    graph3dGroup = ui.OperationTypeGroup(window3d, name="Enter parameters: ", relx=0.1, rely=0.3)
    funcLabel = graph3dGroup.add_label("Function:")
    funcEntry = graph3dGroup.add_entry(width=20, row=1)

    spaceLabel = graph3dGroup.add_label("       ")

    tofLabel = graph3dGroup.add_label("In terms of:")
    tofXEntry = graph3dGroup.add_entry(width=5, placeholder="x")
    tofXEntry.entryFrame.grid_configure(sticky=tk.W)

    tofYEntry = graph3dGroup.add_entry(width=5, placeholder="y")
    tofYEntry.entryFrame.grid_configure(sticky=tk.W)

    vis3dGroup = ui.OperationTypeGroup(window3d, name="Visibility of the function: ", relx=0.45, rely=0.3)
    vis3dInfoLabelX = vis3dGroup.add_label(text="For first variable (x)")
    visFromEntryX = vis3dGroup.add_entry(placeholder="from", width=5)
    visSpaceLabelX = vis3dGroup.add_label("           ")
    visSpaceLabelX.grid_configure(row=0, column=1)
    visToEntryX = vis3dGroup.add_entry(placeholder="to", width=5, column=2, row=1)

    vis3dInfoLabelY = vis3dGroup.add_label(text="For second variable (y)")
    visFromEntryY = vis3dGroup.add_entry(placeholder="from", width=5)
    visToEntryY = vis3dGroup.add_entry(placeholder="to", width=5, column=2, row=5)

    button3dOk = ui.DefaultButton(window3d, text="Draw function", width=0)
    button3dOk.configure(command=lambda: generate3dGraph(window3d, [graph3dGroup, vis3dGroup]))
    button3dOk.placeBt(relx=0.72, rely=0.72)

    button3dCode = ui.DefaultButton(window3d, text="See code", width=0)  # width 0 is default
    button3dCode.placeBt(relx=0.45, rely=0.72)
    button3dCode.configure(command=lambda: generate3dGraph(window3d, [graph3dGroup, vis3dGroup], forWhat="code"))

    window3d.bind("<Escape>", lambda event: window3d.destroy())

    window3d.bind("<Return>", lambda event: generate3dGraph(window3d, [graph3dGroup, vis3dGroup]))
    # Does the same as the button2dOk when you press enter (return key)

    window3d.resizable(False, False)
    window3d.mainloop()


def diffWindow(partial=False) -> None:
    """
    Function that generates a window where the user can introduce mathematical functions and see their derivative
    (partial or full) in real-time.
    :param partial: True if the differential is going to be partial, false otherwise
    """

    #   char acts as a border signalling the end of the itof char that will be inserted
    if partial:
        ansText = "∂ /∂f||"
        insertPosAnsText = 1
    else:
        ansText = "d/d ||"
        insertPosAnsText = 3


    def diffHandleKeyEvent(entryList: list, labelList: list, event=None, forWhat="calc", recalling=False) -> None:
        """
        Handler for the Key event in some entries. It reads the parameters received and decides what to do with them.
        It can either calculate the differential of the given mathematical function, or display a window with the
        python code used to do that.
        :param entryList: A list containing the different entries where the data must be read from in the following
        order: [function entry, function's variable (in terms of)]
        :param labelList: A list containing the label(s) that must be modified to display the result or
        relevant information about the integral calculation.
        They must follow this order: [result label]
        :param event: The event that triggered this function call
        :param forWhat: Can be either 'calc', to indicate that the differential must be calculated,
        or 'code' to indicate that the code necessary for this calculation must be displayed
        :param recalling: Indicates if this is the first call made to the function (False) or if it has been called
        again from a previous call (True)
        :return: None
        """
        recallingDiff = recalling
        func = entryList[0].get()
        itof = entryList[1].get()       # itof stands for in terms of
        resultLabel = labelList[0]

        if forWhat.lower() == "code":
            ui.CodeInfoWindow(code=f"diff({calculus.cleanExpr(func)}{f', {itof}' if partial else ''})",
                           labelTitleText=f"Code used for calculating{' partial' if partial else ''} derivatives",
                           library="from sympy import *", dimensions="380x200")

        if recallingDiff:
            recallingDiff = False
            if forWhat.lower() == "calc":
                try:
                    toShow, diffMsg = calculus.calculateDifferential(func, inTermsOf=itof, partial=partial)
                except Exception as e:
                    # Catches exceptions raised by Sympy whenever it can't calculate a differential
                    # print(f"DEBUG: An error happened, specifically:\n {e} \n\n Tried: {calculus.cleanExpr(func)}")
                    str(e)      # This line removes a warning
                    resultLabel.configure(fg=ui.LIGHT_DARK_DECO_BG)     # Indicates that the differential is being calculated
                else:
                    baseText = resultLabel["text"][:resultLabel["text"].index("=") + 2]

                    baseText = baseText[:insertPosAnsText] + itof + baseText[baseText.index(" "):]
                    resultLabel.configure(text=baseText + calculus.cleanExpr(toShow), fg=ui.FG_LABELS)
            else:
                raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")

        else:
            recallingDiff = True
            windowDiff.after(1, lambda: diffHandleKeyEvent(entryList, labelList, event, forWhat, recallingDiff))


    windowDiff = tk.Tk()
    windowDiff.geometry("460x320")
    windowDiff.configure(background=ui.WINDOW_BG)
    windowDiff.title(f"Calculating a{' partial 'if partial else ' '}derivative (sympy)")
    windowDiff.focus_force()

    labelTitleDiff = ui.TitleLabel(windowDiff, text="Preparing the differential: ", relx=0.1, rely=0.1)

    paramsGroupDiff = ui.OperationTypeGroup(windowDiff, name="Enter parameters: ", relx=0.1, rely=0.3)
    resultLabelDiff = tk.Label(windowDiff, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS, font=ui.GEN_CODE_FONT(), text="", pady=10,
                               padx=10)
    resultLabelDiff.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    paramsGroupDiff.add_label("Enter function: ")
    funcEntryDiff = paramsGroupDiff.add_entry(width=15)

    spaceLabelDiff = paramsGroupDiff.add_label("            ")
    spaceLabelDiff.grid_configure(row=0, column=1)

    itofLabelDiff = paramsGroupDiff.add_label("With respect to: ")
    itofLabelDiff.grid_configure(row=0, column=2, sticky=tk.E)
    itofEntryDiff = paramsGroupDiff.add_entry(placeholder="x", width=5, row=1, column=2)
    itofEntryDiff.configure(justify=tk.LEFT)

    codeButtonDiff = ui.DefaultButton(windowDiff, text="See code", width=0)  # width 0 is default
    codeButtonDiff.placeBt(relx=0.7, rely=0.42)
    codeButtonDiff.configure(command=lambda: diffHandleKeyEvent([funcEntryDiff, itofEntryDiff], [resultLabelDiff], forWhat="code"))


    resultLabelDiff.configure(text=(ansText[:insertPosAnsText] + itofEntryDiff.get() + ansText[insertPosAnsText:]).replace("||", " = "))

    funcEntryDiff.bind("<Key>", lambda e: diffHandleKeyEvent([funcEntryDiff, itofEntryDiff], [resultLabelDiff], e))
    itofEntryDiff.bind("<Key>", lambda e: diffHandleKeyEvent([funcEntryDiff, itofEntryDiff], [resultLabelDiff], e))

    windowDiff.bind("<Escape>", lambda e: windowDiff.destroy())
    windowDiff.mainloop()


def integWindow() -> None:
    """
    Generates the integral calculation window
    :return: None
    """

    def integHandleKeyEvent(entryList: list, labelList: list, event=None, forWhat="calc", recalling=False) -> None:
        """
        Reads the parameters received and decides what to do with them. It can either calculate the integral of the
        given mathematical function, or display a window with the python code used to do that.
        :param entryList: A list containing the different entries where the data must be read from in the following
        order: [function entry, function's variable (in terms of), upper bound entry, lower bound entry]
        :param labelList: A list containing the different labels that must be modified to display the result or
        relevant information about the integral calculation.
        They must follow this order: [result label, upper bound label, lower bound label]
        :param event: The event that triggered this function call
        :param forWhat: Can be either 'calc', to indicate that the integral must be calculated,
        or 'code' to indicate that the code necessary for this calculation must be displayed
        :param recalling: Indicates if this is the first call made to the function (False) or if it has been called
        again from a previous call (True)
        :return: None
        """

        recallingInteg = recalling

        func = entryList[0].get()
        itof = entryList[1].get()       # Stands for in terms of
        uBoundSrc = entryList[2].get()
        lBoundSrc = entryList[3].get()
        rLabel = labelList[0]
        uBoundLabel = labelList[1]
        lBoundLabel = labelList[2]


        if forWhat.lower() == "code":
            definite = True
            if uBoundSrc.__contains__("∞") or lBoundSrc.__contains__("∞"):
                definite = False

            ui.CodeInfoWindow(code=f"integrate({calculus.cleanExpr(func)}, {(f'({itof}, {uBoundSrc}, {lBoundSrc})' if definite else f'Symbol({itof})')})",
                           labelTitleText=f"Code used for calculating {'definite' if definite else 'indefinite'} integrals",
                           library="from sympy import *",
                           dimensions="400x220")
            return None

        if recallingInteg:
            if forWhat.lower() == "calc":
                try:
                    toShow, integMsg = calculus.calculateIntegral(func, inTermsOf=itof, uBound=uBoundSrc, lBound=lBoundSrc)
                except Exception as e:
                    # Exceptions will be caught all the time because the program will try to integrate incomplete expressions
                    # print(f"An error happened, specifically:\n {e} \n\n Tried: {calculus.cleanExpr(func)}")
                    str(e)  # Removes a warning

                    rLabel.configure(fg=ui.LIGHT_DARK_DECO_BG)     # Indicates that the differential is being calculated
                    uBoundLabel.configure(fg=ui.LIGHT_DARK_DECO_BG)
                    lBoundLabel.configure(fg=ui.LIGHT_DARK_DECO_BG)
                else:
                    if toShow is None:
                        rLabel.configure(fg=ui.LIGHT_DARK_DECO_BG)
                        uBoundLabel.configure(fg=ui.LIGHT_DARK_DECO_BG)
                        lBoundLabel.configure(fg=ui.LIGHT_DARK_DECO_BG)
                    else:
                        uBoundLabel.configure(text=uBoundSrc, fg=ui.FG_LABELS)
                        lBoundLabel.configure(text=lBoundSrc, fg=ui.FG_LABELS)
                        rLabel.configure(
                            text=f"{calculus.cleanExpr(func)} d{itof} "
                                 f"= {calculus.cleanExpr(toShow)}",
                            fg=ui.FG_LABELS)

                        symbolLabelInteg.configure(width=round(len(rLabel["text"]) * 0.8))

            else:
                raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")

        if not recallingInteg:
            recallingInteg = True
            windowInteg.after(1, lambda: integHandleKeyEvent(entryList, labelList, event, forWhat, recallingInteg))
        else:
            recallingInteg = False


        # Make it so that this function calculates the integral in real time and displays under the window

    windowInteg = tk.Tk()
    windowInteg.geometry("480x350")
    windowInteg.configure(background=ui.WINDOW_BG)
    windowInteg.title(f"Calculating an integral (sympy)")
    windowInteg.focus_force()

    labelTitleInteg = ui.TitleLabel(windowInteg, text="Preparing the integral", relx=0.15, rely=0.1)

    paramsGroupInteg = ui.OperationTypeGroup(windowInteg, relx=0.15, rely=0.3, name="Parameters")


    resultGroupX = 0.152
    resultGroupY = 0.73
    symbolLabelInteg = tk.Label(windowInteg, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS, font=ui.GEN_CODE_FONT(30), text="∫", pady=10,
                                padx=15, width=10, anchor=tk.W)
    symbolLabelInteg.place(relx=resultGroupX, rely=resultGroupY)

    resultLabelInteg = tk.Label(windowInteg, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS, font=ui.GEN_CODE_FONT(), text="", pady=0, padx=10)
    resultLabelInteg.place(relx=resultGroupX+0.11, rely=resultGroupY+0.08)

    upperBoundLabelInteg = tk.Label(windowInteg, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS, font=ui.GEN_CODE_FONT(12), text="")
    upperBoundLabelInteg.place(relx=resultGroupX+0.08, rely=resultGroupY+0.03)

    lowerBoundLabelInteg = tk.Label(windowInteg, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS, font=ui.GEN_CODE_FONT(12), text="")
    lowerBoundLabelInteg.place(relx=resultGroupX+0.08, rely=resultGroupY+0.14)


    buttonIntegCode = ui.DefaultButton(windowInteg, text="See code", width=0)  # width 0 means default width
    buttonIntegCode.placeBt(relx=0.70, rely=0.62)
    buttonIntegCode.configure(command=lambda: integHandleKeyEvent([funcEntryInteg, itofEntryInteg,
                                                          uBoundEntryInteg, lBoundEntryInteg],
                                                         [resultLabelInteg, upperBoundLabelInteg, lowerBoundLabelInteg],
                                                          forWhat="code"))

    buttonClearAllInteg = ui.DefaultButton(windowInteg, text="Clear all", width=0)  # width 0 means default width
    buttonClearAllInteg.placeBt(relx=0.45, rely=0.62)
    buttonClearAllInteg.configure(command=lambda: ui.UnderlinedEntry.resetEntries(funcEntryInteg, uBoundEntryInteg,
                                                                           lBoundEntryInteg, itofEntryInteg))

    funcLabelInteg = paramsGroupInteg.add_label("Enter function: ")
    funcEntryInteg = paramsGroupInteg.add_entry(width=15)
    funcEntryInteg.bind("<Key>", lambda e: integHandleKeyEvent([funcEntryInteg, itofEntryInteg,
                                                         uBoundEntryInteg, lBoundEntryInteg],
                                                         [resultLabelInteg, upperBoundLabelInteg, lowerBoundLabelInteg], e))

    spaceParamsLabelInteg = paramsGroupInteg.add_label("      ")

    itofLabelInteg = paramsGroupInteg.add_label("In terms of: ")
    itofEntryInteg = paramsGroupInteg.add_entry(width=5, placeholder="x")
    itofEntryInteg.entryFrame.grid_configure(sticky=tk.W)
    itofEntryInteg.bind("<Key>", lambda e: integHandleKeyEvent([funcEntryInteg, itofEntryInteg,
                                                         uBoundEntryInteg, lBoundEntryInteg],
                                                         [resultLabelInteg, upperBoundLabelInteg, lowerBoundLabelInteg], e))


    boundsGroupInteg = ui.OperationTypeGroup(windowInteg, relx=0.45, rely=0.3, name="Bounds")

    boundsLabelInteg = boundsGroupInteg.add_label("Integral bounds: ")
    lBoundEntryInteg = boundsGroupInteg.add_entry(width=5, placeholder="-∞", column=0)
    lBoundEntryInteg.bind("<Key>", lambda e: integHandleKeyEvent([funcEntryInteg, itofEntryInteg,
                                                        uBoundEntryInteg, lBoundEntryInteg],
                                                         [resultLabelInteg, upperBoundLabelInteg, lowerBoundLabelInteg],
                                                        e))

    spaceBoundLabelInteg = boundsGroupInteg.add_label("          ")
    spaceBoundLabelInteg.grid_configure(row=1, column=1)

    uBoundEntryInteg = boundsGroupInteg.add_entry(width=5, row=1, column=2, placeholder="+∞")
    uBoundEntryInteg.bind("<Key>", lambda e: integHandleKeyEvent([funcEntryInteg, itofEntryInteg,
                                                        uBoundEntryInteg, lBoundEntryInteg],
                                                        [resultLabelInteg, upperBoundLabelInteg, lowerBoundLabelInteg],
                                                        e))

    windowInteg.bind("<Escape>", lambda e: windowInteg.destroy())
    windowInteg.mainloop()


def generateMain() -> None:
    """
    Generates the program's main window
    """
    windowMain = tk.Tk()
    windowMain.title("Main menu")
    windowMain.geometry("640x380")
    windowMain.configure(bg=ui.WINDOW_BG)

    canvasMain = tk.Canvas(windowMain, width=640, height=380, bg=ui.WINDOW_BG)
    canvasMain.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    decoLineTopInfoMain = canvasMain.create_line((20, 69, 620, 69), fill=ui.DARK_DECO_BG)  # Line is just 1px under frame ✔
    decoRectBtMain = canvasMain.create_rectangle((20, 89, 620, 360), outline=ui.LIGHT_DARK_DECO_BG)

    frameInfoMain = tk.Frame(canvasMain, width=640, height=70, bg=ui.WINDOW_BG)
    frameInfoMain.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    labelInfoMain = ui.TitleLabel(frameInfoMain, text="Choose what you want to do: ", relx=0.03, rely=0.5)

    graphGroup = ui.OperationTypeGroup(canvasMain, name="Graphing", relx=0.05, rely=0.29, anchor=None)
    btGraph2d = graphGroup.add_button("Draw 2D graph")
    btGraph2d.configure(command=graph2dWindow)

    btGraph3d = graphGroup.add_button("Draw 3D graph")
    btGraph3d.configure(command=graph3dWindow)

    derivateGroupMain = ui.OperationTypeGroup(canvasMain, name="Differentials", relx=0.05, rely=0.52)
    btDeriv = derivateGroupMain.add_button(text="Calculate derivative")
    btDeriv.configure(command=diffWindow)

    btPartDeriv = derivateGroupMain.add_button(text="Calculate partial\nderivative", height=2)
    btPartDeriv.configure(command=lambda: diffWindow(partial=True))

    integGroupMain = ui.OperationTypeGroup(canvasMain, name="Integrals", relx=0.05, rely=0.8)
    btInteg = integGroupMain.add_button(text="Calculate integral")
    btInteg.configure(command=integWindow)

    windowMain.bind("<Escape>", lambda event: windowMain.destroy())
    windowMain.resizable(False, False)
    windowMain.mainloop()

generateMain()
