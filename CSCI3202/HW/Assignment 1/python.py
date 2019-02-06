def calculate(A,bet):
	for i in range(0,26):
		value = .05*(A[abs(16-i)]) + .05*(A[abs(4-i)]) + .05*(A[abs(1-i)]) 
		value = value + .05*(A[abs(13-i)]) + .05*(A[abs(23-i)]) + .15*(A[abs(15-i)]) + .05*(A[abs(9-i)]) + .05*(A[abs(11-i)]) + .05*(A[abs(0-i)]) + .2*(A[abs(13-i)]) + .15*(A[abs(22-i)]) + .05*(A[abs(5-i)])
		print(bet[i])
		print("%.3f"%value)

A = [.08, .015,.03,.04,.130,.02,.015,.060,.065,.005,.005,.035,.030,.070,.080,.020,.002,.065,.060,.090,.030,.01,.015,.005,.02,.002]
bet = "abcdefghijklmnopqrstuvwxyz"
print (calculate(A,bet))
