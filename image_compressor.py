from dataclasses import dataclass
from PIL import Image
import os,pathlib,time,shutil
import logging
from colorama import Fore, Back, Style


@dataclass
class ImageCompressor:
    target_dir: str
    src_dir: str

    def get_filepath(self,path) -> str:
        return os.path.join(os.getcwd(), path)

    
    def get_file_extension(self,filename) -> str:
        path =  pathlib.Path(filename).suffix
        return path.replace('.', '')
    
    
    def create_file_name(self) -> str:
        return  "errors_"+str(time.strftime("%Y%m%d-%H%M%S"))
    

    def crete_error_files(self):
        logging.basicConfig(filename="compress-image/errors.log", level=logging.ERROR) # log file için belki silinecek
        mode = 0o666
        error_path = os.path.join("compress-image/errors",  self.create_file_name())
        os.mkdir(error_path, mode)  
    
    
    def file_operations(self):
        if os.path.exists(self.target_dir):
                shutil.rmtree(self.target_dir)
                print("Dosya zaten var olduğu için siliniyor..")

        time.sleep(1)

        shutil.copytree(self.src_dir, self.target_dir)
        print("Dosyalar test klasörüne kopyalandı")


    def compress(self,root,path,filename):

        filepath = self.get_filepath(path)
        image = Image.open(filepath)

        #extension = get_file_extension(filename); 

        try:
            image.save(root+"/"+filename+"_compressed.jpeg", "JPEG", optimize = True, quality = 30)
            print(Fore.GREEN + path + " =>  işlendi")
            os.remove(filepath)
        except:
            print(Fore.RED+"Hata")
            #hatalı image error folder'ına atılacak
            logging.error(path)

        return
    

    def start(self):

        self.crete_error_files()
        self.file_operations()

        print("İşlem başlatılıyor...")

        time.sleep(1)

        st = time.time()
        
        count = 0
        for (root, dirs, file) in os.walk(self.target_dir):
            for f in file:
                if ('.jpg' in f) or ('.png' in f) or ('.jpeg' in f) :
                    #print(root,dirs,f)
                    path = root + '/' + f
                    self.compress(root,path,f)
                    count+=1

        
        elapsed_time = time.time() - st
        print("---------------------------------------------------")
        print(str(count) + ' adet dosya  ', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), ' sürede işlendi.')
    
     