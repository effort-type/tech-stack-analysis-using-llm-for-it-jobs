import json
from collections import Counter
import pandas as pd


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


# def frequency_counter():
#     """
#     기술스택 빈도수를 카운트하는 함수
#
#     :return: dict, (기술스택, 빈도수)
#     """
#     # JSON 파일 로드
#     with open('techInfoData/tech_info.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#
#     # 기술 스택을 수집할 리스트
#     tech_stacks = []
#
#     # 각 회사의 기술 스택 추출
#     for company in data:
#         skills = company.get('skill', '').split(', ')
#         tech_stacks.extend(skills)
#
#     # 기술 스택 빈도수 계산
#     tech_frequency = Counter(tech_stacks)
#
#     # 기술 스택 빈도수를 내림차순으로 정렬
#     sorted_tech_frequency = sorted(tech_frequency.items(), key=lambda x: x[1], reverse=True)
#
#     frequency = {}
#     tech_temp = []
#     freq_temp = []
#
#     # 결과 출력
#     for tech, freq in sorted_tech_frequency:
#         tech_temp.append(tech)
#         freq_temp.append(freq)
#         print(f"{tech}: {freq}")
#
#     frequency['tech'] = tech_temp
#     frequency['freq'] = freq_temp
#
#     return frequency


def frequency_counter():
    """
    기술스택 빈도수를 카운트하는 함수 (리스트 컴프리헨션 적용 버전)
    JSON 파일 로드 시 예외 처리를 통해 안정성을 높임
    리스트 컴프리헨션을 통해 기술 스택 추출 및 빈도수 계산을 한 줄로 간결하게 작성함

    :return: dict, (기술스택, 빈도수)
    """
    try:
        # JSON 파일 로드
        with open('techInfoData/tech_info.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found.")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return {}

    # 기술 스택을 수집하고 빈도수 계산
    tech_stacks = [skill for company in data for skill in company.get('skill', '').split(', ') if skill]
    tech_frequency = Counter(tech_stacks)

    # 기술 스택 빈도수를 내림차순으로 정렬하여 딕셔너리로 변환
    sorted_tech_frequency = dict(sorted(tech_frequency.items(), key=lambda x: x[1], reverse=True))  # lambda 각 튜플의 두 번째 요소로 정렬하라는 의미

    # 결과 출력 및 반환할 딕셔너리 생성
    frequency = {
        'tech': list(sorted_tech_frequency.keys()),
        'freq': list(sorted_tech_frequency.values())
    }

    for tech, freq in sorted_tech_frequency.items():
        print(f"{tech}: {freq}")

    return frequency


if __name__ == "__main__":
    frequency = frequency_counter()
    save_to_excel(frequency, "techInfoData/frequency_counter.xlsx")
