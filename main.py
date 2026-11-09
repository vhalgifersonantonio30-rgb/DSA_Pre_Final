import ttkbootstrap as ttk
from theme import (
    FONT_TITLE, FONT_BODY, COLOR_TEXT, COLOR_MUTED, COLOR_ACCENT,
)
from ui.binary_ui import Binary_ui
from ui.selection_ui import Selection_ui
from ui.hanoi_ui import Hanoi_ui


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.geometry("1200x650")
        self.minsize(1000, 600)
        self.title("Algorithm Visualizer")
        self.style.configure("Card.TFrame", background="#2a2a3c", relief="flat")
        self.current_shown_frame = None
        self.frames = {}

        menu = self._build_menu()
        self.frames["menu"] = menu
        self.current_shown_frame = menu
        self.show(menu)

    def _build_menu(self):
        menu = ttk.Frame(self, padding=40)

        header = ttk.Frame(menu)
        header.pack(pady=(40, 10))
        ttk.Label(header, text="Algorithm Visualizer", font=FONT_TITLE,
                  foreground=COLOR_ACCENT).pack()
        ttk.Label(menu, text="Pick an algorithm to explore step by step.",
                  font=FONT_BODY, foreground=COLOR_MUTED).pack(pady=(0, 40))

        cards = ttk.Frame(menu)
        cards.pack()

        self._algo_card(cards, "Binary Search",
                        "Find a target in a sorted list by halving the range.",
                        "primary", self.open_binary)
        self._algo_card(cards, "Selection Sort",
                        "Build a sorted list by repeatedly picking the minimum.",
                        "success", self.open_selection)
        self._algo_card(cards, "Tower of Hanoi",
                        "Move a stack of disks across four towers using a recursive strategy.",
                        "info", self.open_hanoi)

        return menu

    def _algo_card(self, parent, title, description, style, command):
        card = ttk.Frame(parent, style="Card.TFrame", padding=24)
        card.pack(side="left", padx=12, ipadx=10, ipady=10)

        ttk.Label(card, text=title, font=FONT_TITLE,
                  foreground=COLOR_TEXT).pack(anchor="w")
        ttk.Label(card, text=description, font=FONT_BODY,
                  foreground=COLOR_MUTED, wraplength=240,
                  justify="left").pack(anchor="w", pady=(6, 20))
        ttk.Button(card, text="Open →", bootstyle=style,
                   command=command).pack(anchor="w")

    def get_frame(self):
        return self.frames["menu"]

    def show(self, frame):
        frame.pack(fill="both", expand=True)

    def unshow(self, frame):
        frame.pack_forget()

    def _switch_to(self, key, factory):
        if key not in self.frames:
            self.frames[key] = factory(self)
        self.unshow(self.current_shown_frame)
        self.current_shown_frame = self.frames[key]
        self.show(self.current_shown_frame)

    def open_binary(self):
        self._switch_to("binary", Binary_ui)

    def open_selection(self):
        self._switch_to("selection", Selection_ui)

    def open_hanoi(self):
        self._switch_to("hanoi", Hanoi_ui)


if __name__ == "__main__":
    App().mainloop()