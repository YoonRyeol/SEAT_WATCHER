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

  
