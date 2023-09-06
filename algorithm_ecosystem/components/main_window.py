from tkinter import Tk, StringVar
from tkinter import ttk

from components.sidebar import Sidebar
from components.algorithm_content import AlgorithmContent

class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        style = ttk.Style()
        style.configure(
            "AlgoEco.TButton",
            background="white",
            foreground="black",
            font=("Verdana", 20),
            padding=10,
        )
        style.map(
            "AlgoEco.TButton",
            background=[("active", "#282a36")],
            foreground=[("active", "#f8f8f2")],
        )

        self.title("Algorithm Ecosystem")
        self.geometry("800x600")

        self.active_label = StringVar()
        self.active_label.set("")

        self.selected_algorithm = StringVar()
        self.selected_algorithm.set("")

        # Create sidebar
        self.sidebar = Sidebar(self, background="#282a36")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Create algorithm window
        self.algorithm_content = AlgorithmContent(self)
        self.algorithm_content.grid(row=0, column=1, sticky="nsew")
        self.algorithm_content.grid_columnconfigure(0, weight=1)