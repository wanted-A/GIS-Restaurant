![logo](https://github.com/wanted-A/GIS-Restaurant/assets/101565486/7a4ea4ff-ac44-415e-91fe-eb3b91c283f2)

# 📍 지리 기반 맛집 추천 서비스
사용자의 위치를 기반으로 하여 주변 맛집을 추천해주는 서비스입니다. <br/>
사용자는 도보(1km이내), 교통수단(5km이내) 을 선택해서 추천 받을 수 있습니다.

<br/>

## 목차
- [개요](#개요)
- [Skills](#Skills)
- [Installation](#Installation)
- [API Documents](#API-Documents)
- [프로젝트 및 이슈관리](#프로젝트-및-이슈관리)
- [Authors](#Authors)
- [References](#References)

<br/>

## 개요
우리는 언제나 어떤 음식을 먹을지 고민합니다.
로그인 한 사용자의 위치를 기반으로 하여 식사시간에 맞춰서 메뉴 혹은 음식점을 추천해주는 서비스를 개발하고 있습니다.
(현재는 경기도 기준)

`주요기능`
> 1. 로그인 시 사용자의 위치를 위도와 경도로 조회합니다.
> 2. OpenAPI를 이용해서 경기도의 음식점과 카페들을 수집합니다. (변동 될 수 있으므로 주기적으로 수집)
> 3. 사용자는 원하는 이동거리(도보/교통수단)를 설정하여 거리에 맞는 맛집들을 조회할 수 있습니다.
> 4. 사용자는 맛집의 리뷰를 남길 수 있습니다.
> 5. 리뷰는 평균점수로 계산되어 사용자에게 보여집니다.

<br>

`추후기능`
> 1. 추천 받을 알림 시간 설정
> 2. 추천 받을 수 있는 지역 확대

<br>

## Skills
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) &nbsp;
![Django](https://img.shields.io/badge/Django-092E20.svg?style=for-the-badge&logo=Django&logoColor=white) &nbsp;
![postgresql](https://img.shields.io/badge/postgresql-4169E1.svg?style=for-the-badge&logo=postgresql&logoColor=white)  <br> 
![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white)  &nbsp;
![Celery](https://img.shields.io/badge/Celery-37814A.svg?style=for-the-badge&logo=Celery&logoColor=white)  &nbsp;
![Redis](https://img.shields.io/badge/Redis-DC382D.svg?style=for-the-badge&logo=Redis&logoColor=white)  &nbsp;
![Rabbitmq](https://img.shields.io/badge/Rabbitmq-FF6600.svg?style=for-the-badge&logo=Rabbitmq&logoColor=white)  &nbsp;

<br>

## Installation
```py
pip install -r requirements.txt
python manage.py runserver
docker compose -f "docker-compose.yml" up -d --build
```

<br>

## API Documents

<a href="https://www.notion.so/ssu-uky/API-Docs-f74fa68afce8405ba80a3f93fab09678?pvs=4">
<img src="https://img.shields.io/badge/API_Document-8CA1AF.svg?style=for-the-badge&logo=readthedocs&logoColor=white&link=https://www.notion.so/ssu-uky/API-Docs-f74fa68afce8405ba80a3f93fab09678?pvs=4"/>
</a>

<br>

## 프로젝트 및 이슈관리
<a href="https://ssu-uky.notion.site/ssu-uky/Team-A-c365d2c6babf4d5494b108fa66b39c1f">
<img src="https://img.shields.io/badge/Notion-000000.svg?style=for-the-badge&logo=Notion&logoColor=white&link=https://ssu-uky.notion.site/ssu-uky/Team-A-c365d2c6babf4d5494b108fa66b39c1f"/>
</a>

## Authors
|name|profile|email|
|------|---|----|
|이수현|[@ssu-uky](https://github.com/ssu-uky)|id_suhyun@naver.com|
|전정헌|[@allen9535](https://github.com/allen9535)|allen9535@naver.com|
|윤기연|[@kyeon06](https://github.com/kyeon06)|jkyeon06@gmail.com|
|김종완|[@mireu-san](https://github.com/mireu-san)|starmireu@gmail.com|

## References
- [원본 문서](https://bow-hair-db3.notion.site/a9a2ec57b65545e4be7da370c4649007)
- [경기도 데이터 드림](https://data.gg.go.kr/portal/mainPage.do)