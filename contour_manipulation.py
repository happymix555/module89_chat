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

#####################################################################################################
#
# Local Import
#
#####################################################################################################

from helper import calculateVectorMagnitude

class ContourStorage:
	''' - store and manage contour object by its type

		- contour has 3 types:
			- square contour
			- triangle contour
			- circle contour
	'''
	
	def __init__( self, contourList ):

		# all contour storage
		self.allContourList = contourList

		# all contour object storage
		self.allContourObjList = list()

		# convert contour to contour object
		# this is going to use for further processing
		self._createContourObj()

		# contour contour in area range storage
		self.contourObjInAreaRangeList = list()

		# square contour object storage
		self.squareContourObjList = list()
		
		# triangle contour object storage
		self.triangleContourObjList = list()
		
		# circle contour object storage
		self.circleContourObjList = list()

		# outer most square contour object storage
		self.outerMostSquareContourObjList = list()

		# outer most triangle contour object storage
		self.outerMostTriangleContourObjList = list()

		# outer most circle contour object storage
		self.outerMostCircleContourObjList = list()

	def _createContourObj( self ):
		''' - construct contour object from list of contour
		'''

		# loop through each contour
		for contour in self.allContourList:

			# create contour object
			contourObj = Contour( contour )

			# store contour object
			self.allContourObjList.append( contourObj )

	def filterContoursOnlyInAreaRange( self, minArea=0, maxArea=0 ):
		''' - get only contour in area range

			ARGS:
				- contourObjList ( list )
				- minArea ( int )
				- maxArea ( int )

			RETURN:
				- contourObjInAreaRangeList ( list )
		'''

		# loop through each contour object
		for contourObj in self.allContourObjList:

			# this contour is in range
			if minArea <= contourObj.area <= maxArea:
				
				# store it
				self.contourObjInAreaRangeList.append( contourObj )
		return self.contourObjInAreaRangeList

	def isOuterMostContour( self, contourObj, otherContourObjList, epsilonPercent ):
		''' - check to see if this contour object is NOT inside any of the other contour object
		'''

		# approximate polygon of contour object
		approximatedPointList = contourObj.approximatePolygonOfContour( epsilonPercent )
		
		# loop through each other contour obj 
		for otherContourObj in otherContourObjList:

			# loop each point in approximated polygon
			for point in approximatedPointList:

				pointTuple = ( int( point[ 0 ][ 0 ] ), int( point[ 0 ][ 1 ] ) )

				# point is inside other approximated polygon
				if cv2.pointPolygonTest( otherContourObj.contour, pointTuple, False ) > 0:
					
					# this is NOT the outer most contour
					return False

		# this is the outer most contour
		return True

	def isSquareContour( self, contourObj, epsilonPercent, errorPercent ):
		''' - check if this contour object is square shape

			- this contour object is square contour if:
				- its approximated curve has 4 points
				- its bounding box has an aspect ration close to 1
		'''

		# calculate approximation curve of contour
		approximatedPointList = contourObj.approximatePolygonOfContour( epsilonPercent  )

		# contour has polygon approximation point equal to 4
		if len( approximatedPointList ) == 4:

			# calculate approximation polygon bounding box
			( xPosition, yPosition, boundingBoxWidth, boundingBoxHeight ) = cv2.boundingRect( approximatedPointList )
			
			# calculate aspect ratio of bounding box
			boundingBoxAspectRatio = boundingBoxWidth / boundingBoxHeight

			# calculate acceptable error
			acceptableError = errorPercent / 100 

			# this bounding box is square
			if 1 - acceptableError <= boundingBoxAspectRatio <= 1 + acceptableError:
				
				# this is square contour
				return True
			
		# this contour is not square
		return False
	
	def isTriangleContour( self, contourObj, epsilonPercent ):
		''' - check if this is a triangle shape contour

			- this contour is triangle if:
				- it approximation curve has 3 points 
		''' 

		# calculate approximation curve of contour
		approximatedPointList = contourObj.approximatePolygonOfContour( epsilonPercent  )

		# this is triangle shape contour
		if len( approximatedPointList ) == 3:
			return True
		
		# this is not a triangle contour
		return False
	
	def isCircleContour( self, contourObj, epsilonPercent, errorPercent ):
		''' - check if this is a circle contour

			- this contour in circle if:
				- approximate point is more than5
				- bounding box has square aspect ratio
		'''

		# calculate approximation curve of contour
		approximatedPointList = contourObj.approximatePolygonOfContour( epsilonPercent  )

		# contour has polygon approximation point more than 5
		if len( approximatedPointList ) > 5:

			# calculate approximation polygon bounding box
			( xPosition, yPosition, boundingBoxWidth, boundingBoxHeight ) = cv2.boundingRect( approximatedPointList )
			
			# calculate aspect ratio of bounding box
			boundingBoxAspectRatio = boundingBoxWidth / boundingBoxHeight

			# calculate acceptable error
			acceptableError = errorPercent / 100 

			# this bounding box is square
			if 1 - acceptableError <= boundingBoxAspectRatio <= 1 + acceptableError:
				
				# this contour is circle
				return True
			
		# this contour is not circle
		return False
	
	def classifyContourObjByShape( self ):
		''' - classify contour object by its shape

			- we are focusing only for 3 type of contour here:
				- square
				- circle
				- triangle
		'''

		# loop through each contour object in area range
		for contourObj in self.contourObjInAreaRangeList:
			
			# this is circle contour
			if self.isCircleContour( contourObj, 4, 6 ):
			
				# store contour object in circle contour storage
				self.circleContourObjList.append( contourObj )

				# set contour's shape type
				contourObj.shapeTypeStr = 'circle'
				continue

			# this is triangle contour
			if self.isTriangleContour( contourObj, 5 ):

				# store contour object in triangle contour storage
				self.triangleContourObjList.append( contourObj )

				# set contour's shape type
				contourObj.shapeTypeStr = 'triangle'
				continue

			# this is square contour
			if self.isSquareContour( contourObj, 4, 5 ):

				# store contour object in square contour storage
				self.squareContourObjList.append( contourObj )

				# set contour's shape type
				contourObj.shapeTypeStr = 'square'
				continue
	
	def filterOnlyOuterMostContourObj( self, contourObjList, epsilonPercent ):
		''' - filter to get only the outer most contour obj from contour object list

			ARGS: 
				- contourObjList ( list ) --> input contour list
				- epsilonPercent ( int )

			RETURN:
				- outerMostContourObjList ( list )
		'''

		# outer most contour object storage
		outerMostContourObjList = list()

		# loop through each contour object
		for contourObj in contourObjList:

			# this is outer most contour object
			if self.isOuterMostContour( contourObj=contourObj, otherContourObjList=contourObjList, epsilonPercent=epsilonPercent ):

				# calculate center point of contour
				contourObj.calculateCenterPoint()

				# calculate coordinate frame of contour
				contourObj.calculateCoordinateFrame()

				# store it
				outerMostContourObjList.append( contourObj )
		
		return outerMostContourObjList
			
class Contour:
	''' - store information about contour of interest
	'''

	def __init__( self, contour ):

		# all pixel coordinate of this contour
		self.contour = contour

		# store the latest epsilon percent value used 
		self.latestEpsilonPercent = None

		# store percent of epsilon to approximated point list of contour
		self.epsilonPercentToApproximatedPointListDict = dict()

		# contour type
		# contour must be one of the following type
		# - square
		# - circle
		# - triangle
		self.shapeTypeStr = None

		# center point of contour
		self.centerPointTuple = tuple()

		# end point of x axis with respect to center point 
		self.xAxisEndPointTuple = tuple()

		# end point of y axis with respect to center point 
		self.yAxisEndPointTuple = tuple()

		# length of vector ( in pixel ) to draw contour's coordinate frame
		self.vectorLengthInt = 50

	@property
	def area( self ):
		''' - find area of contour

			RETURN: 	
				- areaOfContour ( float )
		'''

		# calculate contour area``
		return cv2.contourArea( self.contour )
	
	def approximatePolygonOfContour( self, epsilonPercent ):
		''' - approximate polygon of contour to be a rougher shape

			- mainly used for shape analysis

			- usually set epsilon parameter to 1 - 5 % of contour's perimeter

			- first this function is going to find if the approximated point exist for selected percent of epsilon
				- if exist --> return value from storage
				- else --> calculate, store and return
		'''

		# store the latest epsilon percent used 
		self.latestEpsilonPercent = epsilonPercent

		# approximated point exist for selected epsilon value
		if epsilonPercent in self.epsilonPercentToApproximatedPointListDict:
			
			# just return the calculated approximated point list
			return self.epsilonPercentToApproximatedPointListDict[ epsilonPercent ]

		# the approximated point list dose NOT exist for selected percent of epsilon, then
		# calculate contour perimeter
		contourPerimeter = cv2.arcLength( self.contour, True )

		# approximate curve of contour
		approximatedPointList = cv2.approxPolyDP( self.contour,  epsilonPercent / 100 * contourPerimeter, True )
		
		# store percent of epsilon to approximated point list
		self.epsilonPercentToApproximatedPointListDict[ epsilonPercent ] = approximatedPointList 
		
		return approximatedPointList
	
	def calculateCenterPoint( self ):
		''' - calculate center point of contour using opencv's moment
		'''

		# calculate moment 
		moment = cv2.moments( self.contour )

		# calculate x-axis of center point
		xComponent = int( moment[ "m10" ] / moment[ "m00" ] )

		# calculate y-axis of center point
		yComponent = int( moment[ "m01" ] / moment[ "m00" ] )

		self.centerPointTuple = ( xComponent, yComponent )

	def calculateCoordinateFrame( self ):
		''' - calculate coordinate frame of contour with respect to OpenCV's world coordinate
		'''

		# this contour is circle contour, then
		if self.shapeTypeStr == 'circle':

			print( f'\n\n\n\n self.centerPointTuple[ 0 ] { self.centerPointTuple[ 0 ] }, self.centerPointTuple[ 1 ] { self.centerPointTuple[ 1 ] }, self.vectorLengthInt { self.vectorLengthInt } ' )

			# x-axis component is the same direction with camera's x-axis
			self.xAxisEndPointTuple = ( self.centerPointTuple[ 0 ] + self.vectorLengthInt, self.centerPointTuple[ 1 ] )

			# y-axis component is the same direction with camera's y-axis
			self.yAxisEndPointTuple = ( self.centerPointTuple[ 0 ], self.centerPointTuple[ 1 ] + self.vectorLengthInt )

			print( f'\n\n\n\n [calculateCoordinateFrame] self.xAxisEndPointTuple { self.xAxisEndPointTuple }, self.yAxisEndPointTuple { self.yAxisEndPointTuple }' )

			return

		# this contour is triangle or square contour, then
		# approximate polygon of contour
		approximatedPolygon = self.approximatePolygonOfContour( self.latestEpsilonPercent )

		# approximate polygon of contour in 1D tuple format for each point
		approximatedPolygon1DList = list()

		# loop through each point in approximated polygon
		for point in approximatedPolygon:

			# convert point into 1D tuple
			pointTuple = ( int( point[ 0 ][ 0 ] ), int( point[ 0 ][ 1 ] ) )

			# store it
			approximatedPolygon1DList.append( pointTuple )

		# find two nearest points from OpenCV's world coordinate frame
		# init vector's magnitude storage
		vectorEndPointToVectorMagnitudeDict = dict()

		# loop through each point in approximated polygon
		for point in  approximatedPolygon1DList:

			# calculate vector magnitude and store it
			vectorEndPointToVectorMagnitudeDict[ point ] = calculateVectorMagnitude( ( 0, 0 ), point )

		# sort each point based of its vector's lenght
		sortedVectorEndPointToVectorMagnitudeDict = dict( sorted( vectorEndPointToVectorMagnitudeDict.items(), key=lambda x: x[ 1 ] ) )

		# get the most nearest point from OpenCV's world coordinate frame
		theNearestPointFromWorldCoordinateTuple = list( sortedVectorEndPointToVectorMagnitudeDict.keys() )[ 0 ]

		# get the secord nearest point from OpenCV's world coordinate frame
		theSecordNearestPointFromWorldCoordinateTuple = list( sortedVectorEndPointToVectorMagnitudeDict.keys() )[ 1 ]

		# find start point and end point of vector which is the same direction as contour's x-axis frame
		# in this case, end point is the point with largest x component
		if theNearestPointFromWorldCoordinateTuple[ 1 ] > theSecordNearestPointFromWorldCoordinateTuple[ 1 ]:
			vectorWithTheSameDirectionAsYAxisTuple = ( theNearestPointFromWorldCoordinateTuple, theSecordNearestPointFromWorldCoordinateTuple )
		vectorWithTheSameDirectionAsYAxisTuple = ( theSecordNearestPointFromWorldCoordinateTuple, theNearestPointFromWorldCoordinateTuple )
	
		# calculate directional vector
		directionalVectorXAxisComponentInt = vectorWithTheSameDirectionAsYAxisTuple[ 1 ][ 0 ] - vectorWithTheSameDirectionAsYAxisTuple[ 0 ][ 0 ]
		directionalVectorYAxisComponentInt = vectorWithTheSameDirectionAsYAxisTuple[ 1 ][ 1 ] - vectorWithTheSameDirectionAsYAxisTuple[ 0 ][ 1 ]
		directionalVectorTuple = ( directionalVectorXAxisComponentInt, directionalVectorYAxisComponentInt )

		# calculate directional vector magnitude
		directionalVectorMagnitude = calculateVectorMagnitude( ( 0, 0 ), directionalVectorTuple )
		
		# normalize vector to obtain a unit vector
		normalizedDirectionalVectorXAxisComponentFloat = directionalVectorXAxisComponentInt / directionalVectorMagnitude
		normalizedDirectionalVectorYAxisComponentFloat = directionalVectorYAxisComponentInt / directionalVectorMagnitude

		# include size to the directional vector 
		normalizedDirectionalVectorWithSpecificSizeTuple = ( self.vectorLengthInt * normalizedDirectionalVectorXAxisComponentFloat,
															self.vectorLengthInt * normalizedDirectionalVectorYAxisComponentFloat )
		
		# find end point of contour's coordinate frame x-axis vector
		self.xAxisEndPointTuple = ( self.centerPointTuple[ 0 ] + normalizedDirectionalVectorWithSpecificSizeTuple[ 0 ], 
			     					self.centerPointTuple[ 1 ] + + normalizedDirectionalVectorWithSpecificSizeTuple[ 0 ])