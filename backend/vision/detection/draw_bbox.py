import cv2
import numpy as np

def draw_bbox(img_path,
              bboxes_list:list[list[float]],
              label_list:list[int] = None)-> np.ndarray:
    '''

    ##### 이미지의 경로와 바운딩박스 리스트를 입력받아\n
    ##### 바운딩박스가 그려진 이미지를 반환합니다.
    ---
    Parameters:\n
        img_path (path): 이미지의 경로 \n
        bboxes_list (list): 바운딩박스 리스트 [[xmin, ymin, xmax, ymax], ...]\n
        label_list (list): 라벨 리스트 [x, y, z, ...]\n
    Returns:\n
        box_on_img (ndarray): 바운딩박스가 그려진 넘파이 배열
    '''

    box_on_img = cv2.imread(img_path)
    num_bboxes = len(bboxes_list)

    if label_list:
        assert len(bboxes_list) == len(label_list)
        for i in range(num_bboxes):
            box = bboxes_list[i]
            label = label_list[i]
            xmin, ymin, xmax, ymax = box
            xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
            
            cv2.rectangle(img=box_on_img, 
                        pt1=(xmin, ymin), pt2=(xmax, ymax), 
                        color=(0, 0, 255), thickness=2)
            cv2.putText(img=box_on_img, text=label, org=(xmin, ymin-10),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8,
                        color=(0, 0, 255), thickness=2)
    else:
        for i in range(num_bboxes):
            box = bboxes_list[i]
            xmin, ymin, xmax, ymax = box
            xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
            
            cv2.rectangle(img=box_on_img, 
                        pt1=(xmin, ymin), pt2=(xmax, ymax), 
                        color=(0, 0, 255), thickness=3)
    box_on_img = cv2.cvtColor(box_on_img, cv2.COLOR_BGR2RGB)
    return box_on_img