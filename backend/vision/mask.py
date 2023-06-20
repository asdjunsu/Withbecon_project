
import os
import cv2
import numpy as np

def mask_blush(img_path:os.PathLike):
    """
    White LED로 촬영한 사진에서 홍조가 있는 부분을\n
    붉기 정도에 따라 마스킹하여 강조한 이미지의 배열과 \n
    마스킹한 부위가 차지하는 비율을 반환합니다.\n
    ---
    ## Parameters:  
        img_path (str): 이미지의 경로  
      
    ## Returns:  
        output_array (ndarray): 원본 이미지의 배열과 마스킹의 배열을 합성한 배열\n 
        ratio (float): 전체 면적중 마스킹된 부분의 비율  
    """
    img_array = cv2.imread(img_path)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    height, width, _ = img_array.shape
    total_area = height * width

    lab_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
    l_array, a_array, b_array = lab_array[..., 0], lab_array[..., 1], lab_array[..., 2]

    masked_array = img_array.copy()
    ignore_mask = np.zeros_like(l_array, dtype=bool)
    blush_mask = np.zeros_like(l_array, dtype=np.uint8)

    ignore_mask[(l_array < 120) & (a_array < 140)] = True
    ignore_mask[b_array > 140] = True

    blush_mask[a_array > 140] = 1 
    blush_mask[a_array > 145] = 2 
    blush_mask[a_array > 150] = 3
    blush_mask[a_array > 155] = 4

    masked_array[..., 0][blush_mask==4] = 255
    masked_array[..., 1][blush_mask==4] = 0
    masked_array[..., 2][blush_mask==4] = 0

    masked_array[..., 0][blush_mask==3] = 255
    masked_array[..., 1][blush_mask==3] = 50
    masked_array[..., 2][blush_mask==3] = 50

    masked_array[..., 0][blush_mask==2] = 255
    masked_array[..., 1][blush_mask==2] = 100
    masked_array[..., 2][blush_mask==2] = 100

    masked_array[..., 0][blush_mask==1] = 255
    masked_array[..., 1][blush_mask==1] = 150
    masked_array[..., 2][blush_mask==1] = 150

    blush_score = blush_mask.sum()
    ratio = blush_score /total_area
    return masked_array, ratio


def mask_sebum(img_path:str, 
               porphyrin_r_tres:int=200, 
               porphyrin_g_tres:int=200,
               sebum_r_tres:int=160,  
               sebum_g_tres:int=190,  
               sebum_b_tres:int=210):
    """
    UV LED로 촬영한 사진에서 피지가 있는 부분을\n
    마스킹하여 강조한 이미지의 배열과 마스킹한 부위가 차지하는 비율을 반환합니다.\n
    ---
    ## Parameters:  
        img_path (str): 이미지의 경로  
        porphyrin_r_tres (int): 포피린 마스크 R채널에 대한 임계값\n
        porphyrin_g_tres (int): 포피린 마스크 G채널에 대한 임계값\n
        sebum_r_tres (int): 일반 피지 마스크 R채널에 대한 임계값\n
        sebum_g_tres (int): 일반 피지 마스크 G채널에 대한 임계값\n
        sebum_b_tres (int): 일반 피지 마스크 B채널에 대한 임계값\n
      
    ## Returns:  
        output_array (ndarray): 원본 이미지의 배열과 마스킹의 배열을 합성한 배열\n 
        ratio (float): 전체 면적 (890*890)중 마스킹된 부분의 비율  
    """
    img_array = cv2.imread(img_path)
    lab_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2LAB)

    red_array = img_array[..., 2]
    green_array = img_array[..., 1]
    blue_array = img_array[..., 0]
    
    l_array = lab_array[..., 0]
    a_array = lab_array[..., 1]
    b_array = lab_array[..., 2]

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_array = clahe.apply(l_array)
    lab_array = cv2.merge((l_array, a_array, b_array))
    modified_rgb_array = cv2.cvtColor(lab_array, cv2.COLOR_LAB2RGB)

    modified_red_array = modified_rgb_array[..., 0]
    modified_green_array = modified_rgb_array[..., 1]
    modified_blue_array = modified_rgb_array[..., 2]

    # 포피린 마스크
    porphyrin_mask_array = np.zeros_like(red_array, dtype=bool)
    porphyrin_mask_array[modified_red_array > porphyrin_r_tres] = True
    porphyrin_mask_array[modified_red_array <= porphyrin_r_tres] = False
    porphyrin_mask_array[modified_green_array > porphyrin_g_tres] = False
    
    # 일반 피지 마스크
    sebum_mask_array = np.zeros_like(porphyrin_mask_array, dtype=bool)
    sebum_mask_array[(modified_red_array > sebum_r_tres) &
                     (modified_green_array > sebum_g_tres) &
                     (modified_blue_array > sebum_b_tres)] = True

    # 포피린 마스킹 색상
    red_array[porphyrin_mask_array] = 255
    green_array[porphyrin_mask_array] = 60
    blue_array[porphyrin_mask_array] = 60

    # 일반 피지 마스킹 색상
    red_array[sebum_mask_array] = 50
    green_array[sebum_mask_array] = 255
    blue_array[sebum_mask_array] = 130

    # 마스킹된 부분의 면적 계산
    height, width = porphyrin_mask_array.shape
    total_area = height * width
    porphyrin_area = porphyrin_mask_array.sum()
    porphyrin_ratio = porphyrin_area / total_area
    sebum_area = sebum_mask_array.sum()
    sebum_ratio = sebum_area / total_area
    
    output_array = cv2.merge((red_array, green_array, blue_array))
    return output_array, porphyrin_ratio, sebum_ratio


def boxes_area_calculator(boxes_list: list[list[float]])->float:
    """박스 리스트를 입력받아 면적의 합을 반환하는 함수.
    Parameters
    ----------
    boxes_list : list[list[float]]
        박스 리스트 ex) [[xmin, ymin, xmax, ymax], ...]
    Returns
    -------
    float
        박스면적의 합
    """   
    boxes_area = 0.0
    for box in boxes_list:
        box = [int(value) for value in box]
        xmin, ymin, xmax, ymax = box
        width = xmax - xmin
        height = ymax - ymin
        box_area = width * height
        boxes_area += box_area
    return boxes_area