"""
Search algorithms for vacuum cleaner robot
Implements BFS, DFS, and A* with visualization data
"""

from collections import deque
from typing import List, Tuple, Set, Optional, Dict
import heapq

class SearchResult:
    """Container for search algorithm results"""
    
    def __init__(self):
        self.path: List[Tuple[int, int]] = []
        self.nodes_expanded: int = 0
        self.nodes_in_frontier: int = 0
        self.explored: Set[Tuple[int, int]] = set()
        self.frontier_history: List[Set[Tuple[int, int]]] = []
        self.path_cost: int = 0
        self.found: bool = False

def reconstruct_path(came_from: Dict, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Reconstruct path from start to goal using came_from dict"""
    path = []
    current = goal
    
    while current != start:
        path.append(current)
        current = came_from[current]
    
    path.reverse()
    return path

def bfs(environment, start: Tuple[int, int], goal: Tuple[int, int]) -> SearchResult:
    """
    Breadth-First Search
    
    Args:
        environment: The grid environment
        start: Starting position (x, y)
        goal: Goal position (x, y)
    
    Returns:
        SearchResult with path and statistics
    """
    result = SearchResult()
    
    if start == goal:
        result.found = True
        return result
    
    frontier = deque([start])
    came_from = {start: None}
    explored = set()
    
    while frontier:
        result.frontier_history.append(set(frontier))
        current = frontier.popleft()
        explored.add(current)
        result.nodes_expanded += 1
        
        if current == goal:
            result.path = reconstruct_path(came_from, start, goal)
            result.path_cost = len(result.path)
            result.explored = explored
            result.found = True
            return result
        
        for neighbor in environment.get_neighbors(*current):
            if neighbor not in came_from and neighbor not in explored:
                frontier.append(neighbor)
                came_from[neighbor] = current
    
    result.explored = explored
    return result

def dfs(environment, start: Tuple[int, int], goal: Tuple[int, int]) -> SearchResult:
    """
    Depth-First Search
    
    Args:
        environment: The grid environment
        start: Starting position (x, y)
        goal: Goal position (x, y)
    
    Returns:
        SearchResult with path and statistics
    """
    result = SearchResult()
    
    if start == goal:
        result.found = True
        return result
    
    frontier = [start]
    came_from = {start: None}
    explored = set()
    
    while frontier:
        result.frontier_history.append(set(frontier))
        current = frontier.pop()
        
        if current in explored:
            continue
            
        explored.add(current)
        result.nodes_expanded += 1
        
        if current == goal:
            result.path = reconstruct_path(came_from, start, goal)
            result.path_cost = len(result.path)
            result.explored = explored
            result.found = True
            return result
        
        for neighbor in environment.get_neighbors(*current):
            if neighbor not in came_from and neighbor not in explored:
                frontier.append(neighbor)
                came_from[neighbor] = current
    
    result.explored = explored
    return result

def heuristic(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """Manhattan distance heuristic"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def astar(environment, start: Tuple[int, int], goal: Tuple[int, int]) -> SearchResult:
    """
    A* Search with Manhattan distance heuristic
    
    Args:
        environment: The grid environment
        start: Starting position (x, y)
        goal: Goal position (x, y)
    
    Returns:
        SearchResult with path and statistics
    """
    result = SearchResult()
    
    if start == goal:
        result.found = True
        return result
    
    frontier = [(0, start)]
    came_from = {start: None}
    g_score = {start: 0}
    explored = set()
    
    while frontier:
        # Track frontier for visualization
        result.frontier_history.append({pos for _, pos in frontier})
        
        _, current = heapq.heappop(frontier)
        
        if current in explored:
            continue
            
        explored.add(current)
        result.nodes_expanded += 1
        
        if current == goal:
            result.path = reconstruct_path(came_from, start, goal)
            result.path_cost = len(result.path)
            result.explored = explored
            result.found = True
            return result
        
        for neighbor in environment.get_neighbors(*current):
            if neighbor in explored:
                continue
                
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_score, neighbor))
                came_from[neighbor] = current
    
    result.explored = explored
    return result

def find_nearest_dirty_tile(environment, start: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    """
    Find the nearest dirty tile using Manhattan distance
    
    Returns:
        Position of nearest dirty tile, or None if none exist
    """
    dirty_tiles = environment.get_dirty_tiles()
    
    if not dirty_tiles:
        return None
    
    nearest = min(dirty_tiles, key=lambda pos: heuristic(start, pos))
    return nearest
