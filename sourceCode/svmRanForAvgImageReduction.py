#Jake Felzien
# this will be an image reduction attempt at using the svm and random forest average again
# same code as image Reduction but testing improved accuracy

from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import time
import cv2
import random
import numpy as np
from PIL import Image

accountName = 'loki_the_wolfdog_SMALL'
#accountName = 'destination_wild'

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

def loadImage(path):
	im = cv2.imread(path)
	return flatten(im)
 
def flatten(x):
	result = []
	for el in x:
		if hasattr(el, "__iter__") and not isinstance(el, basestring):
			result.extend(flatten(el))
		else:
			result.append(el)
	return result

def avgErrorCalc(actualAr, expAr):
	resultarray = []
	for index, i in enumerate(actualAr):
		resultarray.append(float((abs(actualAr[index] - expAr[index]) / actualAr[index]) * 100 ))
	total = 0.0
	for i in resultarray:
		total += i 
	return total/len(resultarray)

def loadAccounts():
	readFile = open(logdirectory, 'r')
	accountList = []
	for line in readFile:
		if line.split()[0] not in accountList and len(accountList) < 40:
			accountList.append(line.split()[0])
	return accountList

def smallImageLoad(path):
	image = Image.open(path).convert('L')
	pix = np.asarray(image)
	oneDpixelArray = []
	for i in pix:
		for j in i:
			oneDpixelArray.append(j)
#	print oneDpixelArray
	return oneDpixelArray



if __name__ == "__main__":
	startTime = time.time()
	overallPercentErrorDist = []
	#now we are going to do a quick test with all of the accounts to compare and analyze all of the results
	userNameList = loadAccounts()
	print(userNameList)
	#time.sleep(300)
	for index, accountName in enumerate(userNameList):
		#this was for simple memory testing purposes, only wanted to limit to one account and see what happens
		#if index > 0:
		#	break
		if accountName == 'celebrity_food' or accountName == 'milo_french_bulldog' or accountName == 'tristin_sugi':
			continue
		X = []
		y = []
		imgHash = loadHash(logdirectory, accountName)
		#this is an inital tester, make sure to comment this out later
		t = loadImage(imgdirectory+'img_0.png')
		print (t)
		#print "length of t:", len(t)

		print(imgHash)
		print len(imgHash)
		#time.sleep(30)
		#now we need to load all of these values somewhere to test for outliers... 
			#jam it in a list
		outlierTotalList= []
		for i in imgHash:
			outlierTotalList.append(int(imgHash[i]))
#		print('here we go:')
#		print(outlierTotalList)
#		print(np.mean(outlierTotalList))
#		print(np.std(outlierTotalList))
		m = 2

		#time.spleep(30)
		#now lets load all of the images into our massive array
		#don't forget to add an outlier check. load all of the total like counts into a list and do a similar technique to the plotting file
		#also, I need to implement a random selection and keep track of it, where i select 50 random images or so for training
			#and then test on a huge amount of random ones, but always make sure to not add stuff that has already been used
		#for i in range(0,100):
		countList = []

		i = 0
		smallImageLoad(imgdirectory+'img_'+str(i)+'.png')

		while len(countList) < 90:
			i = random.randint(0, (len(imgHash)+80))
			if i not in countList:
				try:
					if abs(float(imgHash['img_'+str(i)+'.png']) - np.mean(outlierTotalList)) < m * np.std(outlierTotalList):
						print "Loading image: ", i
						print imgHash['img_'+str(i)+'.png']
						temp = smallImageLoad(imgdirectory+'img_'+str(i)+'.png')
						temp.append(i)
						X.append(temp)
						y.append(imgHash['img_'+str(i)+'.png'])
						countList.append(i)
				except:
					print ("Image does not exist, cannot be added to training data")

		print("On Index:", index, "   account Name = ", accountName)
		print ("Training the classifier")
		#clf = MLPClassifier(activation='logistic', solver='lbfgs', alpha=0.001, hidden_layer_sizes=(100, 50, 50, 50, 50, 50), random_state=1, max_iter=2000)
		clf = RandomForestClassifier(n_estimators=100)
		clf2 = svm.SVC(gamma=0.001, C=100)
		#clf2 = MLPClassifier(activation='logistic', solver='lbfgs', alpha=0.001, hidden_layer_sizes=(60, 40, 100, 200), random_state=1, max_iter=50, verbose = True)

		clf.fit(X, y)
		clf2.fit(X, y)

		#this was a single test to see if we had a complete model, good to go
		#print "Printing results of image 0"
		#print clf.predict([t])
		#print imgHash['img_0.png']
		#print imgHash['img_'+str(i)+'.png']
		actual = []
		experimental = []

		tensPlaceComparison = 0.0
		correctValue = 0.0
		totalValue = 0.0

		#this needs to be fixed
		#t = loadImage(imgdirectory+'img_0.png')
		#experimentalVal = ((float(clf.predict([t])[0]) + float(clf2.predict([t])[0])) / 2)

		#for i in range(100, 200):
		while len(countList) < 120:
			i = random.randint(0, (len(imgHash)+80))
			if i not in countList:
				try:
					if abs(float(imgHash['img_'+str(i)+'.png']) - np.mean(outlierTotalList)) < m * np.std(outlierTotalList):
						t = smallImageLoad(imgdirectory+'img_'+str(i)+'.png')
						t.append(i)
						experimentalVal = ((float(clf.predict([t])[0]) + float(clf2.predict([t])[0])) / 2)
						print ("Experimental:", experimentalVal , "     Actual:" , imgHash['img_'+str(i)+'.png'])
						actual.append(float(imgHash['img_'+str(i)+'.png']))
						experimental.append(float(experimentalVal))
						countList.append(i)
						if len(str(float(clf.predict([t])[0]))) == len(str(float(imgHash['img_'+str(i)+'.png']))):
							correctValue+=1
							totalValue+=1
						else:
							totalValue+=1
				except:
					print ('image does not exist, unable to test')
		tensPlaceComparison = correctValue/totalValue
		print ("\n\nError Analysis:")
		print ("Average Error:", avgErrorCalc(actual, experimental))
		print ('\n New Metric Check:', tensPlaceComparison)
		print ("Time to execute: ", time.time() - startTime , " seconds")
		print ("Time to execute: ", (time.time() - startTime)/60 , " minutes")
		print ("Time to execute: ", ((time.time() - startTime)/60)/60 ,  " hours")
		overallPercentErrorDist.append((accountName, tensPlaceComparison, avgErrorCalc(actual, experimental)))
avgList = []
avgList2 = []
print('\n\n\n')
for i in overallPercentErrorDist:
	print(i)
	avgList.append(i[2])
	avgList2.append(i[1])

print "SVM and RanForest COMBO\n\n"
print '\n\n\n Average Calc:', np.mean(avgList) 
print "Precision by tens:", np.mean(avgList2)

print ("Time to execute: ", time.time() - startTime , " seconds")
print ("Time to execute: ", (time.time() - startTime)/60 , " minutes")
print ("Time to execute: ", ((time.time() - startTime)/60)/60 ,  " hours")
print ("Done Executing")