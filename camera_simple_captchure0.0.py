import time
import picamera
import io
import cv2
import numpy as np

acc_count = 0
acc_x = 0
acc_y = 0
mean_x = 0
mean_y = 0


with picamera.PiCamera() as camera:
camera.resolution = (1024, 768)
# Camera warm-up time
time.sleep(2)
	
camera.capture('foo.jpg')
img1 = cv2.imread("foo.jpg")
hsv_img = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
#cv2.imwrite('raw_hsv.jpg',hsv_img)

#limit declaration
ORANGE_MIN = np.array([5, 30, 20],np.uint8)
ORANGE_MAX = np.array([20, 255, 255],np.uint8)
#BLUE_MIN = np.array([240, 30, 20],np.uint8)
#BLUE_MAX = np.array([255, 255, 255],np.uint8)

#filtering the colors
img1o = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
#print("hsv sredinskega pixla")
#p = (img1[5, 5])[0]
#r = uint8(img1[5, 5])[1]
#print(p)
#print(r)
#showing an example
#cv2.imwrite('hsv_filter_applied.jpg', img1o)

z = np.transpose(np.where(img1o>0))
z.shape[0]

for x in range(0, z.shape[0]):
    	acc_x += z[x,0]
    	acc_y += z[x,1]
    	acc_count += 1
#print(acc_count)
print ("coordinates")
if acc_count > 0:
    	mean_x = acc_x / acc_count
    	mean_y = acc_y / acc_count
    	print mean_y
    	print mean_x


img=img1
#print ("drawing on the image")
#draw a small cross in red at the mean position
img[mean_x + 0, mean_y - 1] = 1
img[mean_x - 1, mean_y + 0] = 1
img[mean_x + 0, mean_y + 0] = 1
img[mean_x + 1, mean_y + 0] = 1
img[mean_x + 0, mean_y + 1] = 1
img[mean_x + 0, mean_y - 2] = 1
img[mean_x - 1, mean_y + 0] = 1
img[mean_x + 1, mean_y + 0] = 1
img[mean_x + 0, mean_y + 2] = 1

if mean_x == 0  & mean_y == 0:
	print"blob not found"
else:
	cv2.imwrite('blob_detected.jpg', img)
