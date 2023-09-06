from tkinter import *
from tkinter import ttk
from components.algorithms import ALGORITHMS
from components.algorithm_content import AlgorithmContent

class Sidebar(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.sidebar = Frame(self, width=200, background="#282a36")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        label = Label(
            self.sidebar,
            text="Algorithm Ecosystem",
            bg="#282a36",
            fg="#f8f8f2",
            font=("Verdana", 24),
        )
        label.grid(row=0, column=0, sticky="ew", pady=10)
        active_label = StringVar()
        self.buttons = []
        for i, category in enumerate(ALGORITHMS):
            self.buttons.append(
                ttk.Button(
                    master=self.sidebar,
                    text=category,
                    command=lambda category=category: self._on_click(category),
                    style="AlgoEco.TButton",
                )
            )
            self.buttons[-1].grid(row=i + 1, column=0, sticky="ew")

    def _on_click(self, category):
        self.master.active_label.set(category)
        self.master.selected_algorithm.set("")
        self.update_algorithm_window()

    def update_algorithm_window(self):
        self.master.algorithm_content.destroy()  # destroy current frame
        self.master.algorithm_content = AlgorithmContent(self.master)
        self.master.algorithm_content.grid(row=0, column=1, sticky="nsew")
