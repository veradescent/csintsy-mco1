import math # For euclidean distance
import heapq # Implement priority queue
import os # For screen clearing
from PIL import Image # For opening images

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
    "Taft-Estrada": {"Leon Guinto-Estrada": 95, "Starbucks": 29, "North Gate": 99},
    "North Gate": {"Taft-Estrada": 99, "Taft-Dagonoy": 72, "CBTL": 73},
    "CBTL": {"North Gate": 73},
    "Starbucks": {"Taft-Estrada": 29, "South Gate": 12},
    "South Gate": {"Starbucks": 12, "McDonald's": 54, "Kitchen City": 82},
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
    "Starbucks": (14.56417, 120.99447),
    "South Gate": (14.56409, 120.99449),
    "McDonald's": (14.56363, 120.99465),
    "Tomo Coffee": (14.56342, 120.99476),
    "Kitchen City": (14.56382, 120.99379),
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
    Check if start and goal nodes exist in the graph.
    Returns (is_valid, error_message)
    """
    if start not in graph:
        return False, f"Start node '{start}' does not exist in the graph."
    
    if goal not in graph:
        return False, f"Goal node '{goal}' does not exist in the graph."
    
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
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            
            path, total_cost, error = uniform_cost_search(graph, start, goal)
            
            if path:
                print("Optimal path:", " -> ".join(path))
                print("Total cost:", total_cost)
                
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
                break
            else:
                print(error)
                recovery_choice = handle_error_recovery()
                
                if recovery_choice == "retry":
                    os.system('clear')  # Clear screen before retry
                    continue
                elif recovery_choice == "view_graph":
                    # Dummy path for the image file
                    image_path = "graph_visualization.png"
                    try:
                        # Open the image using Pillow
                        img = Image.open(image_path)
                        img.show()  # This will open the image in the default image viewer
                        print(f"Graph visualization opened: {image_path}")
                    except FileNotFoundError:
                        print(f"Image file not found: {image_path}")
                        print("Please ensure the graph visualization image exists.")
                    except Exception as e:
                        print(f"Error opening image: {e}")
                    input("Press Enter to continue...")
                    continue
                elif recovery_choice == "exit_to_menu":
                    os.system('clear')  # Clear screen before returning to main menu
                    break
    elif choice == "4":
        os.system('clear')  # Clear screen for macOS/Linux
        while True:
            print("=== A* SEARCH ===")
            start = input("Enter your current location: ")
            goal = input("Enter your goal eatery: ")
            path, total_cost, error = a_star(graph, start, goal)

            if path:
                print("Optimal path:", " -> ".join(path))
                print("Total cost:", total_cost)
                
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
                break
            else:
                print(error)
                recovery_choice = handle_error_recovery()
                
                if recovery_choice == "retry":
                    os.system('clear')  # Clear screen before retry
                    continue
                elif recovery_choice == "view_graph":
                    # Dummy path for the image file
                    image_path = "graph_visualization.png"
                    try:
                        # Open the image using Pillow
                        img = Image.open(image_path)
                        img.show()  # This will open the image in the default image viewer
                        print(f"Graph visualization opened: {image_path}")
                    except FileNotFoundError:
                        print(f"Image file not found: {image_path}")
                        print("Please ensure the graph visualization image exists.")
                    except Exception as e:
                        print(f"Error opening image: {e}")
                    input("Press Enter to continue...")
                    continue
                elif recovery_choice == "exit_to_menu":
                    os.system('clear')  # Clear screen before returning to main menu
                    break
    elif choice == "5":
        # Dummy path for the image file
        image_path = "graph_visualization.png"
        try:
            # Open the image using Pillow
            img = Image.open(image_path)
            img.show()  # This will open the image in the default image viewer
            print(f"Graph visualization opened: {image_path}")
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")
            print("Please ensure the graph visualization image exists.")
        except Exception as e:
            print(f"Error opening image: {e}")
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid option. Please try again.")

