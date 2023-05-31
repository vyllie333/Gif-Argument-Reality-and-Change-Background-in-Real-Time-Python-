import numpy as np
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

cap = cv2.VideoCapture(0)

#set size webcam (640, 480) tương tự size cho background để làm background cho output
cap.set(3, 640)
cap.set(4, 480)
segmentor = SelfiSegmentation()

#truy cập list backrgound
listImg = os.listdir("background")
imgList = []
for imgPath in listImg:
    img = cv2.imread(f'background/{imgPath}')
    imgList.append(img)

#khởi tạo ảnh backrgound ban đầu
indexImg = 0

#load ảnh, gif
imgTarget = cv2.imread('dino.jpg')
imgTarget = cv2.resize(imgTarget, (500,500))
myVid = cv2.VideoCapture('dino.gif')

#kiểm tra có detect từ webcam không
detection = False
frameCounter = 0

success, imgVideo = myVid.read()

#reszie từ gif bằng size ảnh
hT, wT, cT = imgTarget.shape
imgVideo = cv2.resize(imgVideo, (hT, wT))

#thuật toán ORB
orb = cv2.ORB_create(nfeatures=1000)
kp1, des1 = orb.detectAndCompute(imgTarget, None)

while True:
    success, imgWebcam = cap.read()
    imgAug = imgWebcam.copy()
    kp2, des2 = orb.detectAndCompute(imgWebcam, None)
    imgStack = imgWebcam.copy()
    imgOut = imgWebcam.copy()

    if detection == False:
        myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 0
    else:
        if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
            myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        success, imgVideo = myVid.read()
        imgVideo = cv2.resize(imgVideo, (wT, hT))

    #hiện output 1: image và đối chiếu ảnh trên webcam
    bf = cv2.BFMatcher()
    macthes = bf.knnMatch(np.asarray(des1,np.float32),np.asarray(des2,np.float32), 2)
    good = []
    for m, n in macthes:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    print(len(good))
    imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags = 2)

    #chuyển output image->gif 3D
    if len(good) > 20 :
        detection = True
        srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
        print('Render success')

        pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, matrix)
        img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)

        imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))

        maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
        cv2.fillPoly(maskNew, [np.int32(dst)], [255, 255, 255])
        maskInv = cv2.bitwise_not(maskNew)
        imgAug = cv2.bitwise_and(imgAug, imgAug, mask = maskInv)
        imgAug = cv2.bitwise_or(imgWarp, imgAug)

        #remove background và change background trong imgList
        imgOut = segmentor.removeBG(imgAug, imgList[indexImg], threshold=0.3)
        #cvzone gộp 2 output cùng show
        imgStack = cvzone.stackImages([imgAug, imgOut], 2,1)
        
    #xuất 2 output 
    cv2.imshow('testimg', imgFeatures)
    cv2.imshow("double output", imgStack)

    #options change background: button=1 hoặc button==2 <=> next or previous
    key = cv2.waitKey(100)
    if key == ord('1'):
        if indexImg>0:
            indexImg -=1
    elif key == ord('2'):
        if indexImg<len(imgList)-1:
            indexImg +=1
    elif key == ord('q'):
        break
    
    frameCounter += 1
