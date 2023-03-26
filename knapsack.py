import os 
from branch_bound import Node, bound
from queue import PriorityQueue

class Knapsack: 
    def __init__(self) -> None:
        self.capacity = self.input()["capacity"]
        self.num_of_classes = self.input()["num_of_classes"]
        self.weights = self.input()["weights"]
        self.values = self.input()["values"]
        self.labels = self.input()["labels"]

    
    def input(self): 
        capacity = 0
        num_of_classes = 0
        weights = []
        values = []
        labels = []

        f = open("input.txt", "r")
        lines = f.readlines()
        capacity = int(lines[0])
        num_of_classes = int(lines[1])
        weights = [int(i) for i in lines[2].split(',')]
        values = [int(i) for i in lines[3].split(',')]
        labels = [int(i) for i in lines[4].split(',')]
        return {
            "capacity": capacity,
            "num_of_classes": num_of_classes,
            "weights": weights, 
            "values": values, 
            "labels": labels
        }
    def brute(self):
        n = len(self.values)
        length_unique_labels = len(set(self.labels))
        res = 0
        curLabels = []
        arrBits = [0] * n
        resBits = [0] * n
        def helper(capacity, curValue, i):
            nonlocal res, arrBits, resBits
            if i == n or capacity == 0:
                if curValue > res and len(set(curLabels)) == length_unique_labels:
                    res = curValue
                    resBits = arrBits.copy()                    
                return

            # include the i-th item
            if self.weights[i] <= capacity:
                curLabels.append(self.labels[i])
                arrBits[i] = 1
                helper(capacity - self.weights[i], curValue + self.values[i], i + 1)
                arrBits[i] = 0
                curLabels.remove(self.labels[i])

            # exclude the i-th item
            helper(capacity, curValue, i + 1)
        helper(self.capacity, 0, 0)
        return [res, resBits]
    
    def getLabelsLength(self, input): 
        labels = set()
        for i in range(len(input)):
            if input[i] == 1: 
                labels.add(self.labels[i])
        return len(labels)

    def branch_and_bound(self):
        data = [[value, weight, label] for value, weight, label in zip(self.values, self.weights, self.labels)] 
        data.sort(key=lambda x: x[0] / x[1])
        pq = []
        root = Node(-1, 0, 0, [])
        pq.append(root)
        max_value = 0
        best_taken = []
        n = len(self.values)
        while pq:
            node = pq.pop(0)
            if node.level == n - 1:
                if node.value > max_value and self.getLabelsLength(node.taken) == len(set(self.labels)):
                    max_value = node.value
                    best_taken = node.taken
            else:
                level = node.level + 1
                taken = node.taken[:]
                taken.append(1)
                new_node = Node(level, node.value + data[level][0], node.weight + data[level][1], taken)
                if bound(new_node, self.capacity, data) > max_value:
                    pq.append(new_node)

                taken = node.taken[:]
                taken.append(0)
                new_node = Node(level, node.value, node.weight, taken)
                if bound(new_node, self.capacity, data) > max_value:
                    pq.append(new_node)
        return max_value, best_taken
a = Knapsack()

print(a.brute())
print(a.branch_and_bound())