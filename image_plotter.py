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

class Image:
	''' - store information about image
	'''

	def __init__( self, image, imageNameStr ):
		self.image = image
		self.rgbImage = cv2.cvtColor( self.image, cv2.COLOR_BGR2RGB )
		self.imageNameStr = imageNameStr

class ImagePlotter:
	''' - used to dynamically create image plot using matplotlib
	'''

	def __init__( self, widthPerImageInch, heightPerImageInInch, numberOfColumn ):
		
		# matplotlib pyplot
		self.plt  = plt

		# image width
		self.widthPerImageInch = widthPerImageInch

		# overall width of figure
		self.overallImageWidthInInch = self.widthPerImageInch * numberOfColumn

		# image height
		self.heightPerImageInInch = heightPerImageInInch

		# all image to plot in this figure
		self.imageObjStorageList = []

		# set number of column in figure
		self.numberOfColumn = numberOfColumn

		# number of row 
		self.numberOfRow = None

		# number of image 
		self.numberOfImage = None

		# figure 
		self.figure = None

	def addImageToPlot( self, image, imageNameStr ):
		''' - add image to be plotted
		'''

		# create image object
		imageObj = Image( image, imageNameStr )

		# store image object
		self.imageObjStorageList.append( imageObj )

	def plotAndShowAllImage( self ):
		''' - construct all image in figure and show them 
		'''

		# get number of image in figure
		self.numberOfImage = len( self.imageObjStorageList )

		# calculate number of row
		self.numberOfRow = math.ceil( self.numberOfImage / self.numberOfColumn )

		# calculate overall plot height in inches
		self.overallImageHeightInInch = self.numberOfRow * self.heightPerImageInInch

		# create figure
		self.figure = self.plt.figure( figsize = ( self.overallImageWidthInInch, self.overallImageHeightInInch ) )

		# loop through image object 
		for imagePosition, imageObj in enumerate( self.imageObjStorageList ):

			# set position of image
			self.figure.add_subplot( self.numberOfRow, self.numberOfColumn, imagePosition + 1 )

			# add image to figure
			self.plt.imshow( imageObj.rgbImage )

			# not show the axis
			self.plt.axis( 'off' )

			# set image title
			self.plt.title( imageObj.imageNameStr )
		
		# show figure
		plt.show()