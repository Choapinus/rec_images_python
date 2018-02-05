"""
TODO: 	- representar la data y dibujar los rectangulos antes # done
		- guardar x, y del cuadrado que hiciste en algun archivo de texto (json) # done
		- dibujar mas de un rectangulo para una imagen # necesario?
idea: if waitkey == somekey, x: x rectangulos a dibujar con un for i in range(x)

parametrizar carga de bboxes
crear archivo de instrucciones
no depender de la base de datos celebA

hacer los clicks para tener las coordenadas, no arrastrar
"""


import sys

sys.path.insert(0, '../') #dir of the module util

import cv2
import json
import util
import numpy as np

js = json.load(open("db.json"))

#bbox = util.get_bboxes(js["bbox_dir"].encode())
base = js["base"]
cont = js["last_cont"] # save this, indica el contador de imagenes en donde quedaste
min_images = js["min_images"]
max_images = js["max_images"]

print "loading..."
cropped_js = json.load(open(js["cropped_js"].encode()))
images_path = util.img_list(js["db_dir"].encode())
images = util.get_images(images_path[min_images:max_images])
#bbox_portion = bbox[min_images:max_images]
print "done!"

cv2.namedWindow("cropper")
#cv2.namedWindow("original")

#bbox_im = bbox_portion[cont]
actual_im = images[cont].copy()
#clone_im = images[cont].copy()
#cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)

list_names = map(lambda x: x["name"], cropped_js)
actual_img_name = images_path[cont+min_images].split('/')[-1]

if actual_img_name in list_names:
	cv2.putText(actual_im,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))


cv2.setMouseCallback("cropper", util.click_and_crop)
cv2.imshow("cropper", actual_im)
#cv2.imshow("original", clone_im)




while True:
	print "imagen:", images_path[cont+min_images]

	key = cv2.waitKey(0)
	
	#if key == util.key_right:
	if key == util.key_d:
		cont += 1
		if cont == len(images):
			cont = 0 # ni se te ocurra poner = min_images porque explota, recuerda que sobreescribes la lista
		try:
			actual_im = images[cont].copy()
			#clone_im = images[cont].copy()
			#bbox_im = bbox_portion[cont]
			#cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			list_names = map(lambda x: x["name"], cropped_js)
			actual_img_name = images_path[cont+min_images].split('/')[-1]
			
			if actual_img_name in list_names:
				cv2.putText(actual_im,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))

			cv2.imshow("cropper", actual_im)
			#cv2.imshow("original", clone_im)

		except Exception:
			print "error: no image found at index", str(cont)
			print images[cont]
			#print bbox_portion[cont]

		#util.refPt = []
	
	#elif key == util.key_left:
	elif key == util.key_a:
		cont -= 1
		if cont == -1:
			cont = len(images)-1
		try:
			actual_im = images[cont].copy()
			#clone_im = images[cont].copy()
			#bbox_im = bbox_portion[cont]
			#cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			list_names = map(lambda x: x["name"], cropped_js)
			actual_img_name = images_path[cont+min_images].split('/')[-1]
			
			if actual_img_name in list_names:
				cv2.putText(actual_im,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))

			cv2.imshow("cropper", actual_im)
			#cv2.imshow("original", clone_im)

		except Exception:
			print "error: no image found at index", str(cont)
			print images[cont]
			#print bbox_portion[cont]

		#util.refPt = []
	
	elif key == ord("r"):
		# resetear a valores originales
		try:
			util.refPt = []
			actual_im = images[cont].copy()
			#clone_im = images[cont].copy()
			#bbox_im = bbox_portion[cont]
			#cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			list_names = map(lambda x: x["name"], cropped_js)
			actual_img_name = images_path[cont+min_images].split('/')[-1]
			
			if actual_img_name in list_names:
				cv2.putText(actual_im,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))

			cv2.imshow("cropper", actual_im)
			#cv2.imshow("original", clone_im)

		except Exception:
			print "error: no image found at index", str(cont)

		print "reset"
	
	elif key == ord("s"): # show changes
		try:
			#clone_im = images[cont].copy()
			#bbox_im = bbox_portion[cont]
			#cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			#cv2.imshow("original", clone_im)
			
			clone = images[cont].copy()
			cv2.rectangle(clone, util.refPt[0], util.refPt[1], (0, 255, 0), 1)

			list_names = map(lambda x: x["name"], cropped_js)
			actual_img_name = images_path[cont+min_images].split('/')[-1]
			
			if actual_img_name in list_names:
				cv2.putText(clone,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))

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
		#bbox_portion = bbox[min_images:max_images]

		try:
			actual_im = images[cont].copy()
			#clone_im = images[cont].copy()
			#bbox_im = bbox_portion[cont]
			#cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			list_names = map(lambda x: x["name"], cropped_js)
			actual_img_name = images_path[cont+min_images].split('/')[-1]
			
			if actual_img_name in list_names:
				cv2.putText(actual_im,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))

			cv2.imshow("cropper", actual_im)
			#cv2.imshow("original", clone_im)

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
		#bbox_portion = bbox[min_images:max_images]

		try:
			actual_im = images[cont].copy()
			#clone_im = images[cont].copy()
			#bbox_im = bbox_portion[cont]
			#cv2.rectangle(clone_im, bbox_im.pt1, bbox_im.pt2, (0, 255, 0), 1)
			list_names = map(lambda x: x["name"], cropped_js)
			actual_img_name = images_path[cont+min_images].split('/')[-1]
			
			if actual_img_name in list_names:
				cv2.putText(actual_im,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))

			cv2.imshow("cropper", actual_im)
			#cv2.imshow("original", clone_im)

		except Exception as e:
			print "Failed to load more. Exception: ", e

		print "done"

	#elif key == util.key_enter:
	elif key == util.key_w:
		# guardar nombre x1 y1 x2 y2
		try:
			x1, y1 = util.refPt[0]
			x2, y2 = util.refPt[1]
			
			crop = images[cont][y1:y2, x1:x2]
			
			cv2.imshow("aux", images[cont][y1:y2, x1:x2])
			aux_key = cv2.waitKey(0)
			im_dir = images_path[cont+min_images]
			im_name = im_dir.split(js["db_dir"].encode())[-1].split('.')[0]
			im_extension = ".png"
			save_dir = js["cropped_dir"].encode()+im_name+"_cropped"+im_extension
			
			# if aux_key == util.key_enter:
			if aux_key == util.key_w:
				# cv2.imwrite(save_dir, crop)
				
				list_names = map(lambda x: x["name"], cropped_js)

				if im_name+im_extension not in list_names:
					cropped_js.append({"name": im_name+im_extension, "x1": x1, "x2": x2, "y1": y1, "y2": y2})
				else:
					print "existing image. Do you want to overwrite it? (w/esc): "
					
					if cv2.waitKey(0) == ord("w"):
						ind = list_names.index(im_name+im_extension)
						cropped_js[ind] = {"name": im_name+im_extension, "x1": x1, "x2": x2, "y1": y1, "y2": y2}
				
				json.dump(cropped_js, open(js["cropped_js"].encode(), "w"))
				cv2.destroyWindow("aux")
				print "coords of the image " + im_dir + " saved"
				cv2.putText(actual_im,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))
				cv2.imshow("cropper", actual_im)
			
			else:
				cv2.destroyWindow("aux")
				actual_im = images[cont].copy()
				list_names = map(lambda x: x["name"], cropped_js)
				actual_img_name = images_path[cont+min_images].split('/')[-1]
				
				if actual_img_name in list_names:
					cv2.putText(actual_im,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))

				cv2.imshow("cropper", actual_im)

		except Exception as ex:
			print "Failed to crop and save. Exception: ", ex

	if key == ord("q"): # delete saved coords from json
		try:
			
			im_dir = images_path[cont+min_images]
			im_name = im_dir.split(js["db_dir"].encode())[-1].split('.')[0]
			im_extension = ".png"
			list_names = map(lambda x: x["name"], cropped_js)
			
			print "Do you want to erase the coords of", im_name+im_extension+" ?. Press again Q"

			if cv2.waitKey(0) == ord("q"):
				if im_name+im_extension in list_names:
					index = list_names.index(im_name+im_extension)
					del cropped_js[index]
					del list_names[index]
					print "coords of the image " + im_dir + " deleted"
					cv2.imshow("cropper", images[cont].copy())

				else:
					print "There is no", im_name+im_extension+" coords"
	
			actual_im = images[cont].copy()
			json.dump(cropped_js, open(js["cropped_js"].encode(), "w"))
			actual_img_name = images_path[cont+min_images].split('/')[-1]
			
			if actual_img_name in list_names:
				cv2.putText(actual_im,"saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))

			cv2.imshow("cropper", actual_im)

		except Exception as ex:
			print "Something gone wrong!. Exception:", ex
	
	if key == ord("e"):
		try:
			
			im_dir = images_path[cont+min_images]
			im_name = im_dir.split(js["db_dir"].encode())[-1].split('.')[0]
			im_extension = ".png"
			list_names = map(lambda x: x["name"], cropped_js)
			clone = images[cont].copy()

			if im_name+im_extension in list_names:
				index = list_names.index(im_name+im_extension)
				img_obj = cropped_js[index]
				cv2.putText(clone, "saved", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (47, 0, 232))
				cv2.rectangle(clone, (img_obj["x1"], img_obj["y1"]), (img_obj["x2"], img_obj["y2"]), (0, 255, 0), 1)
			else:
				print "There are no coords for this image"
			
			cv2.imshow("cropper", clone)

		except Exception as ex:
			print "Something gone wrong!. Exception:", ex
	
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

if the image coords exists, it will be written "saved" on the top

a - d keys => move through images list. The drawn square persist
mouse rectangle => you can draw a square by holding the click button and releasing it in another place of the window, 
				   then press 's' key to show the drawn square
s key => show drawn square
r key => reset drawn square
q key => delete the coords of the actual image if them exists
m key => load more images (base specified)
u key => load previous images (base specified)
o key => save original crop
	  => if the image exists, check the console to confirm the overwrite
w key => crop and save the image
	  => in the new window, w save the image, another key goes out
	  => if the image exists, check the console to confirm the overwrite
	  	 => if you want to overwrite, in the new window press w
	  	 	else, press another key
e key => if the image coords are saved/exists, pressing the 'e' key will show the actual crop
esc key => quit without save

remember json:
	- cropped_dir: where cropped images are going to be saved
	- db_dir: dir of the images
	- img_crops.json must be an array



preguntas:
- que pasa si en el clasificador de arandanos aparece una pelota morada?
- todas las capturas de arandanos poseen rayas por detras. Estas intervendran en el reconocimiento?

"""