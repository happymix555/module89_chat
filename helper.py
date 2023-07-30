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

def calculateVectorMagnitude( vectorStartPointTuple, vectorEndPointTuple ):
	''' - calculate the magnitude of the given vector

		ARGS: 
			- vectorStartPointTuple ( Tuple )
			- vectorEndPointTuple ( Tuple )

		RETURN: 
			- vectorMagnitudeFloat ( Float )
	'''

	assert len( vectorStartPointTuple ) == len( vectorEndPointTuple ), ' Start and End point of vector must be the same size but got \
		 start point {}, size {} end point {}, size {} '.format( vectorStartPointTuple, len( vectorStartPointTuple ), vectorEndPointTuple, len( vectorEndPointTuple ) )
	
	# init vector magnitude
	vectorMagnitudeFloat = float()

	# loop through each position in vector's start point
	for pointCompomentPosition in range( len( vectorStartPointTuple ) ):

		# add up value for vector's magnitude 
		vectorMagnitudeFloat += ( vectorEndPointTuple[ pointCompomentPosition ] - vectorStartPointTuple[ pointCompomentPosition ] ) ** 2

	# calculate the vector's magnitude
	return math.sqrt( vectorMagnitudeFloat )

def findParallelPointWithMagnitude( point1, point2, point3, magnitude ):
    
    # Calculate the direction vector from point1 to point2
    directionVector = ( point2[ 0 ] - point1[ 0 ], point2[ 1 ] - point1[ 1 ] )

    # Calculate the magnitude of the direction vector
    directionMagnitude = ( directionVector[ 0 ] ** 2 + directionVector[ 1 ] ** 2) ** 0.5

    # Calculate the scaling factor to achieve the desired magnitude
    scalingFactor = magnitude / directionMagnitude

    # Find the end point point4
    point4 = ( int( point3[ 0 ] + directionVector[ 0 ] * scalingFactor ),
              int( point3[ 1 ] + directionVector[ 1 ] * scalingFactor ) )

    return point4

def findPerpendicularPoint( point1, point2, point3, point4, magnitude ):
   
    # Calculate the direction vector from point1 to point2 (v1)
    v1X = point2[ 0 ] - point1[ 0 ]
    v1Y = point2[ 1 ] - point1[ 1 ]

    # Calculate the direction vector from point3 to point4 (v2)
    v2X = point4[ 0 ] - point3[ 0 ]
    v2Y = point4[ 1 ] - point3[ 1 ]

    # Calculate the perpendicular vector (v3)
    v3X = -v2Y
    v3Y = v2X

    # Scale v3 to the desired magnitude
    scalingFactor = magnitude / ( ( v3X ** 2 + v3Y ** 2 ) ** 0.5 )
    v3X *= scalingFactor
    v3Y *= scalingFactor

    # Find point5 using v3 and point3
    point5 = ( int( point3[ 0 ] + v3X ), int( point3[ 1 ] + v3Y ) )

    return point5