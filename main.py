from image_compressor import ImageCompressor

def main():

    image_compressor = ImageCompressor(TARGET_PATH,SRC_DIR)
    image_compressor.start()
    

if __name__ == "__main__":

    TARGET_PATH = "compress-image\images_clone"
    SRC_DIR = "compress-image\original_images"


    main()

