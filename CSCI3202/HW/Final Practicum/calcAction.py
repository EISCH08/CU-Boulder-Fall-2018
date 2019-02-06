
def checkDealerGameOver(dealerSum):
	if dealerSum[0]>16:
		return True
	else:
		return False
def willDealerBust(dealerHand,gameBoard):
	valLow = 0
	valHigh = 0
	for x in dealerHand:
			if(gameBoard.deck.getValue(x) == (1,11)): #accounts for the ace draw
				valLow += 1
				valHigh +=11
			else: #any other card
				valLow +=gameBoard.deck.getValue(x)
				valHigh +=gameBoard.deck.getValue(x)
	dealerSum = (valLow,valHigh)
	if(checkDealerGameOver(dealerSum) == False):
		nextCard = gameBoard.deck.dealCard()
		dealerHand.append(nextCard)
		return willDealerBust(dealerHand,gameBoard)
	else:
		if(dealerSum[1]>21):
			return True
		else:
			return False


def willPlayerBustNextTurn(playerHand,deckOrder,gameBoard):
	valLow = 0
	valHigh = 0
	nextCard = deckOrder[-1]
	newPlayerHand = playerHand
	print(playerHand)
	print(nextCard)
	newPlayerHand.append(nextCard)
	print(newPlayerHand)
	for x in newPlayerHand:
			if(gameBoard.deck.getValue(x) == (1,11)): #accounts for the ace draw
				valLow += 1
				valHigh +=11
			else: #any other card
				valLow +=gameBoard.deck.getValue(x)
				valHigh +=gameBoard.deck.getValue(x)
	playerSum = (valLow,valHigh)
	newPlayerHand.pop()
	if playerSum[1]>21:
			print("player will bust nextCard")
			return True
	else:
		return False

		




# def closerTo21ThanDealer(playerHand,dealerHand,gameBoard):
# 	newPlayerHand = playerHand
# 	newDealerHand = dealerHand
# 	nextCard = gameBoard.deck.order[0]
# 	newPlayerHand.append(nextCard)
# 	newDealerHand.append(nextCard)
# 	valLow = 0
# 	valHigh = 0
# 	for x in newPlayerHand:
# 			if(gameBoard.deck.getValue(x) == (1,11)): #accounts for the ace draw
# 				valLow += 1
# 				valHigh +=11
# 			else: #any other card
# 				valLow +=gameBoard.deck.getValue(x)
# 				valHigh +=gameBoard.deck.getValue(x)
# 	newPlayerSum = (valLow,valHigh)
# 	valLow = 0
# 	valHigh = 0
# 	for x in newDealerHand:
# 			if(gameBoard.deck.getValue(x) == (1,11)): #accounts for the ace draw
# 				valLow += 1
# 				valHigh +=11
# 			else: #any other card
# 				valLow +=gameBoard.deck.getValue(x)
# 				valHigh +=gameBoard.deck.getValue(x)
# 	newDealerSum = (valLow,valHigh)

# 	if(newPlayerSum[1]<21 & newPlayerSum[1] > newDealerSum[1]):
# 		return True



	



def calculateBestAction(state):
	gameBoard = state.gameBoard
	player = state.player
	dealer = state.dealer
	deckOrder = gameBoard.deck.order
	playerHand = gameBoard.playerList[1].hand
	dealerHand = gameBoard.playerList[0].hand
	playerSum = gameBoard.playerHandSum(player)
	dealerSum = gameBoard.playerHandSum(dealer)

	if(willDealerBust(dealerHand,gameBoard) == True):
		return "2"
	else:
		if willPlayerBustNextTurn(playerHand,deckOrder,gameBoard) == False:
			return "1"
		else:
			print("player will bust nextCard")
			return "2"







	
