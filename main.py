import cv2
import numpy as np

PASSWORD_LENGTH = 16

#parse through the greyscale image and create a dictionary of pixel values and their corresponding ASCII values
def asciiHash(img, row, col):
    dict = {}
    ascii_enum = 41

    for i in range(row):
        for j in range(col):             
            pixel_value = img[i,j]              
            if pixel_value not in dict:         
                dict[pixel_value] = ascii_enum
                ascii_enum += 1
                if ascii_enum == 177:
                    return dict
                
    raise Exception("ASCII dictionary not fully populated")

if __name__ == "__main__":
    grey_img = cv2.imread('yellowstone.jpg', 0)      # Load the image in greyscale
    color_img = cv2.imread('yellowstone.jpg', 1)     # Load the image in color
    grows, gcols    = grey_img.shape                 # Get the grey image dimensions
    crows, ccols, _ = color_img.shape                # Get the color image dimensions

    ascii_dict = asciiHash(grey_img, grows, gcols)
    
