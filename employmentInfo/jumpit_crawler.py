import requests  # htlm 코드를 가져오기 위한 모듈
import json  # json import하기
import pandas as pd

import pymysql
import os
from dotenv import load_dotenv


def save_to_db(data):
    """
    데이터를 데이터베이스에 저장하는 함수

    :param data: dict, 저장할 딕셔너리 (회사 이름, 기술 스택, 지역)
    :return: None
    """

    connection = None
    try:
        load_dotenv('.env')

        print(f"{os.getenv('HOST_ADDRESS')}, {os.getenv('USER_ID')}, {os.getenv('USER_PW')}")

        # 데이터베이스 연결
        connection = pymysql.connect(
            host=os.getenv("HOST_ADDRESS"),  # MySQL 서버 호스트
            port=int(os.getenv("PORT")),
            user=os.getenv("USER_ID"),  # MySQL 사용자 이름
            password=os.getenv("USER_PW"),  # MySQL 비밀번호
            database=os.getenv("DATABASE_NAME"),  # MySQL 데이터베이스 이름
            charset='utf8',  # 데이터베이스 문자셋
            cursorclass=pymysql.cursors.DictCursor,
            auth_plugin_map={
                'mysql_native_password': 'pymysql.sha256_password'
            }
        )

        with connection.cursor() as cursor:
            # 테이블 생성 구문 주석 처리
            # cursor.execute('''
            #     CREATE TABLE IF NOT EXISTS infoData (
            #         companyName TEXT NOT NULL,
            #         location TEXT NOT NULL,
            #         jobCategory TEXT NOT NULL,
            #         skill TEXT NOT NULL
            #     ) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
            # ''')

            print("\n데이터 삽입 시작\n\n")

            # 데이터 삽입
            for item in data:
                cursor.execute('''
                                        INSERT INTO infoData (companyName, location, jobCategory, skill)
                                        VALUES (%s, %s, %s, %s)
                                    ''', (item['companyName'], item['location'], item['jobCategory'], item['skill']))

            # 커밋
            connection.commit()
            print("\n데이터 삽입 종료\n\n")
            print("Data successfully saved to the database")

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        if connection:
            connection.close()
            print("MySQL connection is closed")


def save_to_excel(data, file_path):
    """
    데이터를 엑셀 파일로 저장하는 함수

    :param data: dict, 저장할 딕셔너리 (회사 이름, 기술 스택, 지역)
    :param file_path: str, 엑셀 데이터를 저장할 파일 경로
    :return: None
    """
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    print(f"Data successfully saved to {file_path}")


def save_file_json(data, file_path):
    """
    데이터를 JSON 파일로 저장하는 함수
    
    :param data: dict, 저장할 딕셔너리 (회사 이름, 기술 스택, 지역)
    :param file_path: str, 파일 이름
    :return: None
    """

    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


def crawler():
    """

    :return:
    """

    # 해당 사이트가 아닌 원본 데이터를 동적으로 들고오는 url을 network에서 가지고 온 것
    dynamic_page = 0

    base_url = "https://api.jumpit.co.kr/api/positions"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.141 Whale/3.15.136.29 Safari/537.36",
        "referer": "https://www.jumpit.co.kr/positions"
    }

    tech_info = []

    # 기술 json이 공백이 나올 때까지 루프
    while True:
        dynamic_page = dynamic_page + 1
        url = base_url + f"?page={dynamic_page}"

        result = requests.get(url, headers=headers)
        result.raise_for_status()  # 정상적으로 접속이 되었는지 확인
        result.encoding = "utf8"

        stock_data = json.loads(result.text)  # json 형태의 데이터 저장

        # 기술 json이 빈칸인 경우
        if len(stock_data['result']['positions']) == 0:
            break

        for data in stock_data['result']['positions']:
            # print(f"{data['locations']}")
            temp_all = {
                "companyName": data['companyName'],
                "location": data['locations'][0],
                "jobCategory": data['jobCategory']
            }

            temp_skill = []
            for skill in data['techStacks']:
                print(skill)
                temp_skill.append(skill)  # 기술 임시 저장

            # temp_all['skill'] = temp_skill  # 기술 스택을 리스트로 저장하길 원할 때 사용
            temp_all['skill'] = ', '.join(temp_skill)  # 기술 스택을 문자열로 변환하여 저장 

            tech_info.append(temp_all)

        print("----- 동적 " + str(dynamic_page + 1) + "페이지 끝 -----")

    return tech_info


if __name__ == "__main__":
    tech_info = crawler()
    print("\n\ncrawler() 종료\n\n")
    print(tech_info)

    # save_file_json(tech_info, "techInfoData/tech_info.json")
    # save_to_excel(tech_info, "techInfoData/tech_info.xlsx")
    save_to_db(tech_info)
