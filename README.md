# Threppa Backend
------------
+ 김우식
------------
## Backend Process
1. Project ERD 작성
2. Modeling
3. EndPoint(Api) 구현
4. FE와 통신 연결 확인
------------
+ ### Project ERD 작성

<img width="952" alt="스크린샷 2022-06-30 오후 11 02 41" src="https://user-images.githubusercontent.com/104283159/177024584-cb9dd541-c6ad-4724-a7f6-7fa4411470aa.png">

------------

+ ### Modeling
  + User, Product로 App을 구분
  + 유저정보와 관련된 테이블은 User App에, 상품정보와 관련된 테이블은 Product App에 Modeling
------------
+ ### EndPoint(Api) 구현
  + ### User 엔드포인트
    #### [회원가입 Api 구현]
    + 회원가입시 필요한 정보 입력 요청
    + 닉네임, Email, 휴대전화번호 중복불가
    + Email, Password는 정규표현식을 사용하여 유효성 검사

    #### [로그인 Api 구현]
    + 로그인시 Email, Password 데이터 입력 요청
    + 입력받은 데이터와 DB에 존재하는 데이터를 대조하여 결과 반환
    + 일치하는 경우 User데이터기반으로 생성된 AccessToken을 생성하여 반환
  
  + ### Product 엔드포인트
    #### [상품정보 페이지 Api 구현]
    + 상품 한개의 상세정보를 불러오는 Api
    + 상품의 이름, 가격, 색상, 사이즈등의 세부정보를 반환
    + 색상별로 이미지 데이터 별도로 존재
  
    #### [상품목록 페이지 Api 구현]
    + 상품 목록의 정보를 불러오는 Api
    + 상품의 카테고리정보를 이용해 필터링한 데이터를 반환
    
    #### [장바구니 페이지 Api 구현]
    + 회원전용 기능으로 구현해 로그인 유효성 검사를 실행
    + 상품 페이지에서 장바구니에 넣을 데이터를 POST받아 장바구니 DB에 넣어준다
    + 유저정보와 상품정보가 일치하는 장바구니 데이터를 반환
    + 클라이언트에서 수량 수정시 DB에 업데이트가 가능한 Api를 추가로 구현
------------
+ ### FE와 통신 연결 확인

   <img width="561" alt="스크린샷 2022-07-03 오후 2 08 30" src="https://user-images.githubusercontent.com/104283159/177025728-aef7d8d8-ac2c-4304-8181-3cf43f03b53a.png">

------------
