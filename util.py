import os
from numpy import empty
from cv2 import (
	imread,
	cvtColor,
	COLOR_RGB2GRAY,
	EVENT_LBUTTONDOWN,
	EVENT_LBUTTONUP
)
from mimetypes import guess_type

def img_list(folder_dir):
	"""
	Given a folder_dir return a list with the true path
	"""
	true_list_path = []
	for path in os.listdir(folder_dir):
		aux_path = os.path.join(folder_dir, path)
		if os.path.isfile(aux_path) and "image" in guess_type(aux_path)[0]:
			true_list_path.append(aux_path)
	return true_list_path

def get_images(images_dir):
	"""
	With the true path image given, return a numpy.array with the images in RGB
	"""
	np_images = empty(len(images_dir), dtype=object)
	for i in range(len(images_dir)):
		np_images[i] = imread(images_dir[i])
	return np_images

def get_one_image(image_dir):
	return imread(image_dir)

def to_bw(image):
	return cvtColor(image, COLOR_RGB2GRAY)


refPt = [] # initialize the list of reference points and boolean indicating
cropping = False # whether cropping is being performed or not

key_up = 2490368
key_right = 2555904
key_down = 2621440
key_left = 2424832
key_enter = 13
key_esc = 27
 
def click_and_crop(event, x, y, flags, param):
	
	# grab references to the global variables
	global refPt, cropping

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
 
	# check to see if the left mouse button was released
	elif event == EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		#print refPt
		cropping = False
