"""
TODO: 	- representar la data y dibujar los rectangulos antes # which data?
		- dibujar mas de un rectangulo para una imagen # in progress
		- guardar x, y del cuadrado que hiciste?, wat
idea: if waitkey == somekey, x: x rectangulos a dibujar con un for i in range(x)
"""


import sys

sys.path.insert(0, '../') #dir of the module

import cv2
import json
import util
import numpy as np

js = json.load(open("db.json"))

base = js["base"]
min_images = js["min_images"]
max_images = js["max_images"]

print "loading..."
#images_path = util.img_list(js["db_dir"].encode())
images_path = util.img_list(js["db_dir"].encode())
images = util.get_images(images_path[min_images:max_images])
print "done!"

cont = js["last_cont"] # save this, indica el contador de imagenes en donde quedaste
cv2.namedWindow("name")
cv2.setMouseCallback("name", util.click_and_crop)
cv2.imshow("name", images[cont])


while True:
	print "imagen:", images_path[cont+min_images]

	key = cv2.waitKey(0)
	
	if key == util.key_right:
		cont += 1
		if cont == len(images):
			cont = 0 # ni se te ocurra poner = min_images porque explota, recuerda que sobreescribes la lista
		try:
			cv2.imshow("name", images[cont])
		except Exception:
			print "error: no image found at index", str(cont)
			print images[cont]
		util.refPt = []
	
	elif key == util.key_left:
		cont -= 1
		if cont == -1:
			cont = len(images)-1
		try:
			cv2.imshow("name", images[cont])
		except Exception:
			print "error: no image found at index", str(cont)
		util.refPt = []
	
	elif key == ord("r"):
		# resetear a valores originales
		try:
			cv2.imshow("name", images[cont])
		except Exception:
			print "error: no image found at index", str(cont)
		print "reset"
	
	elif key == ord("s"): # show changes
		try:
			clone = images[cont].copy()
			cv2.rectangle(clone, util.refPt[0], util.refPt[1], (0, 255, 0), 1)
			cv2.imshow("name", clone)
		except Exception as e:
			print "no coords given. refPt:", util.refPt 

	elif key == ord("m"): # load more
		min_images += base
		max_images += base

		if max_images >= len(images):
			max_images = len(images)-1
		if min_images >= len(images):
			min_images = len(images)-base
		
		print "loading..."
		images = util.get_images(images_path[min_images:max_images])
		cv2.imshow("name", images[cont])
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
		cv2.imshow("name", images[cont])
		print "done"

	elif key == util.key_enter: # enter
		# guardar imagen recortada
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
				cv2.imwrite(save_dir, crop)
				cv2.destroyWindow("aux")
			else:
				cv2.destroyWindow("aux")
				cv2.imshow("name", images[cont])

		except Exception:
			print "failed to crop and save"
		
		

	elif key == util.key_esc: # escape
		js["last_cont"] = cont
		js["min_images"] = min_images
		js["max_images"] = max_images
		json.dump(js, open("db.json", "w"))
		cv2.destroyAllWindows()
		print "\nbye"
		break

"""
instructions:
left-right arrow => move trhough images list
mouse rectangle => se puede dibujar un cuadrado manteniendo presionado el click y soltandolo en otro lugar, luego presionar S
r key => reset drew squares
s key => show drew square
m key => load more images (base specified)
enter key => crop and save the image
		  => in the new window, enter save the image, another key goes out
esc key => quit without save


"""