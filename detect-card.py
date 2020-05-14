import imutils
from skimage import exposure
import numpy as np 
import argparse 
import cv2 

ap = argparse.ArgumentParser()
ap.add_argument("-q","--query",required=True,help="Path to the query image")
args = vars(ap.parse_args())

image = cv2.imread(args["query"])
orig = image.copy()
image = imutils.resize(image, height = 300)
orig = imutils.resize(orig, height = 900)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)

# cv2.imshow("edged",edged)
# cv2.waitKey(0)

cnts = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts , key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

for c in cnts : 
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.015 * peri, True)
    
    if len(approx) == 4:
        screenCnt = approx
        break

print("hmm yes = ",screenCnt)
# cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
x_min=y_min=x_max=y_max=0
x_min = screenCnt[0][0][0] * 3.01
y_min = screenCnt[0][0][1] * 3.01
for i in range(4):
    screenCnt[i] = screenCnt[i] * 3.01
    val = screenCnt[i][0] 
    print(val[0],val[1],sep="\n")   
    if(val[0] > x_max):
        x_max = val[0]
    if(val[1] > y_max):
        y_max = val[1]
    if(val[0] < x_min ):
        x_min = val[0]
        print("hello there",val[0])

    if(val[1] < y_min ):
        y_min = val[1]
        print("general kenobi",val[1])


cv2.drawContours(orig, [screenCnt], -1, (0, 255, 0), 3)

cv2.imshow("Poke Card Maybe?", orig)

print("min = ",x_min,",",y_min," max = ",x_max,",",y_max)
cropped = orig[x_min:x_max,y_min:y_max]
cv2.imshow("perhaps its cropped", cropped)
cv2.waitKey(0)