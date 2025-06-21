'''
Main program flow:
- Define graph and display eateries
- Let user input start and end states (for blind search only)
- Perform blind search or heuristic search depending on user input
- Display end state/s

Example code using networkx library:
import networkx as nx
import matplotlib.pyplot as plt -> for visualization only (optional)

G = nx.MultiGraph()
G.add_edge("S", "A")
G.add_edge("S", "B")
G.add_edge("A", "E")
G.add_edge("B", "C")

nx.draw_spring(G, with_labels=True)
plt.show()

'''

# UCS


# A*
'''
-> Set start state
-> Initialize list of visited nodes
-> Initialize list of candidate nodes
-> Set heuristic function value (distance(n), rating)
Loop:
-> Set cumulative = heuristic(start) + cost(n)
 If unvisited,
  -> Compare candidate nodes
  -> If candidate is with lowest cumulative cost
    -> Change start state
    -> Add to visited node

  Else if goal state
  -> return node, break loop

'''

