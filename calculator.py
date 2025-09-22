import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox

#  ⬇   M Y   O W N   M O D U L E S   ⬇
import graphing
import calculus

# Fonts and colors
TITLE_FONT = ("Calibri", 14)

WINDOW_BG = "#bacaca"
LIGHT_WINDOW_BG = "#cbdbdb"
DARK_DECO_BG = "#546464"
LIGHT_DARK_DECO_BG = "#98a8a8"

BG_ENTRY_LOW_ACTIVE = "#546464"
BG_ENTRY_LOW_DISABLED = "#a9b9b9"
BG_BT_HIGHLIGHT = "#a9b9b9"

FG_DECO_TITLES = "#546464"
FG_LABELS = "#0c0c0c"
FG_ENTRIES = "#000000"


def GEN_CODE_FONT(size=13) -> (str, int):
    """
    Generates a font tuple in tkinter format. The font family of the created font is Cascadia Mono
    (which acts as a code-editor-like font)
    :param size: size of the font to be created
    :return: a tuple (str, int) that represents a font
    """
    fnt = ("Cascadia Mono", size)
    return fnt


def calcFg(masterButton: tk.Button, hue: str) -> str:
    """
    Calculates foreground color based on the received background color so that the text is readable in a button.
    This function is used in the color selecting buttons.
    :param masterButton: used for keeping track of the last foreground color
    :param hue: background color
    :return: The calculated foreground color for better text visibility
    """
    if hue == "None":
        return masterButton['fg']

    fg = "#000000"

    hue = hue.replace("#", "")
    red = int(hue[0]+hue[1], 16)
    green = int(hue[2]+hue[3], 16)
    blue = int(hue[4]+hue[5], 16)

    avg = int((red + green + blue)/3)
    if avg < 255//2:        # Background is mostly dark, so a clear fg is better
        fg = "#ffffff"
    return fg

class DefaultButton(tk.Button):
    """
    Custom button class that only uses some of the attributes from the original tk.Button class.
    It is used to define custom behaviour such as custom highlight when the cursor hovers over it.
    """
    def __init__(self,
                 master: tk.Tk | tk.Frame | tk.Canvas,
                 text: str,
                 width=20,
                 height=1,
                 justify=tk.CENTER,
                 bg=LIGHT_DARK_DECO_BG,
                 activebackground=LIGHT_DARK_DECO_BG):

        super().__init__(master, text=text, bg=bg, width=width, height=height,
                                activebackground=activebackground, bd=0, justify=justify)

        self.master = master
        self.bind("<Enter>", lambda event: self.configure(background=BG_BT_HIGHLIGHT))
        self.bind("<Leave>", lambda event: self.configure(background=LIGHT_DARK_DECO_BG))

    def placeBt(self, relx: float, rely: float, anchor=None):
        self.place(relx=relx, rely=rely, anchor=anchor)

    def gridBt(self, row: int, column: int, sticky=None, padx=0, pady=0):
        self.grid(row=row, column=column, sticky=sticky, pady=pady, padx=padx)

class CodeInfoWindow:
    """
    Custom window used for displaying the python code used for performing the current operation
    """
    def __init__(self,
                 code: str,
                 labelTitleText: str="",
                 title: str="Expression used",
                 library: str="",
                 title_font=TITLE_FONT,
                 code_font=GEN_CODE_FONT(10),
                 bg: str=WINDOW_BG,
                 light_bg: str=LIGHT_WINDOW_BG,
                 dimensions: str="300x200"):

        self.title = title

        self.win = tk.Tk()
        self.win.focus_force()
        self.win.geometry(dimensions)
        self.win.title(self.title)
        self.win.configure(background=bg)

        self.x = int(dimensions.split("x")[0])
        self.y = int(dimensions.split("x")[1])

        self.titleLabel = TitleLabel(self.win, text=labelTitleText, font=title_font, relx=0.1, rely=0.1)

        self.codeText = tk.Text(self.win, width=round(32*self.x/300), height=round(7*self.y/200), bd=0, bg=light_bg, font=code_font, wrap=tk.WORD)
        self.codeText.place(relx=0.1, rely=0.3)

        self.codeText.insert(tk.END, library+"\n\n")
        self.codeText.insert(tk.END, code)

        self.codeText.configure(state="disabled")

        self.btOk = DefaultButton(master=self.win, text="Ok", width=5, bg=bg)
        self.btOk.placeBt(relx=0.81, rely=0.77)
        self.btOk.configure(command=lambda: self.destroyWin())

        self.win.bind("<Escape>", lambda e: self.destroyWin())
        self.win.mainloop()

    def destroyWin(self) -> None:
        self.win.destroy()

class ColorButton(tk.Button):
    """
    Custom button class used to represent a specific color and is intended to be used as a color picker.
    """
    def __init__(self,
                 master: tk.Tk | tk.Frame | tk.Canvas,
                 text: str,
                 width=20,
                 height=1,
                 bg="#0000ff",
                 bd=0):

        super().__init__(master, text=text, width=width, height=height, bg=bg, activebackground=bg, bd=bd,
                                command=self.selectOwnColor)

        self.configure(fg=calcFg(self, bg))
        self.master = master
        self.hue = bg

        self.bind("<Enter>", lambda e: self.configure(text=self['bg']))
        self.bind("<Leave>", lambda e: self.configure(text=""))

    def selectOwnColor(self) -> None:
        """
        Function that is called when a ColorButton is pressed. It opens a tkinter colorchooser window with this
        ColorButton's color pre-selected in said window
        """
        tempHue = str(colorchooser.askcolor(self.hue)[1])
        if tempHue != "None":      # colorpicker returns "None" when the user closes the window without choosing a color
            self.hue = tempHue
            self.configure(bg=self.hue, fg=calcFg(self, self.hue))
        self.master.focus_force()

class TitleLabel(tk.Label):
    """
    Special type of label that is intended for use as a title label.
    It is used instead of a normal tk.Label with future extensions in mind.
    """
    def __init__(self,
                 master: tk.Tk | tk.Frame | tk.Canvas,
                 text: str,
                 relx: float,
                 rely: float,
                 font=TITLE_FONT,
                 bg=WINDOW_BG,
                 anchor=None):

        super().__init__(master, text=text, font=font, bg=bg)

        self.master = master
        self.text = text
        self.font = font
        self.bg = bg

        self.place(relx=relx, rely=rely, anchor=anchor)

class UnderlinedEntry(tk.Entry):
    """
    tk.Entry subclass that is used to define custom behaviours like an underline that
    changes color with focus for example.
    """

    def __init__(self,
                 master: tk.Tk | tk.Frame | tk.Canvas,
                 width: int,
                 sticky,
                 placeholder=""):

        self.entryFrame = tk.Frame(master)
        self.entryFrame.grid(row=0, column=0)
        super().__init__(self.entryFrame, bg=WINDOW_BG, fg=FG_LABELS, bd=0, width=width)

        self.master = master
        self.width = width
        self.sticky = sticky
        self.placeholder = placeholder

        # self.entry_obj = tk.Entry(self.entryFrame, bg=WINDOW_BG, fg=FG_LABELS, bd=0, width=self.width)
        if self.placeholder != "":
            self.configure(fg=LIGHT_DARK_DECO_BG)
            self.insert(0, self.placeholder)

        self.grid(row=0, column=0)

        self.entryLowBorder = tk.Frame(self.entryFrame, width=width * 6 + 2, height=2, bg=BG_ENTRY_LOW_DISABLED)
        self.entryLowBorder.grid(row=1, column=0, sticky=tk.N)

        self.bind("<FocusIn>", lambda event: self.manageFocus(True))
        self.bind("<FocusOut>", lambda event: self.manageFocus(False))


    def manageFocus(self, focusIn: bool) -> None:
        """
        Method that manages the removal and insertion of the entry's placeholder
        when it gains and loses focus respectively
        :param focusIn: True if the entry has gained focus, false otherwise
        """
        if focusIn:
            if self.get() == self.placeholder:
                self.delete('0', 'end')
                self.configure(fg=FG_ENTRIES)
            self.entryLowBorder.configure(bg=BG_ENTRY_LOW_ACTIVE)   # Needed so that the lower border still 'lights up'

        else:
            if self.get() == "":
                self.insert(0, self.placeholder)
                self.configure(fg=LIGHT_DARK_DECO_BG)
            else:
                self.configure(fg=FG_ENTRIES)
            self.entryLowBorder.configure(bg=BG_ENTRY_LOW_DISABLED)

    def setGrid(self, row: int, column: int) -> None:
        """
        Places the whole entry inside its master widget. The inherited .grid() method should not be used
        because this class contains other elements instead of just the parent entry (which would be the one affected
        by said method), so this method moves the frame containing the entire structure.
        """
        # frameRow = self.entry_obj.grid_info()['row'] + 1
        # frameCol = self.entry_obj.grid_info()['column']
        self.entryFrame.grid_configure(row=row, column=column, pady=2)

    def resetEntry(self) -> None:
        """
        Resets the contents of an UnderlinedEntry to the placeholder value (or makes it empty if it has no placeholder)
        :return: None
        """
        self.delete('0', 'end')
        self.insert(0, self.placeholder)
        self.configure(fg=LIGHT_DARK_DECO_BG)

    @staticmethod
    def resetEntries(*args) -> None:
        """
        Resets the specified UnderlinedEntry objects
        :param args: entries to reset
        :return: None
        """
        for i in range(0, len(args)):
            try:
                args[i].resetEntry()
            except AttributeError:
                raise SyntaxError(f"Tried to reset an object of type {type(args[i])}, "
                                  f"expected one of type 'UnderlinedEntry'")

class OperationTypeGroup:
    """
    A special kind of container that is intended to group buttons, labels and other widgets with
    similar contexts together in a visual block.
    """
    def __init__(self,
                 master: tk.Tk | tk.Frame | tk.Canvas,
                 relx: float,
                 rely: float,
                 anchor=None,
                 name=""):

        self.groupButtons = []
        self.groupLabels = []
        self.groupEntries = []

        self.groupAll = []

        self.master = master
        self.name = name
        self.relx = relx
        self.rely = rely
        self.anchor = anchor

        self.masterFrame = tk.Frame(self.master, bg=LIGHT_DARK_DECO_BG, padx=1, pady=1)
        self.masterFrame.place(relx=self.relx, rely=self.rely)
        if anchor is not None:
            self.masterFrame.place_configure(anchor=anchor)

        self.frame_obj = tk.Frame(self.masterFrame, bg=WINDOW_BG, padx=5, pady=5)
        self.frame_obj.grid(row=0, column=0)

        if self.name != "":
            self.titleLabel = tk.Label(self.master, text=name, bg=WINDOW_BG, fg=FG_DECO_TITLES)
            self.titleLabel.place(relx=self.relx+0.03, rely=self.rely-0.038)

    def add_button(self, text:str, width=20, height=1, bg=LIGHT_DARK_DECO_BG, justify=tk.CENTER, typ="normal") -> tk.Button:
        """
        Method that adds a DefaultButton or a ColorButton to the current group
        :param text: Button text
        :param width: Button width
        :param height: Button height
        :param bg: Button background color (only for DefaultButton)
        :param justify: Text justification in the button (only for DefaultButton)
        :param typ: "Normal" for a DefaultButton to be added, or "Color" for a ColorButton
        :return: A button of the selected type, added to the operation group
        """
        if width == 0:
            width = None

        if typ.lower() == "normal":
            tempButton = DefaultButton(self.frame_obj, text=text, height=height, width=width, bg=bg, activebackground=LIGHT_DARK_DECO_BG, justify=justify)

            self.groupButtons.append(tempButton)
            self.groupAll.append(tempButton)

            tempButton.gridBt(row=self.groupAll.index(tempButton), column=0, pady=2)

        elif typ.lower() == "color":
            tempButton = ColorButton(self.frame_obj, text=text)

            self.groupButtons.append(tempButton)
            self.groupAll.append(tempButton)

            tempButton.grid(row=self.groupAll.index(tempButton), column=0, pady=2)
        else:
            raise Exception(f"Invalid button type: {typ}, must be either 'Normal' or 'Color'")

        return tempButton


    def add_label(self, text:str, anchor=None) -> tk.Label:
        """
        Method that adds a tk.Label to the current group
        :param text: Text in the label
        :param anchor: Label's anchor value
        :return: The label that was added to the group
        """
        tempLabel = tk.Label(self.frame_obj, text=text, bg=WINDOW_BG, fg=FG_LABELS, anchor=anchor)

        self.groupLabels.append(tempLabel)
        self.groupAll.append(tempLabel)

        tempLabel.grid(row=self.groupAll.index(tempLabel), column=0, pady=2, sticky=tk.W)

        return tempLabel

    def add_entry(self, width=20, row=None, column=0, placeholder="") -> UnderlinedEntry:
        """
        Method that adds an UnderlinedEntry to the current group
        :param width: Entry width
        :param row: Entry grid row
        :param column: Entry grid row
        :param placeholder: Text that will appear in the entry when it has no focus and nothing already written
        :return: UnderlinedEntry that was added to the group
        """

        tempEntry = UnderlinedEntry(self.frame_obj, width, None, placeholder=placeholder)

        self.groupEntries.append(tempEntry)
        self.groupAll.append(tempEntry)
        if row is None:
            row = self.groupAll.index(tempEntry)

        tempEntry.setGrid(row=row, column=column)

        return tempEntry



def graph2dWindow() -> None:
    """
    Function that generates a window for introducing parameters to generate a representation of a 2D graph from a
    mathematical function.
    """
    def generate2dGraph(master: tk.Tk, params: list, forWhat="graph") -> None:
        """
        Reads a specific set of parameters in order to generate the graph
        :param master: tk.Tk object that contains the button that called this function.
        :param params: a list containing 3 OperationTypeGroups: [graph, color, range]. The graph group contains
        things like the function to represent, the variable it is in terms of etc., the color group contains the color
        and the range group contains information about the range of the function that will be drawn.
        :param forWhat: Indicates if this function should create a CodeInfoWindow ("code") or if it should
        generate a graph ("graph")
        """
        dataList = []

        for group in params:
            for widget in group.groupAll:
                if type(widget) == UnderlinedEntry:
                    dataList.append(widget.get())
                elif type(widget) == ColorButton:
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
                master.after(1, lambda: graphing.showGraph2d(graph))
                master.after(1000, lambda: master.title("Enter graphing parameters"))

        elif forWhat == "code":
            CodeInfoWindow(code=f"plot({dataList[0]}, (inTermsOf={dataList[1]}, visionRangeMin={dataList[3]}, "
                               f"visionRangeMax={dataList[4]}), line_color={dataList[2]})",
                           labelTitleText="Code used for 2D graph", library="from sympy.plotting import plot")
        else:
            raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")


    window2d = tk.Tk()
    window2d.geometry("460x320")
    window2d.title("Enter graphing parameters")
    window2d.configure(bg=WINDOW_BG)
    window2d.focus_force()

    labelTitle2d = TitleLabel(window2d, text="Preparing the 2D graph:", relx=0.15, rely=0.1)

    graph2dGroup = OperationTypeGroup(window2d, name="Enter parameters: ", relx=0.15, rely=0.3)
    funcLabel = graph2dGroup.add_label("Function:")
    funcEntry = graph2dGroup.add_entry(width=20, row=1)

    spaceLabel = graph2dGroup.add_label("       ")

    tofLabel = graph2dGroup.add_label("In terms of:")
    tofEntry = graph2dGroup.add_entry(width=5, placeholder="x")
    tofEntry.entryFrame.grid_configure(sticky=tk.W)

    color2dGroup = OperationTypeGroup(window2d, name="Select color: ", relx=0.5, rely=0.3)
    colLabel = color2dGroup.add_label("Click me  ⬇")
    colButton = color2dGroup.add_button(text="", bg="blue", typ="color")

    vis2dGroup = OperationTypeGroup(window2d, name="Visibility of the function: ", relx=0.5, rely=0.6)
    visFromEntry = vis2dGroup.add_entry(placeholder="from", width=5)
    visSpaceLabel = vis2dGroup.add_label("                         ")
    visSpaceLabel.grid_configure(row=0, column=1)
    visToEntry = vis2dGroup.add_entry(placeholder="to", width=5, column=2, row=0)

    button2dOk = DefaultButton(window2d, text="Draw function", width=0)     # width 0 is default
    button2dOk.configure(command=lambda: generate2dGraph(window2d, [graph2dGroup, color2dGroup, vis2dGroup]))
    button2dOk.placeBt(relx=0.66, rely=0.8)

    button2dCode = DefaultButton(window2d, text="See code", width=0)     # width 0 is default
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
        :param params: A list containing 2 OperationTypeGroup objects in this order [graph, range]
        :param forWhat: Indicates if this function should create a CodeInfoWindow ("code") or if it should
        generate a graph ("graph")
        :return:
        """
        dataList = []

        for group in params:
            for widget in group.groupAll:
                if type(widget) == UnderlinedEntry:
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
            CodeInfoWindow(code=f"plot3d({dataList[0]}, (inTermsOfX={dataList[1]}, visionRangeMinX={dataList[3]}, "
                               f"visionRangeMaxX={dataList[4]}), "
                               f"(inTermsOfY={dataList[2]}, visionRangeMinY={dataList[5]}, "
                               f"visionRangeMaxY={dataList[6]}))",
                           labelTitleText="Code used for 3D graph", library="from sympy.plotting import plot3d")

        else:
            raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")

    window3d = tk.Tk()
    window3d.geometry("460x320")
    window3d.title("Building a 3D graph (sympy)")
    window3d.configure(bg=WINDOW_BG)
    window3d.focus_force()

    labelTitle3d = TitleLabel(window3d, text="Preparing the 3D graph:", relx=0.1, rely=0.1)

    graph3dGroup = OperationTypeGroup(window3d, name="Enter parameters: ", relx=0.1, rely=0.3)
    funcLabel = graph3dGroup.add_label("Function:")
    funcEntry = graph3dGroup.add_entry(width=20, row=1)

    spaceLabel = graph3dGroup.add_label("       ")

    tofLabel = graph3dGroup.add_label("In terms of:")
    tofXEntry = graph3dGroup.add_entry(width=5, placeholder="x")
    tofXEntry.entryFrame.grid_configure(sticky=tk.W)

    tofYEntry = graph3dGroup.add_entry(width=5, placeholder="y")
    tofYEntry.entryFrame.grid_configure(sticky=tk.W)

    vis3dGroup = OperationTypeGroup(window3d, name="Visibility of the function: ", relx=0.45, rely=0.3)
    vis3dInfoLabelX = vis3dGroup.add_label(text="For first variable (x)")
    visFromEntryX = vis3dGroup.add_entry(placeholder="from", width=5)
    visSpaceLabelX = vis3dGroup.add_label("           ")
    visSpaceLabelX.grid_configure(row=0, column=1)
    visToEntryX = vis3dGroup.add_entry(placeholder="to", width=5, column=2, row=1)

    vis3dInfoLabelY = vis3dGroup.add_label(text="For second variable (y)")
    visFromEntryY = vis3dGroup.add_entry(placeholder="from", width=5)
    visToEntryY = vis3dGroup.add_entry(placeholder="to", width=5, column=2, row=5)

    button3dOk = DefaultButton(window3d, text="Draw function", width=0)
    button3dOk.configure(command=lambda: generate3dGraph(window3d, [graph3dGroup, vis3dGroup]))
    button3dOk.placeBt(relx=0.72, rely=0.72)

    button3dCode = DefaultButton(window3d, text="See code", width=0)  # width 0 is default
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
            CodeInfoWindow(code=f"diff({calculus.cleanExpr(func)}{f', {itof}' if partial else ''})",
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
                    resultLabel.configure(fg=LIGHT_DARK_DECO_BG)     # Indicates that the differential is being calculated
                else:
                    baseText = resultLabel["text"][:resultLabel["text"].index("=") + 2]

                    baseText = baseText[:insertPosAnsText] + itof + baseText[baseText.index(" "):]
                    resultLabel.configure(text=baseText + calculus.cleanExpr(toShow), fg=FG_LABELS)
            else:
                raise SyntaxError(f"Invalid 'forWhat' given: {forWhat},\nExpected 'calc' or 'code'")

        else:
            recallingDiff = True
            windowDiff.after(1, lambda: diffHandleKeyEvent(entryList, labelList, event, forWhat, recallingDiff))


    windowDiff = tk.Tk()
    windowDiff.geometry("460x320")
    windowDiff.configure(background=WINDOW_BG)
    windowDiff.title(f"Calculating a{' partial 'if partial else ' '}derivative (sympy)")
    windowDiff.focus_force()

    labelTitleDiff = TitleLabel(windowDiff, text="Preparing the differential: ", relx=0.1, rely=0.1)

    paramsGroupDiff = OperationTypeGroup(windowDiff, name="Enter parameters: ", relx=0.1, rely=0.3)
    resultLabelDiff = tk.Label(windowDiff, bg=LIGHT_WINDOW_BG, fg=FG_LABELS, font=GEN_CODE_FONT(), text="", pady=10,
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

    codeButtonDiff = DefaultButton(windowDiff, text="See code", width=0)  # width 0 is default
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

            CodeInfoWindow(code=f"integrate({calculus.cleanExpr(func)}, {(f'({itof}, {uBoundSrc}, {lBoundSrc})' if definite else f'Symbol({itof})')})",
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

                    rLabel.configure(fg=LIGHT_DARK_DECO_BG)     # Indicates that the differential is being calculated
                    uBoundLabel.configure(fg=LIGHT_DARK_DECO_BG)
                    lBoundLabel.configure(fg=LIGHT_DARK_DECO_BG)
                else:
                    if toShow is None:
                        rLabel.configure(fg=LIGHT_DARK_DECO_BG)
                        uBoundLabel.configure(fg=LIGHT_DARK_DECO_BG)
                        lBoundLabel.configure(fg=LIGHT_DARK_DECO_BG)
                    else:
                        uBoundLabel.configure(text=uBoundSrc, fg=FG_LABELS)
                        lBoundLabel.configure(text=lBoundSrc, fg=FG_LABELS)
                        rLabel.configure(
                            text=f"{calculus.cleanExpr(func)} d{itof} "
                                 f"= {calculus.cleanExpr(toShow)}",
                            fg=FG_LABELS)

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
    windowInteg.configure(background=WINDOW_BG)
    windowInteg.title(f"Calculating an integral (sympy)")
    windowInteg.focus_force()

    labelTitleInteg = TitleLabel(windowInteg, text="Preparing the integral", relx=0.15, rely=0.1)

    paramsGroupInteg = OperationTypeGroup(windowInteg, relx=0.15, rely=0.3, name="Parameters")


    resultGroupX = 0.152
    resultGroupY = 0.73
    symbolLabelInteg = tk.Label(windowInteg, bg=LIGHT_WINDOW_BG, fg=FG_LABELS, font=GEN_CODE_FONT(30), text="∫", pady=10,
                                padx=15, width=10, anchor=tk.W)
    symbolLabelInteg.place(relx=resultGroupX, rely=resultGroupY)

    resultLabelInteg = tk.Label(windowInteg, bg=LIGHT_WINDOW_BG, fg=FG_LABELS, font=GEN_CODE_FONT(), text="", pady=0, padx=10)
    resultLabelInteg.place(relx=resultGroupX+0.11, rely=resultGroupY+0.08)

    upperBoundLabelInteg = tk.Label(windowInteg, bg=LIGHT_WINDOW_BG, fg=FG_LABELS, font=GEN_CODE_FONT(12), text="")
    upperBoundLabelInteg.place(relx=resultGroupX+0.08, rely=resultGroupY+0.03)

    lowerBoundLabelInteg = tk.Label(windowInteg, bg=LIGHT_WINDOW_BG, fg=FG_LABELS, font=GEN_CODE_FONT(12), text="")
    lowerBoundLabelInteg.place(relx=resultGroupX+0.08, rely=resultGroupY+0.14)


    buttonIntegCode = DefaultButton(windowInteg, text="See code", width=0)  # width 0 means default width
    buttonIntegCode.placeBt(relx=0.70, rely=0.62)
    buttonIntegCode.configure(command=lambda: integHandleKeyEvent([funcEntryInteg, itofEntryInteg,
                                                          uBoundEntryInteg, lBoundEntryInteg],
                                                         [resultLabelInteg, upperBoundLabelInteg, lowerBoundLabelInteg],
                                                          forWhat="code"))

    buttonClearAllInteg = DefaultButton(windowInteg, text="Clear all", width=0)  # width 0 means default width
    buttonClearAllInteg.placeBt(relx=0.45, rely=0.62)
    buttonClearAllInteg.configure(command=lambda: UnderlinedEntry.resetEntries(funcEntryInteg, uBoundEntryInteg,
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


    boundsGroupInteg = OperationTypeGroup(windowInteg, relx=0.45, rely=0.3, name="Bounds")

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
    windowMain.configure(bg=WINDOW_BG)

    canvasMain = tk.Canvas(windowMain, width=640, height=380, bg=WINDOW_BG)
    canvasMain.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    decoLineTopInfoMain = canvasMain.create_line((20, 69, 620, 69), fill=DARK_DECO_BG)  # Line is just 1px under frame ✔
    decoRectBtMain = canvasMain.create_rectangle((20, 89, 620, 360), outline=LIGHT_DARK_DECO_BG)

    frameInfoMain = tk.Frame(canvasMain, width=640, height=70, bg=WINDOW_BG)
    frameInfoMain.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    labelInfoMain = TitleLabel(frameInfoMain, text="Choose what you want to do: ", relx=0.03, rely=0.5)

    graphGroup = OperationTypeGroup(canvasMain, name="Graphing", relx=0.05, rely=0.29, anchor=None)
    btGraph2d = graphGroup.add_button("Draw 2D graph")
    btGraph2d.configure(command=graph2dWindow)

    btGraph3d = graphGroup.add_button("Draw 3D graph")
    btGraph3d.configure(command=graph3dWindow)

    derivateGroupMain = OperationTypeGroup(canvasMain, name="Differentials", relx=0.05, rely=0.52)
    btDeriv = derivateGroupMain.add_button(text="Calculate derivative")
    btDeriv.configure(command=diffWindow)

    btPartDeriv = derivateGroupMain.add_button(text="Calculate partial\nderivative", height=2)
    btPartDeriv.configure(command=lambda: diffWindow(partial=True))

    integGroupMain = OperationTypeGroup(canvasMain, name="Integrals", relx=0.05, rely=0.8)
    btInteg = integGroupMain.add_button(text="Calculate integral")
    btInteg.configure(command=integWindow)

    windowMain.bind("<Escape>", lambda event: windowMain.destroy())
    windowMain.resizable(False, False)
    windowMain.mainloop()

generateMain()
