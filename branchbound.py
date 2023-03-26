class Node: 
    def __init__(self,level, weight, value, taken, bound = 0) -> None:
        self.level = level
        self.value = value
        self.weight = weight
        self.taken = taken
        self.bound = bound
    def __lt__(self, other): 
        return self.bound > other.bound
    def __str__(self) -> str:
        print(f"Value={self.value}")

    

def bound(node: Node, capacity, data): 
    values = [data[i][0] for i in range(len(data))]
    weights = [data[i][1] for i in range(len(data))]
    
    if node.weight >= capacity: 
        return 0
    else:
        upper_bound = node.value
        j = node.level + 1
        n = len(weights)
        total_weight = node.weight
        while j < n and total_weight + weights[j] <= capacity: 
            total_weight += weights[j]
            upper_bound += node.value
            j += 1
        
        if j < n: 
            upper_bound += (capacity - weights[j]) * values[j] / weights[j]
        
        return upper_bound
        
