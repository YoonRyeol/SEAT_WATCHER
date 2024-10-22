# SEAT_WATCHER

## 목차

### [1. dependency](https://github.com/YoonRyeol/SEAT_WATCHER/blob/develop/README.md#1-dependency-1)

### [2. 개요](https://github.com/YoonRyeol/SEAT_WATCHER/blob/develop/README.md#2-%EA%B0%9C%EC%9A%94-1)

### [3. 시스템 구성](https://github.com/YoonRyeol/SEAT_WATCHER/blob/develop/README.md#3-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EA%B5%AC%EC%84%B1-1)

### [4. 메인 서버 설명](https://github.com/YoonRyeol/SEAT_WATCHER/blob/develop/README.md#4-%EB%A9%94%EC%9D%B8-%EC%84%9C%EB%B2%84-%EC%84%A4%EB%AA%85-1)

### [5. Can I Go 운용 방법](https://github.com/YoonRyeol/SEAT_WATCHER/blob/develop/README.md#5-can-i-go-%EC%9A%B4%EC%9A%A9-%EB%B0%A9%EB%B2%95-1)


## 1. dependency

### Server

#### Front-end

- Bootstrap4

https://getbootstrap.com/

- fabric.js

http://fabricjs.com/


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


## 2. 개요

 Can I Go는 카페의 빈 테이블을 실시간으로 탐지하여 현재 카페의 빈 테이블이 몇 개가 있는지 알려주는 웹 서비스입니다. 빈 테이블을 관리하기 위해 카페의 관리자는 카메라 모듈을 설치하고 Can I Go를 통해 테이블 정보를 등록해야 합니다. 고객은 관리자가 등록한 테이블 정보를 통하여 현재 빈 자리가 몇 개인지를 웹 브라우저를 통하여 실시간으로 확인할 수 있습니다.
 
 본 문서에서는 Can I Go 시스템의 운영 및 유지보수를 위한 내용을 다루며 자세한 사용법은 아래 시연동영상을 통해 확인할 수 있습니다.

- 홍보 및 시연 영상 (클릭하여 영상시청이 가능합니다.)

  [![CANIGO?-시연동영상](http://img.youtube.com/vi/9pMxyc3VleE/0.jpg)](https://www.youtube.com/watch?v=9pMxyc3VleE)
  
## 3. 시스템 구성
![watcher_시스템구성도 002](https://user-images.githubusercontent.com/38625842/98774087-9a8d1e80-242d-11eb-91f1-61a2ec1dea95.jpeg)  

 Can I Go의 시스템은 위와 같습니다. DB, 메인서버로 이루어진 웹 시스템과 카메라 모듈로 이루어져 있으며 카메라 모듈과 메인서버는 서로 통신을 하게 되는데 내부망이 아닌 인터넷을 통해 서로 통신을 하게 된다면 가상 VPN 서비스인 remot3.it을 통해 통신하도록 시스템이 구성되어 있습니다. 
 
 웹 시스템의 구성은 DB와 메인서버로 구성되어 있습니다. DB는 MySQL을 사용하고 있고 메인서버는 Django를 사용하고 있습니다. 웹 시스템은 현재 aws의 클라우드 서버 위에서 운영되고 있습니다. 
 
 카메라 모듈은 메인서버와의 통신을 위한 서브서버와 감지를 위해 구현된 감지 모듈로 구성이 되어 있습니다. 
 
## 4. 메인 서버 설명

 이 항목에서는 메인서버에 대해서 유지보수에 필요한 지식을 설명합니다.
 
 ### 1. DB 테이블 설명

![db](https://user-images.githubusercontent.com/40683361/103452705-87078100-4d15-11eb-826a-f5eda256ad22.png)

 위 다이어그램은 Can I Go에서 관리하는 정보들에 대한 테이블의 스키마입니다.
 
 - Store
  
  Store는 가게에 관한 정보입니다. 가게의 이름과 위치에 관한 정보를 담을 수 있습니다. 
  
  - Table
  
  가게의 테이블에 관한 정보입니다. 이 좌석을 사용하는 가게, 좌석이 놓여진 층, 좌석을 감지하는 카메라, 전기를 사용할 수 있는 좌석인지, 해당 좌석이 사용되는 지에 대한 정보를 담을 수 있습니다.  
  
  - Camera
  
  가게에서 사용되는 카메라 모듈에 관한 정보입니다. 사용되는 가게, remote.it에 등록된 카메라의 아이디, 현재 카메라에서 구동되는 서브 서버의 주소에 관한 정보를 담을 수 있습니다.
  
  - Floor
  
  가게의 층에 관한 정보이다. 층에 대한 정보와 몇 층인지, 어느 가게에 포함되는 층인지에 대한 정보를 담을 수 있습니다

  - User
  사용자의 관한 정보이다. 아이디와 비밀번호를 저장하고 있습니다.
  
  - Menu
  관리자의 매장에 메뉴에 대한 정보이다. 메뉴이름, 가격 , 카테고리 정보를 담을 수 있습니다.
  
  - Category
  메뉴의 카테고리의 관한 정보입니다. 가게의 메뉴에 관한 카테고리 정보를 담을 수 있습니다.
  
  - Review
  가게에 대한 사용자 평가관한 정보입니다. 가게에대한 평점과 평가를 담고 있습니다. 

 각 스키마 간의 관계는 다음과 같습니다. Table이 Camera에, Camera가 Floor에, Floor가 Store에 종속된 관계입니다. Store는 여러 개의 Floor 데이터를 가질 수 있으며 각 Floor는 여러 Camera를 가질 수 있고, Camera는 Camera가 관리하는 Table들에 관한 정보를 가질 수 있습니다. 
 
 Category,Menu는 Store에 종속된 관계이며 Review는 User와 Store에 종속된 관계입니다. 
 Store는 여러개의 Review,Category,Menu 데이터를 가질 수 있습니다.
 
 
 ### 2. 페이지 흐름 및 페이지별 기능 설명
 
 아래 항목들은 Can I Go의 메인서버가 서비스하는 페이지와 페이지별 기능, 페이지 흐름을 설명하는 항목입니다.

 - 관리자 페이지 
 
 ![image](https://user-images.githubusercontent.com/40683361/103452878-6d673900-4d17-11eb-94be-98523ed4fd8f.png)

 관리자 페이지들에서는 가게 정보, 카메라 정보, 테이블 정보 및 배치도 편집에 관한 기능을 사용할 수 있습니다. 관리자는 가게리스트에서 가게 정보를 생성, 삭제할 수 있습니다. 
 
 가게 정보를 클릭하여 가게 세부 정보 페이지로 들어가게 되면 현재 가게의 정보에 대한 갱신을 수행할 수 있습니다. 카메라 정보에 대한 CRUD, 카테고리 정보의 CURD 가게 배치도에 대한 조회가 이 페이지에서 가능합니다. 
 
 카메라 페이지는 가게 세부 정보 페이지에서 이동할 수 있습니다. 카메라 페이지에서는 설치된 카메라의 현재 영상을 전송받고, 현재 영상을 기반으로 하여 테이블 정보의 CRUD가 가능합니다. 
 
 가게 배치도 페이지는 가게 세부 페이지에서 이동할 수 있습니다. 가게 배치도 페이지에서는 기생성된 테이블 정보를 도면에 배치하여 좌석 정보 배치도 좌표에 대한 CRUD를 수행할 수 있습니다. 

 
 - 고객 페이지

![image](https://user-images.githubusercontent.com/40683361/103452883-748e4700-4d17-11eb-80ff-470633cc2855.png)


 고객 페이지들에서는 카페 이용자들이 회원가입을 하고, 가게리스트를 조회하고, 가게의 좌석 현황을 확인할 수 있습니다.
 회원 정보 페이지에서는 회원가입을 할 수 있습니다.
 
 가게 리스트에서는 가게를 조회하고, 검색하고, 원하는 가게분류를 필터링하거나 찜 기능을 사용할 수 있습니다.
 
 가게 페이지에서는 가게의 현재 빈 테이블 통계를 확인하고, 좌석 배치도를 확인하거나 메뉴 및 리뷰를 볼 수 있습니다.
 
 

## 5. Can I Go 운용 방법

 이 항목에서는 Can I Go 메인서버, 카메라 모듈 실행 방법 및 운용 방법을 설명합니다.
 
 ### 1. 메인 서버 실행
 
 MySQL을 설치한 뒤, master 브렌치의 파일을 다운받은 뒤 requirements.txt에 있는 필요한 패키지들을 모두 설치합니다.
 
 ```
 pip install -r requirements.txt
 ```
 
 설치를 마친 뒤 프로젝트의 최상위 폴더 위치에서 아래와 같은 명령어로 서버를 실행합니다.
 
 ```
 python manage.py runserver ${addr}:${port}
 ```
 ### 2. 카메라 모듈 실행
 
  python-opencv를 아래와 같은 명령어로 설치해줍니다.
  
  ```
  sudo apt-get install python-opencv
  ```
  
  remote.it 서비스도 아래와 같은 명령어로 설치해줍니다.
  
```
sudo apt-get install remoteit
```

  
  
 카메라 모듈을 운용할 하드웨어에 카메라를 연결해 준뒤, cam_new 브렌치에서 카메라 모듈 소스코드를 다운 받고, 소스코드 최상단 폴더에서 다음과 같은 명령어로 서버를 실행합니다.
 
 ```
 python manage.py runserver localhost:${port}
 ```
 
 ### 3. 메인서버와 카메라 모듈 연동
 
  이 항목은 remote.it을 사용하여 메인서버와 카메라 모듈을 연동하는 법을 소개합니다.
  
  먼저 remote.it 서비스에 가입을 합니다. (https://remote.it/)
  
  가입을 하고 로그인을 한 뒤, add devices에 들어가 select an OS를 선택하여 add to existing pi를 선택하여 계정에 라즈베리파이를 등록해 줍니다.
  
  등록이 끝나면 deveices에서 방금 추가한 라즈베리파이를 connect를 눌러 remoteit admin pannel을 클릭합니다.
  
  새로 뜨는 창을 로그인 하고 다음과 같은 형식으로 서비스를 추가해줍니다.
  
  ![90393116-172c8d00-e0cb-11ea-9a73-4ac3b9fbefa8](https://user-images.githubusercontent.com/40683361/103454796-bffe2080-4d2a-11eb-9b4e-0fecaefa5d6d.png)

 이 때, port번호는 현재 카메라 모듈을 실행시킬 때 입력한 포트번호와 같아야 합니다.
 
 서비스를 등록한뒤 다시 devices 페이지로 이동합니다. 이동하여 device name에서 현재 등록한 장비를 이름을 클릭합니다.
 
 ![tempsnip](https://user-images.githubusercontent.com/40683361/103455017-b970a880-4d2c-11eb-9b55-d241592fe530.png)

 
 deveice service 모달에서 방금 등록한 서비스의 service ID를 복사하여 카메라 정보 생성시 mac address에 붙여넣어주면 카메라 모듈과 메인서버의 연동이 완료됩니다.
