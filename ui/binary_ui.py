import ttkbootstrap as ttk
import random
import threading
from tkinter import Label
from logic.binary import BinarySearchLogic
from theme import (
    FONT_TITLE, FONT_SUBTITLE, FONT_HEADING, FONT_BODY, FONT_CELL,
    COLOR_PANEL, COLOR_TEXT, COLOR_MUTED, COLOR_ACCENT,
    CELL_DEFAULT, CELL_TEXT_DEFAULT, CELL_ACTIVE, CELL_ACTIVE_TEXT,
    CELL_DONE, CELL_DONE_TEXT, CELL_ELIMINATED, CELL_ELIMINATED_TEXT,
)


class Binary_ui(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.logic = BinarySearchLogic(delay=0.6)
        self.arr = sorted(random.sample(range(1, 100), 10))
        self.target = None
        self.label_widgets = []
        self.create_widgets()

    def create_widgets(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        ttk.Button(header, text="← Back", bootstyle="secondary-outline",
                   command=self.back_button).pack(side="left")
        ttk.Label(header, text="Binary Search", font=FONT_TITLE,
                  foreground=COLOR_ACCENT).pack(side="left", padx=20)

        ttk.Label(self, text="Enter a target value and watch the search narrow down the range.",
                  font=FONT_SUBTITLE, foreground=COLOR_MUTED).pack(anchor="w", pady=(0, 20))

        controls = ttk.Frame(self)
        controls.pack(fill="x", pady=(0, 20))

        ttk.Label(controls, text="Target:", font=FONT_BODY,
                  foreground=COLOR_TEXT).pack(side="left", padx=(0, 8))
        self.target_entry = ttk.Entry(controls, width=10, font=FONT_BODY)
        self.target_entry.pack(side="left", padx=(0, 12))
        self.target_entry.bind("<Return>", lambda e: self.start_visualization())

        ttk.Button(controls, text="Start Search", bootstyle="primary",
                   command=self.start_visualization).pack(side="left", padx=(0, 8))
        ttk.Button(controls, text="Reset", bootstyle="secondary-outline",
                   command=self.reset).pack(side="left")

        self.status_label = ttk.Label(self, text="Ready", font=FONT_HEADING,
                                      foreground=COLOR_MUTED)
        self.status_label.pack(pady=(10, 10))

        card = ttk.Frame(self, style="Card.TFrame", padding=20)
        card.pack(fill="x", pady=(10, 20))

        self.container = ttk.Frame(card, style="Card.TFrame")
        self.container.pack(expand=True)

        for num in self.arr:
            lbl = Label(self.container, text=str(num), width=4, height=2,
                        relief="flat", font=FONT_CELL,
                        bg=CELL_DEFAULT, fg=CELL_TEXT_DEFAULT, bd=0)
            lbl.pack(side="left", padx=6)
            self.label_widgets.append(lbl)

        legend = ttk.Frame(self)
        legend.pack(fill="x")
        self._legend_item(legend, CELL_ACTIVE, "Midpoint")
        self._legend_item(legend, CELL_ELIMINATED, "Eliminated")
        self._legend_item(legend, CELL_DONE, "Found")

    def _legend_item(self, parent, color, text):
        item = ttk.Frame(parent)
        item.pack(side="left", padx=(0, 20))
        swatch = Label(item, text="  ", bg=color, width=2, height=1, bd=0)
        swatch.pack(side="left", padx=(0, 6))
        ttk.Label(item, text=text, font=FONT_BODY,
                  foreground=COLOR_MUTED).pack(side="left")

    def _set_cell(self, idx, bg, fg):
        self.label_widgets[idx].config(bg=bg, fg=fg)

    def ui_callback(self, index, state):
        if state == "reset":
            for i, lbl in enumerate(self.label_widgets):
                current_bg = lbl.cget("bg")
                if current_bg not in (CELL_DONE, CELL_ELIMINATED):
                    self._set_cell(i, CELL_DEFAULT, CELL_TEXT_DEFAULT)

        elif state == "highlight":
            self.status_label.configure(text=f"Checking index {index} (value {self.arr[index]})")
            self._set_cell(index, CELL_ACTIVE, CELL_ACTIVE_TEXT)

        elif state == "found":
            self._set_cell(index, CELL_DONE, CELL_DONE_TEXT)
            self.status_label.configure(text=f"Found {self.target} at index {index}")

        elif state == "left_red":
            for i in range(0, index + 1):
                self._set_cell(i, CELL_ELIMINATED, CELL_ELIMINATED_TEXT)
            self.status_label.configure(text="Target is higher — eliminating left half")

        elif state == "right_red":
            for i in range(index, len(self.label_widgets)):
                self._set_cell(i, CELL_ELIMINATED, CELL_ELIMINATED_TEXT)
            self.status_label.configure(text="Target is lower — eliminating right half")

        elif state == "Not_found":
            self.status_label.configure(text=f"Value {self.target} not found")

    def reset(self):
        self.status_label.configure(text="Ready")
        self.target_entry.delete(0, "end")
        for i in range(len(self.label_widgets)):
            self._set_cell(i, CELL_DEFAULT, CELL_TEXT_DEFAULT)

    def start_visualization(self):
        try:
            val = int(self.target_entry.get())
            self.target = val
        except ValueError:
            self.target_entry.delete(0, "end")
            self.target_entry.insert(0, "Invalid")
            return

        for i in range(len(self.label_widgets)):
            self._set_cell(i, CELL_DEFAULT, CELL_TEXT_DEFAULT)
        self.status_label.configure(text="Searching...")

        threading.Thread(
            target=self.logic.run_search,
            args=(self.arr, self.target, self.ui_callback),
            daemon=True,
        ).start()

    def back_button(self):
        self.parent.unshow(self)
        main_menu = self.parent.get_frame()
        self.parent.show(main_menu)
        self.parent.current_shown_frame = main_menu