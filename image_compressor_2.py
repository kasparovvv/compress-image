from dataclasses import dataclass
from PIL import Image
import os
import pathlib
import time
import shutil
import logging
from colorama import Fore, Back, Style


@dataclass
class ImageCompressor:
    target_dir: str
    src_dir: str
    success_count: int = 0
    error_count: int = 0
    quality: int = 30
    formats = ('.png', '.jpeg', '.jpg','.pdf')
    new_path:str = ""

    def get_filepath(self, path) -> str:
        return os.path.join(os.getcwd(), path)

    def get_file_extension(self, filename) -> str:
        return pathlib.Path(filename).suffix

    def create_file_name(self) -> str:
        return "images_"+str(time.strftime("%Y%m%d"))

    def crete_files(self) -> None:

        self.new_path = os.path.join(
            "compress-image/tries",  self.create_file_name())
        if os.path.exists( self.new_path):
            shutil.rmtree( self.new_path)
            print("Dosya zaten var olduğu için siliniyor..")
       
        mode = 0o666
        os.mkdir( self.new_path, mode)

    def file_operations(self) -> None:
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)
            print("Dosya zaten var olduğu için siliniyor..")

        time.sleep(1)

        shutil.copytree(self.src_dir, self.target_dir)
        print("Dosyalar test klasörüne kopyalandı")

    def get_file_extension(self, filename):

        extensions = [".jpeg", ".jpg", ".png", ".JPEG", ".PNG", ".JPG"]
        extension = pathlib.Path(filename).suffix

        str_match = [s for s in extensions if extension in s]
        return str_match[0]
    
    def get_folder_name_from_root(self,root):
        folder = root.split('\\')
        return folder[2]


    def compress(self, root, path, filename) -> None:

        filepath = self.get_filepath(path)
        image = Image.open(filepath)

        new_file_name = pathlib.Path(filename).stem

        extension = str(self.get_file_extension(filename))

        folder = self.get_folder_name_from_root(root)
        new_path = self.new_path+"/"+folder+"/"+new_file_name+extension
        new_path = os.path.normpath(new_path)

     
        #print(new_path)
       
        try:
            optimize = False
            if extension.__eq__("png"):
                optimize = True


            if os.path.exists(self.new_path+"/"+folder):
                image.save(new_path, optimize=optimize, quality=self.quality)
            else:
                mode = 0o666
                os.mkdir( self.new_path+"/"+folder, mode)

            
            print(Fore.GREEN + path + " =>  işlendi")

            self.success_count += 1
        except Exception as e:
            print(e)
            # hatalı image error folder'ına atılacak
            self.error_count += 1
            logging.error(path)

        return

    def start(self) -> None:

        self.crete_files()
        print("İşlem başlatılıyor...")

        time.sleep(1)

        st = time.time()

        for (root, dirs, file) in os.walk(self.target_dir):
            for f in file:
                if os.path.splitext(f)[1].lower() in self.formats:
                    path = root + '/' + f
                    self.compress(root, path, f)

        elapsed_time = time.time() - st

        print("###################################################")
        print("İşlem ", time.strftime("%H:%M:%S", time.gmtime(
            elapsed_time)), " sürede tamamlandı")
        print(str(self.success_count) + ' adet dosya  başarıyla işlendi. ')
        print(str(self.error_count) + ' adet dosya  başarısız oldu. ')
        print("###################################################")
