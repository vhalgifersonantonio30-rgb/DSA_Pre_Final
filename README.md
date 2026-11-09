# 🧠 DSA Pre-Final Project: Algorithm Visualizer

An interactive Python desktop application designed to help users understand how classic Data Structures and Algorithms work step-by-step. Built with `tkinter` and styled with `ttkbootstrap` for a clean, modern interface.

This project features three distinct algorithm visualizers and interactive puzzles, demonstrating key computer science concepts through real-time graphical feedback.

---

## ✨ Features

### 1. Binary Search
* **How it works:** Generates a random sorted array of 10 numbers. You can input a target value to see how the algorithm repeatedly halves the search space.
* **Visual Feedback:** 
  * **Yellow:** The current midpoint being checked.
  * **Red:** The half of the array that has been eliminated.
  * **Green:** The target value, if found.
* **Under the hood:** Runs asynchronously on a background thread so the UI never freezes.

### 2. Selection Sort
* **How it works:** Generates a random unsorted array and visually demonstrates how the algorithm repeatedly finds the minimum value and swaps it into its correct position.
* **Visual Feedback:**
  * **Blue:** The current position being filled.
  * **Yellow:** The element currently being compared.
  * **Orange:** A new minimum candidate found.
  * **Green:** Elements that have reached their final sorted position.
* **Under the hood:** Dynamically updates a grid of labels as the array mutates.

### 3. Tower of Hanoi (4 Towers)
* **How it works:** A fully playable puzzle. Choose between **3 and 10 rings**, then click towers to pick up and drop disks. The goal is to move the entire stack from Tower A to any of the other three towers (B, C, or D).
* **Rules Enforced:**
  * Only one disk can be moved at a time.
  * Only the top disk can be moved.
  * A larger disk cannot be placed on top of a smaller disk.
* **Visual Feedback:** 
  * A dynamic canvas that scales disk sizes so 10 rings always fit.
  * Highlights the currently selected tower and top disk.
  * Displays a win dialog when the puzzle is solved, showing your total moves versus the theoretical optimal moves.

---

## 📂 Project Architecture

The repository follows a clean separation of concerns. The algorithm logic is completely decoupled from the graphical user interface, making the code modular and easy to test.

```text
algorithm_visualizer/
├── main.py                  # Application entry point
├── theme.py                 # Global fonts and color palette
├── logic/
│   ├── __init__.py
│   ├── binary.py            # Binary Search algorithm logic
│   ├── selection.py         # Selection Sort algorithm logic
│   └── hanoi.py             # Tower of Hanoi rules & state validation
└── ui/
    ├── __init__.py
    ├── base_view.py         # (Optional) Shared UI components
    ├── binary_ui.py         # Binary Search visualizer frame
    ├── selection_ui.py      # Selection Sort visualizer frame
    └── hanoi_ui.py          # Tower of Hanoi interactive frame
```

---

## 🚀 How to Run

### Prerequisites
Make sure you have **Python 3.8+** installed on your system.

### Installation & Setup

1. Install the required `ttkbootstrap` library for modern UI styling:
   ```bash
   pip install ttkbootstrap
   ```

2. Run the application:
   ```bash
   python main.py
   ```