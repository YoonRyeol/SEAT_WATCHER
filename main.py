import cv2
import requests
import numpy as np
import datetime
import os
import time
import json
import requests

cap = cv2.VideoCapture(0)

#frame_width = int(cap.get(3))
#frame_height = int(cap.get(4))

capture = False
isStart = False

def initializeResult():
    result = []
    tempResult = []
    for elem in data:
        tempResult = {'pk' : data['pk'], 'res' : 'F'}
        result.update(tempResult)
    with open('result.json', 'w') as make_file:
        json.dump(tempResult, make_file)
    

def save_result_json():
    with open('result.json', 'w') as make_file:
        json.dump(result, make_file)
        url = 'http://18.225.11.167:8001/api/get_seat_inspection_result'
        send_data = { 'input' : json.dumps(result)}
        print("post :: " + str(result))
        r = requests.post(url, data=send_data)


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
    isStart = True

table_status = []
    
while (True):
    ret, frame = cap.read()
    now = datetime.datetime.now().strftime("%S")
    now = str(now)

    if ret == True:
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if not os.path.isfile("images/origin.jpg"):
            time.sleep(2)
            cv2.imwrite("images/origin.jpg", frame)
        if((now == "00" or now == "20" or now == "40") and capture != True and isStart is not False) :
            cv2.imwrite("images/30.jpg", frame)
            print("30 is start")
            
            with open('pos_data.json', 'r') as json_file:
                data = json.load(json_file)
            with open('result.json', 'r') as json_file:
                result = json.load(json_file)
                    
            #    print(data["t1"]["x1"])
            #    print(len(json_data))
            #    print(json_data['percentage']['x1'])


            for elem in data:
                table_status.append(0)
                    
            for elem in data:
                status_index = int(elem['pk'])
                x1 = elem['position']['f_x']
                x2 = elem['position']['s_x']
                y1 = elem['position']['f_y']
                y2 = elem['position']['s_y']
                print("axis", x1, x2, y1, y2)
                captured = ROI(x1, x2, y1, y2, elem['pk'])
                if(is_there_seat(x1, x2, y1, y2, elem['pk'])):
                    if True :
                        if(result[status_index]['res'] == "T"):
                            result[status_index]['res'] = "F"
                            save_result_json();
                        else:
                            result[status_index]['res'] = "T"
                            save_result_json();
                            print("table " + str(elem['pk']) + " is diff")
                        table_status[status_index] = 0    
                        cv2.imwrite("images/origin_"+str(elem['pk'])+".jpg", captured)
                    else:
                        table_status[status_index] += 1
                        
                else:
                    if(table_status[status_index] <= -1):
                        print("table " + str(elem['pk']) + " is same")
                        cv2.imwrite("images/origin_"+str(elem['pk'])+".jpg", captured)
                        table_status[status_index] = 0
                    else:
                        table_status[status_index] -= 1
                print("status is = " + str(table_status[status_index]))
            capture = True
        if(now == "31"):
            capture = False
    # Break the loop
    else:
        break
    time.sleep(1)

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()