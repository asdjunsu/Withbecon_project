import cv2
import numpy as np
from vision.mask import boxes_area_calculator
import os, datetime
def moisture_score_calc(moisture):
    if 0 <= moisture <= 15:
        score = moisture * (25 / 15)
    elif 15 < moisture <= 30:
        score = 25 + (moisture - 15) * (25 / 15)
    elif 30 < moisture <= 35:
        score = 50 + (moisture - 31) * (12.5 / 4)
    elif 35 < moisture <= 40:
        score = 62.5 + (moisture - 35) * (12.5 / 4)
    elif 40 < moisture <= 43:
        score = 75 + (moisture - 41) * (7.5 / 2)
    elif 43 < moisture <= 46:
        score = 82.5 + (moisture - 43) * (7.5 / 2)
    elif 46 < moisture <= 50:
        score = 90 + (moisture - 47) * (10 / 3)
    else:
        raise ValueError("Invalid moisture value")

    return round(score)


def temperature_score_calc(temperature):
    if 20 <= temperature <= 31:
        score = (temperature - 20) / (31 - 20) * 100
    elif 31 < temperature <= 45:
        score = (45 - temperature) / (45 - 31) * 100
    else:
        raise ValueError("Invalid temperature value")

    return round(score)



def porphyrin_score_calc(value):
    '''

    ##### 포피린 비율(porphyrin_ratio)를 받아\n
    ##### 점수로 반환합니다. 1-{value} 의 형태로 사용해야 합니다.
    ---
    Parameters:\n
        value: 포피린 비율 \n

    Returns:\n
        score :포피린 점수(int)
    '''
    # Percentiles
    p25 = 0.9965237590020577
    p50 = 0.9985669402744402
    p75 = 0.9998543532765312
    
    # Score ranges
    if value <= p25:
        return 1 + (value - 0) / (p25 - 0) * 24
    elif p25 < value <= p50:
        return 26 + (value - p25) / (p50 - p25) * 24
    elif p50 < value <= p75:
        return 51 + (value - p50) / (p75 - p50) * 24
    else:
        return 76 + (value - p75) / (1 - p75) * 24



def sebum_score_calc(sebum_width, imgpath, sebum_count):
    '''
    ##### boxes_area_calculate 함수를 거친 값,이미지 경로, 피지 갯수를 입력받아\n
    ##### 점수로 반환합니다.
    ---
    Parameters:\n
        sebum_width: boxes_area_calculate 함수 거친 객체 \n
        imgpath : 경로
        sebum_count: 감지되는 피지의 총 개수
    Returns:\n
        score : 전체 피지 점수(float)
    '''    
    img2cv2 = cv2.imread(imgpath)
    h, w, _ = img2cv2.shape
    img_width = h * w
    value = 1 - sebum_width / img_width

    # Percentiles
    p25 = 0.9665421032697892
    p50 = 0.9769852291377351
    p75 = 0.9858378343621399

    # Score ranges
    if value <= p25:
        sebum_score = 1 + (value - 0) / (p25 - 0) * 24
    elif p25 < value <= p50:
        sebum_score = 26 + (value - p25) / (p50 - p25) * 24
    elif p50 < value <= p75:
        sebum_score = 51 + (value - p50) / (p75 - p50) * 24
    else:
        sebum_score = 76 + (value - p75) / (1 - p75) * 24

    # Calculate whole_sebum_score
    sebum_count_score = 100 - sebum_count
    score = (sebum_score + sebum_count_score) / 2

    return score

def blush_score_calc(blush_ratio):
    Minimum= 0
    Maximum= 4.0
    p25 = 1
    p50 = 2
    p75= 3
    redness_value = 4-blush_ratio
    if Minimum <= redness_value <= p25:  # 0 - 25점 구간
        score = ((redness_value - Minimum) / (p25 - Minimum) * 25)
    elif p25 < redness_value <= p50:  # 26 - 50점 구간
        score = (25 + ((redness_value - p25) / (p50 - p25)) * 25)
    elif p50 < redness_value <= p75:  #  - 75점 구간
        score = (50 + ((redness_value - p50) / (p75 - p50)) * 25)
    elif p75 < redness_value <= Maximum:  # 76 - 100점 구간
        score = (75 + ((redness_value - p75) / (Maximum - p75)) * 25)
    else:
        return None
    
    return score


def blush_score_function(x:float)->int:
    """홍조 비율을 입력받아 홍조에 대한 점수를 반환하는 비선형 함수입니다.

    Parameters
    ----------
    x : float
        홍조 비율.

    Returns
    -------
    int
        홍조에 대한 점수.
    """
    assert (x > 0) or (x < 4), 'x는 0과 4 사이의 실수여야 합니다.'
    if (x >= 0) and (x <= 3.9):
        y = ((1 / np.exp(x)) - (1 / np.exp(4))) * 100 + 1.832
    else:
        y = 0
    return int(y)

def dummy_temp(temp):
    if temp >=31 :
        return 1
    else: 
        return 2
def calc_grade(x):
    if 75 < x <= 100:
        return 1
    elif 50 < x <= 75:
        return 2
    elif 25 < x <= 50:
        return 3
    elif x <= 25:
        return 4
    else:
        return 2.5
def moisture_grade(x):
    if 46 < x:
        return 1
    elif 40 < x <= 46:
        return 2
    elif 30 < x <= 40:
        return 3
    elif x <= 30:
        return 4
    else:
        return 2.5
def temp_grade(x):
    if 31 <= x <32 :
        return 1
    elif 29 <= x < 31 or 32 <= x < 35 :
        return 2
    elif 36 <= x < 40:
        return 3
    elif x <= 28 or x>41:
        return 4
    else:
        return 2.5   
    
def get_latest_image(folder_path):
    list_of_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=lambda x: datetime.datetime.strptime(x.split(".")[0], "%Y%m%d%H%M%S%f"))
    return os.path.join(folder_path, latest_file)
