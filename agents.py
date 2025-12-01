"""
Agent implementations for vacuum cleaner robot
Includes Simple Reflex, Model-Based, and Utility-Based agents
"""

import random
from typing import Tuple, Set, Optional, List
from algorithms import astar, bfs, find_nearest_dirty_tile

class Agent:
    """Base agent class"""
    
    def __init__(self, name: str):
        self.name = name
        self.steps_taken = 0
        self.tiles_cleaned = 0
        
    def perceive(self, environment) -> dict:
        """Perceive the environment"""
        x, y = environment.robot_pos
        return {
            'position': (x, y),
            'tile_state': environment.get_tile_state(x, y),
            'neighbors': environment.get_neighbors(x, y),
            'all_clean': environment.is_all_clean()
        }
    
    def act(self, environment, perception: dict) -> Tuple[str, any]:
        """
        Decide on an action based on perception
        
        Returns:
            Tuple of (action_type, action_data)
            action_type: 'clean', 'move', or 'wait'
            action_data: None for clean/wait, (x, y) for move
        """
        raise NotImplementedError
    
    def reset(self):
        """Reset agent statistics"""
        self.steps_taken = 0
        self.tiles_cleaned = 0

class SimpleReflexAgent(Agent):
    """
    Simple Reflex Agent
    Rules:
    - If current tile is dirty, clean it
    - Otherwise, move randomly to a neighbor
    """
    
    def __init__(self):
        super().__init__("Simple Reflex Agent")
    
    def act(self, environment, perception: dict):
        from environment import TileState
        
        # If current tile is dirty, clean it
        if perception['tile_state'] == TileState.DIRTY:
            return ('clean', None)
        
        # Otherwise, move randomly
        neighbors = perception['neighbors']
        if neighbors:
            next_pos = random.choice(neighbors)
            return ('move', next_pos)
        
        return ('wait', None)

class ModelBasedAgent(Agent):
    """
    Model-Based Agent
    Maintains internal state of cleaned tiles and avoids revisiting
    Uses BFS to find path to dirty tiles
    """
    
    def __init__(self, search_algorithm='bfs'):
        super().__init__("Model-Based Agent")
        self.cleaned_tiles: Set[Tuple[int, int]] = set()
        self.current_path: List[Tuple[int, int]] = []
        self.search_algorithm = search_algorithm
        
    def act(self, environment, perception: dict):
        from environment import TileState
        
        # Clean current tile if dirty
        if perception['tile_state'] == TileState.DIRTY:
            self.cleaned_tiles.add(perception['position'])
            return ('clean', None)
        
        # If we have a path, follow it
        if self.current_path:
            next_pos = self.current_path.pop(0)
            return ('move', next_pos)
        
        # Find nearest dirty tile and plan path
        nearest_dirty = find_nearest_dirty_tile(environment, perception['position'])
        
        if nearest_dirty:
            # Use BFS to find path
            if self.search_algorithm == 'bfs':
                result = bfs(environment, perception['position'], nearest_dirty)
            else:
                result = astar(environment, perception['position'], nearest_dirty)
                
            if result.found:
                self.current_path = result.path.copy()
                if self.current_path:
                    next_pos = self.current_path.pop(0)
                    return ('move', next_pos)
        
        # No dirty tiles found, move randomly to unvisited tile
        unvisited_neighbors = [n for n in perception['neighbors'] 
                              if n not in self.cleaned_tiles]
        
        if unvisited_neighbors:
            return ('move', random.choice(unvisited_neighbors))
        elif perception['neighbors']:
            return ('move', random.choice(perception['neighbors']))
        
        return ('wait', None)
    
    def reset(self):
        super().reset()
        self.cleaned_tiles.clear()
        self.current_path.clear()

class UtilityBasedAgent(Agent):
    """
    Utility-Based Agent
    Always moves to the nearest dirty tile using A* search
    Maximizes utility by minimizing distance to dirty tiles
    """
    
    def __init__(self):
        super().__init__("Utility-Based Agent (A*)")
        self.current_path: List[Tuple[int, int]] = []
        self.current_goal: Optional[Tuple[int, int]] = None
        
    def act(self, environment, perception: dict):
        from environment import TileState
        
        # Clean current tile if dirty
        if perception['tile_state'] == TileState.DIRTY:
            self.current_path.clear()
            self.current_goal = None
            return ('clean', None)
        
        # If we have a path to current goal, follow it
        if self.current_path and self.current_goal:
            # Check if goal is still dirty
            if environment.get_tile_state(*self.current_goal) == TileState.DIRTY:
                next_pos = self.current_path.pop(0)
                return ('move', next_pos)
            else:
                # Goal was cleaned (shouldn't happen), replan
                self.current_path.clear()
                self.current_goal = None
        
        # Find nearest dirty tile
        nearest_dirty = find_nearest_dirty_tile(environment, perception['position'])
        
        if nearest_dirty:
            # Plan path using A*
            result = astar(environment, perception['position'], nearest_dirty)
            
            if result.found:
                self.current_path = result.path.copy()
                self.current_goal = nearest_dirty
                if self.current_path:
                    next_pos = self.current_path.pop(0)
                    return ('move', next_pos)
        
        # No dirty tiles, we're done
        return ('wait', None)
    
    def reset(self):
        super().reset()
        self.current_path.clear()
        self.current_goal = None

class GoalBasedAgent(Agent):
    """
    Goal-Based Agent using DFS
    Plans path to dirty tiles using Depth-First Search
    """
    
    def __init__(self):
        super().__init__("Goal-Based Agent (DFS)")
        self.current_path: List[Tuple[int, int]] = []
        
    def act(self, environment, perception: dict):
        from environment import TileState
        from algorithms import dfs
        
        # Clean current tile if dirty
        if perception['tile_state'] == TileState.DIRTY:
            self.current_path.clear()
            return ('clean', None)
        
        # If we have a path, follow it
        if self.current_path:
            next_pos = self.current_path.pop(0)
            return ('move', next_pos)
        
        # Find a dirty tile and plan path
        dirty_tiles = environment.get_dirty_tiles()
        
        if dirty_tiles:
            target = dirty_tiles[0]  # Take first dirty tile
            result = dfs(environment, perception['position'], target)
            
            if result.found:
                self.current_path = result.path.copy()
                if self.current_path:
                    next_pos = self.current_path.pop(0)
                    return ('move', next_pos)
        
        # No dirty tiles
        return ('wait', None)
    
    def reset(self):
        super().reset()
        self.current_path.clear()
