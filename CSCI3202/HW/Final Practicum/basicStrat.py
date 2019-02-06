




    
def calculateMoveOnStrategy(state,ace): #uses basic strategy to decide a move for the AI
  playerHandSum = state.gameBoard.playerHandSum(state.player)
  dealerHandSum = state.gameBoard.playerHandSum(state.dealer)
  if(ace == False): #player doesnt have an ace
    if(playerHandSum[1] == 21 | playerHandSum[0] == 21):#balckJack dealt
      return "2"
    elif(playerHandSum[1]<=11):#freehit
      if (10<=playerHandSum[1]<=11) & (dealerHandSum[1] <=9) & (dealerHandSum[0]!=2): #doubleDown
        return "3"
      else:
        return "1"
    elif(playerHandSum[1]>11): #bring up decision to hit or stand and return a percentage
      if(playerHandSum[1]>=17):
        return "2"
      elif((playerHandSum[1]>12) & (dealerHandSum[1]>6)):
        return "1"
      elif(playerHandSum[1]>12 & 2<=dealerHandSum[1]<=6):
        return "2"  
      elif(playerHandSum[1]==12):
        #print("SUM 12")
        if(dealerHandSum[1]<4):
          return "1"
        elif dealerHandSum[1]>6:
          return "1"
        else:
          return "2"
      else:
        return "2"

  else: #player dealt an ace
    #print("PLAYER has ace")
    if(playerHandSum[1]>18):
      return "2"

    elif playerHandSum[0] ==8: # A 7
      if (dealerHandSum[0] ==2) | (dealerHandSum[0] ==7) | (dealerHandSum[0] ==8):
        return "2"
      elif(2<dealerHandSum[1]<7):
        return "3"
      else:
        return "1"
    else:
      if(playerHandSum[0] == 21 | playerHandSum[0] == 21):#balckJack dealt
        return "2"
      elif(playerHandSum[0]<=11):#freehit
        if (10<=playerHandSum[0]<=11) & (dealerHandSum[1] <=9) & (dealerHandSum[0]!=2): #doubleDown
          return "3"
        else:
          return "1"
      elif(playerHandSum[0]>11): #bring up decision to hit or stand and return a percentage
        if(playerHandSum[0]>=17):
          return "2"
        elif((playerHandSum[0]>12) & (dealerHandSum[1]>6)):
          return "1"
        elif(playerHandSum[0]>12) & (2<=dealerHandSum[1]<=6):
          return "2"  
        elif(playerHandSum[0]==12):
          if(dealerHandSum[0]<4):
            return "1"
          elif dealerHandSum[0]>6:
            return "1"
          else:
            return "2"
        else:
          return "2"
          
      

def AIBetAmount(state):
  trueSum = state.getTrueCount()
  if(trueSum>4):
    if(state.gameBoard.playerList[1].bet*2>state.player.cash):
      return "5"
    else:
      return "10"
  elif(trueSum<1):
    if(state.gameBoard.playerList[1].bet*2)>5:
      return "10"
    else:
      return "5"
  else:
    return"5"
