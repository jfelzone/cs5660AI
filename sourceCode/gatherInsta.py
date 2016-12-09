import pyautogui
import time
import pytesseract
from PIL import Image
import pybrain
import os
#from instagram.client import InstagramAPI

#this must be run with chrome at 150% zoom to be able to read the like counts correctly

#based on this working so well my thought from here that i will need to implement 
	# (maybe later tonight as a sample)
	#is to have the heart symbol be a marker and as soon as it is gone that is the picture we care about.
	# (we would get there through really really small jumps at at ime)
	#scroll down at a larger speed (maybe 10),
		#if no likes are recognized, scrap the picture, if likes are recognized, 
		# rename the picture and save it off

	#rinse and repeat

#this was just a little gut test to analyze how slow a one scroll speed was (aka the heart scroll speed)

#couldn't get the api to work and my new approach seemed faster anyway
'''
api = InstagramAPI(client_id='1338ae628ba84de0a61a5bda4491e901', client_secret='596ff77174aa4f5691ffec4b31d75ff5')
popular_media = api.media_popular(count=20)
for media in popular_media:
    print(media.images['standard_resolution'].url)
'''
#for some reason we never were able to get the API to work,
	#however, this technique should be able to pull more pictures an hour anyway

#keep in mind we are running this with chrome zoomed into 150% (it allows us to read the like counts)
	#otherwise tesseract doesn't pick up these values

#created a log file to store all of the images and their like counts


#this is used to modify the account before running it on a given account
#account = 'loki_the_wolfdog'
#account = 'donald_trump'
#account = 'star_wars'
#account = 'milo_french_bulldog'
#account = 'google'
#account = 'discovery_channel'
#account = 'loki_the_wolfdog_SMALL'
#account = 'milo_french_bulldog'
#account = 'destination_wild'
#account = 'tristin_sugi'
account = 'star_wars'

#this is used because for some reason the first click goes through, but then the rest need double clicks
count = 0 

#make the new folder we will place these specific images in
newpath = r'images/'+account 
if not os.path.exists(newpath):
    os.makedirs(newpath)


# this function will be called logging, and it is responsible for checking if we have a valid file
	# that we can log, 
	# it will also be responsible for saving and updating the log file if the picture is valid
	# and lastly, it will be responsible for removing saved pictures that cannot be logged 
	# (if the likes aren't readable, or if it is a video, etc)

def logger(accountName, fileName, numberOfLikesString):
	deleteFile = False
	if numberOfLikesString == '':
		deleteFile = True
	if 'k' in numberOfLikesString:
		numberOfLikesString = numberOfLikesString.split('k')[0]
		if numberOfLikesString == '':
			deleteFile = True
		else:
			numberOfLikesString += '000'
		if '.' in numberOfLikesString:
			numberOfLikesString = numberOfLikesString.replace('.', '')
			numberOfLikesString = numberOfLikesString[:-1]

	if 'm' in numberOfLikesString:
		numberOfLikesString = numberOfLikesString.split('m')[0]
		if numberOfLikesString =='':
			deleteFile = True
		else:
			numberOfLikesString += '000000'
			if '.' in numberOfLikesString:
				numberOfLikesString = numberOfLikesString.replace('.', '')
				numberOfLikesString = numberOfLikesString[:-1]
	if ',' in numberOfLikesString:
		numberOfLikesString=numberOfLikesString.replace(',', '')
	print(numberOfLikesString)

	if deleteFile:
		os.remove('images/'+accountName+'/'+fileName)
		print("file removed: ", fileName, accountName)
	else:
		file = open('logFile.txt', 'a')
		file.write(accountName+" "+fileName+" "+numberOfLikesString+'\n')
		file.close()

while True:
	#scroll then capture the first picture
	pyautogui.scroll(-10.6)
	pyautogui.moveTo(290, 400, .5)
	pyautogui.click(290, 400, 2)
	time.sleep(.5)
	buttonLocation = pyautogui.locateOnScreen('back.png')
	buttonx, buttony = pyautogui.center(buttonLocation)
	pyautogui.moveTo(buttonx, buttony, .5)
	time.sleep(.2)
	#analyzing the text on the image
	im1 = pyautogui.screenshot()
	directory = 'images/'+account+'/img_'+str(count)+'.png'
	#thinking i will leave this in, but then resave the image again with the smaller screenshot
	if not os.path.exists(directory):
		im1.save(directory)
	text = pytesseract.image_to_string(Image.open(directory))
	im2 = pyautogui.screenshot(region=(200, 300, 300, 300))
	im2.save(directory)
	#print (text.split())
	#a variable we will pass into the logger function
	likeRead = ''
	for index, item in enumerate(text.split()):
		if item == 'likes':
			likeRead = text.split()[index-1] 
			print (text.split()[index-1], text.split()[index])

	logger(account, 'img_'+str(count)+'.png', likeRead)
	
	if count == 0:
		pyautogui.click()
	else:
		pyautogui.click()
		time.sleep(.5)
		pyautogui.click()
	count +=1
	pyautogui.moveRel(0, 30, .2)

#now we capture the second picture
	time.sleep(1)
	pyautogui.moveTo(590, 400, .5)
	pyautogui.click(590, 400, 2)
	time.sleep(.5)
	buttonLocation = pyautogui.locateOnScreen('back.png')
	buttonx, buttony = pyautogui.center(buttonLocation)
	pyautogui.moveTo(buttonx, buttony, .5)
	time.sleep(.2)
	#analyzing the text on the image
	im1 = pyautogui.screenshot()
	directory = 'images/'+account+'/img_'+str(count)+'.png'
	if not os.path.exists(directory):
		im1.save(directory)
	text = pytesseract.image_to_string(Image.open(directory))
	im2 = pyautogui.screenshot(region=(200, 300, 300, 300))
	im2.save(directory)
	#print (text.split())
	#a variable we will pass into the logger function
	likeRead = ''
	for index, item in enumerate(text.split()):
		if item == 'likes':
			likeRead = text.split()[index-1] 
			print (text.split()[index-1], text.split()[index])

	logger(account, 'img_'+str(count)+'.png', likeRead)
	
	if count == 0:
		pyautogui.click()
	else:
		pyautogui.click()
		time.sleep(.5)
		pyautogui.click()
	count +=1
	pyautogui.moveRel(0, 30, .2)

#now we capture the last picture on that row
	time.sleep(1)
	pyautogui.moveTo(890, 400, .5)
	pyautogui.click(890, 400, 2)
	time.sleep(.5)
	buttonLocation = pyautogui.locateOnScreen('back.png')
	buttonx, buttony = pyautogui.center(buttonLocation)
	pyautogui.moveTo(buttonx, buttony, .5)
	time.sleep(.2)
	#analyzing the text on the image
	im1 = pyautogui.screenshot()
	directory = 'images/'+account+'/img_'+str(count)+'.png'
	if not os.path.exists(directory):
		im1.save(directory)
	text = pytesseract.image_to_string(Image.open(directory))
	im2 = pyautogui.screenshot(region=(200, 300, 300, 300))
	im2.save(directory)
	#print (text.split())
	#a variable we will pass into the logger function
	likeRead = ''
	for index, item in enumerate(text.split()):
		if item == 'likes':
			likeRead = text.split()[index-1] 
			print (text.split()[index-1], text.split()[index])

	logger(account, 'img_'+str(count)+'.png', likeRead)
	
	if count == 0:
		pyautogui.click()
	else:
		pyautogui.click()
		time.sleep(.5)
		pyautogui.click()
	count +=1
	pyautogui.moveRel(0, 30, .2)



	#if pyautogui.locateOnScreen('x.png'):
	#	print("we found the x")
	#if pyautogui.locateOnScreen('loadmore.png'):
	#	print("we found the load more")
	#time.sleep(.5)
    

'''


for i in range(0,200):
	im1 = pyautogui.screenshot(region=(150, 70, 900, 680))
	im1.save('newImage.png')
	text = pytesseract.image_to_string(Image.open('newImage.png'))
	#print (text.split())
	for index, item in enumerate(text.split()):
		if item == 'likes':
			print (text.split()[index-1], text.split()[index])
	print ('\n')
	pyautogui.scroll(-10)
'''