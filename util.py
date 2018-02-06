import os
from numpy import empty
from cv2 import (
	imread,
	cvtColor,
	COLOR_RGB2GRAY
)
from mimetypes import guess_type

key_up = 2490368
key_right = 2555904
key_down = 2621440
key_left = 2424832
key_enter = 13
key_esc = 27
key_a = 97
key_d = 100
key_w = 119

class Bbox(object):
	#(x, y), (x+w, y+h)
	"""
	First Row: number of images => deleted
	Second Row: entry names 	=> deleted

	Rest of the Rows: <image_id> <bbox_locations>

	<bbox_locations> => x1 y1 width height	
	"""
	def __init__(self, coords):
		#coords = list
		self.name = coords[0]
		self.x_1 = int(coords[1])
		self.y_1 = int(coords[2])
		self.x_2 = self.x_1 + int(coords[3])
		self.y_2 = self.y_1 + int(coords[4])

	@property
	def pt1(self):
		return (self.x_1, self.y_1)

	@property
	def pt2(self):
		return (self.x_2, self.y_2)


def get_bboxes(file_dir):
	bboxes = []
	file = open(file_dir, "r")
	data = file.readlines()
	file.close()
	
	del data[:2]
	
	coords = map(lambda x: x.split(), data)
	
	for item in coords:
		bboxes.append(Bbox(item))
	
	return bboxes



def img_list(folder_dir):
	"""
	Given a folder_dir return a list with the true path
	"""
	true_list_path = []
	for path in os.listdir(folder_dir):
		aux_path = os.path.join(folder_dir, path)
		try:
			if os.path.isfile(aux_path) and "image" in guess_type(aux_path)[0]:
				true_list_path.append(aux_path)
		except TypeError as tp:
			pass
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
