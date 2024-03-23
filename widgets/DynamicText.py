from tkinter import Frame, Text

tags = {
        "pad": 3,
        "<h1>": 52,
        "<h2>": 36,
        "<h3>": 31,
        "<p>": 25,
        "<code>": 34,
        "ROOT": 1,
        }

class DynamicText(Text):
    def __init__(self, parent, **kwargs):
        self.frame = Frame(parent, height=60, background="red")
        self.frame.pack_propagate(False)
        super(DynamicText, self).__init__(self.frame, spacing1=10, spacing2=10, spacing3=10, **kwargs)
        self.frame.pack(fill="x", side="top")
        self.lastLines = 0

    def insert(self, *args, **kwargs):
        super(DynamicText, self).insert(*args, **kwargs)
        self.calculate_height(args[2][0])

    def calculate_height(self, type):
        lineCount = self.count("1.0", "end", "update", "displaylines")
        inserted = lineCount - self.lastLines
        self.lastLines = lineCount
        newHeight = self.frame.cget("height") + inserted * tags[type]
        spacing = 20 if type != "<code>" else -5
        self.frame.configure(height=newHeight + spacing)
