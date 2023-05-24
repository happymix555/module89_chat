# image processing
import cv2

# showing image in multiple format we want
from matplotlib import pyplot as plt

def filterContoursOnlyInAreaRange( contourList, minArea=0, maxArea=0 ):
	''' - get only contour in area range

		ARGS:
			- contourList ( list )
			- minArea ( int )
			- maxArea ( int )

		RETURN:
			- contourListInAreaRange ( list )
	'''

	# contour in area range storage
	contourListInAreaRange = []

	# loop through each contour
	for contour in contourList:

		# calculate contour area
		contourArea = cv2.contourArea( contour )

		# this contour is in range
		if minArea <= contourArea <= maxArea:
			
			# store it
			contourListInAreaRange.append( contour )
	return contourListInAreaRange

def isSquareContour(contour, epsilon=0.05):

	# approximate contour to a rough shape
	# calculate perimeter
	perimeter = cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, epsilon * perimeter, True)
	for point in approx:
		print( '[isSquareContour] approx: {}'.format( point[0] ) )
		print( '[isSquareContour] x: {}, y: {}'.format( point[0][0], point[0][1] ) )

	# is this shape has 4 vertices?
	# is each of vertices make 90 degree angle to each other?
	# is each of the side has an equally length?

def isCircle(contour, circularity_threshold=0.2):
	pass

def isTriangle(contour):
	
	pass

def addImageToFigure( figure, image, imageTitle, numberOfRow, numberOfColumn, imagePosition ):
	''' - add image to matplotlib figure at specific position
	'''

	# set position of image
	figure.add_subplot( numberOfRow, numberOfColumn, imagePosition )

	# convert image to rgb 
	rgbImage = cv2.cvtColor( image, cv2.COLOR_BGR2RGB )

	# add image to figure
	plt.imshow( rgbImage )

	# not show the axis
	plt.axis( 'off' )

	# set image title
	plt.title( imageTitle )

# create figure with size 10 * 7 inches
fig = plt.figure( figsize = ( 10, 70 ) )

# reading image
originalImage = cv2.imread( 'field_image_from_manual.png' )

# add original image to figure
addImageToFigure( fig, originalImage, 'original image', 4, 1, 1 )

# converting image into grayscale image
grayScaleImage = cv2.cvtColor( originalImage, cv2.COLOR_BGR2GRAY )

# add gray scale image to figure 
addImageToFigure( fig, grayScaleImage, 'gray scale image', 4, 1, 2 )

# convert to binary image
_, binaryImage = cv2.threshold( grayScaleImage, 127, 255, cv2.THRESH_BINARY )

# add binary image to figure 
addImageToFigure( fig, binaryImage, 'binary image', 4, 1, 3 )

# using a findContours() function
contourList, _ = cv2.findContours( binaryImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE )

# filter contour by area
contourInAreaRangeList = filterContoursOnlyInAreaRange( contourList, 1000, 100000 )

# copy original image to draw contour in area range
originalImageForDrawContourInAreaRange = originalImage.copy()

# loop through contour in area range
for contour in contourInAreaRangeList:
	
	# using drawContours() function
	cv2.drawContours( originalImageForDrawContourInAreaRange, [ contour ], 0, (0, 0, 255), 3 )

# add original image with contour in area range to figure 
addImageToFigure( fig, originalImageForDrawContourInAreaRange, 'binary image', 4, 1, 4 )

# show figure
plt.show()

# # converting image into grayscale image
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # display image wit

# # setting threshold of gray image
# _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# # displaying the image after drawing contours
# cv2.imshow('threshold', threshold)

# # using a findContours() function
# contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# # filter contour by size
# filteredContoursByArea = filterContoursOnlyInAreaRange( contours, 1000, 100000 )

# # debug
# print( 'number of filteredContours: {}'.format( len( filteredContoursByArea ) ) )

# i = 0

# finalContours = []

# # list for storing names of shapes
# for contour in filteredContoursByArea:

# 	# is square
# 	if isSquareContour( contour ):
# 		finalContours.append( contour )
# 		continue

# 	# is circle
# 	# if isCircle( contour ):
# 	# 	finalContours.append( contour )
# 	# 	continue

# 	# # is triangle
# 	# if isTriangle( contour ):
# 	# 	finalContours.append( contour )
# 	# 	continue   

# for finalContour in finalContours:
	
# 	# using drawContours() function
# 	cv2.drawContours(img, [finalContour], 0, (0, 0, 255), 3)

# # displaying the image after drawing contours
# cv2.imshow('shapes', img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()