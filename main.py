"""
Vacuum Cleaner Robot Simulation
Main entry point for the AI project
"""

import pygame
import sys
from environment import Environment
from agents import SimpleReflexAgent, ModelBasedAgent, UtilityBasedAgent, GoalBasedAgent
from ui import VacuumUI

class VacuumSimulation:
    """Main simulation controller"""
    
    def __init__(self):
        """Initialize simulation"""
        # Create environment (20x15 grid with 30% dirt, 10% obstacles)
        self.environment = Environment(width=20, height=15, 
                                      dirt_probability=0.3, 
                                      obstacle_probability=0.1)
        
        # Create UI
        self.ui = VacuumUI(self.environment, cell_size=35)
        
        # Available agents
        self.agents = [
            SimpleReflexAgent(),
            ModelBasedAgent(search_algorithm='bfs'),
            UtilityBasedAgent(),
            GoalBasedAgent()
        ]
        
        self.current_agent_index = 2  # Start with Utility-Based Agent
        self.current_agent = self.agents[self.current_agent_index]
        
        # Simulation state
        self.is_running = False
        self.is_complete = False
        self.step_delay = 0.1  # Delay between steps in seconds
        self.step_timer = 0.0
        
    def select_agent(self, index: int):
        """Select agent by index"""
        if 0 <= index < len(self.agents):
            self.current_agent_index = index
            self.current_agent = self.agents[index]
            self.reset()
            print(f"Selected: {self.current_agent.name}")
    
    def reset(self):
        """Reset simulation"""
        self.environment.reset()
        self.current_agent.reset()
        self.ui.reset_metrics()
        self.ui.robot_display_pos = list(self.environment.robot_pos)
        self.is_running = False
        self.is_complete = False
        self.step_timer = 0.0
        print("Simulation reset")
    
    def step(self):
        """Execute one simulation step"""
        if self.is_complete:
            return
        
        # Perceive environment
        perception = self.current_agent.perceive(self.environment)
        
        # Decide action
        action_type, action_data = self.current_agent.act(self.environment, perception)
        
        # Execute action
        if action_type == 'clean':
            if self.environment.clean_current_tile():
                self.current_agent.tiles_cleaned += 1
                self.ui.cleaning_actions += 1
                print(f"Cleaned tile at {self.environment.robot_pos}")
        
        elif action_type == 'move':
            if action_data:
                old_pos = self.environment.robot_pos
                if self.environment.move_robot(*action_data):
                    self.current_agent.steps_taken += 1
                    self.ui.handle_robot_move(*action_data)
                    # print(f"Moved from {old_pos} to {action_data}")
        
        elif action_type == 'wait':
            # Check if all tiles are clean
            if self.environment.is_all_clean():
                self.is_complete = True
                self.is_running = False
                print(f"\n🎉 Cleaning complete!")
                print(f"Total steps: {self.ui.steps_taken}")
                print(f"Tiles cleaned: {self.environment.cleaned_dirt}")
                print(f"Efficiency: {(self.environment.cleaned_dirt / max(self.ui.steps_taken, 1)) * 100:.1f}%")
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                # ESC - Quit
                if event.key == pygame.K_ESCAPE:
                    return False
                
                # SPACE - Pause/Resume
                elif event.key == pygame.K_SPACE:
                    if not self.is_complete:
                        self.is_running = not self.is_running
                        status = "Running" if self.is_running else "Paused"
                        print(f"Simulation {status}")
                
                # R - Reset
                elif event.key == pygame.K_r:
                    self.reset()
                
                # V - Toggle visualization
                elif event.key == pygame.K_v:
                    self.ui.show_explored = not self.ui.show_explored
                    status = "ON" if self.ui.show_explored else "OFF"
                    print(f"Visualization: {status}")
                
                # 1-4 - Select agent
                elif event.key == pygame.K_1:
                    self.select_agent(0)
                elif event.key == pygame.K_2:
                    self.select_agent(1)
                elif event.key == pygame.K_3:
                    self.select_agent(2)
                elif event.key == pygame.K_4:
                    self.select_agent(3)
        
        return True
    
    def run(self):
        """Main simulation loop"""
        print("=" * 60)
        print("VACUUM CLEANER ROBOT SIMULATION")
        print("=" * 60)
        print(f"Environment: {self.environment.width}x{self.environment.height} grid")
        print(f"Total dirt tiles: {self.environment.total_dirt}")
        print(f"Starting agent: {self.current_agent.name}")
        print("\nControls:")
        print("  SPACE - Start/Pause")
        print("  R - Reset")
        print("  V - Toggle visualization")
        print("  1-4 - Select agent")
        print("  ESC - Quit")
        print("=" * 60)
        
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Get delta time
            dt = self.ui.tick()
            
            # Update animation
            self.ui.update(dt)
            
            # Execute simulation step
            if self.is_running and not self.ui.robot_target_pos:
                self.step_timer += dt
                
                if self.step_timer >= self.step_delay:
                    self.step()
                    self.step_timer = 0.0
            
            # Render
            self.ui.render(self.current_agent, self.is_running, self.is_complete)
        
        pygame.quit()
        print("\nSimulation ended.")

def main():
    """Entry point"""
    simulation = VacuumSimulation()
    simulation.run()

if __name__ == '__main__':
    main()
