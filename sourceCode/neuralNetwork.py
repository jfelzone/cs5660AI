#this file will be used to write my neural network and train my images
	# currently waiting to transfer all of my images from mac to linux box
	# definitely a bummer how much of an inconvenience getting all these dependencies running together has been

#Jake Felzien
import pyautogui
from pybrain.datasets.supervised import SupervisedDataSet 
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import cv2
import time
import math
#pyautogui.moveTo(100,100, 5)

#current account we will be looking at (basically the folder name of the images for the account)
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
		resultarray.append(float((abs(actualAr[index] - expAr[index]) / actualAr[index]) * 100))
	total = 0.0
	for i in resultarray:
		total += i
	return total/len(resultarray)
 
if __name__ == "__main__":
	startTime = time.time()
	imgHash = loadHash(logdirectory, accountName)
	print(imgHash)
	print(imgdirectory)
	
	#t = loadImage('a.png')
   	#t = loadImage('baby1.png')
	t = loadImage(imgdirectory+'img_0.png')
	print "length of t:", len(t)
	net = buildNetwork(len(t), 45, 1)

	#net = buildNetwork(10, 10, 1)
	ds = SupervisedDataSet(len(t), 1)
	#ds = SupervisedDataSet(10, 1)
	#ds.addSample(loadImage('img_0.png'),(34500,))
	#ds.addSample(loadImage('img_1.png'),(41100,))
	#ds.addSample(loadImage('img_2.png'),(25800,))
	#ds.addSample(loadImage('img_4.png'),(47600,))

    	#so this works very well and very quickly
	for i in range(0,21):
		try:
			ds.addSample(loadImage(imgdirectory+'img_'+str(i)+'.png'), (imgHash['img_'+str(i)+'.png'],))
		except:
			print "Image does not exist, cannot be added to training data"
		#ds.addSample(loadImage(imgdirectory+'img_0.png'), (imgHash['img_0.png'],))
    	#ds.addSample(loadImage(imgdirectory+'img_1.png'), (imgHash['img_1.png'],))
    	#ds.addSample(loadImage('baby2.png'), (250,))
	    
    	#ds.addSample(loadImage('a.png'),(1,))
    	#ds.addSample(loadImage('b.png'),(2,))
    	#ds.addSample(loadImage('c.png'),(3,))
    	#ds.addSample(loadImage('d.png'),(4,))
	


	trainer = BackpropTrainer(net, ds)
	error = 10
	iteration = 0
	while error > 0.001:
		error = trainer.train()
		iteration += 1
		print "Iteration: {0} Error {1}".format(iteration, error)
	
	actualArray = []
	experimentalArray =[]
	for i in range(35, 60):
		try:
			print "\nResult: ", net.activate(loadImage(imgdirectory+'img_'+str(i)+'.png')) , " Actual: " , imgHash['img_'+str(i)+'.png']
			experimentalArray.append(float(net.activate(loadImage(imgdirectory+'img_'+str(i)+'.png'))))
			actualArray.append(float(imgHash['img_'+str(i)+'.png']))
		except:
			print "image does not exist, cannot test"

	#print "\nResult: ", net.activate(loadImage('baby1.png'))
    	#print "\nResult: ", net.activate(loadImage('baby2.png'))
    	#print "\nResult: ", net.activate(loadImage('baby3.png'))
    	
    	print "Here is the length of t: " , len(t)
	print "Average error: " , avgErrorCalc(actualArray, experimentalArray)
	print "Done Executing"
	print "Time to execute: ", time.time() - startTime , " seconds"
	print "Time to execute: ", (time.time() - startTime)/60 , " minutes"
	print "Time to execute: ", ((time.time() - startTime)/60)/60 ,  " hours"
