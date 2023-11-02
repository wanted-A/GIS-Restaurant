from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import raw_data_handler

from datetime import datetime


# OPEN API 사용시 참고사항
# 1. response 자체는 리스트
# 2. response[0]은 'head'라는 키 값을 갖는 딕셔너리
# 3. 예) {'head': [{'list_total_count': 16}, {'RESULT': {'CODE': 'INFO-000', 'MESSAGE': '정상 처리되었습니다.'}}, {'api_version': '1.0'}]}
# 4. response[1]은 'row'라는 키 값을 갖는 딕셔너리
# 5. 예) {'row': [{'SIGUN_NM': '평택시', 'SIGUN_CD': '41220', 'BIZPLC_NM': '(주)비앤비', 'LICENSG_DE': '20120823', 'BSN_STATE_NM': '폐업', 'CLSBIZ_DE': '20130401', 'LOCPLC_AR': None, 'GRAD_FACLT_DIV_NM': '상수도전용', 'MALE_ENFLPSN_CNT': None, 'YY': None, 'MULTI_USE_BIZESTBL_YN': 'N', 'GRAD_DIV_NM': None, 'TOT_FACLT_SCALE': None, 'FEMALE_ENFLPSN_CNT': None, 'BSNSITE_CIRCUMFR_DIV_NM': '기타', 'SANITTN_INDUTYPE_NM': None, 'SANITTN_BIZCOND_NM': '이동조리', 'TOT_EMPLY_CNT': None, 'REFINE_LOTNO_ADDR': '경기도 평택시 오성면 죽리 19번지', 'REFINE_ROADNM_ADDR': '경기도 평택시 오성면 서동대로 2064-1', 'REFINE_ZIP_CD': '17926', 'REFINE_WGS84_LOGT': '126.9725130', 'REFINE_WGS84_LAT': '37.0065480'}


class TestAPIView(APIView):
    def get(self, request):
        start = datetime.now()

        result = raw_data_handler()
        if result.get("status") != 201:
            return Response(
                {
                    "error_page": result.get("error_page"),
                    "error_point": result.get("error_point"),
                    "error_message": result.get("error_message"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        end = datetime.now()
        print(f"소요시간: {end - start}")  # celery 미적용시: 0:03:29.111738       # celery 적용시:

        return Response({"messgae": "데이터 처리 완료"}, status=status.HTTP_201_CREATED)
