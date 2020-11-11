# SEAT_WATCHER
## dependency
  + Ubuntu 18.04
  + MYSQL
  + DJANGO
## 개요
  + 동영상
## 시스템 구성
![watcher_시스템구성도 002](https://user-images.githubusercontent.com/38625842/98774087-9a8d1e80-242d-11eb-91f1-61a2ec1dea95.jpeg)  
  + DB
    - MYSQL
  + Server
    - DJANGO
  + Camera
    - RASBERRYPI
    - REMOTE IT
## 설치 방법
  + REMOTEIT
    - https://docs.remote.it/getting-started?utm_source=website&utm_content=features_header
## 실행방법
  + DB
    - MYSQL
      >sudo systemctl start mysql
  + SERVER
    - DJANGO 
      > python3 manage.py runserver 0:8000
  + CAMERA
    >
    
## DB테이블 설명
  + Store
    - 가게의 정보를 저장하는 테이블
  + Table
    - Table의 좌표 카메라로 찍은 사진에서의 좌표와 배치도에서의 좌표등이 저장되어있다. record 생성시 Store테이블의 pk가 외래키로 설정되며 카메라 등록 시 해당Floor의 pk와 Camera가 pk도 외래키로 등록된다.
  + Camera
    - record 생성시 Store테이블의 pk가 외래키로 설정되며 카메라가 위치한 층에 등록하게 될시 Floor의 pk또한 외래키로 등록된다. 카메라가 찍은 사진파일명 MAC주소와 카메라에 대한 간단한 설명이 저장된다.
    - 
  + Floor
    
 ## ㅇㅇ
