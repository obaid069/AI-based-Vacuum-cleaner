# 🤖 Vacuum Cleaner Robot Simulation - AI Project

## 📋 Project Overview

This is a comprehensive **Artificial Intelligence project** that simulates a vacuum cleaner robot navigating a grid environment to clean dirty tiles. The project demonstrates fundamental AI concepts including **agent architectures**, **search algorithms**, and **intelligent decision-making**.

**Course:** Introduction to Artificial Intelligence  
**Difficulty Level:** Medium-High  
**Tech Stack:** Python 3.13, Pygame  
**Project Type:** Interactive Simulation with Visual UI

---

## 🎯 Learning Objectives

This project covers essential AI concepts from **"Artificial Intelligence: A Modern Approach"** (Russell & Norvig):

1. **Agent Theory** - Understanding different types of intelligent agents
2. **Search Algorithms** - Implementing and comparing BFS, DFS, and A*
3. **Environment Modeling** - Working with grid-based, observable, deterministic environments
4. **Performance Measurement** - Evaluating agent efficiency and optimality
5. **Heuristic Functions** - Using Manhattan distance for informed search

---

## ✨ Features Implemented

### 🌍 **Environment System**
- **20×15 grid world** with configurable size
- **Three tile states:**
  - 🟢 Clean tiles (light green)
  - 🟤 Dirty tiles (brown) - 30% of tiles
  - ⬛ Obstacles (dark gray) - 10% of tiles
- **Dynamic state tracking** - monitors cleaned vs total dirt
- **Collision detection** - prevents robot from moving through obstacles

### 🤖 **Four AI Agent Types**

#### 1. **Simple Reflex Agent**
- **Type:** Reactive agent
- **Strategy:** 
  - If current tile is dirty → clean it
  - Otherwise → move randomly to a neighbor
- **Pros:** Simple implementation, no memory required
- **Cons:** Inefficient, may revisit tiles multiple times
- **Best for:** Understanding basic agent behavior

#### 2. **Model-Based Agent (BFS)**
- **Type:** Agent with internal state
- **Strategy:**
  - Maintains memory of cleaned tiles
  - Uses **Breadth-First Search** to find path to dirty tiles
  - Avoids revisiting cleaned areas
- **Pros:** More systematic than reflex agent, guaranteed shortest path
- **Cons:** BFS can be slower for distant goals
- **Best for:** Demonstrating state-based reasoning

#### 3. **Utility-Based Agent (A*)**
- **Type:** Goal-based agent with utility function
- **Strategy:**
  - Always targets the **nearest dirty tile**
  - Uses **A* search** with Manhattan distance heuristic
  - Maximizes efficiency by minimizing travel distance
- **Pros:** Optimal pathfinding, highly efficient
- **Cons:** Requires heuristic design
- **Best for:** Showing optimal decision-making

#### 4. **Goal-Based Agent (DFS)**
- **Type:** Goal-oriented agent
- **Strategy:**
  - Uses **Depth-First Search** to find paths
  - Targets first available dirty tile
- **Pros:** Memory efficient
- **Cons:** May not find shortest path
- **Best for:** Comparing search strategy differences

### 🔍 **Search Algorithms**

#### **Breadth-First Search (BFS)**
```python
- Complete: ✅ Yes (finds solution if exists)
- Optimal: ✅ Yes (finds shortest path)
- Time Complexity: O(b^d)
- Space Complexity: O(b^d)
- Use Case: When shortest path is critical
```

#### **Depth-First Search (DFS)**
```python
- Complete: ⚠️ Not in infinite spaces
- Optimal: ❌ No (path may not be shortest)
- Time Complexity: O(b^m)
- Space Complexity: O(bm)
- Use Case: When memory is limited
```

#### **A* Search**
```python
- Complete: ✅ Yes (with admissible heuristic)
- Optimal: ✅ Yes (with admissible heuristic)
- Time Complexity: O(b^d)
- Space Complexity: O(b^d)
- Heuristic: Manhattan distance
- Use Case: When efficiency matters most
```

### 🎮 **Interactive UI Features**

- **Real-time visualization** with Pygame
- **Smooth animations** for robot movement
- **Color-coded tiles** for easy state identification
- **Control panel** with live metrics
- **Search visualization** (toggle with 'V' key)
  - Blue overlay: Explored nodes
  - Yellow overlay: Frontier nodes
- **Agent switching** on-the-fly (keys 1-4)

### 📊 **Performance Metrics**

The simulation tracks and displays:

1. **Steps Taken** - Total moves made by robot
2. **Tiles Cleaned** - Current/Total dirty tiles
3. **Cleanliness %** - Percentage of environment cleaned
4. **Efficiency** - Tiles cleaned per step (higher = better)
5. **Time Elapsed** - Total simulation time
6. **Nodes Expanded** - For algorithm analysis (stored in code)

---

## 🗂️ Project Structure

```
project/
│
├── main.py              # Main entry point, simulation controller
├── environment.py       # Grid world, tile states, robot position
├── agents.py           # All 4 agent implementations
├── algorithms.py       # BFS, DFS, A* search algorithms
├── ui.py              # Pygame rendering, animations, UI
└── README.md          # This file
```

### **File Descriptions:**

#### `main.py` (189 lines)
- **VacuumSimulation class** - Main controller
- Handles game loop, event processing, agent selection
- Manages simulation state (running/paused/complete)
- Orchestrates agent actions and UI updates

#### `environment.py` (152 lines)
- **Environment class** - Grid world representation
- **TileState enum** - Clean/Dirty/Obstacle states
- Methods: `move_robot()`, `clean_current_tile()`, `get_neighbors()`
- Tracks dirt statistics and cleanliness percentage

#### `agents.py` (209 lines)
- **Agent base class** - Common interface for all agents
- **SimpleReflexAgent** - Random movement strategy
- **ModelBasedAgent** - BFS-based pathfinding with memory
- **UtilityBasedAgent** - A* with nearest-dirty-tile utility
- **GoalBasedAgent** - DFS-based goal seeking

#### `algorithms.py` (182 lines)
- **SearchResult class** - Stores path, statistics, visualization data
- **bfs()** - Breadth-first search implementation
- **dfs()** - Depth-first search implementation
- **astar()** - A* search with Manhattan heuristic
- Helper: `find_nearest_dirty_tile()`, `reconstruct_path()`

#### `ui.py` (319 lines)
- **VacuumUI class** - Pygame interface handler
- Grid rendering with color-coded tiles
- Smooth robot animation system
- Control panel with metrics display
- Search visualization overlay system

---

## 🚀 How to Run

### **Prerequisites:**
```bash
Python 3.7+
Pygame library
```

### **Installation:**
```bash
# Install Pygame
pip install pygame

# Navigate to project directory
cd "d:\C drive\Document\AI\project"

# Run the simulation
python main.py
```

### **Controls:**

| Key | Action |
|-----|--------|
| **SPACE** | Start/Pause simulation |
| **R** | Reset environment and agent |
| **V** | Toggle search visualization |
| **1** | Select Simple Reflex Agent |
| **2** | Select Model-Based Agent (BFS) |
| **3** | Select Utility-Based Agent (A*) |
| **4** | Select Goal-Based Agent (DFS) |
| **ESC** | Quit application |

---

## 🧪 Testing & Experimentation

### **Recommended Experiments:**

1. **Compare Agent Efficiency:**
   - Run each agent on same environment (use Reset to restart)
   - Compare steps taken and efficiency percentage
   - Observe which completes fastest

2. **Analyze Search Algorithms:**
   - Enable visualization (V key)
   - Watch BFS explore layer-by-layer
   - See A* make direct paths to goals
   - Compare DFS's deep exploration

3. **Modify Environment:**
   - Change dirt probability (line 21 in `main.py`)
   - Adjust obstacle density
   - Try different grid sizes

4. **Performance Benchmarking:**
   - Record completion time for each agent
   - Calculate average efficiency across multiple runs
   - Create comparison charts

---

## 📚 AI Concepts Demonstrated

### **1. Agent Architectures (Chapter 2 - Russell & Norvig)**
- ✅ Simple reflex agents
- ✅ Model-based reflex agents
- ✅ Goal-based agents
- ✅ Utility-based agents

### **2. Search Algorithms (Chapter 3)**
- ✅ Uninformed search (BFS, DFS)
- ✅ Informed search (A*)
- ✅ Heuristic functions
- ✅ Path cost optimization

### **3. Problem Formulation**
- **States:** Robot position + tile cleanliness configuration
- **Actions:** Move(Up/Down/Left/Right), Clean
- **Goal Test:** All dirty tiles cleaned
- **Path Cost:** Number of steps taken

### **4. Environment Properties**
- **Observable:** Agent can see current tile state
- **Deterministic:** Actions have predictable outcomes
- **Episodic:** Each cleaning is independent
- **Static:** Environment doesn't change (except through agent actions)
- **Discrete:** Finite states and actions
- **Single-agent:** One robot operates

---

## 🎓 Appropriateness for Introduction to AI Course

### ✅ **Why This Project is Perfect:**

1. **Classic AI Problem:** The vacuum world is explicitly discussed in AI textbooks
2. **Core Concepts Coverage:** Agents, search, heuristics, performance metrics
3. **Hands-On Learning:** Visualizing abstract AI concepts
4. **Comparative Analysis:** Students see trade-offs between approaches
5. **Scalable Difficulty:** Can start simple and add features
6. **Real-World Relevance:** Connects to actual robotics (Roomba, etc.)

### 📊 **Difficulty Assessment:**

- **Coding Complexity:** Medium (well-structured Python)
- **AI Concepts:** Introductory (perfect for first AI course)
- **Time Required:** 2-4 weeks for group of 2-3 students
- **Prerequisites:** Basic Python, OOP concepts

### 🎯 **Learning Outcomes:**

Students will be able to:
- ✅ Implement different agent architectures
- ✅ Compare search algorithm performance
- ✅ Design heuristic functions
- ✅ Measure and analyze agent efficiency
- ✅ Visualize AI decision-making processes

---

## 🔧 Potential Extensions

### **Easy Extensions:**
- 🔋 Add battery constraint (robot must recharge)
- 🎲 Add dynamic dirt generation over time
- 📍 Implement charging station locations
- 📈 Add graphical performance comparison charts

### **Medium Extensions:**
- 🤖 Multiple robots cooperating
- 🗺️ Partial observability (limited vision)
- 🎯 Different dirt priorities (weights)
- 🧩 More complex obstacle patterns

### **Advanced Extensions:**
- 🧠 Machine learning for adaptive strategy
- 🌐 3D environment visualization
- 🔄 Dynamic replanning when environment changes
- 🏆 Reinforcement learning agent

---

## 📖 References & Resources

1. **Russell, S., & Norvig, P.** (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
   - Chapter 2: Intelligent Agents
   - Chapter 3: Solving Problems by Searching

2. **Search Algorithms:**
   - BFS/DFS: Introduction to Algorithms (Cormen et al.)
   - A*: Hart, P. E., Nilsson, N. J., & Raphael, B. (1968)

3. **Pygame Documentation:**
   - https://www.pygame.org/docs/

---

## 👥 Team Collaboration Tips

### **Suggested Task Distribution:**

**Member 1: Environment & Core Logic**
- Implement `environment.py`
- Set up grid system and tile states
- Handle robot movement logic

**Member 2: AI & Algorithms**
- Implement `algorithms.py` and `agents.py`
- Develop search algorithms
- Create agent decision-making logic

**Member 3: UI & Visualization**
- Implement `ui.py` and integrate `main.py`
- Design Pygame interface
- Add animations and metrics display

**Everyone:**
- Testing and debugging
- Performance analysis
- Documentation and presentation

---

## 📊 Expected Results

### **Typical Performance (20×15 grid, 30% dirt):**

| Agent Type | Avg Steps | Efficiency | Comments |
|------------|-----------|------------|----------|
| Simple Reflex | 400-600 | 10-15% | Random, inefficient |
| Model-Based (BFS) | 150-250 | 25-35% | Systematic coverage |
| Utility-Based (A*) | 100-180 | 35-50% | Most efficient |
| Goal-Based (DFS) | 200-350 | 20-30% | Variable performance |

*Note: Results vary based on random obstacle/dirt placement*

---

## ✅ Conclusion

This project successfully demonstrates:
- ✅ Multiple AI agent architectures
- ✅ Search algorithm implementation and comparison
- ✅ Interactive visualization of AI decision-making
- ✅ Performance measurement and analysis
- ✅ Real-world problem-solving application

**Perfect for:** Introduction to AI course, demonstrates fundamental concepts with practical implementation.

**Recommendation:** ✅ **Proceed with this project** - It's well-scoped for an intro AI course and covers essential topics.

---

## 📝 License

Educational project for Introduction to Artificial Intelligence course.

---

**Built with ❤️ for AI Education**
