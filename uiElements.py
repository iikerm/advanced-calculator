import tkinter as tk
from tkinter import colorchooser

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


def calculateForegroundColor(masterButton: tk.Button, hue: str) -> str:
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

        self.configure(fg=calculateForegroundColor(self, bg))
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
            self.configure(bg=self.hue, fg=calculateForegroundColor(self, self.hue))
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
