import cv2
import json
import os
import time
import requests

cur_path = os.path.dirname(os.path.realpath(__file__))

THRESHOLD = 100

#서버 주소를 지정해 줄 것
SERVER_ADDR = '' + '/api/get_seat_inspection_result'


def draw_rectangle(frame, pos_data):


    shape = frame.shape
    img_width = shape[1]
    img_height = shape[0]
    for elem in pos_data:
        f_x = elem['position']['f_x']
        f_y = elem['position']['f_y']
        s_x = elem['position']['s_x']
        s_y = elem['position']['s_y']
        cv2.rectangle(frame, (int(img_width*f_x)+1, int(img_height*f_y)+1), (int(img_width*s_x)-1, int(img_height*s_y)-1), (0,255,0), 3)

    return frame


def detect_module():

    cap = cv2.VideoCapture(1+cv2.CAP_DSHOW)

    if cap.open(1):
	    print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))

    start_frame_counter = 0

#wait for white balancing
    while start_frame_counter <= 300:
        cap.read()
        start_frame_counter+=1

#make origin
    ret, frame = cap.read()
    cv2.imwrite(os.path.join(cur_path, 'origin.jpg'), frame)

#read json
    fd = open(os.path.join(cur_path, 'pos_data.json'))
    pos_data = json.loads(fd.read())['data']

    pk_list = []
    origin_picture_list = []
    capture_picture_list = []
    
#origin ROI
    for elem in pos_data:
        img_part = ROI(elem['position']['f_x'], elem['position']['f_y'], elem['position']['s_x'], elem['position']['s_y'], frame)
        origin_picture_list.append(img_part)
        pk_list.append(elem['pk'])
        cv2.imwrite(os.path.join(cur_path, 'origin_'+str(elem['pk']) + '.jpg'), img_part)


    while True:
        capture_picture_list.clear()
        ret, frame = cap.read()
        #show image
        if ret:
            tagged = draw_rectangle(frame.copy(), pos_data)
            cv2.imshow('video', tagged)
        else:
            continue
        #read json
        new_data = json.loads(open(os.path.join(cur_path, 'pos_data.json')).read())
        #if json is updated
        if new_data['is_updated']:
            #get new origin and new origin roi
            new_data['is_updated'] = False
            fd = open(os.path.join(cur_path, 'pos_data.json'), 'w')
            fd.write(json.dumps(new_data, indent=4))
            fd.close()
            cv2.imwrite(os.path.join(cur_path, 'origin.jpg'), frame)

            pos_data = new_data['data']
            pk_list.clear()
            origin_picture_list.clear()
            capture_picture_list.clear()
            #have to clear result save list

            for elem in pos_data:
                img_part = ROI(elem['position']['f_x'], elem['position']['f_y'], elem['position']['s_x'], elem['position']['s_y'], frame)
                origin_picture_list.append(img_part)
                pk_list.append(elem['pk'])
                cv2.imwrite(os.path.join(cur_path, 'origin_'+str(elem['pk']) + '.jpg'), img_part)

        #get captured and roi

        cv2.imwrite(os.path.join(cur_path, 'capture.jpg'),frame)
        for elem in pos_data:
            img_part = ROI(elem['position']['f_x'], elem['position']['f_y'], elem['position']['s_x'], elem['position']['s_y'], frame)
            capture_picture_list.append(img_part)
            cv2.imwrite(os.path.join(cur_path, 'capture_'+str(elem['pk']) + '.jpg'), img_part)

        print(pk_list)
        for i in range(0, len(origin_picture_list)):
            #put result on result_save_list
            if compare_hist(origin_picture_list[i], capture_picture_list[i], i) >= THRESHOLD:
                res = 'T'
                requests.post(SERVER_ADDR, data={'input' : str({'pk' : pk_list[i], 'res' : res})})
            else
                res = 'F'
                requests.post(SERVER_ADDR, data={'input' : str({'pk' : pk_list[i], 'res' : res})})


        
        time.sleep(3)

        cv2.waitKey(1)
        # if k == 27:
        #     break

def ROI(f_x, f_y, s_x, s_y, img_data):
    shape = img_data.shape
    img_width = shape[1]
    img_height = shape[0]
    return img_data[int(img_height*f_y+1):int(img_height*s_y-1), int(img_width*f_x+1):int(img_width*s_x-1)]


def compare_hist(origin, next, idx):

    origin = cv2.Canny(origin, 100, 255)
    next = cv2.Canny(next, 100, 255)

    cv2.imshow('next' + str(idx), next)

    origin_hist = cv2.calcHist([origin],[0],None,[256],[0,256])
    next_hist = cv2.calcHist([next],[0],None,[256],[0,256])
    return int(cv2.compareHist(origin_hist, next_hist, cv2.HISTCMP_CHISQR)**2)

detect_module()