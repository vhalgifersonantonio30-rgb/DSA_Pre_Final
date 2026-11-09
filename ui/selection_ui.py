import ttkbootstrap as ttk
import threading
import random
from tkinter import Label
from logic.selection import SelectionSortLogic
from theme import (
    FONT_TITLE, FONT_SUBTITLE, FONT_HEADING, FONT_BODY, FONT_CELL,
    COLOR_TEXT, COLOR_MUTED, COLOR_ACCENT,
    CELL_DEFAULT, CELL_TEXT_DEFAULT, CELL_ACTIVE, CELL_ACTIVE_TEXT,
    CELL_COMPARE, CELL_COMPARE_TEXT, CELL_MIN, CELL_MIN_TEXT,
    CELL_DONE, CELL_DONE_TEXT,
)


class Selection_ui(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.logic = SelectionSortLogic(delay=0.4)
        self.arr = random.sample(range(1, 100), 10)
        self.label_widgets = []
        self.create_widgets()

    def create_widgets(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        ttk.Button(header, text="← Back", bootstyle="secondary-outline",
                   command=self.back_button).pack(side="left")
        ttk.Label(header, text="Selection Sort", font=FONT_TITLE,
                  foreground=COLOR_ACCENT).pack(side="left", padx=20)

        ttk.Label(self, text="Each pass finds the smallest remaining value and swaps it into place.",
                  font=FONT_SUBTITLE, foreground=COLOR_MUTED).pack(anchor="w", pady=(0, 20))

        controls = ttk.Frame(self)
        controls.pack(fill="x", pady=(0, 20))
        ttk.Button(controls, text="Start Sort", bootstyle="success",
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
        self._legend_item(legend, CELL_ACTIVE, "Current position")
        self._legend_item(legend, CELL_COMPARE, "Comparing")
        self._legend_item(legend, CELL_MIN, "New minimum")
        self._legend_item(legend, CELL_DONE, "Sorted")

    def _legend_item(self, parent, color, text):
        item = ttk.Frame(parent)
        item.pack(side="left", padx=(0, 20))
        swatch = Label(item, text="  ", bg=color, width=2, height=1, bd=0)
        swatch.pack(side="left", padx=(0, 6))
        ttk.Label(item, text=text, font=FONT_BODY,
                  foreground=COLOR_MUTED).pack(side="left")

    def _set_cell(self, idx, bg, fg, text=None):
        lbl = self.label_widgets[idx]
        lbl.config(bg=bg, fg=fg)
        if text is not None:
            lbl.config(text=str(text))

    def _reset_cells(self):
        for i in range(len(self.label_widgets)):
            self._set_cell(i, CELL_DEFAULT, CELL_TEXT_DEFAULT)

    def ui_callback(self, i, j, data, state):
        for idx, val in enumerate(data):
            self.label_widgets[idx].config(text=str(val))

        if state == "start":
            for k in range(i):
                self._set_cell(k, CELL_DONE, CELL_DONE_TEXT)
            for k in range(i, len(self.label_widgets)):
                self._set_cell(k, CELL_DEFAULT, CELL_TEXT_DEFAULT)
            self._set_cell(i, CELL_ACTIVE, CELL_ACTIVE_TEXT)
            self.status_label.configure(text=f"Pass {i + 1}: scanning from index {i}")

        elif state == "compare":
            if self.label_widgets[j].cget("bg") == CELL_DEFAULT:
                self._set_cell(j, CELL_COMPARE, CELL_COMPARE_TEXT)
            self.status_label.configure(text=f"Comparing index {j} with current minimum")

        elif state == "new_min":
            self._set_cell(j, CELL_MIN, CELL_MIN_TEXT)
            self.status_label.configure(text=f"New minimum at index {j}")

        elif state == "swap":
            self._set_cell(i, CELL_DONE, CELL_DONE_TEXT)
            self._set_cell(j, CELL_DONE, CELL_DONE_TEXT)
            self.status_label.configure(text=f"Swapped — index {i} is now sorted")

        elif state == "done":
            for k in range(len(self.label_widgets)):
                self._set_cell(k, CELL_DONE, CELL_DONE_TEXT)
            self.status_label.configure(text="Array sorted")

    def reset(self):
        self.status_label.configure(text="Ready")
        for i, val in enumerate(self.arr):
            self._set_cell(i, CELL_DEFAULT, CELL_TEXT_DEFAULT, text=val)

    def start_visualization(self):
        self.reset()
        self.status_label.configure(text="Sorting...")
        threading.Thread(
            target=self.logic.run_sort,
            args=(self.arr, self.ui_callback),
            daemon=True,
        ).start()

    def back_button(self):
        self.parent.unshow(self)
        main_menu = self.parent.get_frame()
        self.parent.show(main_menu)
        self.parent.current_shown_frame = main_menu