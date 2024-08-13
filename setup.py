def getMaximumEfficiency(connect_nodes, connect_from, connect_to, computer_val, k):
    from collections import defaultdict

    # Step 1: Build the adjacency list for the tree
    tree = defaultdict(list)
    for u, v in zip(connect_from, connect_to):
        tree[u-1].append(v-1)
        tree[v-1].append(u-1)
    
    # Step 2: DFS to calculate subtree sums and maximize efficiency
    def dfs(node, parent):
        subtree_sum = computer_val[node]
        for neighbor in tree[node]:
            if neighbor != parent:
                child_sum = dfs(neighbor, node)
                if child_sum > 0:
                    subtree_sum += child_sum
        return subtree_sum
    
    # Start DFS from the root (node 0)
    max_efficiency = -float('inf')
    total_sum = dfs(0, -1)  # Compute sum of the whole tree
    num_ops = 0
    efficiency = total_sum - (k * num_ops)
    max_efficiency = max(max_efficiency, efficiency)
    
    def maximize_dfs(node, parent):
        nonlocal num_ops, max_efficiency
        subtree_sum = computer_val[node]
        for neighbor in tree[node]:
            if neighbor != parent:
                child_sum = maximize_dfs(neighbor, node)
                if child_sum > 0:
                    subtree_sum += child_sum
        if subtree_sum < 0:
            num_ops += 1
            efficiency = (total_sum - subtree_sum) - (k * num_ops)
            max_efficiency = max(max_efficiency, efficiency)
        return subtree_sum
    
    maximize_dfs(0, -1)
    
    return max_efficiency

# Example usage:
connect_nodes = 3
connect_from = [1, 2]
connect_to = [2, 3]
computer_val = [9, -1, 3]
k = 3

print(getMaximumEfficiency(connect_nodes, connect_from, connect_to, computer_val, k))  # Output should be 11
