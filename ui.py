"""
Pygame UI for Vacuum Cleaner Robot Simulation
Handles rendering, animations, and user interface
"""

import pygame
import sys
from typing import Optional, Tuple
from environment import Environment, TileState
from agents import Agent

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

class VacuumUI:
    """UI handler for vacuum cleaner simulation"""
    
    def __init__(self, environment: Environment, cell_size: int = 35):
        """
        Initialize UI
        
        Args:
            environment: The environment to visualize
            cell_size: Size of each grid cell in pixels
        """
        pygame.init()
        
        self.environment = environment
        self.cell_size = cell_size
        self.panel_width = 300
        
        # Calculate window size
        self.grid_width = environment.width * cell_size
        self.grid_height = environment.height * cell_size
        self.window_width = self.grid_width + self.panel_width
        self.window_height = self.grid_height
        
        # Create window
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Vacuum Cleaner Robot Simulation")
        
        # Fonts
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        # Animation
        self.robot_animation_progress = 0.0
        self.robot_target_pos = None
        self.robot_display_pos = list(environment.robot_pos)
        
        # Visualization
        self.show_explored = False
        self.explored_tiles = set()
        self.frontier_tiles = set()
        
        # Performance metrics
        self.steps_taken = 0
        self.cleaning_actions = 0
        self.start_time = pygame.time.get_ticks()
        
        # FPS
        self.clock = pygame.time.Clock()
        self.fps = 30
        
    def handle_robot_move(self, new_x: int, new_y: int):
        """Start robot movement animation"""
        self.robot_target_pos = (new_x, new_y)
        self.robot_animation_progress = 0.0
        self.steps_taken += 1
        
    def update_animation(self, dt: float):
        """Update animation state"""
        if self.robot_target_pos:
            # Animate robot movement
            self.robot_animation_progress += dt * 5  # Animation speed
            
            if self.robot_animation_progress >= 1.0:
                # Animation complete
                self.robot_display_pos = list(self.robot_target_pos)
                self.robot_target_pos = None
                self.robot_animation_progress = 0.0
            else:
                # Interpolate position
                current_x, current_y = self.robot_display_pos
                target_x, target_y = self.robot_target_pos
                
                t = self.robot_animation_progress
                # Ease-in-out interpolation
                t = t * t * (3 - 2 * t)
                
                self.robot_display_pos[0] = current_x + (target_x - current_x) * t
                self.robot_display_pos[1] = current_y + (target_y - current_y) * t
    
    def draw_grid(self):
        """Draw the environment grid"""
        for y in range(self.environment.height):
            for x in range(self.environment.width):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                # Get tile state and draw
                tile_state = self.environment.get_tile_state(x, y)
                
                if tile_state == TileState.OBSTACLE:
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)
                elif tile_state == TileState.DIRTY:
                    pygame.draw.rect(self.screen, BROWN, rect)
                else:  # CLEAN
                    pygame.draw.rect(self.screen, LIGHT_GREEN, rect)
                
                # Draw explored/frontier visualization
                if self.show_explored:
                    if (x, y) in self.explored_tiles:
                        overlay = pygame.Surface((self.cell_size, self.cell_size))
                        overlay.set_alpha(100)
                        overlay.fill(BLUE)
                        self.screen.blit(overlay, rect)
                    elif (x, y) in self.frontier_tiles:
                        overlay = pygame.Surface((self.cell_size, self.cell_size))
                        overlay.set_alpha(100)
                        overlay.fill(YELLOW)
                        self.screen.blit(overlay, rect)
                
                # Draw grid lines
                pygame.draw.rect(self.screen, GRAY, rect, 1)
    
    def draw_robot(self):
        """Draw the vacuum robot"""
        # Use display position for smooth animation
        display_x, display_y = self.robot_display_pos
        
        center_x = int(display_x * self.cell_size + self.cell_size / 2)
        center_y = int(display_y * self.cell_size + self.cell_size / 2)
        radius = int(self.cell_size * 0.35)
        
        # Draw robot body (circle)
        pygame.draw.circle(self.screen, RED, (center_x, center_y), radius)
        pygame.draw.circle(self.screen, BLACK, (center_x, center_y), radius, 2)
        
        # Draw robot "eye" (direction indicator)
        eye_offset = radius // 2
        pygame.draw.circle(self.screen, WHITE, (center_x, center_y - eye_offset), radius // 3)
        pygame.draw.circle(self.screen, BLACK, (center_x, center_y - eye_offset), radius // 3, 1)
    
    def draw_control_panel(self, agent: Optional[Agent], is_running: bool, is_complete: bool):
        """Draw the control panel on the right side"""
        panel_x = self.grid_width
        
        # Background
        panel_rect = pygame.Rect(panel_x, 0, self.panel_width, self.window_height)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 2)
        
        y_offset = 20
        
        # Title
        title = self.font_large.render("Control Panel", True, BLACK)
        self.screen.blit(title, (panel_x + 20, y_offset))
        y_offset += 50
        
        # Agent info
        if agent:
            agent_text = self.font_medium.render(f"Agent:", True, BLACK)
            self.screen.blit(agent_text, (panel_x + 20, y_offset))
            y_offset += 25
            
            agent_name = self.font_small.render(agent.name, True, BLUE)
            self.screen.blit(agent_name, (panel_x + 30, y_offset))
            y_offset += 30
        
        # Status
        status_text = "Running" if is_running else ("Complete!" if is_complete else "Paused")
        status_color = GREEN if is_running else (ORANGE if is_complete else RED)
        status = self.font_medium.render(f"Status: {status_text}", True, status_color)
        self.screen.blit(status, (panel_x + 20, y_offset))
        y_offset += 40
        
        # Separator line
        pygame.draw.line(self.screen, BLACK, (panel_x + 10, y_offset), 
                        (panel_x + self.panel_width - 10, y_offset), 2)
        y_offset += 20
        
        # Performance Metrics
        metrics_title = self.font_medium.render("Metrics", True, BLACK)
        self.screen.blit(metrics_title, (panel_x + 20, y_offset))
        y_offset += 30
        
        # Steps taken
        steps_text = self.font_small.render(f"Steps: {self.steps_taken}", True, BLACK)
        self.screen.blit(steps_text, (panel_x + 30, y_offset))
        y_offset += 25
        
        # Tiles cleaned
        cleaned_text = self.font_small.render(
            f"Cleaned: {self.environment.cleaned_dirt}/{self.environment.total_dirt}",
            True, BLACK
        )
        self.screen.blit(cleaned_text, (panel_x + 30, y_offset))
        y_offset += 25
        
        # Cleanliness percentage
        cleanliness = self.environment.get_cleanliness_percentage()
        clean_text = self.font_small.render(f"Clean: {cleanliness:.1f}%", True, BLACK)
        self.screen.blit(clean_text, (panel_x + 30, y_offset))
        y_offset += 25
        
        # Efficiency (tiles cleaned per step)
        if self.steps_taken > 0:
            efficiency = (self.environment.cleaned_dirt / self.steps_taken) * 100
            eff_text = self.font_small.render(f"Efficiency: {efficiency:.1f}%", True, BLACK)
            self.screen.blit(eff_text, (panel_x + 30, y_offset))
            y_offset += 25
        
        # Time elapsed
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        time_text = self.font_small.render(f"Time: {elapsed_time:.1f}s", True, BLACK)
        self.screen.blit(time_text, (panel_x + 30, y_offset))
        y_offset += 40
        
        # Separator line
        pygame.draw.line(self.screen, BLACK, (panel_x + 10, y_offset), 
                        (panel_x + self.panel_width - 10, y_offset), 2)
        y_offset += 20
        
        # Controls
        controls_title = self.font_medium.render("Controls", True, BLACK)
        self.screen.blit(controls_title, (panel_x + 20, y_offset))
        y_offset += 30
        
        # Instructions
        instructions = [
            "SPACE - Pause/Resume",
            "R - Reset",
            "V - Toggle Viz",
            "1-4 - Select Agent",
            "ESC - Quit"
        ]
        
        for instruction in instructions:
            inst_text = self.font_small.render(instruction, True, BLACK)
            self.screen.blit(inst_text, (panel_x + 30, y_offset))
            y_offset += 22
        
        y_offset += 20
        
        # Agent selection help
        pygame.draw.line(self.screen, BLACK, (panel_x + 10, y_offset), 
                        (panel_x + self.panel_width - 10, y_offset), 2)
        y_offset += 20
        
        agents_title = self.font_medium.render("Agents", True, BLACK)
        self.screen.blit(agents_title, (panel_x + 20, y_offset))
        y_offset += 25
        
        agent_list = [
            "1 - Simple Reflex",
            "2 - Model-Based",
            "3 - Utility (A*)",
            "4 - Goal (DFS)"
        ]
        
        for agent_item in agent_list:
            agent_text = self.font_small.render(agent_item, True, DARK_GRAY)
            self.screen.blit(agent_text, (panel_x + 30, y_offset))
            y_offset += 20
    
    def render(self, agent: Optional[Agent] = None, is_running: bool = False, 
               is_complete: bool = False):
        """Render the entire UI"""
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_robot()
        self.draw_control_panel(agent, is_running, is_complete)
        pygame.display.flip()
    
    def update(self, dt: float):
        """Update UI state"""
        self.update_animation(dt)
    
    def tick(self) -> float:
        """
        Tick the clock and return delta time
        
        Returns:
            Delta time in seconds
        """
        return self.clock.tick(self.fps) / 1000.0
    
    def set_visualization_data(self, explored: set, frontier: set):
        """Set explored and frontier tiles for visualization"""
        self.explored_tiles = explored
        self.frontier_tiles = frontier
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.steps_taken = 0
        self.cleaning_actions = 0
        self.start_time = pygame.time.get_ticks()
        self.robot_display_pos = list(self.environment.robot_pos)
        self.robot_target_pos = None
