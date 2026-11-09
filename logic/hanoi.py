class HanoiLogic:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.towers = {
            "A": list(range(num_disks, 0, -1)),
            "B": [],
            "C": [],
            "D": [],
        }
        self.moves = 0
        self.min_moves = (3 ** num_disks) - 1

    def can_move(self, src, dst):
        if src not in self.towers or dst not in self.towers:
            return False, "Invalid tower"
        if src == dst:
            return False, "Source and destination are the same"
        if not self.towers[src]:
            return False, f"Tower {src} is empty"
        if self.towers[dst] and self.towers[dst][-1] < self.towers[src][-1]:
            return False, "Cannot place a larger disk on a smaller one"
        return True, ""

    def move(self, src, dst):
        ok, reason = self.can_move(src, dst)
        if not ok:
            return False, reason
        disk = self.towers[src].pop()
        self.towers[dst].append(disk)
        self.moves += 1
        return True, f"Moved disk {disk} from {src} to {dst}"

    def solved_tower(self):
        for name in ("B", "C", "D"):
            if len(self.towers[name]) == self.num_disks:
                return name
        return None