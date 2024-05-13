import cv2
import numpy as np

PASSWORD_LENGTH = 16
IMAGE_SIZE = 750

#parse through the greyscale image and create a dictionary of pixel values and their corresponding ASCII values
def asciiScramble(img, row: int, col: int) -> dict:
    dict = {}
    ascii_enum = 33

    for i in range(row):
        for j in range(col):             
            pixel_value = img[i,j]
            if pixel_value not in dict:         
                dict[pixel_value] = ascii_enum
                ascii_enum += 1
                if ascii_enum == 126:
                    return dict
                
    raise Exception("ASCII dictionary not fully populated")

#parse through the color image and generate a list of passwords based on the pixel values
def generatePasswordBank(img, row: int, col: int, ascii_dict: dict) -> list[str]:
    password_bank = []
    str = ""
    decode_enum = 0

    for i in range(row):
        for j in range(col):
            pixel_rgb_avg = int(np.mean(img[i,j]))

            str += pixelDecode(pixel_rgb_avg, ascii_dict, decode_enum)
            decode_enum = (decode_enum + 1) % 4

            #only add to dictionary if the string is of length PASSWORD_LENGTH and has no repeating characters
            if len(str) == PASSWORD_LENGTH:
                if len(set(str)) == PASSWORD_LENGTH:
                    password_bank.append(str)
                str = ""

    return password_bank

#decodes the pixel value to an ASCII character
#cycles through the different decoding functions based on the function number
def pixelDecode(pixel_value: int, ascii_dict: dict, funct: int) -> str:
    match funct:

        # normal ascii table and color image
        case 0:
            if pixel_value in range(33, 126):
                return chr(pixel_value)
            return chr(pixel_value % 93 + 33)
        
        # modified ascii table and color image
        case 1:
            if pixel_value in ascii_dict.keys():
                return chr(ascii_dict[pixel_value])
            return chr(pixel_value % 93 + 33)
        
        # normal ascii table and inverted image
        case 2:
            pixel_value = 255 - pixel_value
            if pixel_value in range(33, 126):
                return chr(pixel_value)
            return chr(pixel_value % 93 + 33)
        
        # modified ascii table and inverted image
        case 3:
            pixel_value = 255 - pixel_value
            if pixel_value in ascii_dict.keys():
                return chr(ascii_dict[pixel_value])
            return chr(pixel_value % 93 + 33)
        
        case _:
            raise Exception("Invalid function")
        
#resize the image to IMAGE_SIZE x IMAGE_SIZE if the image is larger than IMAGE_SIZE
#resizes the image to the center of the image
def resizeImage(gimg, cimg, row: int, col: int) -> tuple:
    if row > IMAGE_SIZE: 
        resize_rows = (row - IMAGE_SIZE) // 2
        gimg = gimg[resize_rows:resize_rows+IMAGE_SIZE, 0:col]
        cimg = cimg[resize_rows:resize_rows+IMAGE_SIZE, 0:col]
        row = IMAGE_SIZE

    if col > IMAGE_SIZE:
        resize_cols = (col - IMAGE_SIZE) // 2
        gimg = gimg[0:row, resize_cols:resize_cols+IMAGE_SIZE]
        cimg = cimg[0:row, resize_cols:resize_cols+IMAGE_SIZE]
        col = IMAGE_SIZE

    return gimg, cimg, row, col
    

if __name__ == "__main__":
    image = ''                                      # Path to the image or image name in directory
    grey_img = cv2.imread(image, 0)                 # Load the image in greyscale
    color_img = cv2.imread(image, 1)                # Load the image in color
    rows, cols = grey_img.shape                     # Get the image dimensions

    grey_img, color_img, rows, cols = resizeImage(grey_img, color_img, rows, cols)

    ascii_dict = asciiScramble(grey_img, rows, cols)
    passord_bank = generatePasswordBank(color_img, rows, cols, ascii_dict)

    #[print(password) for password in passord_bank]             # all passwords of length PASSWORD_LENGTH with no repeating characters

    print(passord_bank[rows * cols % len(passord_bank)])        # choose a password from password_bank based on the number of pixels in the image
    
