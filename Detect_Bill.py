from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils
import tkinter
from tkinter import filedialog
import pytesseract
import os
import re
from datetime import datetime

src_path = "./"
def get_string(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    result = pytesseract.image_to_string(img)
    return(result)

def detect(text):
    Bills = { 'Electricity Bill' : ['torrent','electricity bill','electricity', 'electric', 'kwh','elecrtic usage', 'electric supply', 'energy', 'generation charges','utility', 'energy charges'] , 'Mobile Bill' : ['mobile services', 'internet bill', 'mobile' , 'phone' , 'mobile bill', 'postpaid bill', 'airtel', 'vodafone', 'idea', 'bsnl','jio', 'prepaid','postpaid', 'broadband', 'fixline'] , 'Water Bill' : [ 'water' , 'water bill', 'water supply', 'water usage', 'bore well charge', 'water budget', 'water utility bill', 'water conservation'] , 'Gas Bill' : ['gas','hp gas', 'natural gas', 'gas bill', 'gas piplines', 'gas charges', 'gas limited', 'gas supply', 'gas use'] , 'Restaurant Bill' : ['restaurant', 'hotel', 'dhaba', 'panjabi', 'chinese', 'kathiyawadi', 'italian', 'maxican', 'coffee', 'tea', 'fast food', 'dinner', 'lunch','breakfast', 'food', 'cafe'] , 'Shopping Bill' : ['mall','shop', 'supermarket', 'shopping', 'megamarket', 'dmart', 'retail store', 'cloth', 'store'] , 'Hospital Bill' : ['hospital', 'medical', 'laboratory', 'pharmacy', 'surgical', 'physical therapy','therapy', 'recovery', 'blood', 'emergency', 'surgery', 'pathology', 'health', 'radiology', 'cardiology'] , 'Newspaper Bill' : ['newspaper','news', 'papers', 'the times of india', 'hindustantimes', 'the indian express', 'news paper', 'divyabhasker', 'sandesh','gujarat samachar', 'magazine'] }
    Guess = { 'Electricity Bill' : 0 , 'Mobile Bill' : 0 , 'Water Bill' : 0 , 'Gas Bill' : 0 , 'Restaurant Bill' : 0 , 'Shopping Bill' : 0 , 'Hospital Bill' : 0 , 'Newspaper Bill' : 0 }
    path = './Bills/'
    subpath = ''
    for i in Bills:
        count = 0
        for j in Bills[i]:
            #print(j,j in text)
            if j in text:
                Guess[i] += 1
                #if flag:
                #    print("OR",end=' ')
                #print(j)
                #print(i,end=' ')
                #flag = True
                #break
    value = list(Guess.values())
    bill = list(Guess.keys())
    #print(value)
    #print(bill)
    flag = False
    print('\n\n\n\t\t\t***',end='  ')
    if max(value)!= 0 :
        for i in Guess:
            if Guess[i] == max(value) :
                if flag :
                    path += "OTHER/"
                    subpath += "OR "
                    print("OR",end=' ')
                subpath += (i + " ")
                print(i,end=' ')
                flag = True    
        path += (subpath.strip() + '/')
    else :
        print("Please Upload Clear Image..... Not Detected",end=' ')
        path += ('OTHER/')
    print(' ***')
    return path

                
window = tkinter.Tk() 
window.withdraw()
window.overrideredirect(True)
window.geometry('0x0+0+0')
window.deiconify()
window.lift()
window.focus_force()

window.sourceFile = filedialog.askopenfilename(filetypes = (("Image Files",("*.jpg","*.png","*.jpeg")),("All Files","*")),parent=window, initialdir= "/",
title='Please select a image file')

window.destroy()
img_path = window.sourceFile

text = get_string(img_path)

#print(text.lower())
path = detect(text.lower())
#print(path)

img = cv2.imread(img_path)

now = datetime.now()
dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")

if not os.path.exists(path):
    os.makedirs(path)

path += ( 'IMG_' + dt_string + '.jpg' )
print("\nYour Bill is saved in this Location :",path)
cv2.imwrite(path,img)