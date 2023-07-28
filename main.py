#####################################################################################################
#
# Standard Import
#
#####################################################################################################

# image processing
import cv2

# display image
from matplotlib import pyplot as plt

# mathematical operation
import math

# argument parser
import argparse

import os

#####################################################################################################
#
# Local Import
#
#####################################################################################################

from helper import calculateVectorMagnitude

from image_plotter import Image, ImagePlotter

from contour_manipulation import Contour, ContourStorage 

if __name__ == '__main__':

	# argument parser
	parser = argparse.ArgumentParser()
	parser.add_argument( 'resultImageStoragePathStr', type=str, 
		     			help='path to save result image' )
	args = parser.parse_args()
	resultImageStoragePathStr = os.getcwd() +  args.resultImageStoragePathStr
	print( f'\n\n\n { resultImageStoragePathStr }' )

	# create image plotter object
	imagePlotter = ImagePlotter( 7, 7, 2, resultImageStoragePathStr )

	# reading image
	originalImage = cv2.imread( 'field_image_from_manual.png' )

	# add original image to figure
	imagePlotter.addImageToPlot( originalImage, 'original image' )

	# converting image into grayscale image
	grayScaleImage = cv2.cvtColor( originalImage, cv2.COLOR_BGR2GRAY )

	# add gray scale image to figure 
	imagePlotter.addImageToPlot( grayScaleImage, 'gray scale image' )

	# convert to binary image
	_, binaryImage = cv2.threshold( grayScaleImage, 127, 255, cv2.THRESH_BINARY )

	# add binary image to figure 
	imagePlotter.addImageToPlot( binaryImage, 'binary image' )

	# finding contours from binary image
	contourList, _ = cv2.findContours( binaryImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE )

	# init contour storage
	contourStorageObj = ContourStorage( contourList )

	# filter contour only in area range
	contourObjInAreaRangeList = contourStorageObj.filterContoursOnlyInAreaRange( 1000, 300000 )

	# copy original image to draw contour in area range
	originalImageForDrawContourInAreaRange = originalImage.copy()

	# loop through contour in area range
	for contourObj in contourObjInAreaRangeList:
		
		# using drawContours() function
		cv2.drawContours( originalImageForDrawContourInAreaRange, [ contourObj.contour ], 0, (0, 0, 255), 3 )

	# add original image with contour in area range to figure 
	imagePlotter.addImageToPlot( originalImageForDrawContourInAreaRange, 'contour in area range' )

	# copy original image to draw circle contour
	originalImageForDrawCircleContour = originalImage.copy()

	# copy original image to draw triangle contour
	originalImageForDrawTriangleContour = originalImage.copy()

	# copy original image to draw square contour
	originalImageForDrawSquareContour = originalImage.copy()

	# classify contour object by its shape
	contourStorageObj.classifyContourObjByShape()

	print( contourStorageObj.circleContourObjList )
	print( contourStorageObj.triangleContourObjList )
	print( contourStorageObj.squareContourObjList )

	# loop through each circle contour
	for circleContourObj in contourStorageObj.circleContourObjList:

		# draw contour 
		cv2.drawContours( originalImageForDrawCircleContour, [ circleContourObj.contour ], 0, (0, 0, 255), 3 )

	# add original image with circle contour 
	imagePlotter.addImageToPlot( originalImageForDrawCircleContour, 'circle contour' )

	# loop through each circle contour
	for triangleContourObj in contourStorageObj.triangleContourObjList:

		# draw contour 
		cv2.drawContours( originalImageForDrawTriangleContour, [ triangleContourObj.contour ], 0, (0, 0, 255), 3 )

	# add original image with triangle contour 
	imagePlotter.addImageToPlot( originalImageForDrawTriangleContour, 'triangle contour' )

	# loop through each circle contour
	for squareContourObj in contourStorageObj.squareContourObjList:

		# draw contour 
		cv2.drawContours( originalImageForDrawSquareContour, [ squareContourObj.contour ], 0, (0, 0, 255), 3 )

	# add original image with square contour 
	imagePlotter.addImageToPlot( originalImageForDrawSquareContour, 'square contour' )

	# copy original image to draw outer most circle contour
	originalImageForDrawOuterMostCircleContour = originalImage.copy()

	# copy original image to draw outer most triangle contour
	originalImageForDrawOuterMostTriangleContour = originalImage.copy()

	# copy original image to draw outer most square contour
	originalImageForDrawOuterMostSquareContour = originalImage.copy()

	# filter only outer most circle contour object
	contourStorageObj.outerMostCircleContourObjList = contourStorageObj.filterOnlyOuterMostContourObj( contourStorageObj.circleContourObjList, 4 )

	# loop through each outer most circle contour object
	for circleContourObj in contourStorageObj.outerMostCircleContourObjList:

		# draw contour 
		cv2.drawContours( originalImageForDrawOuterMostCircleContour, [ circleContourObj.contour ], 0, ( 0, 0, 255 ), 3 )

		# draw center point of contour
		cv2.circle( originalImageForDrawOuterMostCircleContour, circleContourObj.centerPointTuple, 7, ( 255, 255, 255 ), -1)

		# draw x-axis line of coordinate frame
		# cv2.line( originalImageForDrawOuterMostCircleContour, circleContourObj.centerPointTuple, circleContourObj.xAxisEndPointTuple, ( 0, 0, 255 ), 3)

		# draw y-axis line of coordinate frame
		cv2.line( originalImageForDrawOuterMostCircleContour, circleContourObj.centerPointTuple, circleContourObj.yAxisEndPointTuple, ( 0, 255, 0 ), 3)

	# add original image with outer most circle contour to figure
	imagePlotter.addImageToPlot( originalImageForDrawOuterMostCircleContour, 'outer most circle contour' )

	# filter only outer most triangle contour object
	contourStorageObj.outerMostTriangleContourObjList = contourStorageObj.filterOnlyOuterMostContourObj( contourStorageObj.triangleContourObjList, 5 )

	# loop through each outer most triangle contour object
	for triangleContourObj in contourStorageObj.outerMostTriangleContourObjList:

		# draw contour 
		cv2.drawContours( originalImageForDrawOuterMostTriangleContour, [ triangleContourObj.contour ], 0, ( 0, 0, 255 ), 3 )

		# draw center point of contour
		cv2.circle( originalImageForDrawOuterMostTriangleContour, triangleContourObj.centerPointTuple, 7, ( 255, 255, 255 ), -1)

	# add original image with outer most triangle contour to figure
	imagePlotter.addImageToPlot( originalImageForDrawOuterMostTriangleContour, 'outer most triangle contour' )

	# filter only outer most square contour object
	contourStorageObj.outerMostSquareContourObjList = contourStorageObj.filterOnlyOuterMostContourObj( contourStorageObj.squareContourObjList, 4 )

	# loop through each outer most square contour object
	for squareContourObj in contourStorageObj.outerMostSquareContourObjList:

		# draw contour 
		cv2.drawContours( originalImageForDrawOuterMostSquareContour, [ squareContourObj.contour ], 0, ( 0, 0, 255 ), 3 )

		# draw center point of contour
		cv2.circle( originalImageForDrawOuterMostSquareContour, squareContourObj.centerPointTuple, 7, ( 255, 255, 255 ), -1)

	# add original image with outer most square contour to figure
	imagePlotter.addImageToPlot( originalImageForDrawOuterMostSquareContour, 'outer most square contour' )

	# show figure
	imagePlotter.plotAndShowAllImage()