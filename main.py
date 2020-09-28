import cv2
import sys
import requests
import numpy as np
import datetime
import os
import time
import json
import requests
from matplotlib import pyplot as plt


capture = False

def initialize():
    print("init....")
    with open('pos_data.json', 'r') as json_file:
        data = json.load(json_file)
        origin_data = data
        if(origin_data['is_updated']):
            origin_data['is_updated'] = False
        data = data['data']


    result = []
    table_status = []
    for elem in data:
        result.append({"pk" : elem['pk'], "res" : "F"})
        table_status.append(0)

    with open('result.json', 'w') as make_file:
        json.dump(result, make_file, indent = 4)
    with open('pos_data.json', 'w') as json_file:
        json.dump(origin_data, json_file, indent = 4)
    return table_status
        
    
def save_result_json():
    with open('result.json', 'w') as make_file:
        json.dump(result, make_file, indent = 4)
        url = 'http://3.21.102.124:8001/api/get_seat_inspection_result'
        send_data = { 'input' : json.dumps(result, indent = 4)}
        try :
            r = requests.post(url, data=send_data, timeout = 3)
        except :
            print("\n=====AWS Server is not working=====\n")
        
def swap(x1, x2):
    v_swap = 0
    if(x1 > x2):
        v_swap = x1
        x1 = x2
        x2 = v_swap
    return x1, x2

#Get ROI(Region of Interest)
def ROI(x1, x2, y1, y2, pk):
    captured = cv2.imread("images/captured.jpg", 1)
    spot1, spot2 = [int(round(captured.shape[0] * y1)), int(round(captured.shape[1] * x1))], [int(round(captured.shape[0] * y2)), int(round(captured.shape[1] * x2))]
    captured = captured[spot1[0]:spot2[0], spot1[1]:spot2[1]]
    cv2.imwrite("images/captured_"+str(pk)+".jpg", captured)

    if os.path.isfile("images/origin_"+str(pk)+".jpg") is not True:
        origin = cv2.imread("images/origin.jpg", 1)
        origin = origin[spot1[0]:spot2[0], spot1[1]:spot2[1]]
        cv2.imwrite("images/origin_"+str(pk)+".jpg", origin)
    return captured
    

def is_there_seat(x1, x2, y1, y2, pk):
    origin = cv2.imread("images/origin_"+str(pk)+".jpg", 1)
    captured = cv2.imread("images/captured_"+str(pk)+".jpg", 1)
    cv2.imshow("origin", origin)
    cv2.imshow("cap", captured)
    spot = [int(origin.shape[0]), int(origin.shape[1])]
    cnt_correct = 0
    avg = 0.0
    test_sum = 0
    test_list = []
    index_list = []
    test_index = 0
    #calculate average diffrence of RGB pixel value between origin and captured picture
    for y in range(0, spot[0]):
        for x in range(0, spot[1]):
            avg = 0.0
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
            test_sum += avg
            test_list.append(avg)
            index_list.append(test_index)
            test_index += 1
            if(avg <=0.88):
                cnt_correct += 1
    print("pk is =", pk)
    print("average is = " + str(test_sum / float((spot[1] * spot[0]))))
    print("average is = " + str(cnt_correct / float((spot[1] * spot[0]))))
#    plt.plot(index_list, test_list)
#    plt.show()
    #if rate of pixel has low similarity is large than 30%, that table status is changed. 
    if(cnt_correct / float((spot[1] * spot[0])) >= 0.2):
        return True
    else:
        return False
    
def detect():
    print("detection loop is start....")
    with open('pos_data.json', 'r') as json_file:
            data = json.load(json_file)
            origin_data = data
            data = data['data']
    status_index = 0
    for elem in data:
        if(origin_data['is_updated']):
            initialize()
            print('\'pos_data.json\' has been changed... restart loop')
            break                
        x1 = elem['position']['f_x']
        x2 = elem['position']['s_x']
        y1 = elem['position']['f_y']
        y2 = elem['position']['s_y']
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
        captured = ROI(x1, x2, y1, y2, elem['pk'])
        if(is_there_seat(x1, x2, y1, y2, elem['pk'])):
            if(table_status[status_index] >= 1):
                if(result[status_index]['res'] == "T"):
                    result[status_index]['res'] = "F"
                    save_result_json()
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
        print("status is = " + str(table_status[status_index]) +"\n")
        status_index += 1    


with open('pos_data.json', 'r') as json_file:
    data = json.load(json_file)
table_status = initialize()
with open('result.json', 'r') as json_file:
    result = json.load(json_file)
    
cap = cv2.VideoCapture(0)
#frame_width = int(cap.get(3))
#frame_height = int(cap.get(4))
    
while True:
    now = datetime.datetime.now().strftime("%S")
    now = str(now)
    ret, frame = cap.read()
    if ret :
        cv2.imshow('cam', frame)
        if not os.path.isfile("images/origin.jpg"):
            cv2.imwrite("images/origin.jpg", frame)
            initialize()
            time.sleep(2)
        if((now == "00" or now == "20" or now == "40") and capture != True) :
            cv2.imwrite("images/captured.jpg", frame)
            detect()
            capture = True
        if(now == "31"):
            capture = False
        if cv2.waitKey(1) & 0xFF == 27 :
            print("delete images....")
            if(os.path.isfile("images/captured.jpg")):                
                for elem in result :
                    os.remove("images/origin_"+str(elem['pk'])+".jpg")
                    os.remove("images/captured_"+str(elem['pk'])+".jpg")
                os.remove("images/captured.jpg")
            os.remove("images/origin.jpg")
            break
            
    # Break the loop
    else:
        break
cap.release()
cv2.destroyAllWindows()