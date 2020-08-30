import cv2
import requests
import numpy as np
import datetime
import os
import time
import json

cap = cv2.VideoCapture(0)
result = dict()

#frame_width = int(cap.get(3))
#frame_height = int(cap.get(4))

capture = False
isStart = False

def is_there_seat(x1, x2, y1, y2, pk):
#     origin = cv2.imread("origin.jpg", 0)
    g_captured = cv2.imread("30.jpg", 0)
    origin = cv2.imread("origin.jpg", 1)
    captured = cv2.imread("30.jpg", 1)

    spot1, spot2 = [int(round(origin.shape[0] * y1 * 0.01)), int(round(origin.shape[1] * x1 * 0.01))], [int(round(origin.shape[0] * y2 * 0.01)), int(round(origin.shape[1] * x2 * 0.01))]
#     origin = origin[spot1[0]:spot2[0], spot1[1]:spot2[1]]
    test = g_captured[spot1[0]:spot2[0], spot1[1]:spot2[1]]

    origin = origin[spot1[0]:spot2[0], spot1[1]:spot2[1]]
    captured = captured[spot1[0]:spot2[0], spot1[1]:spot2[1]]
    cv2.imwrite("origin_"+str(pk)+".jpg", origin)
    cv2.imwrite("captured_"+str(pk)+".jpg", captured)


    cnt_correct = 0
    SUM = 0

    cv2.imshow("origin"+str(pk), origin)
    cv2.imshow("captured"+str(pk), captured)
    
    for y in range(0, spot2[0] - spot1[0]):
        for x in range(0, spot2[1] - spot1[1]):
            test.itemset((y, x), 255)
    avg = 0.0
    for y in range(0, spot2[0] - spot1[0]):
        for x in range(0, spot2[1] - spot1[1]):
            avg = 0.0
#            if (origin_result.item(y, x) == captured_result.item(y, x)):
#                cnt_correct += 1
            if(captured.item(y,x,0) >= origin.item(y,x,0) and captured.item(y,x,0) != 0):
                avg += origin.item(y,x,0) / float(captured.item(y,x,0))
            elif(captured.item(y,x,0) <= origin.item(y,x,0) and origin.item(y,x,0) != 0):
                avg += captured.item(y,x,0) / float(origin.item(y,x,0))

            if(captured.item(y,x,1) >= origin.item(y,x,1) and captured.item(y,x,1) != 0):
                avg += origin.item(y,x,1) / float(captured.item(y,x,1))
            elif(captured.item(y,x,1) <= origin.item(y,x,1) and origin.item(y,x,1) != 0):
                avg += captured.item(y,x,1) / float(origin.item(y,x,1))

            if(captured.item(y,x,2) >= origin.item(y,x,2) and captured.item(y,x,2) != 0):
                avg += origin.item(y,x,2) / float(captured.item(y,x,2))
            elif(captured.item(y,x,2) <= origin.item(y,x,2) and origin.item(y,x,2) != 0):
                avg += captured.item(y,x,2) / float(origin.item(y,x,2))
                
            avg = avg / 3.0
            if(avg <=0.80):
                test[y,x] = 0
                cnt_correct += 1
            


                
    cv2.imshow("after"+str(pk), test)
    print("pk is =", pk)
    if(cnt_correct / float(((spot2[1] - spot1[1]) * (spot2[0] - spot1[0]))) >= 0.3):
        result[str(pk)] = "T"
        return True
    else:
        cv2.imwrite("origin_"+str(pk)+".jpg", captured)
        result[str(pk)] = "F"
        return False


if os.path.isfile("origin.jpg"):
    isStart = True

with open('pos_data.json', 'r') as json_file:
    data = json.load(json_file)
#    print(data["t1"]["x1"])
#    print(len(json_data))
#    print(json_data['percentage']['x1'])

    
while (True):
    ret, frame = cap.read()
    now = datetime.datetime.now().strftime("%S")
    now = str(now)

    if ret == True:
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if not os.path.isfile("origin.jpg"):
            time.sleep(2)
            cv2.imwrite("origin.jpg", frame)

        if cv2.waitKey(1) & 0xFF == ord('o'):
            cv2.imwrite("origin.jpg", frame)
            isStart = True
        if cv2.waitKey(1) & 0xFF == ord('t'):
            is_there_seat(30, 60, 25, 75)
            capture = True
        if(now == "30" and capture != True and isStart is not False) :
            cv2.imwrite(str(now)+".jpg", frame)
            for elem in data:
                x1 = elem['position']['f_x']
                x2 = elem['position']['s_x']
                y1 = elem['position']['f_y']
                y2 = elem['position']['s_y']
                print("Test", x1, x2, y1, y2)
                if(is_there_seat(x1 * 100, x2 * 100, y1 * 100, y2 * 100, elem['pk'])):
                    print("yes")
                else:
                    print("no")
            with open('result.json', 'w') as make_file:
                json.dump(result, make_file)
            capture = True

        if(now == "31"):
            capture = False

    # Break the loop
    else:
        break
cap.release()



#   https://m.blog.naver.com/PostView.nhn?blogId=samsjang&logNo=220502203203&proxyReferer=https:%2F%2Fwww.google.com%2F
#   img = cv2.GaussianBlur(img, (5, 5), 0)
#   _, img_result3 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#   cv2.imshow("3_"+str(n), img_result3)



cv2.waitKey(0)
cv2.destroyAllWindows()