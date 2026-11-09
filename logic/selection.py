import time


class SelectionSortLogic:
    def __init__(self, delay=0.5):
        self.delay = delay

    def run_sort(self, arr, callback):
        data = list(arr)
        n = len(data)

        for i in range(n - 1):
            min_idx = i
            callback(i, min_idx, data, "start")
            time.sleep(self.delay)

            for j in range(i + 1, n):
                callback(i, j, data, "compare")
                time.sleep(self.delay)

                if data[j] < data[min_idx]:
                    min_idx = j
                    callback(i, min_idx, data, "new_min")
                    time.sleep(self.delay)

            if min_idx != i:
                data[i], data[min_idx] = data[min_idx], data[i]
                callback(i, min_idx, data, "swap")
                time.sleep(self.delay)

        callback(n - 1, n - 1, data, "done")