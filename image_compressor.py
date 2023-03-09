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
    formats = ('.png', '.jpeg', '.jpg')

    def get_filepath(self, path) -> str:
        return os.path.join(os.getcwd(), path)

    def get_file_extension(self, filename) -> str:
        return pathlib.Path(filename).suffix

    def create_file_name(self) -> str:
        return "errors_"+str(time.strftime("%Y%m%d-%H%M%S"))

    def crete_error_files(self) -> None:
        # log file için belki silinecek
        logging.basicConfig(
            filename="compress-image/errors.log", level=logging.ERROR)

        mode = 0o666
        error_path = os.path.join(
            "compress-image/errors",  self.create_file_name())
        os.mkdir(error_path, mode)

    def file_operations(self) -> None:
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)
            print("Dosya zaten var olduğu için siliniyor..")

        time.sleep(1)

        shutil.copytree(self.src_dir, self.target_dir)
        print("Dosyalar test klasörüne kopyalandı")

    def get_file_extension(self, filename) -> str:

        extensions = [".jpeg", ".jpg", ".png", ".JPEG", ".PNG", ".JPG"]
        extension = pathlib.Path(filename).suffix

        str_match = [s for s in extensions if extension in s]
        return str_match[0]

    def compress(self, root, path, filename) -> None:

        filepath = self.get_filepath(path)
        image = Image.open(filepath)

        new_file_name = pathlib.Path(filename).stem

        extension = str(self.get_file_extension(filename))

        new_path = root+"/"+new_file_name+extension

        try:
            # optimize = False
            # if extension.__eq__("png"):
            #     optimize = True

            image.save(new_path, optimize=True, quality=self.quality)
            #os.remove(filepath)

            print(Fore.GREEN + path + " =>  işlendi")

            self.success_count += 1
        except Exception as e:
            print(Fore.RED+new_path)
            # hatalı image error folder'ına atılacak
            self.error_count += 1
            logging.error(e)

        return

    def start(self) -> None:

        self.crete_error_files()
        self.file_operations()

        print("İşlem başlatılıyor...")

        time.sleep(1)

        st = time.time()

        for (root, dirs, file) in os.walk(self.target_dir):
            for f in file:
                if os.path.splitext(f)[1].lower() in self.formats:
                    # if ('.png' in f) or ('.jpeg' in f) :
                    # print(root,dirs,f)
                    path = root + '/' + f
                    self.compress(root, path, f)

        elapsed_time = time.time() - st

        print("###################################################")
        print("İşlem ", time.strftime("%H:%M:%S", time.gmtime(
            elapsed_time)), " sürede tamamlandı")
        print(str(self.success_count) + ' adet dosya  başarıyla işlendi. ')
        print(str(self.error_count) + ' adet dosya  başarısız oldu. ')
        print("###################################################")
