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