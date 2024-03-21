from tkinter import Text

tags = {
        "pad": 4,
        "<h1>": 3,
        "<h2>": 3,
        "<h3>": 2,
        "<p>": 1,
        "<code>": 2,
        "ROOT": 1,
        }

class DynamicText(Text):
    def __init__(self, parent, **kwargs):
        super(DynamicText, self).__init__(parent, **kwargs)
        self.lastLines = 0

    def insert(self, *args, **kwargs):
        super(DynamicText, self).insert(*args, **kwargs)
        self.calculate_height(args[2][0])

    def calculate_height(self, type):
        lineCount = self.count("1.0", "end", "update", "displaylines")
        inserted = lineCount - self.lastLines
        self.lastLines = lineCount
        newHeight = self.cget("height") + inserted * tags[type]
        self.configure(height=newHeight)
