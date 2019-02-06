
import random
import os
import matplotlib.pyplot as plt

import basicStrat
import calcAction

class Deck: #creates a functioning deck of cards
	def __init__(self,numDecks):
		self.cardDenominations = {"A":(1,11), "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
		self.order =[]
		for key in self.cardDenominations:
			for i in range(0,4):
				for decks in range(0,numDecks):
					self.order.append(key)
	def shuffleDeck(self, numTimes):
		for times in range(0,numTimes):
			random.shuffle(self.order)
	def dealCard(self):
		card = self.order.pop(0)
		return card
	def getValue(self,card):
		value = self.cardDenominations[card]
		return value

class Player: #creates the dealer and player characters
	def __init__(self,playerNumber): #0 for dealer, 1+ for players
		self.hand = []
		self.playerNumber = playerNumber
		if playerNumber == 0:
			self.actions = ["0:HIT","1:STAND"]
			self.name = "DEALER"
		else:
			self.actions = ["1:HIT", "2:STAND","3:DOUBLE DOWN","4:SPLIT"]
			self.name = "PLAYER"
			self.cash = 100
			self.bet = 5
	def getCard(self,card): #add a card to the players hand
		self.hand.append(card)


class GameBoard:
	def __init__(self,numberOfPlayers,numberDecks):
		self.playerList = []
		self.playerWins = 0
		self.dealerWins = 0
		self.pushGames = 0
		self.numberDecks = numberDecks
		self.betAmount = (5,10,15)
		self.pot = 0
		self.rollingSum = 0
		for x in range(0,numberOfPlayers):
			newPlayer = Player(x)
			self.playerList.append(newPlayer)

		self.deck = Deck(numberDecks)
		self.deck.shuffleDeck(3)

	def giveCard(self,player): #give a card to a random player
		card = self.deck.dealCard()
		player.getCard(card)

	def playerHandSum(self,player): #adds a players hand
		valLow = 0
		valHigh = 0
		for x in player.hand:
			if(self.deck.getValue(x) == (1,11)): #accounts for the ace draw
				valLow += 1
				valHigh +=11
			else: #any other card
				valLow +=self.deck.getValue(x)
				valHigh +=self.deck.getValue(x)

		return valLow,valHigh
	def checkBust(self,player):
		if self.playerHandSum(player)[0] > 21:
			print(player.name,"BUSTS",sep=' ')
			return True
		elif self.playerHandSum(player)[0]< 22 & self.playerHandSum(player)[1]>21:
			return False
		else:
			return False

class State:
	def __init__(self,GameBoard,turn):
		self.gameBoard = GameBoard
		self.player = GameBoard.playerList[1]
		self.dealer = GameBoard.playerList[0]
		self.playerHand = GameBoard.playerList[1].hand
		self.dealerHand = GameBoard.playerList[0].hand
		self.deck = GameBoard.deck
		self.turn = turn
		

	def countCards(self): #counts the values of each card in the deck
		cardCount = dict()
		for y in self.deck.cardDenominations:
			cardCount[y] = 0
		for x in self.deck.order:
			cardCount[x] = cardCount[x]+1

		return cardCount

	def checkGameOver(self):
		if ((self.gameBoard.playerHandSum(self.gameBoard.playerList[0])[1] > 16) & (self.turn == 0) & (self.gameBoard.playerHandSum(self.gameBoard.playerList[0])[0] < 17)):
			return False
		if ((self.gameBoard.playerHandSum(self.gameBoard.playerList[0])[1] > 16) & (self.turn == 0)):
			return True
		if ((22>self.gameBoard.playerHandSum(self.gameBoard.playerList[0])[1] > 16) & (self.turn == 0)):
			print('DEALER STANDS')
			return True
		if self.gameBoard.checkBust(self.dealer):
			return True

		else: return False

	def checkWinner(self):
		playerWin = False
		dealerWin = False
		if self.turn!=2:
			print("game is not over yet")
		else:
			playerBust = self.gameBoard.checkBust(self.player)
			dealerBust = self.gameBoard.checkBust(self.dealer)
			playerSum = self.gameBoard.playerHandSum(self.player)[1]
			dealerSum = self.gameBoard.playerHandSum(self.dealer)[1]
			if(playerBust & dealerBust):
				print('Push Game')
				self.gameBoard.pushGames+=1
				self.gameBoard.playerList[1].cash+=self.gameBoard.pot
			elif(dealerBust & (playerBust==False)): #player victory
				playerWin = True
			elif((dealerBust==False) & playerBust):
				dealerWin = True
			else: #neither busts and we need to sum the hands to find victor
				if((self.gameBoard.playerHandSum(self.player)[1] > 21) & (self.gameBoard.playerHandSum(self.player)[0]<21)):
					playerSum = self.gameBoard.playerHandSum(self.player)[0]
				
				if((self.gameBoard.playerHandSum(self.dealer)[1] > 21) & (self.gameBoard.playerHandSum(self.dealer)[0]<21)):
					dealerSum = self.gameBoard.playerHandSum(self.dealer)[0]
				
				if(playerSum > dealerSum):
					playerWin = True
				elif(playerSum <dealerSum):
					dealerWin = True
				else: #tie
					print('Push Game')
					self.gameBoard.pushGames+=1
					self.gameBoard.playerList[1].cash+=self.gameBoard.pot
		closest = abs(21-self.gameBoard.playerHandSum(self.dealer)[1])
		for x in self.gameBoard.playerHandSum(self.dealer):
			if abs(21-x) < closest:
				dealerSum = x
		closest = abs(21-self.gameBoard.playerHandSum(self.player)[1])
		for x in self.gameBoard.playerHandSum(self.player):
			if abs(21-x) < closest:
				playerSum = x
		print(self.gameBoard.playerList[0].hand,dealerSum)
		print(self.gameBoard.playerList[1].hand,playerSum)
		if playerWin:
			self.gameBoard.playerWins+=1
			print("PLAYER WINS")
			self.gameBoard.playerList[1].cash+=self.gameBoard.pot*2
		elif dealerWin:
			self.gameBoard.dealerWins+=1
			print("PLAYER LOSES")

	
	def getRollingSum(self):
		dealerSum = self.gameBoard.playerHandSum(self.dealer)
		playerCards = self.player.hand
		playerSum = self.gameBoard.playerHandSum(self.player)
		cardCount = self.countCards()
		cardCountValue = {"A":-1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":0, "8":0, "9":0, "10":-1, "J":-1, "Q":-1, "K":-1}
		index = 0
		for x in cardCount:
			if  cardCount[x]< (self.gameBoard.numberDecks*4): #that card has been delt
				self.gameBoard.rollingSum+=cardCountValue[x]


		return self.gameBoard.rollingSum
	def getTrueCount(self):
		rollingSum = self.getRollingSum()
		totalCards =0
		cardCount = self.countCards()
		for x in cardCount:
			totalCards+=cardCount[x]
		numberofDecksLeft = float(totalCards/52)
		num = round(numberofDecksLeft * 2) / 2
		#print('decksLeft',num)
		return round(rollingSum/num)

	

def prettyPrint(State):
	print('=======================================================')
	print('			BLACKJACK				')
	print('DEALER WINS',State.gameBoard.dealerWins,sep =':')
	print('PLAYER WINS',State.gameBoard.playerWins,sep =':')
	print('PUSH GAMES', State.gameBoard.pushGames,sep = ':')
	print('DEALER HAND')
	print(State.dealerHand,State.gameBoard.playerHandSum(State.dealer))
	print()
	print("			POT: ", State.gameBoard.pot)
	print()
	print()
	print('YOUR HAND')
	print(State.playerHand,State.gameBoard.playerHandSum(State.player))
	print()
	print(State.player.actions,"You Have :$",State.player.cash,State.getTrueCount())
	print('======================================================')
def prettyPrintStart(state):
	print('=======================================================')
	print('			BLACKJACK				')
	print("YOU Have :$",state.player.cash)
	
	
	
def playGameAIStrategy(numberOfGames,numberDecks): #runs the game to be played by a human vs dealer
	gameBoard = GameBoard(2,numberDecks)
	
	turn = 1 #meaning its players turn
	
	for x in range(1,numberOfGames+1):
		gameBoard.giveCard(gameBoard.playerList[0]) #gives first card to dealer
		gameBoard.giveCard(gameBoard.playerList[1]) 
		gameBoard.giveCard(gameBoard.playerList[1])#gives the player two cards
		state = State(gameBoard,1)
		choiceMade = False
		prettyPrintStart(state)
		print("Game #:",x)
		
		while(choiceMade==False):
			playerAction = basicStrat.AIBetAmount(state)
			type(playerAction)

			if playerAction == '': #keep same bet value
				gameBoard.playerList[1].bet=gameBoard.playerList[1].bet
				choiceMade = True
			elif (int(playerAction)%5 == 0) & (int(playerAction)<=gameBoard.playerList[1].cash):
				gameBoard.playerList[1].bet = int(playerAction)
				choiceMade = True
			else:
				print('Choice has to be a valid number, a multiple of 5 and less than your current cash size. Please try again')
				print()

		print("AI BETS:",gameBoard.playerList[1].bet)
		gameBoard.playerList[1].cash-=gameBoard.playerList[1].bet
		gameBoard.pot = gameBoard.playerList[1].bet
		playerTurn = True
		dealerTurn = True
		ace = False
		print("Dealer Hand:",state.dealer.hand, state.gameBoard.playerHandSum(state.dealer))
		while playerTurn == True:
			state = State(gameBoard,1)
			
			print("Player Hand:",state.player.hand, state.gameBoard.playerHandSum(state.player))
			#prettyPrint(state)
			if(gameBoard.playerHandSum(state.player)[0]!=gameBoard.playerHandSum(state.player)[1]):
				#print("Ace in hand")
				ace =True
			playerAction = basicStrat.calculateMoveOnStrategy(state,ace)
			#print(playerAction)
			if playerAction == '1': #hit
				gameBoard.giveCard(gameBoard.playerList[1])#give another card
				state = State(gameBoard,1)
				if(state.gameBoard.checkBust(gameBoard.playerList[1])):
					playerTurn = False
			elif playerAction == '2': #stand
				playerTurn = False
			elif playerAction == '3': # doubleDown
				print("AI DOUBLES DOWN")
				gameBoard.giveCard(gameBoard.playerList[1])#give another card
				gameBoard.playerList[1].cash-=gameBoard.playerList[1].bet
				gameBoard.pot += gameBoard.playerList[1].bet
				state = State(gameBoard,1)

				#prettyPrint(state)
				gameBoard.checkBust(state.player)
				playerTurn = False
			elif ((state.playerHand[0] == state.playerHand[1]) & (playerAction =='4')): #player is eligible to split
				print('This is a work in progess')
				
			else:
				print("invalid action please try again")

		


		while dealerTurn:
			gameBoard.giveCard(gameBoard.playerList[0])
			state = State(gameBoard,0)
			if(state.checkGameOver()): #dealer is above 17 or has busted
				dealerTurn = False
		state = State(gameBoard,2)
		state.checkWinner()
		gameBoard.playerList[0].hand = []
		gameBoard.playerList[1].hand = []
		if(gameBoard.playerList[1].cash <=0):
			break
		
	return gameBoard.playerList[1].cash
		
def playGameAICheat(numberOfGames,numberDecks): #runs the game to be played by a human vs dealer
	gameBoard = GameBoard(2,numberDecks)
	
	turn = 1 #meaning its players turn
	
	for x in range(1,numberOfGames+1):
		gameBoard.giveCard(gameBoard.playerList[0]) #gives first card to dealer
		gameBoard.giveCard(gameBoard.playerList[1]) 
		gameBoard.giveCard(gameBoard.playerList[1])#gives the player two cards
		state = State(gameBoard,1)
		choiceMade = False
		prettyPrintStart(state)
		print("Game #:",x)
		
		while(choiceMade==False):
			playerAction = basicStrat.AIBetAmount(state)
			type(playerAction)

			if playerAction == '': #keep same bet value
				gameBoard.playerList[1].bet=gameBoard.playerList[1].bet
				choiceMade = True
			elif (int(playerAction)%5 == 0) & (int(playerAction)<=gameBoard.playerList[1].cash):
				gameBoard.playerList[1].bet = int(playerAction)
				choiceMade = True
			else:
				print('Choice has to be a valid number, a multiple of 5 and less than your current cash size. Please try again')
				print()

		print("AI BETS:",gameBoard.playerList[1].bet)
		gameBoard.playerList[1].cash-=gameBoard.playerList[1].bet
		gameBoard.pot = gameBoard.playerList[1].bet
		playerTurn = True
		dealerTurn = True
		ace = False
		print("Dealer Hand:",state.dealer.hand, state.gameBoard.playerHandSum(state.dealer))
		while playerTurn == True:
			state = State(gameBoard,1)
			
			print("Player Hand:",state.player.hand, state.gameBoard.playerHandSum(state.player))
			#prettyPrint(state)
			if(gameBoard.playerHandSum(state.player)[0]!=gameBoard.playerHandSum(state.player)[1]):
				#print("Ace in hand")
				ace =True
			playerAction = calcAction.calculateBestAction(state)
			print(playerAction)
			if playerAction == '1': #hit
				gameBoard.giveCard(gameBoard.playerList[1])#give another card
				state = State(gameBoard,1)
				if(state.gameBoard.checkBust(gameBoard.playerList[1])):
					playerTurn = False
			elif playerAction == '2': #stand
				playerTurn = False
			elif playerAction == '3': # doubleDown
				print("AI DOUBLES DOWN")
				gameBoard.giveCard(gameBoard.playerList[1])#give another card
				gameBoard.playerList[1].cash-=gameBoard.playerList[1].bet
				gameBoard.pot += gameBoard.playerList[1].bet
				state = State(gameBoard,1)

				#prettyPrint(state)
				gameBoard.checkBust(state.player)
				playerTurn = False
			elif ((state.playerHand[0] == state.playerHand[1]) & (playerAction =='4')): #player is eligible to split
				print('This is a work in progess')
				
			else:
				print("invalid action please try again")

		


		while dealerTurn:
			gameBoard.giveCard(gameBoard.playerList[0])
			state = State(gameBoard,0)
			if(state.checkGameOver()): #dealer is above 17 or has busted
				dealerTurn = False
		state = State(gameBoard,2)
		state.checkWinner()
		gameBoard.playerList[0].hand = []
		gameBoard.playerList[1].hand = []
		if(gameBoard.playerList[1].cash <=0):
			break
		
	return gameBoard.playerList[1].cash

def playGame(numberOfGames,numberDecks): #runs the game to be played by a human vs dealer
	gameBoard = GameBoard(2,numberDecks)
	
	turn = 1 #meaning its players turn
	for x in range(0,numberOfGames):

		gameBoard.giveCard(gameBoard.playerList[0]) #gives first card to dealer
		gameBoard.giveCard(gameBoard.playerList[1]) 
		gameBoard.giveCard(gameBoard.playerList[1])#gives the player two cards
		state = State(gameBoard,1)
		#print(state.countCards())
		choiceMade = False
		prettyPrintStart(state)
		
		while(choiceMade==False):
			print("Current bet value:",gameBoard.playerList[1].bet)
			playerAction = input("What is your bet? Enter a multiple of 5 or return to keep current bet size ")
			type(playerAction)

			if playerAction == '': #keep same bet value
				gameBoard.playerList[1].bet=gameBoard.playerList[1].bet
				choiceMade = True
			elif (int(playerAction)%5 == 0) & (int(playerAction)<=gameBoard.playerList[1].cash):
				gameBoard.playerList[1].bet = int(playerAction)
				choiceMade = True
			else:
				print('Choice has to be a valid number, a multiple of 5 and less than your current cash size. Please try again')
				print()
		print("YOU BET:",gameBoard.playerList[1].bet)
		gameBoard.playerList[1].cash-=gameBoard.playerList[1].bet
		gameBoard.pot = gameBoard.playerList[1].bet
		playerTurn = True
		dealerTurn = True
		while playerTurn == True:
			state = State(gameBoard,1)

			prettyPrint(state)
			playerAction = input("Type in your action(number)")
			
			if playerAction == '1': #hit
				gameBoard.giveCard(gameBoard.playerList[1])#give another card
				state = State(gameBoard,1)
				if(state.gameBoard.checkBust(gameBoard.playerList[1])):
					playerTurn = False
			elif playerAction == '2': #stand
				playerTurn = False
			elif playerAction == '3': # doubleDown
				gameBoard.giveCard(gameBoard.playerList[1])#give another card
				gameBoard.playerList[1].cash-=gameBoard.playerList[1].bet
				gameBoard.pot += gameBoard.playerList[1].bet
				state = State(gameBoard,1)

				prettyPrint(state)
				gameBoard.checkBust(state.player)
				playerTurn = False
			elif ((state.playerHand[0] == state.playerHand[1]) & (playerAction =='4')): #player is eligible to split
				print('This is a work in progess')
				
			else:
				print("invalid action please try again")

		


		while dealerTurn:
			print('DEALER HITS')
			gameBoard.giveCard(gameBoard.playerList[0])
			state = State(gameBoard,0)
			prettyPrint(state)
			if(state.checkGameOver()): #dealer is above 17 or has busted
				dealerTurn = False
		state = State(gameBoard,2)
		state.checkWinner()
		gameBoard.playerList[0].hand = []
		gameBoard.playerList[1].hand = []

	return gameBoard.playerList[1].cash

	if(gameBoard.playerList[1].cash >= 100): #player has a surplus
		print("After:",numberOfGames,"games","You Won:$",gameBoard.playerList[1].cash -100)
	else:
		print("After:",numberOfGames,"games","You Lost:$",100 - gameBoard.playerList[1].cash)	

def simulateAICheatStrategy(numOfGames,numDecks,numberOfSims):
	xaxis = [i for i in range(1,numberOfSims)]
	yaxis = []
	totalProfit = 0
	for x in range(1,numberOfSims):
		winnings = playGameAICheat(numOfGames,numDecks)
		totalProfit += winnings
		yaxis.append(winnings-100)
		if(winnings >= 100): #player has a surplus
			print("After:",numOfGames,"games","You Won:$",winnings -100)
		else:
			print("After:",numOfGames,"games","You Lost:$",100 - winnings)
	totalProfit = int(totalProfit/numberOfSims)
	totalProfity = [totalProfit for i in range(1,numberOfSims)]
	plt.plot(xaxis,yaxis,'g',xaxis,totalProfity,'r--')
	plt.xlabel("Simulations Played")
	plt.ylabel("Cash left after putting in $100")
	title = "Total Surplus of: $"+str(totalProfit)+" after "+str(numberOfSims)+ " Simulations of "+str(numOfGames)+" Games(Cheat strategy)"
	plt.title(title)
	print("TOTAL PROFIT:$",totalProfit)
	plt.show()


def simulateAIStrategy(numOfGames,numDecks,numberOfSims):
	xaxis = [i for i in range(1,numberOfSims)]
	yaxis = []
	totalProfit = 0
	for x in range(1,numberOfSims):
		winnings = playGameAIStrategy(numOfGames,numDecks)
		totalProfit += winnings
		yaxis.append(winnings-100)
		if(winnings >= 100): #player has a surplus
			print("After:",numOfGames,"games","You Won:$",winnings -100)
		else:
			print("After:",numOfGames,"games","You Lost:$",100 - winnings)
	totalProfit = int(totalProfit/numberOfSims)
	totalProfity = [totalProfit for i in range(1,numberOfSims)]
	plt.plot(xaxis,yaxis,'g',xaxis,totalProfity,'r--')
	plt.xlabel("Simulations Played")
	plt.ylabel("Cash left after putting in $100")
	title = "Avg Surplus of: $"+str(totalProfit)+" after "+str(numberOfSims)+ " Simulations of "+str(numOfGames)+" Games(Basic strategy)"
	plt.title(title)
	print("TOTAL PROFIT:$",totalProfit)
	plt.show()


#plays the game (numOfGames, numDecks)
def main():
	simulateAIStrategy(100,25,60)
	gameBoard = GameBoard(2,5)
	state = State(gameBoard,0)
	simulateAICheatStrategy(100,25,60)
	
	

if __name__=="__main__":
	main()















