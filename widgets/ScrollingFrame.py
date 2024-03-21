from tkinter import Canvas, Frame, Scrollbar

class ScrollingFrame(Frame):
    def __init__(self, parent, **kwargs):
        outerFrame = Frame(parent)
        outerFrame.pack(fill="both", expand=1)

        self.canvas = Canvas(outerFrame)
        self.canvas.pack(side="left", fill="both", expand=1)

        vBar = Scrollbar(outerFrame, command=self.canvas.yview)
        vBar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=vBar.set)

        super(ScrollingFrame, self).__init__(self.canvas, **kwargs)
        self.win = self.canvas.create_window((0, 0), window=self, anchor="nw")

        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.bind("<Configure>", lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
    def onCanvasConfigure(self, event):
        self.canvas.itemconfigure(self.win, width=event.width)

