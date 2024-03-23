from tkinter import Frame, Text

tags = {
        "pad": 3,
        "<h1>": 52,
        "<h2>": 36,
        "<h3>": 31,
        "<p>": 25,
        "<code>": 26,
        "ROOT": 1,
        }

class DynamicText(Text):
    def __init__(self, parent, **kwargs):
        self.frame = Frame(parent, height=60, background="red")
        self.frame.pack_propagate(False)
        super(DynamicText, self).__init__(self.frame, spacing1=10, spacing2=10, **kwargs)
        self.frame.pack(fill="x", side="top")
        self.lastLines = 0

    def insert(self, *args, **kwargs):
        super(DynamicText, self).insert(*args, **kwargs)
        self.calculate_height(args[2][0])
        print(self.frame.cget("height"))

    def calculate_height(self, type):
        lineCount = self.count("1.0", "end", "update", "displaylines")
        inserted = lineCount - self.lastLines
        self.lastLines = lineCount
        newHeight = self.frame.cget("height") + inserted * tags[type]
        self.frame.configure(height=newHeight + 10)
