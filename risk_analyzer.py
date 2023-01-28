import json
import random
import time
import matplotlib.pyplot as plt

def load_config(config_path):
    """Loads the attack graph data from a JSON file."""
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Reconstruct the data structures from the config
    nodes = config['nodes']
    
    # Type array
    type_cfg = config['type_config']
    type_arr = [type_cfg['default']] * nodes
    for i in type_cfg['c']:
        type_arr[i] = 'c'
    for r_start, r_end in type_cfg['l']['ranges']:
        for i in range(r_start, r_end):
            type_arr[i] = 'l'

    # Parent dictionary (keys need to be converted to int)
    parent_cfg = config['parent']
    parent_arr = [0] * nodes
    for k, v in parent_cfg.items():
        parent_arr[int(k)] = v

    # Initial probabilities
    prob_cfg = config['initial_prob']
    prob_arr = [0.0] * nodes
    # Set random probabilities for nodes not in the config
    random.seed(16)
    for i in range(nodes):
        prob_arr[i] = random.random()
    # Override with specific initial probabilities
    for k, v in prob_cfg.items():
        prob_arr[int(k)] = v
        
    return {
        "nodes": nodes,
        "vnode": config['vnode'],
        "cost": config['cost'],
        "type": type_arr,
        "parent": parent_arr,
        "prob": prob_arr,
    }

def riskcalc(P, graph_data, threshold=1e-9):
    """Performs the iterative risk calculation."""
    probi = graph_data['prob'][:]
    nodes = graph_data['nodes']
    parent = graph_data['parent']
    type_arr = graph_data['type']

    for i in range(len(P)):
        probi[P[i]] = 0

    store = [probi[:]]
    it = 1
    while it != 0:
        for i in range(nodes):
            if parent[i] == -1:
                continue
            if type_arr[i] == 'c':
                if len(parent[i][0]) == 2:
                    probi[i] = probi[parent[i][0][0]] * probi[parent[i][0][1]]
                elif len(parent[i][0]) == 3:
                    probi[i] = probi[parent[i][0][0]] * (1 - (1 - probi[parent[i][0][1]]) * (1 - probi[parent[i][0][2]]))
            elif type_arr[i] == 'd':
                prod = 1
                for j in range(len(parent[i])):
                    prod = prod * (1 - probi[parent[i][j]])
                probi[i] = 1 - prod
            elif type_arr[i] == 'l':
                continue
        
        store.append(probi[:])
        t1 = store[-1]
        t2 = store[-2]
        sumi = sum([(t1[i] - t2[i])**2 for i in range(len(probi))])

        if sumi < threshold:
            it = 0
            return (probi[16], store)

def main():
    """Main execution function."""
    # Load configuration
    graph_data = load_config('config/attack_graph.json')
    
    # Run a sample risk calculation
    print("Calculating risk with no countermeasures...")
    final_risk, store = riskcalc([], graph_data)
    print(f"Final risk of accessing database server: {final_risk}")

    # Plot probability evolution
    ra = [i + 1 for i in range(graph_data['nodes'])]
    plt.figure()
    for i in range(0, 25, 5):
        if i < len(store):
            plt.plot(ra, store[i], label=f'iter={i+1}')
    plt.legend(loc='center right')
    plt.xlim(0, 60)
    plt.ylim(0, 1.1)
    plt.xlabel('Index of nodes')
    plt.ylabel('Probability')
    plt.title('Probability Evolution per Node')
    plt.show()

if __name__ == "__main__":
    main()
