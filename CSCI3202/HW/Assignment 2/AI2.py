import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
def expected_loss(d, k, M, mu, sigma):
    #d decision that is made
	#k and M are parameter from the loss function
	#mu is the central tendency parameter from the lognormal prior distribution (mu = log m
	#sigma is the uncertainty parameter from the lognormal prior distribution (sigma = log s
	#return the expected loss using the catastrophic/plane-catching/Cinnabonmageddon loss function
	x = np.linspace(0,d,M)
	cdf = stats.lognorm.cdf(x,sigma,scale=np.exp(mu))
	Ex = np.exp(mu + (.5*sigma**2))
	result = k*d - k*Ex +M - M*cdf 
	return(result[-1])
k=1
M=300
mu=np.log(50)
sigma=np.log(1.2)

xbar = np.exp(mu + (.5*sigma**2))

sqrt = (sigma**2) - (2*mu) - 2*np.log((np.sqrt(2*np.pi)*sigma*k)/M)
dB_p = np.exp((mu - sigma**2) + sigma*np.sqrt(sqrt))
dB_m = np.exp((mu - sigma**2) - sigma*np.sqrt(sqrt))

expected_loss_dB_p = expected_loss(dB_p, k, M, mu, sigma)
expected_loss_dB_m = expected_loss(dB_m, k, M, mu, sigma)

dB = dB_p if expected_loss_dB_p < expected_loss_dB_m else dB_m

sigma = np.log(np.arange(1, 3, 0.01))
eviu = [0]*len(sigma)
evpi = [0]*len(sigma)
for i in range(len(sigma)):
    eviu[i] = expected_loss(xbar, k, M, mu, sigma[i]) - expected_loss(dB, k, M, mu, sigma[i])
    evpi[i] = expected_loss(dB, k, M, mu, sigma[i])
eviuData = np.round(eviu,4)
evpiData =np.round(evpi,4)
print(eviuData)
print(sigma)

plt.plot(sigma,eviuData,'r--',sigma,evpiData, 'b--')
plt.xlabel('sigma')
plt.ylabel('EVIU and EVPI')
plt.show()