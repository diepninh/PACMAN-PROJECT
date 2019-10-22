# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    stack_xy = Stack()

    visited = []
    path = []

    if problem.isGoalState(problem.getStartState()):
        return []

    stack_xy.push((problem.getStartState(), []))

    while (True):

        if stack_xy.isEmpty():
            return []

        xy, path = stack_xy.pop()
        visited.append(xy)

        if problem.isGoalState(xy):
            return path

        successors = problem.getSuccessors(xy)
        if successors:
            for item in successors:
                if item[0] not in visited:
                    new_path = path + [item[1]]
                    stack_xy.push((item[0], new_path))


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    _queue = Queue()
    _visited = []
    _path = []
    if problem.isGoalState(problem.getStartState()):
        return []

    _queue.push((problem.getStartState(), []))
    while (True):

        if _queue.isEmpty():
            return []

        xy, path = _queue.pop()
        _visited.append(xy)

        if problem.isGoalState(xy):
            return path

        successors = problem.getSuccessors(xy)
        if successors:
            for item in successors:
                if item[0] not in _visited:
                    new_path = path + [item[1]]
                    _queue.push((item[0], new_path))


    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()

    fringe = util.PriorityQueue()
    visited = []
    succeeded = []

    fringe.push((start, [], 0), 0)

    while not fringe.isEmpty():
        n = fringe.pop()
        print "node: ", n
        actions = n[1]

        visited.append(n[0])

        if problem.isGoalState(n[0]):
            return actions


        for successor in problem.getSuccessors(n[0]):
            if not successor[0] in visited:
                if (not successor[0] in succeeded) or (problem.isGoalState(successor[0])):
                    succeeded.append(successor[0])
                    successorActions = list(n[1])
                    successorActions.append(successor[1])
                    successorCost = n[2] + successor[2]
                    fringe.push((successor[0], successorActions, successorCost), successorCost)

        if problem.isGoalState(n[0]):
            return actions

    return actions

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()

    # create fringe queue and visited list
    fringe = util.PriorityQueue()
    visited = []
    succeeded = []

    # push the start node on the fringe queue
    h = heuristic(start, problem)
    ch = 0 + h
    # node(coordinates, actions, cost, heuristic)
    fringe.push((start, [], 0), ch)

    while not fringe.isEmpty():
        n = fringe.pop()
        # print "node: ", n
        actions = n[1]
        # h = heuristic(n[0], problem)

        visited.append(n[0])

        # check if goal state found
        if problem.isGoalState(n[0]):
            return actions

        # print "successors: ", problem.getSuccessors(n[0])
        # print "current action on node: ", n[1]

        # node(coordinates, actions, cost, heuristic)

        for successor in problem.getSuccessors(n[0]):
            # print "successors on %s : %s" % (str(n[0]), problem.getSuccessors(n[0]))
            if not successor[0] in visited:
                if (not successor[0] in succeeded) or (problem.isGoalState(successor[0])):
                    succeeded.append(successor[0])
                    successorActions = list(n[1])
                    successorActions.append(successor[1])
                    successorCost = n[2] + successor[2]
                    # successorHeuristic = h + heuristic(successor[0], problem)
                    successorHeuristic = heuristic(successor[0], problem)
                    scsh = successorCost + successorHeuristic
                    # print "pushing: ", (successor[0], successorCost)
                    fringe.push((successor[0], successorActions, successorCost), scsh)
        # print "went through successors"

        # check if goal state found
        if problem.isGoalState(n[0]):
            return actions

    return actions

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

