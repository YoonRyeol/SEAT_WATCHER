# SEAT_WATCHER

## 목차

## dependency

### Server

#### Front-end



#### Back-end
  + Ubuntu 18.04
  + MySQL 8.0.21
  
  ``
  sudo apt-get install mysql-server
  ``
  
  + Django 3.1
  
  ``
  pip install django==3.1
  ``
  +  mysqlclient
  
  ``
  pip install mysqlclient==2.0.1
  ``
  + django-rest-framework
  
  ``
  pip install djangorestframework==3.11.1
  ``
  + google-cloud-vision
  
  ``
  pip install google-cloud-vision==1.0.0
  ``
  + requests
  
  ``
  pip install requests=2.24.0
  ``

### Camera

+ python-opencv

``
sudo apt-get install python-opencv
``

+ remot3.it

``
sudo apt-get install remoteit
``

+ Django 3.1

``
pip install django==3.1
``

  + requests
  
  ``
  pip install requests=2.24.0
  ``


## 개요

 Can I Go는 카페의 빈 테이블을 실시간으로 탐지하여 현재 카페의 빈 테이블이 몇 개가 있는지 알려주는 웹 서비스입니다. 빈 테이블을 관리하기 위해 카페의 관리자는 카메라 모듈을 설치하고 Can I Go를 통해 테이블 정보를 등록해야 합니다. 고객은 관리자가 등록한 테이블 정보를 통하여 현재 빈 자리가 몇 개인지를 웹 브라우저를 통하여 실시간으로 확인할 수 있습니다.
 
 본 문서에서는 Can I Go 시스템의 운영 및 유지보수를 위한 내용을 다루며 자세한 사용법은 아래 시연동영상을 통해 확인할 수 있습니다.

- 홍보 및 시연 영상

  [![CANIGO?-시연동영상](http://img.youtube.com/vi/9pMxyc3VleE/0.jpg)](https://www.youtube.com/watch?v=9pMxyc3VleE) 
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
```
      $sudo systemctl start mysql
```
  + SERVER
    - DJANGO
    
```
      $python3 manage.py runserver 0:8000
      
```
  + CAMERA
    - 
    
## DB테이블 설명
  + Store
    - Store는 가게에 관한 정보이다. 가게의 이름과 위치에 관한 정보를 담을 수 있다. 
  + Table
    - 가게의 테이블에 관한 정보이다. 이 좌석을 사용하는 가게, 좌석이 놓여진 층, 좌석을 감지하는 카메라, 전기를 사용할 수 있는 좌석인지, 해당 좌석이 사용되는 지에 대한 정보를 담을 수 있다.  각 스키마 간의 관계는 다음과 같다. Table이 Camera에, Camera가 Floor에, Floor가 Store에 종속된 관계이다. Store는 여러 개의 Floor 데이터를 가질 수 있으며 각 Floor는 여러 Camera를 가질 수 있고, Camera는 Camera가 관리하는 Table들에 관한 정보를 가질 수 있다.
  + Camera
    - 가게에서 사용되는 카메라 모듈에 관한 정보이다. 사용되는 가게, remote.it에 등록된 카메라의 아이디, 현재 카메라에서 구동되는 서브 서버의 주소에 관한 정보를 담을 수 있다.
  + Floor
    - 가게의 층에 관한 정보이다. 층에 대한 정보와 몇 층인지, 어느 가게에 포함되는 층인지에 대한 정보를 담을 수 있다.
 ## 기능
  #### 관리자
   + 가게 추가
    - 가게이름, 위치, 대표사진을 올려 정보를 저장할 수 있습니다.
     <img width="1198" alt="스크린샷 2020-10-02 오후 4 24 43" src="https://user-images.githubusercontent.com/38625842/98784105-f364b300-243d-11eb-94ec-5d4976bb41e7.png">
   + 카메라 추가
    - 가게에 설치되어있는 카메라를 추가 할 수 있습니다. MAC주소만 입력하면 자동으로 연결이 됩니다.
    <img width="1174" alt="스크린샷 2020-10-04 오후 3 39 07" src="https://user-images.githubusercontent.com/38625842/98784239-2c048c80-243e-11eb-9217-8bd160d47089.png">
   + 층 추가 
    - 매장이 있는 또는 관리하고 있는 층의 정보를 입력합니다(ex 1층,2층,3층). 이때 해당 층에 설치되어있는 카메라를 등록 할 수 있습니다. 
    <img width="959" alt="스크린샷 2020-10-04 오후 6 21 46" src="https://user-images.githubusercontent.com/38625842/98784305-4474a700-243e-11eb-8453-c8ba3736e91d.png">
   + 테이블 등록
   <img width="1178" alt="스크린샷 2020-10-12 오후 5 38 04 3" src="https://user-images.githubusercontent.com/38625842/98784814-05932100-243f-11eb-9a6a-450dffda121a.png">

   + 배치도 편집
   <img width="1186" alt="스크린샷 2020-10-12 오후 5 53 20" src="https://user-images.githubusercontent.com/38625842/98784712-ded4ea80-243e-11eb-900e-cff135ac19db.png">
  
  #### 사용자
   + 매장 방문
   ![KakaoTalk_Photo_2020-11-11-16-34-37](https://user-images.githubusercontent.com/38625842/98782776-eba40f00-243b-11eb-9833-d72500322597.png)
   + 검색 및 찜
    - 찾고싶은 가게를 가게이름,위치로 검색가능 
    - 하트버튼을 클릭하여 마음에 드는 가게 또는 가고 싶은 가게를 찜목록에 추가 할 수 있다.
  #### 카메라

  
