"""
TODO: 	- representar la data y dibujar los rectangulos antes # done
		- dibujar mas de un rectangulo para una imagen # in progress?
		- guardar x, y del cuadrado que hiciste # done
idea: if waitkey == somekey, x: x rectangulos a dibujar con un for i in range(x)
"""


import sys

sys.path.insert(0, '../') #dir of the module util

import cv2
import json
import util
import numpy as np

js = json.load(open("db.json"))

bbox = util.get_bboxes(js["bbox_dir"].encode())
base = js["base"]
cont = js["last_cont"] # save this, indica el contador de imagenes en donde quedaste
min_images = js["min_images"]
max_images = js["max_images"]

print "loading..."
cropped_js = json.load(open(js["cropped_js"].encode()))
images_path = util.img_list(js["db_dir"].encode())
images = util.get_images(images_path[min_images:max_images])
bbox_portion = bbox[min_images:max_images]
print "done!"

cv2.namedWindow("cropper")
cv2.namedWindow("original")

bbox_im = bbox_portion[cont]
actual_im = images[cont]
clone_im = images[cont].copy()
cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)

cv2.setMouseCallback("cropper", util.click_and_crop)
cv2.imshow("cropper", actual_im)
cv2.imshow("original", clone_im)


while True:
	print "imagen:", images_path[cont+min_images]

	key = cv2.waitKey(0)
	
	if key == util.key_right:
		cont += 1
		if cont == len(images):
			cont = 0 # ni se te ocurra poner = min_images porque explota, recuerda que sobreescribes la lista
		try:
			actual_im = images[cont]
			clone_im = images[cont].copy()
			bbox_im = bbox_portion[cont]
			cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			cv2.imshow("cropper", actual_im)
			cv2.imshow("original", clone_im)

		except Exception:
			print "error: no image found at index", str(cont)
			print images[cont]
			print bbox_portion[cont]

		util.refPt = []
	
	elif key == util.key_left:
		cont -= 1
		if cont == -1:
			cont = len(images)-1
		try:
			actual_im = images[cont]
			clone_im = images[cont].copy()
			bbox_im = bbox_portion[cont]
			cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			cv2.imshow("cropper", actual_im)
			cv2.imshow("original", clone_im)

		except Exception:
			print "error: no image found at index", str(cont)
			print images[cont]
			print bbox_portion[cont]

		util.refPt = []
	
	elif key == ord("r"):
		# resetear a valores originales
		try:
			actual_im = images[cont]
			clone_im = images[cont].copy()
			bbox_im = bbox_portion[cont]
			cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			cv2.imshow("cropper", actual_im)
			cv2.imshow("original", clone_im)

		except Exception:
			print "error: no image found at index", str(cont)

		print "reset"
	
	elif key == ord("s"): # show changes
		try:
			clone_im = images[cont].copy()
			bbox_im = bbox_portion[cont]
			cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			cv2.imshow("original", clone_im)
			
			clone = images[cont].copy()
			cv2.rectangle(clone, util.refPt[0], util.refPt[1], (0, 255, 0), 1)
			cv2.imshow("cropper", clone)

		except Exception as e:
			print "no coords given. refPt:", util.refPt 

	elif key == ord("m"): # load more
		min_images += base
		max_images += base

		if max_images >= len(images_path):
			max_images = len(images_path)-1
		if min_images >= len(images_path):
			min_images = len(images_path)-base

		print "max", max_images
		print "min", min_images
		
		print "loading..."

		images = util.get_images(images_path[min_images:max_images])
		bbox_portion = bbox[min_images:max_images]

		try:
			actual_im = images[cont]
			clone_im = images[cont].copy()
			bbox_im = bbox_portion[cont]
			cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			cv2.imshow("cropper", actual_im)
			cv2.imshow("original", clone_im)

		except Exception as e:
			print "Failed to load more. Exception: ", e

		print "done"

	elif key == ord("u"): # unload
		min_images -= base
		max_images -= base

		if min_images < 0:
			min_images = 0
		if max_images <= 0:
			max_images = base

		print "max", max_images
		print "min", min_images
		
		print "loading..."

		images = util.get_images(images_path[min_images:max_images])
		bbox_portion = bbox[min_images:max_images]

		try:
			actual_im = images[cont]
			clone_im = images[cont].copy()
			bbox_im = bbox_portion[cont]
			cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			cv2.imshow("cropper", actual_im)
			cv2.imshow("original", clone_im)

		except Exception as e:
			print "Failed to load more. Exception: ", e

		print "done"

	elif key == util.key_enter: # enter
		# guardar nombre x1 y1 x2 y2
		try:
			x1, y1 = util.refPt[0]
			x2, y2 = util.refPt[1]
			
			crop = images[cont][y1:y2, x1:x2]
			
			cv2.imshow("aux", images[cont][y1:y2, x1:x2])
			aux_key = cv2.waitKey(0)
			im_dir = images_path[cont+min_images]
			im_name = im_dir.split(js["db_dir"].encode())[-1][1:-4]
			im_extension = ".png"
			save_dir = js["cropped_dir"].encode()+im_name+"_cropped"+im_extension
			
			if aux_key == util.key_enter:
				print "coords of the image " + im_dir + " saved"
				# cv2.imwrite(save_dir, crop)
				
				list_names = map(lambda x: x["name"], cropped_js)

				if im_name+im_extension not in list_names:
					cropped_js.append({"name": im_name+im_extension, "x1": x1, "x2": x2, "y1": y1, "y2": y2})
				else:
					option = raw_input("existing image. Do you want to overwrite it? (y/n): ")
					if option.lower() == 'y':
						ind = list_names.index(im_name+im_extension)
						cropped_js[ind] = {"name": im_name+im_extension, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
				
				json.dump(cropped_js, open(js["cropped_js"].encode(), "w"))
				cv2.destroyWindow("aux")
			else:
				cv2.destroyWindow("aux")
				cv2.imshow("cropper", images[cont])

		except Exception as ex:
			print "Failed to crop and save. Exception: ", ex
	
	elif key == ord("o"): #save the original crop
		try:
			bbox_im = bbox_portion[cont]
			x1, y1 = bbox_im.pt1
			x2, y2 = bbox_im.pt2

			crop = images[cont][y1:y2, x1:x2]

			cv2.imshow("aux", images[cont][y1:y2, x1:x2])
			aux_key = cv2.waitKey(0)
			im_dir = images_path[cont+min_images]
			im_name = im_dir.split(js["db_dir"].encode())[-1][1:-4]
			im_extension = ".png"
			save_dir = js["cropped_dir"].encode()+im_name+"_cropped"+im_extension
			
			if aux_key == util.key_enter:
				print "original coords of the crop saved. image " + save_dir
				# cv2.imwrite(save_dir, crop)
				
				list_names = map(lambda x: x["name"], cropped_js)

				if im_name+im_extension not in list_names:
					cropped_js.append({"name": im_name+im_extension, "x1": x1, "x2": x2, "y1": y1, "y2": y2})
				else:
					option = raw_input("existing image. Do you want to overwrite it? (y/n): ")
					if option.lower() == 'y':
						ind = list_names.index(im_name+im_extension)
						cropped_js[ind] = {"name": im_name+im_extension, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
				
				json.dump(cropped_js, open(js["cropped_js"].encode(), "w"))
				cv2.destroyWindow("aux")
			else:
				cv2.destroyWindow("aux")
				cv2.imshow("cropper", images[cont])

		except Exception as ex:
			print "Failed to crop and save. Exception: ", ex
		
	elif key == util.key_esc: # escape
		js["last_cont"] = cont
		js["min_images"] = min_images
		js["max_images"] = max_images
		json.dump(js, open("db.json", "w"))
		#json.dump(cropped_js, open(js["cropped_js"].encode(), "w"))
		cv2.destroyAllWindows()

		print "\nbye"
		break

"""
instructions:
the "original" window is just to see the pre-crop did by someone else
the "cropper" is our possible crop

left-right arrow => move trhough images list
mouse rectangle => se puede dibujar un cuadrado manteniendo presionado el click y soltandolo en otro lugar, luego presionar S
s key => show drawn square
r key => reset drawn squares
m key => load more images (base specified)
u key => load previous images (base specified)
o key => save original crop
enter key => crop and save the image
		  => in the new window, enter save the image, another key goes out
esc key => quit without save

remember json:
	- cropped_dir: where cropped images are going to be saved
	- db_dir: dir of the images


"""