import math # For euclidean distance
import heapq # Implement priority queue
import os # For screen clearing
from PIL import Image # For opening images
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

graph = {
    "Sherwood Place": {"Jollibee": 60},
    "Jollibee": {"Sherwood Place": 60, "Taft-Castro": 44},
    "Taft-Castro": {"Jollibee": 44, "Gokongwei Hall": 28, "Agno-Castro": 85},
    "Gokongwei Hall": {"Taft-Castro": 28, "Taft-Dagonoy": 85},
    "Agno-Castro": {"Taft-Castro": 85, "Agno Food Court": 29, "Andrew Gonzales Hall": 62},
    "Agno Food Court": {"Agno-Castro": 29, "24 Chicken": 44},
    "24 Chicken": {"Agno Food Court": 44, "Agno-Fidel A. Reyes": 41},
    "Agno-Fidel A. Reyes": {"24 Chicken": 41, "Taft-Dagonoy": 80},
    "Andrew Gonzales Hall": {"Perico's": 23, "Agno-Castro": 62},
    "Perico's": {"The Barn": 53, "Andrew Gonzales Hall": 23},
    "The Barn": {"Perico's": 53},
    "Taft-Dagonoy": {"Gokongwei Hall": 85, "Tinuhog ni Benny": 59, "North Gate": 72, "Agno-Fidel A. Reyes": 80},
    "Tinuhog ni Benny": {"Taft-Dagonoy": 59, "Leon Guinto-Dagonoy": 40},
    "Leon Guinto-Dagonoy": {"Tinuhog ni Benny": 40, "Drip Kofi": 84},
    "Drip Kofi": {"Leon Guinto-Dagonoy": 84, "Chomp Chomp": 35},
    "Chomp Chomp": {"Drip Kofi": 35, "Leon Guinto-Estrada": 42},
    "Leon Guinto-Estrada": {"Chomp Chomp": 42, "Taft-Estrada": 95},
    "Taft-Estrada": {"South Gate": 41, "Leon Guinto-Estrada": 95, "North Gate": 99},
    "North Gate": {"Taft-Estrada": 99, "Taft-Dagonoy": 72, "CBTL": 73},
    "CBTL": {"North Gate": 73},
    "South Gate": {"Taft-Estrada": 41, "McDonald's": 54, "Kitchen City": 82},
    "McDonald's": {"South Gate": 54, "Tomo Coffee": 28},
    "Tomo Coffee": {"McDonald's": 28},
    "Kitchen City": {"South Gate": 82},
}

coordinates = {
    "Sherwood Place": (14.56757, 120.99283),
    "Jollibee": (14.56709, 120.99308),
    "Taft-Castro": (14.56672, 120.99324),
    "Gokongwei Hall": (14.56648, 120.99336),
    "Agno-Castro": (14.56641, 120.99252),
    "Agno Food Court": (14.56619, 120.99265),
    "24 Chicken": (14.56585, 120.99284),
    "Agno-Fidel A. Reyes": (14.56554, 120.99299),
    "Andrew Gonzales Hall": (14.56692, 120.99228),
    "Perico's": (14.5671, 120.99218),
    "The Barn": (14.56754, 120.99197),
    "Taft-Dagonoy": (14.56577, 120.9937),
    "Tinuhog ni Benny": (14.56598, 120.99419),
    "Leon Guinto-Dagonoy": (14.56611, 120.99454),
    "Drip Kofi": (14.56542, 120.99489),
    "Chomp Chomp": (14.56512, 120.99501),
    "Leon Guinto-Estrada": (14.56477, 120.99516),
    "Taft-Estrada": (14.5644, 120.99435),
    "North Gate": (14.56518, 120.99396),
    "CBTL": (14.56497, 120.99333),
    "South Gate": (14.56409, 120.99449),
    "McDonald's": (14.56363, 120.99465),
    "Tomo Coffee": (14.56342, 120.99476),
    "Kitchen City": (14.56382, 120.99379),
}

# List of non-eatery nodes that cannot be used as end goals
non_eatery_nodes = {
    "Gokongwei Hall", "Taft-Castro", "Agno-Castro", "Agno-Fidel A. Reyes", "Taft-Dagonoy",
    "Leon Guinto-Dagonoy", "Leon Guinto-Estrada", "Taft-Estrada", "North Gate", "South Gate"
}

# UCS
def uniform_cost_search(graph, start, goal):
    # Validate nodes first
    is_valid, error_message = validate_nodes(graph, start, goal)
    if not is_valid:
        return None, None, error_message
    
    to_visit = []
    heapq.heappush(to_visit, (0, start)) # Push start node to priority queue

    visited = {start: None}
    cost_so_far = {start: 0}

    while to_visit:
        current_cost, current = heapq.heappop(to_visit)

        if current == goal:
            break

        for node, edge_cost in graph[current].items():
            new_cost = cost_so_far[current] + edge_cost # Cost Accumulation
            if node not in cost_so_far or new_cost < cost_so_far[node]:
                cost_so_far[node] = new_cost
                heapq.heappush(to_visit, (new_cost, node))
                visited[node] = current

    # Trace optimal path
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = visited[current]
    path.reverse()
    return path, cost_so_far[goal], None

# Error detection function
def validate_nodes(graph, start, goal):
    """
    Check if start and goal nodes exist in the graph and if goal is a valid eatery.
    Returns (is_valid, error_message)
    """
    if start not in graph:
        return False, f"Start node '{start}' does not exist in the graph."
    if goal not in graph:
        return False, f"Goal node '{goal}' does not exist in the graph."
    # Non-eatery nodes that cannot be used as end goals
    if goal in non_eatery_nodes:
        return False, f"Error: '{goal}' is not an eatery and cannot be used as the end goal. Please choose a valid eatery as the goal."
    return True, ""

# A*
def a_star(graph, start, goal):
    # Validate nodes first
    is_valid, error_message = validate_nodes(graph, start, goal)
    if not is_valid:
        return None, None, error_message
    
    to_visit = [] 
    heapq.heappush(to_visit, (0, start)) # Push start node to priority queue

    visited = {start: None}
    cost_so_far = {start: 0} 
      
    while to_visit:
        current_priority, current = heapq.heappop(to_visit)

        if current == goal:
            break
        
        for node, cost in graph[current].items():
            point1 = coordinates.get(current)
            point2 = coordinates.get(goal)
            heuristic = math.dist(point1, point2) # Compute euclidean distance as heuristic
            new_cost = cost_so_far[current] + cost
            if node not in cost_so_far or new_cost < cost_so_far[node]:
                cost_so_far[node] = new_cost
                priority = new_cost + heuristic # Cumulative cost
                heapq.heappush(to_visit, (priority, node)) # Push node to priority queue
                visited[node] = current

    # Trace optimal path
    path = []
    current = goal
    while current:
        path.append(current)
        current = visited[current]
    path.reverse()

    return path, cost_so_far[goal], None

# Error recovery function
def handle_error_recovery():
    """
    Prompt user with three options after an error:
    1) Try Again
    2) View Graph
    3) Exit to main menu
    """
    while True:
        print("\nWhat would you like to do?")
        print("1) Try Again")
        print("2) View Graph")
        print("3) Exit to main menu")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            return "retry"
        elif choice == "2":
            return "view_graph"
        elif choice == "3":
            return "exit_to_menu"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Function to generate and save the graph image
def generate_graph_image(graph, coordinates, image_path="graph_visualization.png", highlight_path=None, total_cost=None):
    G = nx.Graph()
    for node, pos in coordinates.items():
        G.add_node(node, pos=pos)
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            if not G.has_edge(node, neighbor):
                G.add_edge(node, neighbor, weight=weight)
    pos = {node: (lon, lat) for node, (lat, lon) in coordinates.items()}
    plt.figure(figsize=(30, 20))
    # Node coloring
    eatery_nodes = set(G.nodes()) - non_eatery_nodes
    node_colors = []
    for node in G.nodes():
        if highlight_path and len(highlight_path) > 1:
            if node == highlight_path[0] or node == highlight_path[-1]:
                node_colors.append('lightgreen')  # Start or End (light green)
            elif node in eatery_nodes:
                node_colors.append('plum')  # Eatery
            else:
                node_colors.append('lightblue')    # Non-eatery
        else:
            if node in eatery_nodes:
                node_colors.append('plum')  # Eatery
            else:
                node_colors.append('lightblue')    # Non-eatery
    # Highlight optimal path if provided (draw first, with lower opacity)
    if highlight_path and len(highlight_path) > 1:
        path_edges = list(zip(highlight_path, highlight_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, alpha=0.5)
    # Draw all edges in gray and nodes/labels on top
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=1400, font_size=12)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    # Add total cost as text on the image if provided
    if total_cost is not None and highlight_path and len(highlight_path) > 1:
        plt.text(0.5, 0.97, f"Total cost: {total_cost}", fontsize=24, color='black', ha='center', va='top', transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    # Add legend
    legend_handles = [
        mpatches.Patch(color='plum', label='Eatery'),
        mpatches.Patch(color='lightblue', label='Non-eatery'),
    ]
    if highlight_path and len(highlight_path) > 1:
        legend_handles.append(mpatches.Patch(color='lightgreen', label='Start/End Node'))
        legend_handles.append(mpatches.Patch(color='red', label='Best Path', alpha=0.5))
    plt.legend(handles=legend_handles, loc='lower left', fontsize=16, framealpha=1)
    plt.axis('off')
    plt.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08)
    plt.savefig(image_path)
    plt.close()

# Main menu
while True:
    print("\n--- Graph Menu ---")
    print("1) Add Node to Graph")
    print("2) Remove Node from Graph")
    print("3) Uniform Cost Search")
    print("4) A* Search")
    print("5) View Graph")
    print("6) Exit")

    choice = input("Choose an option: ")

    if choice == "1":
       print("Add node") # Placeholder
        # add_node(graph)
    elif choice == "2":
       print("Remove node") # Placeholder
        # remove_node(graph)
    elif choice == "3":
        os.system('clear')  # Clear screen for macOS/Linux
        while True:
            print("=== UNIFORM COST SEARCH (UCS) ===")
            start = input("Enter start node: ").strip().title()
            goal = input("Enter goal node: ").strip().title()
            path, total_cost, error = uniform_cost_search(graph, start, goal)
            
            if path:
                print("Optimal path:", " -> ".join(path))
                print("Total cost:", total_cost)
                # Generate and show highlighted graph
                generate_graph_image(graph, coordinates, highlight_path=path, total_cost=total_cost)
                image_path = "graph_visualization.png"
                try:
                    img = Image.open(image_path)
                    img.show()
                    print(f"Graph visualization opened: {image_path}")
                except FileNotFoundError:
                    print(f"Image file not found: {image_path}")
                    print("Please ensure the graph visualization image exists.")
                except Exception as e:
                    print(f"Error opening image: {e}")
                # Prompt user to return to main menu or exit
                while True:
                    user_choice = input("\nPress 'y' to return to main menu or 'n' to exit: ").lower()
                    if user_choice == 'y':
                        os.system('clear')
                        break
                    elif user_choice == 'n':
                        print("Exiting...")
                        exit()
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                break
            else:
                print(error)
                recovery_choice = handle_error_recovery()
                
                if recovery_choice == "retry":
                    os.system('clear')  # Clear screen before retry
                    continue
                elif recovery_choice == "view_graph":
                    # Regenerate the graph image before viewing (same as option 5)
                    generate_graph_image(graph, coordinates)
                    image_path = "graph_visualization.png"
                    try:
                        img = Image.open(image_path)
                        img.show()
                        print(f"Graph visualization opened: {image_path}")
                    except FileNotFoundError:
                        print(f"Image file not found: {image_path}")
                        print("Please ensure the graph visualization image exists.")
                    except Exception as e:
                        print(f"Error opening image: {e}")
                    input("Press Enter to continue...")
                    os.system('clear')
                    continue
                elif recovery_choice == "exit_to_menu":
                    os.system('clear')  # Clear screen before returning to main menu
                    break
    elif choice == "4":
        os.system('clear')  # Clear screen for macOS/Linux
        while True:
            print("=== A* SEARCH ===")
            start = input("Enter your current location: ").strip().title()
            goal = input("Enter your goal eatery: ").strip().title()
            path, total_cost, error = a_star(graph, start, goal)

            if path:
                print("Optimal path:", " -> ".join(path))
                print("Total cost:", total_cost)
                # Generate and show highlighted graph
                generate_graph_image(graph, coordinates, highlight_path=path, total_cost=total_cost)
                image_path = "graph_visualization.png"
                try:
                    img = Image.open(image_path)
                    img.show()
                    print(f"Graph visualization opened: {image_path}")
                except FileNotFoundError:
                    print(f"Image file not found: {image_path}")
                    print("Please ensure the graph visualization image exists.")
                except Exception as e:
                    print(f"Error opening image: {e}")
                # Prompt user to return to main menu or exit
                while True:
                    user_choice = input("\nPress 'y' to return to main menu or 'n' to exit: ").lower()
                    if user_choice == 'y':
                        os.system('clear')
                        break
                    elif user_choice == 'n':
                        print("Exiting...")
                        exit()
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                break
            else:
                print(error)
                recovery_choice = handle_error_recovery()
                
                if recovery_choice == "retry":
                    os.system('clear')  # Clear screen before retry
                    continue
                elif recovery_choice == "view_graph":
                    # Regenerate the graph image before viewing (same as option 5)
                    generate_graph_image(graph, coordinates)
                    image_path = "graph_visualization.png"
                    try:
                        img = Image.open(image_path)
                        img.show()
                        print(f"Graph visualization opened: {image_path}")
                    except FileNotFoundError:
                        print(f"Image file not found: {image_path}")
                        print("Please ensure the graph visualization image exists.")
                    except Exception as e:
                        print(f"Error opening image: {e}")
                    input("Press Enter to continue...")
                    os.system('clear')
                    continue
                elif recovery_choice == "exit_to_menu":
                    os.system('clear')  # Clear screen before returning to main menu
                    break
    elif choice == "5":
        os.system('clear')  # Clear screen for macOS/Linux
        print("=== VIEW GRAPH ===")
        # Generate the graph image before viewing (no highlight)
        generate_graph_image(graph, coordinates)
        image_path = "graph_visualization.png"
        try:
            img = Image.open(image_path)
            img.show()  # This will open the image in the default image viewer
            print(f"Graph visualization opened: {image_path}")
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
            print("Please ensure the graph visualization image exists.")
        except Exception as e:
            print(f"Error opening image: {e}")
        # Prompt user to return to main menu or exit
        while True:
            user_choice = input("\nPress 'y' to return to main menu or 'n' to exit: ").lower()
            if user_choice == 'y':
                os.system('clear')  # Clear screen before returning to main menu
                break
            elif user_choice == 'n':
                print("Exiting...")
                exit()
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid option. Please try again.")

