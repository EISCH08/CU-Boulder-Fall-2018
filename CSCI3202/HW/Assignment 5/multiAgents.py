# multiAgents.py
# --------------
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


#Parker Eischen

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.gameBoard.playerList[1].actions

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generateSuccessorState(action)
        "*** YOUR CODE HERE ***"
        xPos,yPos = currentGameState.getPacmanPosition()
        xNew,yNew = newPos
        ghostPosistions = currentGameState.getGhostPositions()
        dist = []
        gDistance = []
        for x in range(0,newFood.width):
          for y in range(0,newFood.height):
            if(newFood[x][y] == True):
              distance = ((xNew-x)**2 + (yNew-y)**2) **.5
              dist.append(distance)
            for ghosts in ghostPosistions:
              ghostX,ghostY = ghosts
              distanceG = ((xNew-ghostX)**2 + (yNew-ghostY)**2) **.5
              gDistance.append(distanceG)
        
        if len(dist) != 0: #make sure we can refer to dist
          closestFood = min(dist)
          closetGhost = min(gDistance)
          score = (1/(closestFood)) + .2 * successorGameState.getScore() 
          if(closetGhost < 1.2 ): #run away from ghosts
            return -100
          if(action == "Stop"): #dont want pacman to get stuck in a stopped state
            return -100
          print(score)
          return score
        else:
          closestFood = 1 #fixes error when food = 0
          score = (1/(closestFood)) + .2 * successorGameState.getScore()
          return score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        self.numAgents = gameState.getNumAgents()
        self.action = 'Stop'
        #pacman is the maximizing agent becasue we want a better score
        #ghosts are the minimizing agents
        def MiniMax(gameState,agentIndex,depth,action):
          bestScore = float('-Inf')
          legalMoves = gameState.getLegalActions(agentIndex)
          print(legalMoves)
          for move in legalMoves:
            maxScore = bestScore
            successorGameState = gameState.generateSuccessor(agentIndex,move)
            bestScore = max(bestScore,minimumValue(successorGameState,agentIndex+1,depth))
            #print(bestScore)
            if maxScore < bestScore:
              action = move

          return action

        def minimumValue(gameState,agentIndex,depth): #getting the ghost values
          gameOver = gameState.isWin() or gameState.isLose()
          if depth == self.depth or gameOver:
            return self.evaluationFunction(gameState)
          else:
            minScore = float('Inf')
            if agentIndex + 1 == self.numAgents:
              for move in gameState.getLegalActions(agentIndex):
                
                successorGameState = gameState.generateSuccessor(agentIndex,move)
                minScore = min(minScore,maximumValue(successorGameState,agentIndex,depth+1))
            else:
              legalMoves = gameState.getLegalActions(agentIndex)
              for move in legalMoves:
                successorGameState = gameState.generateSuccessor(agentIndex,move)
                minScore = min(minScore,minimumValue(successorGameState,agentIndex+1,depth))
            return minScore


        def maximumValue(gameState,agentIndex,depth):
          gameOver = gameState.isWin() or gameState.isLose()
          if depth == self.depth or gameOver:
            return self.evaluationFunction(gameState)
          else:
            agentIndex %= (self.numAgents - 1)
            maxScore = float('-Inf')
            for move in gameState.getLegalActions(agentIndex):
              successorGameState = gameState.generateSuccessor(agentIndex,move)
              maxScore = max(maxScore,minimumValue(successorGameState,agentIndex+1,depth))  
            return(maxScore)


        


    
        return MiniMax(gameState, 0, 0, 'Nothin"')


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)

"""
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
            """
        "*** YOUR CODE HERE ***"
        self.numAgents = gameState.getNumAgents()
        self.action = 'Stop'
        #pacman is the maximizing agent becasue we want a better score
        #ghosts are the minimizing agents
        def MiniMax(gameState,agentIndex,depth,action):
          bestScore = float('-Inf')
          legalMoves = gameState.getLegalActions(agentIndex)
          for move in legalMoves:
            maxScore = bestScore
            successorGameState = gameState.generateSuccessor(agentIndex,move)
            bestScore = max(bestScore,minimumValue(successorGameState,agentIndex+1,depth,float('-Inf'),float('Inf')))
            if maxScore < bestScore:
              action = move
          return action

        def minimumValue(gameState,agentIndex,depth, alpha, beta): #getting the ghost values
          gameOver = gameState.isWin() or gameState.isLose()
          if depth == self.depth or gameOver:
            return self.evaluationFunction(gameState)
          else:
            minScore = float('Inf')
            if agentIndex + 1 == self.numAgents:
              for move in gameState.getLegalActions(agentIndex):
                successorGameState = gameState.generateSuccessor(agentIndex,move)
                minScore = min(minScore,maximumValue(successorGameState,agentIndex,depth+1,alpha,beta))
                if(minScore < alpha):
                  return minScore
                beta = min(beta,minScore)
            else:
              legalMoves = gameState.getLegalActions(agentIndex)
              for move in legalMoves:
                successorGameState = gameState.generateSuccessor(agentIndex,move)
                minScore = min(minScore,minimumValue(successorGameState,agentIndex+1,depth,alpha,beta))
                if(minScore < alpha):
                  return minScore
                beta = min(beta,minScore)

            return minScore


        def maximumValue(gameState,agentIndex,depth,alpha,beta):
          gameOver = gameState.isWin() or gameState.isLose()
          if depth == self.depth or gameOver:
            return self.evaluationFunction(gameState)
          else:
            agentIndex %= (self.numAgents - 1)
            maxScore = float('-Inf')
            for move in gameState.getLegalActions(agentIndex):
              successorGameState = gameState.generateSuccessor(agentIndex,move)
              maxScore = max(maxScore,minimumValue(successorGameState,agentIndex+1,depth,alpha,beta))
              if(maxScore > beta):
                  return maxScore
              alpha = max(alpha,maxScore)  
          return maxScore

        return MiniMax(gameState, 0, 0, 'Nothin"')
        


    
        



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        self.numAgents = gameState.getNumAgents()
        self.action = 'Stop'
        def miniMax(gameState,agentIndex,depth,action):
          bestScore = float('-Inf')
          legalMoves = gameState.getLegalActions(agentIndex)
          for move in legalMoves:
            maxScore = bestScore
            successorGameState = gameState.generateSuccessor(agentIndex,move)
            bestScore = max(bestScore,expectedValue(successorGameState,agentIndex+1,depth))
            if maxScore < bestScore:
              action = move
          return action

        def expectedValue(gameState,agentIndex,depth): #getting the ghost values
          gameOver = gameState.isWin() or gameState.isLose()
          if depth == self.depth or gameOver:
            return self.evaluationFunction(gameState)
          else:
            ExpectedValue = float(0)
            probability = float(1/len(gameState.getLegalActions(agentIndex)))
            if agentIndex + 1 == self.numAgents:
              for move in gameState.getLegalActions(agentIndex):
                successorGameState = gameState.generateSuccessor(agentIndex,move)
                ExpectedValue+= probability * maximumValue(successorGameState,agentIndex,depth+1)
            else:
              legalMoves = gameState.getLegalActions(agentIndex)
              for move in legalMoves:
                successorGameState = gameState.generateSuccessor(agentIndex,move)
                ExpectedValue+= probability * expectedValue(successorGameState,agentIndex+1,depth)


            return ExpectedValue


        def maximumValue(gameState,agentIndex,depth):
          gameOver = gameState.isWin() or gameState.isLose()
          if depth == self.depth or gameOver:
            return self.evaluationFunction(gameState)
          else:
            agentIndex %= (self.numAgents - 1)
            maxScore = float('-Inf')
            for move in gameState.getLegalActions(agentIndex):
              successorGameState = gameState.generateSuccessor(agentIndex,move)
              maxScore = max(maxScore,expectedValue(successorGameState,agentIndex+1,depth))  
          return maxScore

        return miniMax(gameState, 0, 0, 'Nothin"')

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: create an evaluation function that draws pacman towards food based on his neighbors. First we give score to the state in which pacman is closest to food
      to draw him closer. I added the score value to each state too so that he wont walk towards ghosts and die. Lastly, if one of his neighboring sqares had food, i wanted him
      to follow that path and go down that way, resulting in a higher score. 
    """
    "*** YOUR CODE HERE ***"
    
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    xPos,yPos = currentGameState.getPacmanPosition()
    ghostPosistions = currentGameState.getGhostPositions()
    capLocations = currentGameState.getCapsules()
    print(capLocations)
    capDist = []
    dist = []
    gDistance = []
    for x in range(0,Food.width):
      for y in range(0,Food.height):
        if(Food[x][y] == True):
          distance = ((xPos-x)**2 + (yPos-y)**2) **.5
          dist.append(distance)
        for ghosts in ghostPosistions:
          ghostX,ghostY = ghosts
          distance = ((xPos-ghostX)**2 + (yPos-ghostY)**2) **.5
          gDistance.append(distance)
        if len(capLocations)!=0:
          for capsules in capLocations:
            capX, capY = capsules
            distance = ((xPos-capX)**2 + (yPos-capY)**2) **.5
            capDist.append(distance)
    closestCapsule = 0
    if len(dist)!=0:
      closestFood = min(dist)
    else: 
      closestFood = 1
    if len(capLocations)!=0:
      closestCapsule = min(capDist)
    score = 1/closestFood + currentGameState.getScore()
    if(currentGameState.hasFood(xPos+1,yPos) | currentGameState.hasFood(xPos,yPos+1)) | currentGameState.hasFood(xPos-1,yPos) |currentGameState.hasFood(xPos,yPos-1):
      score+= 3
      
 
    return score

# Abbreviation
better = betterEvaluationFunction

