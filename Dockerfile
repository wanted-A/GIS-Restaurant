# 기본 이미지를 파이썬 3.11.3으로
FROM python:3.11.3

# 작업 폴더 디렉터리 설정
WORKDIR /gis-restaurant

# 현재 디렉터리(Dockerfile이 있는 디렉터리)의 파일들을 작업 폴더 디렉터리에 복사
COPY . /gis-restaurant

# 명령어 실행
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt