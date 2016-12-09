#jake felzien

#	this file will be used to generate the plots to see and analyze the overal slop or regression line 
#	i am anticipating likes for popular accounts to diminish over time

import matplotlib.pyplot as plt
import numpy as np
import time
#import random

accountName = 'loki_the_wolfdog_SMALL'

#this will be a directory variable in which i plan to put the directory to the images, as well as the log file, i wish to access
imgdirectory = '/home/jfelzien/Desktop/cs5660/neuralNetFeed/images/'+accountName+'/'
logdirectory = '/home/jfelzien/Desktop/cs5660/neuralNetFeed/logFile.txt'

def loadHash(logFile, account):
	imageHash = {}
	hashFile = open(logFile, 'r')
	for line in hashFile:
		#print line.split()
		if line.split()[0] == account:
			imageHash[line.split()[1]] = line.split()[2]
	return imageHash
	
def loadAccounts():
	readFile = open(logdirectory, 'r')
	accountList = []
	for line in readFile:
		if line.split()[0] not in accountList and len(accountList) < 40:
			accountList.append(line.split()[0])
	return accountList

#testName = 'milo_french_bulldog'
#testName = 'taylor_swift'
	
if __name__ == "__main__":
	plt.title('Account Likes Over Time')
	plt.xlabel('Image ID')
	plt.ylabel('Like Counts')
	accountNames = loadAccounts()
	print accountNames
	#time.sleep(5)
	totalSlopes = []
	
	for name in accountNames:	
#		if name == testName:
#			continue
		count = 211
		imgHash = loadHash(logdirectory, name)
		yaxis = []
		xaxis = []
	
		for i in range(0, 10000):
			try:
				#print i , imgHash['img_'+str(i)+'.png']
				yaxis.append(float(imgHash['img_'+str(i)+'.png']))
				xaxis.append(i)
			except:
				print "does not exist"
				
		
		print "======="
		print "Messing around with my own outlier removal now:"
		#print "should be a value?" , abs(yaxis - np.mean(yaxis)) < 2 * np.std(yaxis)
		boolList = []
		m = 2
		for i in yaxis:
			if abs(i - np.mean(yaxis)) < m * np.std(yaxis):
				boolList.append(True)
			else:
				boolList.append(False)
				print i
				
		print "yaxis:", len(yaxis)
		print "how many values do we have" , len(boolList)
		print "standard dev * m:", m*np.std(yaxis)
		print "average of the y axis:", np.mean(yaxis)
		print boolList
				
		newx = []
		newy = []
		for index, i in enumerate(boolList):
			if i == False:
				print "we found a false"
			elif i == True:
				newx.append(xaxis[index])
				newy.append(yaxis[index])
					
		print "has it shrunken at all?", len(yaxis), len(xaxis), len(newx), len(newy)
		
		newy = np.asarray(newy)
		newx = np.asarray(newx)
		#plt.scatter(xaxis, yaxis)
		fit = np.polyfit(newx, newy, 1)
		fit_fn = np.poly1d(fit)
		#plt.add_subplot(count)
		plt.plot(newx, newy,'o', newx, fit_fn(newx))
		print "Here is the fit value:", fit
		print "Here is the slope value:", fit[0]/fit[1]
		count +=1
		print name
		totalSlopes.append(fit[0]/fit[1])
		plt.show()
		
	
	print "===="
	print totalSlopes
#	plt.show()
	print "Done Executing"
	
