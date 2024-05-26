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


def frequency_counter():
    # JSON 파일 로드
    with open('techInfoData/tech_info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 기술 스택을 수집할 리스트
    tech_stacks = []

    # 각 회사의 기술 스택 추출
    for company in data:
        skills = company.get('skill', '').split(', ')
        tech_stacks.extend(skills)

    # 기술 스택 빈도수 계산
    tech_frequency = Counter(tech_stacks)

    # 기술 스택 빈도수를 내림차순으로 정렬
    sorted_tech_frequency = sorted(tech_frequency.items(), key=lambda x: x[1], reverse=True)

    frequency = {}
    tech_temp = []
    freq_temp = []

    # 결과 출력
    for tech, freq in sorted_tech_frequency:
        tech_temp.append(tech)
        freq_temp.append(freq)
        print(f"{tech}: {freq}")

    frequency['tech'] = tech_temp
    frequency['freq'] = freq_temp

    return frequency


if __name__ == "__main__":
    frequency = frequency_counter()
    save_to_excel(frequency, "techInfoData/frequency_counter.xlsx")
