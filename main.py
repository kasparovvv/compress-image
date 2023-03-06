from PIL import Image
import os

TARGET_PATH = "/home/gasparov/DEV/python/compress_images/images_test"

def get_filepath(path):
    return os.path.join(os.getcwd(), path)

def compress(root,path,filename):
    
    filepath = get_filepath(path)
   
    image = Image.open(filepath)

    image.save(root+"/"+filename+"compressed.jpeg", "JPEG", optimize = True, quality = 10)

    os.remove(filepath)

    return



for (root, dirs, file) in os.walk(TARGET_PATH):
    for f in file:
        if '.jpg' in f:
            #print(root,dirs,f)
            path = root + '/' + f
            compress(root,path,f)



