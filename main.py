import logging
from PIL import Image
import os
import shutil
import time
import pathlib


def file_operations(TARGET_PATH,SRC_DIR):
    
    if os.path.exists(TARGET_PATH):
            shutil.rmtree(TARGET_PATH)
            print("Dosya zaten var olduğu için siliniyor..")

    time.sleep(1)
    shutil.copytree(SRC_DIR, TARGET_PATH)
    print("Dosyalar test klasörüne kopyalandı")


def get_file_extension(filename):
    path =  pathlib.Path(filename).suffix
    return path.replace('.', '')


def get_filepath(path):
    return os.path.join(os.getcwd(), path)


def compress(root,path,filename):

    filepath = get_filepath(path)
   
    image = Image.open(filepath)

    #extension = get_file_extension(filename); 

    try:
        image.save(root+"/"+filename+"_compressed.jpeg", "JPEG", optimize = True, quality = 30)
        print(path + " =>  işlendi")
        os.remove(filepath)
    except:
        print("Hata")
        #hatalı image error folder'ına atılacak
        logging.error(path)

    return

def create_file_name():
    return  "errors_"+str(time.strftime("%Y%m%d-%H%M%S"))


def crete_error_files():

    logging.basicConfig(filename="compress-image/errors.log", level=logging.ERROR) # log file için belki silinecek
    mode = 0o666
    error_path = os.path.join("compress-image",  create_file_name())
    os.mkdir(error_path, mode)  


def main():

    crete_error_files()
    file_operations(TARGET_PATH,SRC_DIR)

    print("İşlem başlatılıyor...")

    time.sleep(1)

    st = time.time()
    
    count = 0
    for (root, dirs, file) in os.walk(TARGET_PATH):
        for f in file:
            if ('.jpg' in f) or ('.png' in f) or ('.jpeg' in f) :
                #print(root,dirs,f)
                path = root + '/' + f
                compress(root,path,f)
                count+=1

    
    elapsed_time = time.time() - st
    print("---------------------------------------------------")
    print(str(count) + ' adet dosya  ', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), ' sürede işlendi.')







if __name__ == "__main__":
    
    TARGET_PATH = "compress-image\images_clone"
    SRC_DIR = "compress-image\original_images"

    main()

