import pygame
import heapq
from maze import SearchSpace
from const import RED,BLUE,WHITE,YELLOW,ORANGE,PURPLE
def DFS(g: SearchSpace, sc: pygame.Surface):
    open_set = [g.start.id]
    closed_set = []
    father = [-1] * g.get_length()

    g.start.set_color(ORANGE, sc)  # Set the start node to orange
    g.goal.set_color(PURPLE, sc)  # Set the goal node to purple
    while open_set:
        current_node_id = open_set.pop()
        current_node = g.get_node_by_id(current_node_id)

        if(current_node_id!=g.start.id and current_node_id!=g.goal.id):
            # Set the current node to yellow
            current_node.set_color(YELLOW, sc)  
            pygame.time.delay(50)
        if g.is_goal(current_node):
            break
        
        if current_node_id in closed_set:
            continue

        for neighbor in g.get_neighbors(current_node):
            neighbor_id = neighbor.id
            if neighbor_id not in closed_set and neighbor_id not in open_set:
                open_set.append(neighbor_id)
                father[neighbor_id] = current_node.id
                # Color the neighbor red (Node in open_set)
                if(neighbor_id!=g.start.id and neighbor_id!=g.goal.id):
                    g.get_node_by_id(neighbor_id).set_color(RED, sc)

        closed_set.append(current_node_id)
  
        if(current_node_id!=g.start.id and current_node_id!=g.goal.id):
            current_node.set_color(BLUE, sc)  

    # Here, you can trace back the path and color it white
    if g.is_goal(current_node):
        path = [current_node.id]
        while current_node.id != g.start.id:
            current_node = g.get_node_by_id(father[current_node.id])
            path.append(current_node.id)

        # Reverse the path
        path = path[::-1]

        # Color the path white (The path you found)
        for i in range(1, len(path)):
            node1 = g.get_node_by_id(path[i - 1])
            node2 = g.get_node_by_id(path[i])
            x1, y1 = node1.rect.center
            x2, y2 = node2.rect.center
            pygame.draw.line(sc, WHITE, (x1, y1), (x2, y2), 5)  # Adjust line width as needed
            pygame.time.delay(50)
            pygame.display.update()
    else:
        raise NotImplementedError('not implemented')

def BFS(g: SearchSpace, sc: pygame.Surface):
    open_set = [g.start.id]
    closed_set = []
    father = [-1] * g.get_length()
    g.start.set_color(ORANGE, sc)  # Set the start node to orange
    g.goal.set_color(PURPLE, sc)  # Set the goal node to purple

    while open_set:
        current_node_id = open_set.pop(0)  # Pop the first node in the queue
        current_node = g.get_node_by_id(current_node_id)

        if(current_node_id!=g.start.id and current_node_id!=g.goal.id):
            # Set the current node to yellow
            current_node.set_color(YELLOW, sc)  
            pygame.time.delay(20)

        if g.is_goal(current_node):      
            break 

        if current_node_id in closed_set:
            continue

        for neighbor in g.get_neighbors(current_node):
            neighbor_id = neighbor.id
            if neighbor_id not in closed_set and neighbor_id not in open_set:
                open_set.append(neighbor_id)
                father[neighbor_id] = current_node.id
                # Color the neighbor red (Node in open_set)
                if(neighbor_id!=g.start.id and neighbor_id!=g.goal.id):
                    g.get_node_by_id(neighbor_id).set_color(RED, sc)

        closed_set.append(current_node_id)
        if(current_node_id!=g.start.id and current_node_id!=g.goal.id):
            current_node.set_color(BLUE, sc)  
        pygame.display.update()
            # Here, you can trace back the path and color it white
    if g.is_goal(current_node):
        path = [current_node.id]
        while current_node.id != g.start.id:
            current_node = g.get_node_by_id(father[current_node.id])
            path.append(current_node.id)

        # Reverse the path
        path = path[::-1]

        # Color the path white (The path you found)
        for i in range(1, len(path)):
            node1 = g.get_node_by_id(path[i - 1])
            node2 = g.get_node_by_id(path[i])
            x1, y1 = node1.rect.center
            x2, y2 = node2.rect.center
            pygame.draw.line(sc, WHITE, (x1, y1), (x2, y2), 5)  # Adjust line width as needed
            pygame.time.delay(50)
            pygame.display.update()
    else:
        raise NotImplementedError('not implemented')

def UCS(g: SearchSpace, sc: pygame.Surface):
    open_set = [(0, g.start.id)]
    closed_set = []
    father = [-1] * g.get_length()
    cost = [100_000] * g.get_length()
    cost[g.start.id] = 0

    g.start.set_color(ORANGE, sc)  # Set the start node to orange
    g.goal.set_color(PURPLE, sc)  # Set the goal node to purple
    while open_set:
        current_cost, current_node_id = heapq.heappop(open_set)
        current_node = g.get_node_by_id(current_node_id)
        
        if(current_node_id!=g.start.id and current_node_id!=g.goal.id):
            # Set the current node to yellow
            current_node.set_color(YELLOW, sc)  
            pygame.time.delay(20)

        if g.is_goal(current_node):
            break

        if current_node_id in closed_set:
            continue

        for neighbor in g.get_neighbors(current_node):
            neighbor_id = neighbor.id
            new_cost = cost[current_node_id] + 1  

            if neighbor_id not in closed_set and (neighbor_id not in [node[1] for node in open_set] or new_cost < cost[neighbor_id]):
                cost[neighbor_id] = new_cost
                father[neighbor_id] = current_node.id
                # Add the neighbor to the open set with its cost
                heapq.heappush(open_set, (new_cost, neighbor_id))
                # Color the neighbor red (Node in open_set)
                if(neighbor_id!=g.start.id and neighbor_id!=g.goal.id):
                    g.get_node_by_id(neighbor_id).set_color(RED, sc)

        closed_set.append(current_node_id)

        if(current_node_id!=g.start.id and current_node_id!=g.goal.id):
            current_node.set_color(BLUE, sc)

    # Here, you can trace back the path and color it white
    if g.is_goal(current_node):
        path = [current_node.id]
        while current_node.id != g.start.id:
            current_node = g.get_node_by_id(father[current_node.id])
            path.append(current_node.id)

        # Reverse the path
        path = path[::-1]

        # Color the path white (The path you found)
        for i in range(1, len(path)):
            node1 = g.get_node_by_id(path[i - 1])
            node2 = g.get_node_by_id(path[i])
            x1, y1 = node1.rect.center
            x2, y2 = node2.rect.center
            pygame.draw.line(sc, WHITE, (x1, y1), (x2, y2), 5)  # Adjust line width as needed
            pygame.time.delay(50)
            pygame.display.update()
    else:
        raise NotImplementedError('not implemented')

def AStar(g: SearchSpace, sc: pygame.Surface):
    def heuristic(node, goal):
        # A simple Euclidean distance heuristic
        x1, y1 = node.rect.center
        x2, y2 = goal.rect.center
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    open_set = [(0, g.start.id)]
    closed_set = []
    father = [-1] * g.get_length()
    cost = [float('inf')] * g.get_length()
    cost[g.start.id] = 0

    g.start.set_color(ORANGE, sc)  # Set the start node to orange
    g.goal.set_color(PURPLE, sc)  # Set the goal node to purple
    
    while open_set:
        open_set.sort()  # Sort the open set by cost
        _, current_node_id = open_set.pop(0)  # Pop the node with the lowest cost
        current_node = g.get_node_by_id(current_node_id)

        if(current_node_id!=g.start.id and current_node_id!=g.goal.id):
            # Set the current node to yellow
            current_node.set_color(YELLOW, sc)  
            pygame.time.delay(50)

        if g.is_goal(current_node):
            break 

        if current_node_id in closed_set:
            continue

        for neighbor in g.get_neighbors(current_node):
            neighbor_id = neighbor.id
            neighbor_cost = cost[current_node_id] + 1  # Assuming uniform cost
            if neighbor_cost < cost[neighbor_id]:
                father[neighbor_id] = current_node.id
                cost[neighbor_id] = neighbor_cost
                priority = neighbor_cost + heuristic(neighbor, g.goal)  # A* cost function
                open_set.append((priority, neighbor_id))
                # Color the neighbor red (Node in open_set)
                if(neighbor_id!=g.start.id and neighbor_id!=g.goal.id):
                    g.get_node_by_id(neighbor_id).set_color(RED, sc)

        closed_set.append(current_node_id)
        if(current_node_id!=g.start.id and current_node_id!=g.goal.id):
            current_node.set_color(BLUE, sc)
        pygame.display.update()
        
    if g.is_goal(current_node):
        path = [current_node.id]
        while current_node.id != g.start.id:
            current_node = g.get_node_by_id(father[current_node.id])
            path.append(current_node.id)

        # Reverse the path
        path = path[::-1]

        # Color the path white (The path you found)
        for i in range(1, len(path)):
            node1 = g.get_node_by_id(path[i - 1])
            node2 = g.get_node_by_id(path[i])
            x1, y1 = node1.rect.center
            x2, y2 = node2.rect.center
            pygame.draw.line(sc, WHITE, (x1, y1), (x2, y2), 5)  # Adjust line width as needed
            pygame.time.delay(50)
            pygame.display.update()
    else:
        raise NotImplementedError('not implemented')