# Cybersecurity Risk Assessment in Banking Systems
This project involved a comprehensive cybersecurity risk assessment of banking systems, with the aim of identifying potential threats and proposing effective countermeasures. As a Cybersecurity Analyst, I utilized Bayesian Attack Graphs (BAGs) and the A* search algorithm to model and visualize the cybersecurity risks in the banking system. The risk assessment revealed several vulnerabilities in web APIs, database servers, and middleware. Based on these findings, I proposed a range of countermeasures, including standard authentication techniques for web APIs, encryption of sensitive data in configuration files, and adding digital signatures to critical database securables. This proactive approach to cybersecurity can help prevent potential attacks, protect sensitive data, and ultimately save significant costs associated with a security breach.

Important variables to run the code:
bstart=200 #starting budget to start simulation
bend=4000 #end budget of simulation
bstep=200 #step increment in budget
max_iter=25 #maximum iterations to visualize for the access probability vs iteration graph
threshold = 0.000000001 #Do not change. threshold that calculates the mean square error between probability of nodes at iteration i vs iteration i-1 
vnode=[26,28,30,32,34,36,40,51,52,53,54] #All nodes where countermeasures can be applied
cost=[100,200,1000,300,700,500,400,200,300,1200,1300] #budgets of all nodes. The index of this array matches to the index od vnode array.

Use Shift+Enter to run any block
Block 1:
Initialises the important variables (bstart, bend, bstep, max_iter,threshold, vnode, cost). Also initialise the BAG, type of nodes (leaf, circle, diamond). We also define the parent of each node in an array called “parent”. The initial probability of all nodes is present in “prob” array.

Block 2:
Runs the algorithm that uses Matthews combinational logic to iteratively update the access probability of nodes until a steady state is achieved. Also prints the figure for probability vs index of node (as a function of iterations)

Block 3:
Set of functions that are used in running the main algorithm.

Block 4:
Performs Countermeasure assessment algorithm. Submits Countermeasure plan in 2 ways: increasing order (C1,C2,…Cn), decreasing order (Cn, Cn-1, .., C1). Outputs the optimum countermeasure plan and the figures (risk vs budget and time taken vs budget) for the 2 types of countermeasure plans.
