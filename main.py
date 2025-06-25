import math # For euclidean distance
import heapq # Implement priority queue
import os # For screen clearing
from PIL import Image # For opening images
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import platform

graph = {
    "sherwood place": {"jollibee": 60},
    "jollibee": {"sherwood place": 60, "taft-castro": 44},
    "taft-castro": {"jollibee": 44, "gokongwei hall": 28, "agno-castro": 85},
    "gokongwei hall": {"taft-castro": 28, "taft-dagonoy": 85},
    "agno-castro": {"taft-castro": 85, "agno food court": 29, "andrew gonzales hall": 62},
    "agno food court": {"agno-castro": 29, "24 chicken": 44},
    "24 chicken": {"agno food court": 44, "agno-fidel a. reyes": 41},
    "agno-fidel a. reyes": {"24 chicken": 41, "taft-dagonoy": 80},
    "andrew gonzales hall": {"perico's": 23, "agno-castro": 62},
    "perico's": {"the barn": 53, "andrew gonzales hall": 23},
    "the barn": {"perico's": 53},
    "taft-dagonoy": {"gokongwei hall": 85, "tinuhog ni benny": 59, "north gate": 72, "agno-fidel a. reyes": 80},
    "tinuhog ni benny": {"taft-dagonoy": 59, "leon guinto-dagonoy": 40},
    "leon guinto-dagonoy": {"tinuhog ni benny": 40, "drip kofi": 84},
    "drip kofi": {"leon guinto-dagonoy": 84, "chomp chomp": 35},
    "chomp chomp": {"drip kofi": 35, "leon guinto-estrada": 42},
    "leon guinto-estrada": {"chomp chomp": 42, "taft-estrada": 95},
    "taft-estrada": {"south gate": 41, "leon guinto-estrada": 95, "north gate": 99},
    "north gate": {"taft-estrada": 99, "taft-dagonoy": 72, "cbtl": 73},
    "cbtl": {"north gate": 73},
    "south gate": {"taft-estrada": 41, "mcdonald's": 54, "kitchen city": 82},
    "mcdonald's": {"south gate": 54, "tomo coffee": 28},
    "tomo coffee": {"mcdonald's": 28},
    "kitchen city": {"south gate": 82},
}

coordinates = {
    "sherwood place": (14.56757, 120.99283),
    "jollibee": (14.56709, 120.99308),
    "taft-castro": (14.56672, 120.99324),
    "gokongwei hall": (14.56648, 120.99336),
    "agno-castro": (14.56641, 120.99252),
    "agno food court": (14.56619, 120.99265),
    "24 chicken": (14.56585, 120.99284),
    "agno-fidel a. reyes": (14.56554, 120.99299),
    "andrew gonzales hall": (14.56692, 120.99228),
    "perico's": (14.5671, 120.99218),
    "the barn": (14.56754, 120.99197),
    "taft-dagonoy": (14.56577, 120.9937),
    "tinuhog ni benny": (14.56598, 120.99419),
    "leon guinto-dagonoy": (14.56611, 120.99454),
    "drip kofi": (14.56542, 120.99489),
    "chomp chomp": (14.56512, 120.99501),
    "leon guinto-estrada": (14.56477, 120.99516),
    "taft-estrada": (14.5644, 120.99435),
    "north gate": (14.56518, 120.99396),
    "cbtl": (14.56497, 120.99333),
    "south gate": (14.56409, 120.99449),
    "mcdonald's": (14.56363, 120.99465),
    "tomo coffee": (14.56342, 120.99476),
    "kitchen city": (14.56382, 120.99379),
}

# List of non-eatery nodes that cannot be used as end goals
non_eatery_nodes = {
    "gokongwei hall", "taft-castro", "agno-castro", "agno-fidel a. reyes", "taft-dagonoy",
    "leon guinto-dagonoy", "leon guinto-estrada", "taft-estrada", "north gate", "south gate"
}

def format_node_name_for_display(node_name):
    """
    Convert node name to title case for display purposes.
    Special handling for CBTL to keep it as CBTL.
    """
    if node_name.lower() == "cbtl":
        return "CBTL"
    elif node_name.lower() == "perico's":
        return "Perico's"
    return node_name.title()

node_name_map = {name.lower(): name for name in graph.keys()}
def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def add_node(graph):
    clear_screen()
    print("=== ADD NODE TO GRAPH ===")
    new_node = input("Enter the name of the new node: ").strip()

    if new_node in graph:
        print(f"Node '{format_node_name_for_display(new_node)}' already exists.")
    else:
        while True:
            try:
                x = float(input("Enter X coordinate for the node: "))
                y = float(input("Enter Y coordinate for the node: "))
                coordinates[new_node] = (x, y)
                break
            except ValueError:
                print("Invalid coordinates. Please enter numeric values for X and Y.\n")

        is_non_eatery = input("Is this a NON-eatery node? (y/n): ").strip().lower()
        if is_non_eatery == "y":
            non_eatery_nodes.add(new_node)

        graph[new_node] = {}
        node_name_map[new_node.lower()] = new_node
        print(f"\nNode '{format_node_name_for_display(new_node)}' has been added with coordinates ({x}, {y}).")
        print("\nNote: You must connect this node to at least one other node before finishing.")

        while True:
            connect_to = input("Enter a node to connect to (or type 'done' to finish): ").strip()
            if connect_to.lower() == 'done':
                # Check if the new node has at least one connection
                if len(graph[new_node]) == 0:
                    print(f"Error: Node '{format_node_name_for_display(new_node)}' must have at least one connection before finishing.")
                    print("Please connect it to at least one other node.\n")
                    continue
                break
            existing_node = node_name_map.get(connect_to.lower())
            if existing_node is None:
                print(f"Node '{format_node_name_for_display(connect_to)}' does not exist. Please enter a valid node.\n")
                continue
            try:
                cost = int(input(f"Enter cost from '{format_node_name_for_display(new_node)}' to '{format_node_name_for_display(existing_node)}': "))
            except ValueError:
                print("Invalid cost. Please enter a number.\n")
                continue
            graph[new_node][existing_node] = cost
            graph[existing_node][new_node] = cost
            print(f"Connected '{format_node_name_for_display(new_node)}' <-> '{format_node_name_for_display(existing_node)}' with cost {cost}.\n")

    input("\nPress Enter to return to the main menu...")
    clear_screen()

def remove_node(graph):
    clear_screen()
    print("=== REMOVE NODE FROM GRAPH ===")

    node_to_remove = input("Enter the name of the node to remove: ").strip()
    real_node = node_name_map.get(node_to_remove.lower())

    if real_node is None or real_node not in graph:
        print(f"Error: Node '{format_node_name_for_display(node_to_remove)}' does not exist in the graph.\n")
        input("\nPress Enter to return to the menu...")
        clear_screen()
        return

    # Get the neighbors of the node to be removed
    neighbors = list(graph[real_node].keys())
    
    # Remove connections from neighbors to the target node
    for neighbor in neighbors:
        graph[neighbor].pop(real_node, None)
    
    # Remove the target node
    graph.pop(real_node)
    
    # Find all nodes that are still connected to the main graph
    # Start from any remaining node (not the removed one or its neighbors)
    remaining_nodes = set(graph.keys()) - set(neighbors)
    if remaining_nodes:
        # Use BFS to find all connected nodes from a starting node
        start_node = next(iter(remaining_nodes))
        connected_nodes = set()
        to_visit = [start_node]
        visited = set()
        
        while to_visit:
            current = to_visit.pop(0)
            if current in visited:
                continue
            visited.add(current)
            connected_nodes.add(current)
            
            for neighbor in graph[current]:
                if neighbor not in visited:
                    to_visit.append(neighbor)
        
        # Find disconnected nodes (nodes not in connected_nodes)
        all_nodes = set(graph.keys())
        disconnected_nodes = all_nodes - connected_nodes
        
        # Remove disconnected nodes
        for node in disconnected_nodes:
            graph.pop(node)
            coordinates.pop(node, None)
            node_name_map.pop(node.lower(), None)
            non_eatery_nodes.discard(node)
    else:
        # If no remaining nodes, all neighbors are disconnected
        disconnected_nodes = set(neighbors)
        for node in disconnected_nodes:
            graph.pop(node)
            coordinates.pop(node, None)
            node_name_map.pop(node.lower(), None)
            non_eatery_nodes.discard(node)

    # Remove the target node from other data structures
    coordinates.pop(real_node, None)
    node_name_map.pop(real_node.lower(), None)
    non_eatery_nodes.discard(real_node)

    # Display results
    print(f"Node '{format_node_name_for_display(real_node)}' removed successfully.")
    if disconnected_nodes:
        print(f"Also removed disconnected nodes: {', '.join([format_node_name_for_display(node) for node in disconnected_nodes])}")
    print()
    input("Press Enter to return to the menu...")
    clear_screen()

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
        return False, f"Start node '{format_node_name_for_display(start)}' does not exist in the graph."
    if goal not in graph:
        return False, f"Goal node '{format_node_name_for_display(goal)}' does not exist in the graph."
    # Non-eatery nodes that cannot be used as end goals
    if goal in non_eatery_nodes:
        return False, f"Error: '{format_node_name_for_display(goal)}' is not an eatery and cannot be used as the end goal. Please choose a valid eatery as the goal."
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
    # Create formatted labels for display
    labels = {node: format_node_name_for_display(node) for node in G.nodes()}
    # Draw all edges in gray and nodes/labels on top
    nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors, edge_color='gray', node_size=1400, font_size=12)
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

    choice = input("\nChoose an option: ")

    if choice == "1":
        add_node(graph)
    elif choice == "2":
        remove_node(graph)
    elif choice == "3":
        clear_screen() # Clear screen for macOS/Linux
        while True:
            print("=== UNIFORM COST SEARCH (UCS) ===")
            user_start = input("Enter your current location: ").strip()
            user_goal = input("Enter your goal eatery: ").strip()
            start = node_name_map.get(user_start.lower())
            goal = node_name_map.get(user_goal.lower())
            path, total_cost, error = uniform_cost_search(graph, start, goal)
            
            if path:
                formatted_path = [format_node_name_for_display(node) for node in path]
                print("\nOptimal path:", " -> ".join(formatted_path))
                print("Total cost:", total_cost)
                # Generate and show highlighted graph
                generate_graph_image(graph, coordinates, highlight_path=path, total_cost=total_cost)
                image_path = "graph_visualization.png"
                try:
                    img = Image.open(image_path)
                    img.show()
                    print(f"\nGraph visualization opened: {image_path}")
                except FileNotFoundError:
                    print(f"\nImage file not found: {image_path}")
                    print("Please ensure the graph visualization image exists.")
                except Exception as e:
                    print(f"\nError opening image: {e}")
                # Prompt user to return to main menu or exit
                input("\nPress Enter to return to the menu...")
                clear_screen()
                break
            else:
                print(error)
                recovery_choice = handle_error_recovery()
                
                if recovery_choice == "retry":
                    clear_screen()  # Clear screen before retry
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
                    clear_screen()
                    continue
                elif recovery_choice == "exit_to_menu":
                    clear_screen()  # Clear screen before returning to main menu
                    break
    elif choice == "4":
        clear_screen() # Clear screen for macOS/Linux
        while True:
            print("=== A* SEARCH ===")
            user_start = input("Enter your current location: ").strip()
            user_goal = input("Enter your goal eatery: ").strip()
            start = node_name_map.get(user_start.lower())
            goal = node_name_map.get(user_goal.lower())
            path, total_cost, error = a_star(graph, start, goal)

            if path:
                formatted_path = [format_node_name_for_display(node) for node in path]
                print("\nOptimal path:", " -> ".join(formatted_path))
                print("Total cost:", total_cost)
                # Generate and show highlighted graph
                generate_graph_image(graph, coordinates, highlight_path=path, total_cost=total_cost)
                image_path = "graph_visualization.png"
                try:
                    img = Image.open(image_path)
                    img.show()
                    print(f"\nGraph visualization opened: {image_path}")
                except FileNotFoundError:
                    print(f"\nImage file not found: {image_path}")
                    print("Please ensure the graph visualization image exists.")
                except Exception as e:
                    print(f"\nError opening image: {e}")
                # Prompt user to return to main menu or exit
                input("\nPress Enter to return to the menu...")
                clear_screen()
                break
            else:
                print(error)
                recovery_choice = handle_error_recovery()
                
                if recovery_choice == "retry":
                    clear_screen()  # Clear screen before retry
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
                    clear_screen()
                    continue
                elif recovery_choice == "exit_to_menu":
                    clear_screen() # Clear screen before returning to main menu
                    break
    elif choice == "5":
        clear_screen()  # Clear screen for macOS/Linux
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
        input("\nPress Enter to return to the menu...")
        clear_screen()
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid option. Please try again.")

