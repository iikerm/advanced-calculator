import tkinter as tk
from tkinter import messagebox

#  ⬇   M Y   O W N   M O D U L E S   ⬇
import graphing
import calculus
import uiElements as ui


class Graph2D:
    DETAILS_LABEL_CONTENT = "Click here to enter the window for introducing the 2D graph's details.\n\n" \
                            "This part of the program is able to draw any function in terms of any one variable" \
                            " given. You will also be able to specify the color, as well as the range in which the" \
                            " function is drawn.\nIn the same way as with every other part, there is also a button to" \
                            " show what the code that computes this part looks like in python."

    def __init__(self):
        """
        Generates a window for introducing parameters to generate a representation of a 2D graph from a
        mathematical function.
        """

        self.window2d = tk.Tk()
        self.window2d.geometry("460x320")
        self.window2d.title("Building a 2D graph (sympy)")
        self.window2d.configure(bg=ui.WINDOW_BG)
        self.window2d.focus_force()

        labelTitle2d = ui.TitleLabel(self.window2d, text="Preparing the 2D graph:", relx=0.15, rely=0.1)

        self.graph2dGroup = ui.OperationTypeGroup(self.window2d, name="Enter parameters: ", relx=0.15, rely=0.3)
        funcLabel = self.graph2dGroup.add_label("Function:")
        funcEntry = self.graph2dGroup.add_entry(width=20, row=1)

        spaceLabel = self.graph2dGroup.add_label("       ")

        tofLabel = self.graph2dGroup.add_label("In terms of:")
        tofEntry = self.graph2dGroup.add_entry(width=5, placeholder="x")
        tofEntry.entryFrame.grid_configure(sticky=tk.W)

        self.color2dGroup = ui.OperationTypeGroup(self.window2d, name="Select color: ", relx=0.5, rely=0.3)
        colLabel = self.color2dGroup.add_label("Click me  ⬇")
        colButton = self.color2dGroup.add_color_button(text="", bg="#0000ff")

        self.vis2dGroup = ui.OperationTypeGroup(self.window2d, name="Visibility of the function: ", relx=0.5, rely=0.6)
        visFromEntry = self.vis2dGroup.add_entry(placeholder="from", width=5)
        visSpaceLabel = self.vis2dGroup.add_label("                         ")
        visSpaceLabel.grid_configure(row=0, column=1)
        visToEntry = self.vis2dGroup.add_entry(placeholder="to", width=5, column=2, row=0)

        button2dOk = ui.DefaultButton(self.window2d, text="Draw function", width=0)  # width 0 is default
        button2dOk.configure(
            command=lambda: self.generateGraph())
        button2dOk.placeBt(relx=0.66, rely=0.8)

        button2dCode = ui.DefaultButton(self.window2d, text="See code", width=0)  # width 0 is default
        button2dCode.placeBt(relx=0.46, rely=0.8)
        button2dCode.configure(
            command=lambda: self.generateGraph(forWhat="code"))

        self.window2d.bind("<Escape>", lambda event: self.window2d.destroy())

        self.window2d.bind("<Return>",
                           lambda event: self.generateGraph())
        # Does the same as the button2dOk when you press enter (return key)

        self.window2d.resizable(False, False)
        self.window2d.mainloop()

    def generateGraph(self, forWhat="graph") -> None:
        """
        Generates the actual 2D graph
        :param forWhat: Indicates if this function should create an ui.CodeInfoWindow ("code") or if it should
        generate a graph ("graph")
        """
        dataList = []

        for group in [self.graph2dGroup, self.color2dGroup, self.vis2dGroup]:
            for widget in group.groupAll:
                if type(widget) == ui.UnderlinedEntry:
                    dataList.append(widget.get())
                elif type(widget) == ui.ColorButton:
                    dataList.append(widget.hue)

        # The loop above produces a list of strings: [func, inTermsOf, color, from, to]

        if dataList[0] == "":
            messagebox.showerror("Unfilled parameters", "Please fill in all of the parameters")
            self.window2d.focus_force()
            return

        # Sets unfilled parameters to default
        if dataList[3] == "from":
            dataList[3] = "-5"
        if dataList[4] == "to":
            dataList[4] = "5"

        if forWhat == "graph":
            self.window2d.title("Generating graph...")
            graph, errReport = graphing.makeGraph2d(func=dataList[0], inTermsOf=dataList[1],
                                                    visionRange=(dataList[3], dataList[4]), funcHue=dataList[2])

            if graph is None:
                errReport = errReport.split(" | ")
                messagebox.showerror(errReport[0], errReport[1])
                self.window2d.focus_force()
                return
            else:
                self.window2d.after(1, lambda: graph.show())
                self.window2d.after(1000, lambda: self.window2d.title("Building a 2D graph (sympy)"))

        elif forWhat == "code":
            ui.CodeInfoWindow(code=f"plot({dataList[0]}, (inTermsOf={dataList[1]}, visionRangeMin={dataList[3]}, "
                                   f"visionRangeMax={dataList[4]}), line_color={dataList[2]})",
                              labelTitleText="Code used for 2D graph", library="from sympy.plotting import plot")
        else:
            raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")


class Graph3D:
    DETAILS_LABEL_CONTENT = "Click here to enter the window for introducing the 3D graph's details.\n\n" \
                            "This part of the program is able to draw any function in terms of any two variables" \
                            " given. You will also be able to specify the range (for both variables) in which the" \
                            " function is drawn.\nIn the same way as with every other part, there is also a button to" \
                            " show what the code that computes this part looks like in python."

    def __init__(self):
        """
        Generates a window for introducing parameters to generate a representation of a 3D graph from a
        mathematical function.
        """

        self.window3d = tk.Tk()
        self.window3d.geometry("460x320")
        self.window3d.title("Building a 3D graph (sympy)")
        self.window3d.configure(bg=ui.WINDOW_BG)
        self.window3d.focus_force()

        labelTitle3d = ui.TitleLabel(self.window3d, text="Preparing the 3D graph:", relx=0.1, rely=0.1)

        self.graph3dGroup = ui.OperationTypeGroup(self.window3d, name="Enter parameters: ", relx=0.1, rely=0.3)
        funcLabel = self.graph3dGroup.add_label("Function:")
        funcEntry = self.graph3dGroup.add_entry(width=20, row=1)

        spaceLabel = self.graph3dGroup.add_label("       ")

        tofLabel = self.graph3dGroup.add_label("In terms of:")
        self.tofXEntry = self.graph3dGroup.add_entry(width=5, placeholder="x")
        self.tofXEntry.entryFrame.grid_configure(sticky=tk.W)
        self.tofXEntry.bind("<FocusOut>", lambda event: self.updateItofLabel("x"))

        self.tofYEntry = self.graph3dGroup.add_entry(width=5, placeholder="y")
        self.tofYEntry.entryFrame.grid_configure(sticky=tk.W)
        self.tofYEntry.bind("<FocusOut>", lambda event: self.updateItofLabel("y"))

        self.vis3dGroup = ui.OperationTypeGroup(self.window3d, name="Visibility of the function: ", relx=0.45, rely=0.3)
        self.vis3dInfoLabelX = self.vis3dGroup.add_label(text="For first variable (x)")
        visFromEntryX = self.vis3dGroup.add_entry(placeholder="from", width=5)
        visSpaceLabelX = self.vis3dGroup.add_label("           ")
        visSpaceLabelX.grid_configure(row=0, column=1)
        visToEntryX = self.vis3dGroup.add_entry(placeholder="to", width=5, column=2, row=1)

        self.vis3dInfoLabelY = self.vis3dGroup.add_label(text="For second variable (y)")
        visFromEntryY = self.vis3dGroup.add_entry(placeholder="from", width=5)
        visToEntryY = self.vis3dGroup.add_entry(placeholder="to", width=5, column=2, row=5)

        button3dOk = ui.DefaultButton(self.window3d, text="Draw function", width=0)
        button3dOk.configure(command=lambda: self.generateGraph())
        button3dOk.placeBt(relx=0.72, rely=0.72)

        button3dCode = ui.DefaultButton(self.window3d, text="See code", width=0)  # width 0 is default
        button3dCode.placeBt(relx=0.45, rely=0.72)
        button3dCode.configure(command=lambda: self.generateGraph(forWhat="code"))

        self.window3d.bind("<Escape>", lambda event: self.window3d.destroy())

        self.window3d.bind("<Return>", lambda event: self.generateGraph())
        # Does the same as the button2dOk when you press enter (return key)

        self.window3d.resizable(False, False)
        self.window3d.mainloop()

    def updateItofLabel(self, variable: str = "x") -> None:
        if variable == "x":
            self.vis3dInfoLabelX.configure(text=f"For first variable ({self.tofXEntry.get()})")
        elif variable == "y":
            self.vis3dInfoLabelY.configure(text=f"For second variable ({self.tofYEntry.get()})")
        else:
            raise SyntaxError(f"Invalid variable '{variable}' received for Graph3D.updateItofLabel. Must be 'x' or 'y'")

    def generateGraph(self, forWhat="graph") -> None:
        """
        Generates the actual 3D graph
        :param forWhat: Indicates if this function should create an ui.CodeInfoWindow ("code") to display the code or
        if it should generate the graph ("graph")
        :return:
        """
        dataList = []

        for group in [self.graph3dGroup, self.vis3dGroup]:
            for widget in group.groupAll:
                if type(widget) == ui.UnderlinedEntry:
                    dataList.append(widget.get())

        # The loop above produces a list of strings: [func, inTermsOfX, inTermsOfY, fromX, toX, fromY, toY]

        if dataList[0] == "":
            messagebox.showerror("Unfilled parameters", "Please fill in all of the parameters")
            self.window3d.focus_force()
            return

        for i in range(3, len(dataList)):
            if dataList[i] == "from":
                dataList[i] = "-10"  # Sets unfilled parameters to default
            if dataList[i] == "to":
                dataList[i] = "10"

        if forWhat == "graph":
            self.window3d.title("Generating graph...")
            graph, errReport = graphing.makeGraph3d(func=dataList[0], inTermsOfX=dataList[1], inTermsOfY=dataList[2],
                                                    visionRangeX=(dataList[3], dataList[4]),
                                                    visionRangeY=(dataList[5], dataList[6]))

            if graph is None:
                errReport = errReport.split(" | ")
                messagebox.showerror(errReport[0], errReport[1])
                self.window3d.focus_force()
                return
            else:
                self.window3d.after(1, lambda: graph.show())
                self.window3d.after(1000, lambda: self.window3d.title("Building a 3D graph (sympy)"))

        elif forWhat == "code":
            ui.CodeInfoWindow(code=f"plot3d({dataList[0]}, (inTermsOfX={dataList[1]}, visionRangeMinX={dataList[3]}, "
                                   f"visionRangeMaxX={dataList[4]}), "
                                   f"(inTermsOfY={dataList[2]}, visionRangeMinY={dataList[5]}, "
                                   f"visionRangeMaxY={dataList[6]}))",
                              labelTitleText="Code used for 3D graph", library="from sympy.plotting import plot3d")

        else:
            raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")


class DifferentialCalculator:
    DETAILS_LABEL_CONTENT_PARTIALDIFF = "Click here to enter the window for real-time " \
                                        "calculation of the partial derivative.\n\nThis part of the " \
                                        "program is able to calculate any partial derivative in terms of the variable" \
                                        " given.\nIn the same way as with every other part, there" \
                                        " is also a button to show what the code that computes" \
                                        " this part looks like in python."

    DETAILS_LABEL_CONTENT_NORMALDIFF = "Click here to enter the window for real-time calculation of the differential" \
                                       " equation.\n\nThis part of the program is able to calculate any differential" \
                                       " equation given.\nIn the same way as with every other part, there is also a" \
                                       " button to show what the code that computes this part looks like in python."

    def __init__(self, partial=False):
        """
        Function that generates a window where the user can introduce mathematical functions and see their derivative
        (partial or full) in real-time.
        :param partial: True if the differential is going to be partial, false otherwise
        """
        self.partial = partial

        #   char acts as a border signalling the end of the 'in terms of' char that will be inserted
        if partial:
            self.ansText = "∂ /∂f||"
            self.insertPosAnsText = 1
        else:
            self.ansText = "d/d ||"
            self.insertPosAnsText = 3

        self.windowDiff = tk.Tk()
        self.windowDiff.geometry("460x320")
        self.windowDiff.configure(background=ui.WINDOW_BG)
        self.windowDiff.title(f"Calculating a{' partial ' if partial else ' '}derivative (sympy)")
        self.windowDiff.focus_force()

        labelTitleDiff = ui.TitleLabel(self.windowDiff, text="Define the differential: ", relx=0.1, rely=0.1)

        paramsGroupDiff = ui.OperationTypeGroup(self.windowDiff, name="Enter parameters: ", relx=0.1, rely=0.3)
        self.resultLabelDiff = tk.Label(self.windowDiff, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS,
                                        font=ui.GEN_CODE_FONT(), text="", pady=10, padx=10)
        self.resultLabelDiff.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        paramsGroupDiff.add_label("Enter function: ")
        self.funcEntryDiff = paramsGroupDiff.add_entry(width=15)

        spaceLabelDiff = paramsGroupDiff.add_label("            ")
        spaceLabelDiff.grid_configure(row=0, column=1)

        itofLabelDiff = paramsGroupDiff.add_label("With respect to: ")
        itofLabelDiff.grid_configure(row=0, column=2, sticky=tk.E)
        self.itofEntryDiff = paramsGroupDiff.add_entry(placeholder="x", width=5, row=1, column=2)
        self.itofEntryDiff.configure(justify=tk.LEFT)

        codeButtonDiff = ui.DefaultButton(self.windowDiff, text="See code", width=0)  # width 0 is default
        codeButtonDiff.placeBt(relx=0.7, rely=0.42)
        codeButtonDiff.configure(
            command=lambda: self.handleKeyEvent(forWhat="code"))

        self.resultLabelDiff.configure(
            text=(self.ansText[:self.insertPosAnsText] +
                  self.itofEntryDiff.get() +
                  self.ansText[self.insertPosAnsText:]).replace("||", " = "))

        self.funcEntryDiff.bind("<Key>", lambda e: self.handleKeyEvent(e))
        self.itofEntryDiff.bind("<Key>", lambda e: self.handleKeyEvent(e))

        self.windowDiff.bind("<Escape>", lambda e: self.windowDiff.destroy())
        self.windowDiff.mainloop()

    def handleKeyEvent(self, event=None, forWhat="calc", recalling=False) -> None:
        """
        Handler for the Key event in some entries. It reads the parameters received and decides what to do with them.
        It can either calculate the differential of the given mathematical function, or display a window with the
        python code used to do that.
        :param event: The event that triggered this function call
        :param forWhat: Can be either 'calc', to indicate that the differential must be calculated,
        or 'code' to indicate that the code necessary for this calculation must be displayed
        :param recalling: Indicates if this is the first call made to the function (False) or if it has been called
        again from a previous call (True)
        :return: None
        """
        recallingDiff = recalling
        func = self.funcEntryDiff.get()
        itof = self.itofEntryDiff.get()  # itof stands for in terms of
        # resultLabel = labelList[0]

        if forWhat.lower() == "code":
            ui.CodeInfoWindow(code=f"diff({calculus.cleanExpr(func)}{f', {itof}' if self.partial else ''})",
                              labelTitleText=f"Code used for calculating{' partial' if self.partial else ''} "
                                             f"derivatives",
                              library="from sympy import *", dimensions="380x200")

        if recallingDiff:
            recallingDiff = False
            if forWhat.lower() == "calc":
                try:
                    toShow, diffMsg = calculus.calculateDifferential(func, inTermsOf=itof, partial=self.partial)
                except Exception as e:
                    # Catches exceptions raised by Sympy whenever it can't calculate a differential
                    # print(f"DEBUG: An error happened, specifically:\n {e} \n\n Tried: {calculus.cleanExpr(func)}")
                    str(e)  # This line removes a warning

                    # Indicates that the differential is being calculated:
                    self.resultLabelDiff.configure(fg=ui.LIGHT_DARK_DECO_BG)
                else:
                    baseText = self.resultLabelDiff["text"][:self.resultLabelDiff["text"].index("=") + 2]

                    baseText = baseText[:self.insertPosAnsText] + itof + baseText[baseText.index(" "):]
                    self.resultLabelDiff.configure(text=baseText + calculus.cleanExpr(toShow), fg=ui.FG_LABELS)
            else:
                raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")

        else:
            recallingDiff = True
            self.windowDiff.after(1, lambda: self.handleKeyEvent(event, forWhat, recallingDiff))


class IntegralCalculator:
    DETAILS_LABEL_CONTENT = "Click here to enter the window for real-time calculation of the integral.\n\n" \
                            "This part of the program is able to calculate any integral, be it in a" \
                            " defined range or not.\nIn the same way as with every other part, there is also a" \
                            " button to show what the code that computes this part looks like in python."

    def __init__(self):
        """
        Generates the integral calculation window
        :return: None
        """

        self.windowInteg = tk.Tk()
        self.windowInteg.geometry("480x350")
        self.windowInteg.configure(background=ui.WINDOW_BG)
        self.windowInteg.title(f"Calculating an integral (sympy)")
        self.windowInteg.focus_force()

        labelTitleInteg = ui.TitleLabel(self.windowInteg, text="Define the integral: ", relx=0.15, rely=0.1)

        paramsGroupInteg = ui.OperationTypeGroup(self.windowInteg, relx=0.15, rely=0.3, name="Parameters")

        resultGroupX = 0.152
        resultGroupY = 0.73
        self.symbolLabelInteg = tk.Label(self.windowInteg, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS,
                                         font=ui.GEN_CODE_FONT(30),
                                         text="∫", pady=10,
                                         padx=15, width=10, anchor=tk.W)
        self.symbolLabelInteg.place(relx=resultGroupX, rely=resultGroupY)

        self.resultLabelInteg = tk.Label(self.windowInteg, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS,
                                         font=ui.GEN_CODE_FONT(),
                                         text="", pady=0, padx=10)
        self.resultLabelInteg.place(relx=resultGroupX + 0.11, rely=resultGroupY + 0.08)

        self.upperBoundLabelInteg = tk.Label(self.windowInteg, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS,
                                             font=ui.GEN_CODE_FONT(12),
                                             text="")
        self.upperBoundLabelInteg.place(relx=resultGroupX + 0.08, rely=resultGroupY + 0.03)

        self.lowerBoundLabelInteg = tk.Label(self.windowInteg, bg=ui.LIGHT_WINDOW_BG, fg=ui.FG_LABELS,
                                             font=ui.GEN_CODE_FONT(12),
                                             text="")
        self.lowerBoundLabelInteg.place(relx=resultGroupX + 0.08, rely=resultGroupY + 0.14)

        buttonIntegCode = ui.DefaultButton(self.windowInteg, text="See code", width=0)  # width 0 means default width
        buttonIntegCode.placeBt(relx=0.70, rely=0.62)
        buttonIntegCode.configure(command=lambda: self.handleKeyEvent(forWhat="code"))

        buttonClearAllInteg = ui.DefaultButton(self.windowInteg, text="Clear all",
                                               width=0)  # width 0 means default width
        buttonClearAllInteg.placeBt(relx=0.45, rely=0.62)
        buttonClearAllInteg.configure(
            command=lambda: ui.UnderlinedEntry.resetEntries(self.funcEntryInteg, self.uBoundEntryInteg,
                                                            self.lBoundEntryInteg, self.itofEntryInteg))

        funcLabelInteg = paramsGroupInteg.add_label("Enter function: ")
        self.funcEntryInteg = paramsGroupInteg.add_entry(width=15)
        self.funcEntryInteg.bind("<Key>", lambda e: self.handleKeyEvent(e))

        spaceParamsLabelInteg = paramsGroupInteg.add_label("      ")

        itofLabelInteg = paramsGroupInteg.add_label("In terms of: ")
        self.itofEntryInteg = paramsGroupInteg.add_entry(width=5, placeholder="x")
        self.itofEntryInteg.entryFrame.grid_configure(sticky=tk.W)
        self.itofEntryInteg.bind("<Key>", lambda e: self.handleKeyEvent(e))

        boundsGroupInteg = ui.OperationTypeGroup(self.windowInteg, relx=0.45, rely=0.3, name="Bounds")

        boundsLabelInteg = boundsGroupInteg.add_label("Integral bounds: ")
        self.lBoundEntryInteg = boundsGroupInteg.add_entry(width=5, placeholder="-∞", column=0)
        self.lBoundEntryInteg.bind("<Key>", lambda e: self.handleKeyEvent(e))

        spaceBoundLabelInteg = boundsGroupInteg.add_label("          ")
        spaceBoundLabelInteg.grid_configure(row=1, column=1)

        self.uBoundEntryInteg = boundsGroupInteg.add_entry(width=5, row=1, column=2, placeholder="+∞")
        self.uBoundEntryInteg.bind("<Key>", lambda e: self.handleKeyEvent(e))

        self.windowInteg.bind("<Escape>", lambda e: self.windowInteg.destroy())
        self.windowInteg.mainloop()

    def handleKeyEvent(self, event=None, forWhat="calc", recalling=False) -> None:
        """
        It can either calculate the integral of the
        given mathematical function, or display a window with the python code used to do that.
        :param event: The event that triggered this function call
        :param forWhat: Can be either 'calc', to indicate that the integral must be calculated,
        or 'code' to indicate that the code necessary for this calculation must be displayed
        :param recalling: Indicates if this is the first call made to the function (False) or if it has been called
        again from a previous call (True)
        :return: None
        """

        recallingInteg = recalling

        # [resultLabelInteg, upperBoundLabelInteg, lowerBoundLabelInteg]
        func = self.funcEntryInteg.get()
        itof = self.itofEntryInteg.get()  # 'itof' stands for in terms of
        uBoundSrc = self.uBoundEntryInteg.get()
        lBoundSrc = self.lBoundEntryInteg.get()

        if forWhat.lower() == "code":
            definite = True
            if uBoundSrc.__contains__("∞") or lBoundSrc.__contains__("∞"):
                definite = False

            ui.CodeInfoWindow(code=f"integrate({calculus.cleanExpr(func)}, "
                                   f"{(f'({itof}, {uBoundSrc}, {lBoundSrc})' if definite else f'Symbol({itof})')})",
                              labelTitleText=f"Code used for calculating "
                                             f"{'definite' if definite else 'indefinite'} integrals",
                              library="from sympy import *", dimensions="400x220")
            return None

        if recallingInteg:
            if forWhat.lower() == "calc":
                try:
                    toShow, integMsg = calculus.calculateIntegral(func, inTermsOf=itof,
                                                                  uBound=uBoundSrc, lBound=lBoundSrc)
                except Exception as e:
                    # Exceptions will be caught all the time because the program
                    # will try to integrate incomplete expressions
                    # print(f"An error happened, specifically:\n {e} \n\n Tried: {calculus.cleanExpr(func)}")
                    str(e)  # Removes a warning

                    # Indicates that the differential is being calculated
                    self.resultLabelInteg.configure(fg=ui.LIGHT_DARK_DECO_BG)

                    self.upperBoundLabelInteg.configure(fg=ui.LIGHT_DARK_DECO_BG)
                    self.lowerBoundLabelInteg.configure(fg=ui.LIGHT_DARK_DECO_BG)
                else:
                    if toShow is None:
                        self.resultLabelInteg.configure(fg=ui.LIGHT_DARK_DECO_BG)
                        self.upperBoundLabelInteg.configure(fg=ui.LIGHT_DARK_DECO_BG)
                        self.lowerBoundLabelInteg.configure(fg=ui.LIGHT_DARK_DECO_BG)
                    else:
                        self.upperBoundLabelInteg.configure(text=uBoundSrc, fg=ui.FG_LABELS)
                        self.lowerBoundLabelInteg.configure(text=lBoundSrc, fg=ui.FG_LABELS)
                        self.resultLabelInteg.configure(
                            text=f"{calculus.cleanExpr(func)} d{itof} = {calculus.cleanExpr(toShow)}",
                            fg=ui.FG_LABELS)

                        self.symbolLabelInteg.configure(width=round(len(self.resultLabelInteg["text"]) * 0.8))

            else:
                raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")

        if not recallingInteg:
            recallingInteg = True
            self.windowInteg.after(1, lambda: self.handleKeyEvent(event, forWhat, recallingInteg))
        else:
            recallingInteg = False


class Main:
    # Default content for the details label
    DETAILS_LABEL_CONTENT = "Welcome to the Advanced Scientific Calculator!\n\n" \
                            "Place the mouse pointer over any of the buttons to the left in order to see " \
                            "a description of what they do.\n\n" \
                            "This calculator is intended as a learning resource for some of the libraries that work" \
                            " with mathematical functions in python, and so in all of the parts there is a button" \
                            " that will allow you to see the code required to compute that specific mathematical" \
                            " operation."

    DETAILS_DELAY_MS = 100

    detailsLabel: tk.Label
    windowMain: tk.Tk

    @staticmethod
    def replaceDetails(classHovered, partialDiff=False) -> None:
        """
        Replaces the contents of the details label by the details of the class being received as a parameter
        :param classHovered: Class whose description is to be shown
        :param partialDiff: If classHovered is DifferentialCalculator, chooses which one of the descriptions (for
        partial derivative or for differential) is shown
        """

        text = ""
        try:
            text = classHovered.DETAILS_LABEL_CONTENT
        except AttributeError:
            try:
                if partialDiff:
                    text = classHovered.DETAILS_LABEL_CONTENT_PARTIALDIFF
                else:
                    text = classHovered.DETAILS_LABEL_CONTENT_NORMALDIFF
            except AttributeError as e:
                raise SyntaxError(f"Using invalid class '{classHovered}', use a valid one"
                                  f" (i.e. one that has the attribute DETAILS_LABEL_CONTENT)."
                                  f"\n\nCaught from: {e}")

        Main.windowMain.after(Main.DETAILS_DELAY_MS, lambda: Main.detailsLabel.configure(text=text))

    @staticmethod
    def generate() -> None:
        """
        Generates the program's main window
        """
        WIN_X = 540
        WIN_Y = 380

        Main.windowMain = tk.Tk()
        Main.windowMain.title("Main menu")
        Main.windowMain.geometry(f"{WIN_X}x{WIN_Y}")
        Main.windowMain.configure(bg=ui.WINDOW_BG)

        canvasMain = tk.Canvas(Main.windowMain, width=WIN_X, height=WIN_Y, bg=ui.WINDOW_BG)
        canvasMain.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        canvasMain.bind("<Enter>", lambda e: Main.replaceDetails(Main))

        # Line is just 1px under frame
        decoLineTopInfoMain = canvasMain.create_line((20, 69, 520, 69), fill=ui.DARK_DECO_BG)

        decoRectBtMain = canvasMain.create_rectangle((20, 89, 520, 360), outline=ui.LIGHT_DARK_DECO_BG)

        frameInfoMain = tk.Frame(canvasMain, width=WIN_X, height=70, bg=ui.WINDOW_BG)
        frameInfoMain.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        labelInfoMain = ui.TitleLabel(frameInfoMain, text="Choose what you want to do: ", relx=0.03, rely=0.5)

        # RIGHT SIDE:
        infoGroupMain = ui.OperationTypeGroup(canvasMain, name="Details", relx=0.41, rely=0.29)
        Main.detailsLabel = infoGroupMain.add_label(Main.DETAILS_LABEL_CONTENT, wraplength=275, justify=tk.LEFT)
        infoGroupMain.resize(relWidth=0.535, relHeight=0.607)

        # LEFT SIDE:
        graphGroup = ui.OperationTypeGroup(canvasMain, name="Graphing", relx=0.05, rely=0.29, anchor=None)
        btGraph2d = graphGroup.add_button("Draw 2D graph")
        btGraph2d.configure(command=lambda: Graph2D())
        btGraph2d.overrideEnterBinding(lambda: Main.replaceDetails(Graph2D))

        btGraph3d = graphGroup.add_button("Draw 3D graph")
        btGraph3d.configure(command=lambda: Graph3D())
        btGraph3d.overrideEnterBinding(lambda: Main.replaceDetails(Graph3D))

        derivateGroupMain = ui.OperationTypeGroup(canvasMain, name="Differentials", relx=0.05, rely=0.52)
        btDeriv = derivateGroupMain.add_button(text="Calculate derivative")
        btDeriv.configure(command=lambda: DifferentialCalculator())

        # This line has a warning, but it is controlled.
        btDeriv.overrideEnterBinding(lambda: Main.replaceDetails(DifferentialCalculator, False))

        btPartDeriv = derivateGroupMain.add_button(text="Calculate partial\nderivative", height=2)
        btPartDeriv.configure(command=lambda: DifferentialCalculator(partial=True))

        # This line has a warning, but it is controlled.
        btPartDeriv.overrideEnterBinding(lambda: Main.replaceDetails(DifferentialCalculator, True))

        integGroupMain = ui.OperationTypeGroup(canvasMain, name="Integrals", relx=0.05, rely=0.8)
        btInteg = integGroupMain.add_button(text="Calculate integral")
        btInteg.configure(command=lambda: IntegralCalculator())
        btInteg.overrideEnterBinding(lambda: Main.replaceDetails(IntegralCalculator))

        Main.windowMain.bind("<Escape>", lambda event: Main.windowMain.destroy())
        Main.windowMain.resizable(False, False)
        Main.windowMain.mainloop()


if __name__ == '__main__':
    Main.generate()
