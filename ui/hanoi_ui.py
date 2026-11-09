import ttkbootstrap as ttk
from tkinter import Canvas, StringVar
from logic.hanoi import HanoiLogic
from theme import (
    FONT_TITLE, FONT_SUBTITLE, FONT_HEADING, FONT_BODY, FONT_CELL,
    COLOR_TEXT, COLOR_MUTED, COLOR_ACCENT,
)


TOWER_NAMES = ["A", "B", "C", "D"]

DISK_COLORS = [
    "#f7768e", "#ff9e64", "#e0af68", "#9ece6a",
    "#7dcfff", "#7aa2f7", "#bb9af7", "#c0caf5",
    "#f7768e", "#ff9e64",
]

MIN_RINGS = 3
MAX_RINGS = 10


class Hanoi_ui(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.logic = None
        self.num_disks = 3
        self.selected = None
        self.create_widgets()

    def create_widgets(self):
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        ttk.Button(header, text="Back", bootstyle="secondary-outline",
                   command=self.back_button).pack(side="left")
        ttk.Label(header, text="Tower of Hanoi", font=FONT_TITLE,
                  foreground=COLOR_ACCENT).pack(side="left", padx=20)

        ttk.Label(self, text="Pick how many rings, then click a tower to select its top "
                             "disk and click another tower to drop it. Stack every ring "
                             "on any tower except A to win.",
                  font=FONT_SUBTITLE, foreground=COLOR_MUTED,
                  wraplength=1000, justify="left").pack(anchor="w", pady=(0, 20))

        self._build_setup_panel()
        self._build_game_panel()
        self._show_setup()

    def _build_setup_panel(self):
        self.setup_panel = ttk.Frame(self, style="Card.TFrame", padding=30)

        ttk.Label(self.setup_panel, text="How many rings?", font=FONT_HEADING,
                  foreground=COLOR_TEXT).pack(pady=(0, 10))
        ttk.Label(self.setup_panel,
                  text=f"Choose between {MIN_RINGS} and {MAX_RINGS} rings. "
                       f"More rings = bigger challenge.",
                  font=FONT_BODY, foreground=COLOR_MUTED).pack(pady=(0, 20))

        row = ttk.Frame(self.setup_panel, style="Card.TFrame")
        row.pack()

        self.ring_var = StringVar(value=str(MIN_RINGS))
        self.ring_spin = ttk.Spinbox(
            row, from_=MIN_RINGS, to=MAX_RINGS, width=6,
            textvariable=self.ring_var,
            font=FONT_HEADING, justify="center",
        )
        self.ring_spin.pack(side="left", padx=(0, 12))

        ttk.Button(row, text="Start Puzzle", bootstyle="primary",
                   command=self._start_from_setup).pack(side="left")

    def _build_game_panel(self):
        self.game_panel = ttk.Frame(self)

        controls = ttk.Frame(self.game_panel)
        controls.pack(fill="x", pady=(0, 10))

        ttk.Button(controls, text="Restart", bootstyle="secondary-outline",
                   command=self._show_setup).pack(side="left", padx=(0, 8))

        self.move_label = ttk.Label(controls, text="Moves: 0", font=FONT_BODY,
                                    foreground=COLOR_MUTED)
        self.move_label.pack(side="right")

        self.status_label = ttk.Label(self.game_panel,
                                      text="Select a tower to pick up a disk.",
                                      font=FONT_HEADING, foreground=COLOR_MUTED)
        self.status_label.pack(pady=(0, 10))

        card = ttk.Frame(self.game_panel, style="Card.TFrame", padding=10)
        card.pack(fill="both", expand=True)

        self.canvas = Canvas(card, bg="#2a2a3c", highlightthickness=0, height=420,
                             cursor="hand2")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw_board())
        self.canvas.bind("<Button-1>", self._on_canvas_click)

    def _show_setup(self):
        self.game_panel.pack_forget()
        self.setup_panel.pack(fill="x", pady=40)

    def _start_from_setup(self):
        try:
            val = int(self.ring_var.get())
        except ValueError:
            val = MIN_RINGS
        val = max(MIN_RINGS, min(MAX_RINGS, val))
        self.ring_var.set(str(val))
        self._start_game(val)

    def _start_game(self, num_disks):
        self.num_disks = num_disks
        self.logic = HanoiLogic(num_disks)
        self.selected = None
        self.setup_panel.pack_forget()
        self.game_panel.pack(fill="both", expand=True)
        self.move_label.configure(text="Moves: 0")
        self.status_label.configure(text="Select a tower to pick up a disk.")
        self.canvas.update_idletasks()
        self._draw_board()

    def _draw_board(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10 or self.logic is None:
            return

        base_y = h - 30
        tower_width = w / len(TOWER_NAMES)
        max_disk_w = tower_width * 0.8

        for i, name in enumerate(TOWER_NAMES):
            cx = tower_width * (i + 0.5)
            is_selected = self.selected == name
            peg_color = COLOR_ACCENT if is_selected else "#565f89"
            self.canvas.create_line(cx, base_y, cx, 40, fill=peg_color, width=4)
            self.canvas.create_line(cx - tower_width * 0.35, base_y,
                                    cx + tower_width * 0.35, base_y,
                                    fill=peg_color, width=4)
            label_color = COLOR_ACCENT if is_selected else COLOR_MUTED
            self.canvas.create_text(cx, base_y + 18, text=name,
                                    fill=label_color, font=FONT_HEADING)

        available_h = base_y - 50
        disk_h = max(12, min(22, available_h // (self.num_disks + 1)))
        gap = max(2, disk_h // 5)

        for i, name in enumerate(TOWER_NAMES):
            cx = tower_width * (i + 0.5)
            disks = self.logic.towers[name]
            for level, disk in enumerate(disks):
                width = max_disk_w * (disk / self.num_disks)
                y = base_y - 6 - level * (disk_h + gap)
                color = DISK_COLORS[(disk - 1) % len(DISK_COLORS)]
                outline = COLOR_ACCENT if (self.selected == name
                                           and level == len(disks) - 1) else ""
                self.canvas.create_rectangle(
                    cx - width / 2, y - disk_h,
                    cx + width / 2, y,
                    fill=color, outline=outline,
                    width=3,
                )
                if disk_h >= 14:
                    self.canvas.create_text(
                        cx, y - disk_h / 2, text=str(disk),
                        fill="#1e1e2e", font=FONT_CELL,
                    )

    def _tower_at(self, x):
        w = self.canvas.winfo_width()
        if w < 10:
            return None
        index = int(x // (w / len(TOWER_NAMES)))
        if 0 <= index < len(TOWER_NAMES):
            return TOWER_NAMES[index]
        return None

    def _on_canvas_click(self, event):
        if self.logic is None:
            return
        tower = self._tower_at(event.x)
        if tower is None:
            return

        if self.selected is None:
            if not self.logic.towers[tower]:
                self.status_label.configure(
                    text=f"Tower {tower} is empty — pick another."
                )
                return
            self.selected = tower
            self.status_label.configure(
                text=f"Picked up from tower {tower}. Now click a destination."
            )
            self._draw_board()
            return

        if self.selected == tower:
            self.selected = None
            self.status_label.configure(text="Selection cleared.")
            self._draw_board()
            return

        ok, message = self.logic.move(self.selected, tower)
        if ok:
            self.move_label.configure(text=f"Moves: {self.logic.moves}")
            self.status_label.configure(text=message)
            self.selected = None
            self._draw_board()
            winner = self.logic.solved_tower()
            if winner:
                self._show_success_dialog(winner)
        else:
            self.status_label.configure(text=f"Invalid move: {message}")
            self.selected = None
            self._draw_board()

    def _show_success_dialog(self, tower_name):
        dialog = ttk.Toplevel(self)
        dialog.title("Puzzle Solved")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding=24)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Puzzle Solved!", font=FONT_TITLE,
                  foreground="#9ece6a").pack(pady=(0, 8))
        ttk.Label(frame,
                  text=f"You stacked all {self.num_disks} rings on tower {tower_name}.",
                  font=FONT_BODY, foreground=COLOR_TEXT).pack(pady=(0, 4))
        ttk.Label(frame, text=f"Your moves: {self.logic.moves}",
                  font=FONT_HEADING, foreground=COLOR_ACCENT).pack(pady=(0, 2))
        ttk.Label(frame, text=f"Optimal moves: {self.logic.min_moves}",
                  font=FONT_BODY, foreground=COLOR_MUTED).pack(pady=(0, 16))

        buttons = ttk.Frame(frame)
        buttons.pack()
        ttk.Button(buttons, text="Play Again", bootstyle="primary",
                   command=lambda: (dialog.destroy(), self._start_game(self.num_disks))
                   ).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Choose Rings", bootstyle="secondary-outline",
                   command=lambda: (dialog.destroy(), self._show_setup())
                   ).pack(side="left")

        dialog.update_idletasks()
        px = self.winfo_rootx() + (self.winfo_width() - dialog.winfo_width()) // 2
        py = self.winfo_rooty() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{px}+{py}")

    def back_button(self):
        self.parent.unshow(self)
        main_menu = self.parent.get_frame()
        self.parent.show(main_menu)
        self.parent.current_shown_frame = main_menu