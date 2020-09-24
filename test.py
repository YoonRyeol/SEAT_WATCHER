import cv2
import requests
import numpy as np
import datetime
import os
import time
import json
import requests


capture = False
isStart = False

def initializeResult():
    result = []
    for elem in data:
        result.append({"pk" : elem['pk'], "res" : "F"})

    with open('result.json', 'w') as make_file:
        json.dump(result, make_file, indent = 4)
    

def save_result_json():
    with open('result.json', 'w') as make_file:
        json.dump(result, make_file, indent = 4)
        url = 'http://18.219.121.103:8001/api/get_seat_inspection_result'
        send_data = { 'input' : json.dumps(result, indent = 4)}
        print("post :: " + str(result))
        r = requests.post(url, data=send_data)

def swap(x1, x2):
    v_swap = 0
    if(x1 > x2):
        v_swap = x1
        x1 = x2
        x2 = v_swap

def ROI(x1, x2, y1, y2, pk):

    captured = cv2.imread("images/30.jpg", 1)
    spot1, spot2 = [int(round(captured.shape[0] * y1)), int(round(captured.shape[1] * x1))], [int(round(captured.shape[0] * y2)), int(round(captured.shape[1] * x2))]

    if os.path.isfile("images/captured_"+str(pk)+".jpg"):
        captured = captured[spot1[0]:spot2[0], spot1[1]:spot2[1]]
        cv2.imwrite("images/captured_"+str(pk)+".jpg", captured)
        return(captured)

    origin = cv2.imread("images/origin.jpg", 1)
    origin = origin[spot1[0]:spot2[0], spot1[1]:spot2[1]]
    captured = captured[spot1[0]:spot2[0], spot1[1]:spot2[1]]
    cv2.imwrite("images/origin_"+str(pk)+".jpg", origin)
    cv2.imwrite("images/captured_"+str(pk)+".jpg", captured)
    return captured
    

def is_there_seat(x1, x2, y1, y2, pk):
    origin = cv2.imread("images/origin_"+str(pk)+".jpg", 1)
    captured = cv2.imread("images/captured_"+str(pk)+".jpg", 1)

    spot = [int(origin.shape[0]), int(origin.shape[1])]
    cnt_correct = 0
    avg = 0.0
    for y in range(0, spot[0]):
        for x in range(0, spot[1]):
            avg = 0.0
            if(captured.item(y,x,0) >= origin.item(y,x,0) and captured.item(y,x,0) != 0):
                avg += origin.item(y,x,0) / float(captured.item(y,x,0))
            elif(captured.item(y,x,0) <= origin.item(y,x,0) and origin.item(y,x,0) != 0):
                avg += captured.item(y,x,0) / float(origin.item(y,x,0))
                
#            print("avg 1 : " + str(avg))

            if(captured.item(y,x,1) >= origin.item(y,x,1) and captured.item(y,x,1) != 0):
                avg += origin.item(y,x,1) / float(captured.item(y,x,1))
            elif(captured.item(y,x,1) <= origin.item(y,x,1) and origin.item(y,x,1) != 0):
                avg += captured.item(y,x,1) / float(origin.item(y,x,1))

 #           print("avg 2 : " + str(avg))

            if(captured.item(y,x,2) >= origin.item(y,x,2) and captured.item(y,x,2) != 0):
                avg += origin.item(y,x,2) / float(captured.item(y,x,2))
            elif(captured.item(y,x,2) <= origin.item(y,x,2) and origin.item(y,x,2) != 0):
                avg += captured.item(y,x,2) / float(origin.item(y,x,2))


            avg = avg / 3.0
            if(avg <=0.75):
                cnt_correct += 1
#                print("avg isssss : " + str(avg))
                
    print("pk is =", pk)
    print("average is = " + str(cnt_correct / float((spot[1] * spot[0]))))

    if(cnt_correct / float((spot[1] * spot[0])) >= 0.3):
        return True
    else:
        return False


if os.path.isfile("images/origin.jpg"):
    os.remove('images/origin.jpg')

with open('pos_data.json', 'r') as json_file:
    data = json.load(json_file)
#with open('pos_data.json', 'w') as json_file:
#    json.dump(data, json_file, indent = 4)

#initializeResult()
with open('result.json', 'r') as json_file:
    result = json.load(json_file)


table_status = []



cap = cv2.VideoCapture(0)

while cap.isOpened():
    now = datetime.datetime.now().strftime("%S")
    now = str(now)
    ret, frame = cap.read()
    if ret:
        cv2.imshow('cam', frame)
        if cv2.waitKey(1) & 0xFF == 27 :
            break
        
    else:
        print("sibal")
        break
    
cap.release()
cv2.destroyAllWindows()