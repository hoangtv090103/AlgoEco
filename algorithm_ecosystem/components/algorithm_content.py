from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from components.algorithms import ALGORITHMS
import pandas as pd

class AlgorithmContent(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        if master.active_label.get() != "":
            self.label = Label(
                self,
                textvariable=master.active_label,
                bg="#6272a4",
                fg="#f8f8f2",
                font=("Verdana", 24),
            )
            self.label.grid(row=0, column=0, sticky="ew")
        self.buttons = []
        if master.selected_algorithm.get() != "":
            self.entry_algorithm(master.selected_algorithm.get())
        elif master.active_label.get() != "":
            self.load_algorithm_list()

    def load_algorithm_list(self):
        self.buttons = []
        for i, algorithm in enumerate(ALGORITHMS[self.master.active_label.get()]):
            self.buttons.append(
                ttk.Button(
                    master=self,
                    text=algorithm,
                    command=lambda algorithm=algorithm: self.entry_algorithm(algorithm),
                )
            )
            self.buttons[-1].grid(row=i + 1, column=0, sticky="ew", pady=5, padx=5)

    def entry_algorithm(self, algorithm):
        self.master.selected_algorithm.set(algorithm)
        self.clear_window()
        self.label = Label(
            self,
            textvariable=self.master.selected_algorithm,
            bg="#6272a4",
            fg="#f8f8f2",
            font=("Verdana", 24),
        )
        self.label.grid(row=0, column=0, sticky="we")
        back_button = ttk.Button(
            master=self,
            text="Back",
            command=lambda: self._on_click_back(),
        )
        upload_dataset_button = ttk.Button(
            master=self,
            text="Upload Dataset",
            command=lambda: self._on_click_upload_dataset(),
        )

        self.buttons.append(upload_dataset_button)
        self.buttons[-1].grid(row=1, column=0, sticky="ew")

        self.buttons.append(back_button)
        self.buttons[-1].grid(row=2, column=0, sticky="ew")

    def _on_click_back(self):
        self.master.selected_algorithm.set("")
        self.clear_window()
        self.label = Label(
            self,
            textvariable=self.master.active_label,
            bg="#6272a4",
            fg="#f8f8f2",
            font=("Verdana", 24),
        )
        self.label.grid(row=0, column=0, sticky="ew")
        self.load_algorithm_list()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _on_click_upload_dataset(self):
        file_types = [("CSV Files", "*.csv")]
        file_path = filedialog.askopenfilename(filetypes=file_types)

        # Read file
        with open(file_path, "r") as f:
            dataset = pd.read_csv(f)

        self.buttons.insert(
            1,
            ttk.Button(
                master=self,
                text="Run Algorithm",
                command=lambda: self.run_algorithm(dataset),
            ),
        )
        self.buttons[1].grid(row=1, column=0, sticky="ew", pady=5, padx=5)

    def run_algorithm(self, dataset):
        try:
            algorithm = (
                self.master.selected_algorithm.get()
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )
            module = __import__("algorithms." + algorithm, fromlist=[algorithm])
            module.run(dataset, 3)
        except Exception as e:
            if e.__class__.__name__ == "ModuleNotFoundError":
                self.label = Label(
                    self,
                    text="%s algorithm is not implemented yet"
                    % self.master.selected_algorithm.get(),
                    bg="#6272a4",
                    fg="#f8f8f2",
                    font=("Verdana", 24),
                )
                self.label.grid(row=3, column=0, sticky="we")