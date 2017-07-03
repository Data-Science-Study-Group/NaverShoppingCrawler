<h1>Naver Shopping Crawler</h1>

<h2>V1.13</h2><br>
단순 키워드 입력시 해당 키워드를 검색어로, Naver Shopping페이지에 검색 후 나온 데이터를 수집. 

한 페이지당 80개 출력 기준으로 10개 페이지 수집

데이터 수집 후 정제하여 JSON 파일 생성

JSON 파일 양식
{
    "size" : Int,
    "result" : [{ "name":String, "price":StringInt, "seller":String, "DeliveryPrice":value}...]
}

"2017. 07. 03." - V 1.13<br>
제품 이름 수집 방식 개선

"2017. 07. 03." - V 1.12<br>
판매자 정보 수집 중 에러 수정

"2017. 06. 30." - V 1.11<br>
판매자 정보 수집 중 에러 수정

"2017. 06. 30." - V 1.1<br>
이름, 가격, 판매자, 배송비 수집 및 출력<br>
자잘한 오류 및 기능 수정<br>

"2017. 06. 30." - V 1.0<br>
이름, 가격, 판매자 수집 및 출력<br>
