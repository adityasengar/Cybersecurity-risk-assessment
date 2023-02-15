import json
import random
import time
import matplotlib.pyplot as plt
import argparse
import numpy

def load_config(config_path):
    """Loads the attack graph data from a JSON file."""
    with open(config_path, 'r') as f:
        config = json.load(f)

    nodes = config['nodes']
    type_cfg = config['type_config']
    type_arr = [type_cfg['default']] * nodes
    for i in type_cfg['c']:
        type_arr[i] = 'c'
    for r_start, r_end in type_cfg['l']['ranges']:
        for i in range(r_start, r_end):
            type_arr[i] = 'l'

    parent_cfg = config['parent']
    parent_arr = [0] * nodes
    for k, v in parent_cfg.items():
        parent_arr[int(k)] = v

    prob_cfg = config['initial_prob']
    prob_arr = [0.0] * nodes
    random.seed(16)
    for i in range(nodes):
        prob_arr[i] = random.random()
    for k, v in prob_cfg.items():
        prob_arr[int(k)] = v
        
    return {
        "nodes": nodes, "vnode": config['vnode'], "cost": config['cost'],
        "type": type_arr, "parent": parent_arr, "prob": prob_arr,
    }

def riskcalc(P, graph_data, threshold=1e-9):
    """Performs the iterative risk calculation."""
    probi = graph_data['prob'][:]
    nodes, parent, type_arr = graph_data['nodes'], graph_data['parent'], graph_data['type']

    for node_idx in P:
        probi[node_idx] = 0

    store = [probi[:]]
    while True:
        for i in range(nodes):
            if parent[i] == -1: continue
            if type_arr[i] == 'c':
                if len(parent[i][0]) == 2:
                    probi[i] = probi[parent[i][0][0]] * probi[parent[i][0][1]]
                elif len(parent[i][0]) == 3:
                    probi[i] = probi[parent[i][0][0]] * (1 - (1 - probi[parent[i][0][1]]) * (1 - probi[parent[i][0][2]]))
            elif type_arr[i] == 'd':
                probi[i] = 1 - numpy.prod([(1 - probi[p]) for p in parent[i]])
        
        store.append(probi[:])
        t1, t2 = store[-1], store[-2]
        if sum([(t1[i] - t2[i])**2 for i in range(len(probi))]) < threshold:
            return probi[16], store

def sorter(V, C, budget):
    """Sorts a plan in decreasing order of cost."""
    arrange = numpy.argsort(C).tolist()
    arrange.reverse()
    newplan2 = [V[i] for i in arrange]
    newcost2 = [C[i] for i in arrange]
    c = 0
    for i in range(len(newcost2)):
        if sum(newcost2[i:]) <= budget:
            break
        else:
            c += 1
    return newplan2, newcost2, c

def conv(A):
    """Converts node indices to countermeasure IDs."""
    # This is a simplified mapping based on the notebook
    mapping = {26: 'C1', 28: 'C2', 30: 'C3', 32: 'C4', 34: 'C5', 36: 'C6', 40: 'C7', 51: 'C8', 52: 'C9', 53: 'C10', 54: 'C11'}
    return [mapping.get(node, str(node)) for node in A]

def bud(budget, vnode, cost, graph_data, reverse=False):
    """Finds the optimal countermeasure plan for a given budget using A* search."""
    if reverse:
        vnode.reverse()
        cost.reverse()
    
    start_time = time.time()
    OL, CL, OLcost, FX = [vnode], [], [cost], [0]
    I = 0
    while I < len(OL):
        plan, current_cost = OL[I], OLcost[I]
        if sum(current_cost) <= budget:
            print(f"eureka. Plan found: {conv(plan)}")
            risk = riskcalc(plan, graph_data)[0]
            print(f"--- {time.time() - start_time:.2f} seconds ---")
            print(f"Budget: {budget}, Risk: {risk}")
            return budget, risk, plan, time.time() - start_time
        
        CL.append(plan)
        for k in range(len(plan)):
            newplan = plan[:k] + plan[k+1:]
            newcost = current_cost[:k] + current_cost[k+1:]
            if newplan not in OL and newplan not in CL:
                gx = riskcalc(newplan, graph_data)[0]
                # Simplified heuristic for demonstration
                hx = gx * 0.1 
                fx = hx + gx
                
                # Insert into sorted Open List
                insert_pos = 0
                for i in range(1, len(FX)):
                    if fx < FX[i]:
                        insert_pos = i
                        break
                else:
                    insert_pos = len(FX)
                
                FX.insert(insert_pos, fx)
                OL.insert(insert_pos, newplan)
                OLcost.insert(insert_pos, newcost)
        I += 1
    print("No plan found within budget")
    return budget, -1, [], time.time() - start_time

def main():
    """Main execution function with command-line arguments."""
    parser = argparse.ArgumentParser(description="Cybersecurity Risk Analyzer")
    parser.add_argument('--config', type=str, default='config/attack_graph.json', help='Path to the attack graph JSON file.')
    parser.add_argument('--bstart', type=int, default=300, help='Starting budget for analysis.')
    parser.add_argument('--bend', type=int, default=1500, help='Ending budget for analysis.')
    parser.add_argument('--bstep', type=int, default=200, help='Step increment for budget.')
    parser.add_argument('--mode', type=str, choices=['risk', 'budget'], default='risk', help='Run mode: "risk" for simple calculation or "budget" for A* analysis.')
    args = parser.parse_args()

    graph_data = load_config(args.config)
    
    if args.mode == 'risk':
        print("Calculating risk with no countermeasures...")
        final_risk, _ = riskcalc([], graph_data)
        print(f"Final risk of accessing database server: {final_risk}")
    
    elif args.mode == 'budget':
        print(f"Running budget analysis from {args.bstart} to {args.bend}...")
        tempbudget, temprisk, temptime = [], [], []
        for B in range(args.bstart, args.bend, args.bstep):
            b, r, _, t = bud(B, graph_data['vnode'], graph_data['cost'], graph_data)
            tempbudget.append(b)
            temprisk.append(r * 100)
            temptime.append(t)
        
        plt.figure()
        plt.plot(tempbudget, temprisk, label='Risk (f)')
        plt.xlabel('Budget')
        plt.ylabel('Risk (%)')
        plt.legend()
        plt.title('Risk vs. Budget')
        plt.show()

if __name__ == "__main__":
    main()