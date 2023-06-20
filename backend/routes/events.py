import base64
import datetime
import os,json,re
import numpy as np
import PIL.Image
from fastapi import APIRouter,File, Form, UploadFile, Request, HTTPException, Response, status
from vision.mask import mask_blush, mask_sebum, boxes_area_calculator
from vision.detection import *
from utils.database import create_conn, check_username_email
from utils.functions import moisture_score_calc, temperature_score_calc, sebum_score_calc, porphyrin_score_calc, blush_score_function, dummy_temp, calc_grade, moisture_grade, temp_grade, get_latest_image
from routes.event_models import UserModel, RegisterModel
from pymysql.cursors import DictCursor
from datetime import date
import random
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_IMG_DIR = os.path.join(BASE_DIR,'storage/')
WHITE_IMG_DIR = os.path.join(SERVER_IMG_DIR,'white/')
UV_IMG_DIR = os.path.join(SERVER_IMG_DIR,'uv/')
DL_IMG_DIR = os.path.join(SERVER_IMG_DIR,'dl/')
SEBUM_IMG_DIR = os.path.join(SERVER_IMG_DIR,'sebum/')
BLUSH_IMG_DIR = os.path.join(SERVER_IMG_DIR,'blush/')
device=torch.device("cpu")
model = torch.load('/home/ubuntu/withskin/backend/vision/detection/best_model_mobilenet_singleclass.pt',
                   map_location=device)
router = APIRouter()
user_question_cache={}
#수정완료. uv랑 화이트 각각 나뉘어서 들어감. (완)
@router.post("/api/paperweightone", tags=['paperweight'])
async def upload_images(session : str = Form(None),
                        image1: UploadFile = File(None),
                        image2: UploadFile = File(None),
                        selectedPart: int = Form(None)):
    global user_question_cache
    username = json.loads(session)

    filenames = []
    images = [image1, image2]
    folder_names = ['white/', 'uv/']
    
    if images:
        for idx, img in enumerate(images):
            currentTime = datetime.datetime.now().strftime(f"%Y%m%d%H%M%S%f")
            content = await img.read()
            filename = f"{SERVER_IMG_DIR}{folder_names[idx]}{int(currentTime)}.png"
            print(filename)

            with open(filename, "wb+") as f:
                f.write(content)
            filenames.append(filename)

    try:
        img_list = []
        for img_file in filenames:
            img_list.append(img_file)

        result = {'username': username,
        'image1': img_list[0] if len(img_list) > 0 else None,
        'image2': img_list[1] if len(img_list) > 1 else None,
        'selectedPart': selectedPart}
        
        # print('***********result debug*********')
        # print(result)

        user_question_cache[username] = result

        # print('***********UQC*******')
        # print(user_question_cache)
        # print('유저네임')
        # print(username)

        return {
            'result' : result
        }
    except Exception as e:
        print(f'오류 발생{e}')
        raise

@router.post('/api/paperweighttwo', tags=['paperweight'])
async def get_paperweight_two(
    selectedGender: int = Form(None),
    selectedAge: int = Form(None),
    session: str = Form(...),
    ):
    
    
    try:
        session=json.loads(session)
        global user_question_cache
        user_question_cache[session]["selectedGender"] = selectedGender
        user_question_cache[session]["selectedAge"] = selectedAge
    except Exception as e:
        return {
            'errorData.message': '백엔드 에러',
            'errorData.detail': str(e),
        }, print(e)
    return {
        'saved in server': user_question_cache[session]
    }
@router.post('/api/paperweightthree', tags=['paperweight'])
async def get_paperweight_three(
    selectedQuestion1: int = Form(None),
    selectedQuestion2: int = Form(None),
    selectedQuestion3: int = Form(None),
    selectedQuestion4: int = Form(None),
    selectedQuestion5: int = Form(None),
    selectedQuestion6: int = Form(None),
    session : str = Form(...)
    ):
    try:
        session=json.loads(session)
        global user_question_cache
        user_question_cache[session]["selectedQuestion1"]=selectedQuestion1
        user_question_cache[session]["selectedQuestion2"]=selectedQuestion2
        user_question_cache[session]["selectedQuestion3"]=selectedQuestion3
        user_question_cache[session]["selectedQuestion4"]=selectedQuestion4
        user_question_cache[session]["selectedQuestion5"]=selectedQuestion5
        user_question_cache[session]["selectedQuestion6"]=selectedQuestion6


    except Exception as e:
        return {
            'errorData.message': '백엔드 에러',
            'errorData.detail': str(e),
        }, print(e)
    return {
        'saved in server': user_question_cache[session]
    }, print(user_question_cache[session])


@router.post('/api/paperweightfour', tags=['paperweight'])
async def get_paperweight_four(
    selectedQuestion7: int = Form(None),
    selectedQuestion8: int = Form(None),
    selectedQuestion9: int = Form(None),
    selectedQuestion10: int = Form(None),
    selectedQuestion11: int = Form(None),
    selectedQuestion12: int = Form(None),
    selectedQuestion13: int = Form(None),
    session : str = Form(...)
    ):
    try:
        session=json.loads(session)
        global user_question_cache
        user_question_cache[session]["selectedQuestion7"]=selectedQuestion7
        user_question_cache[session]["selectedQuestion8"]=selectedQuestion8
        user_question_cache[session]["selectedQuestion9"]=selectedQuestion9
        user_question_cache[session]["selectedQuestion10"]=selectedQuestion10
        user_question_cache[session]["selectedQuestion11"]=selectedQuestion11
        user_question_cache[session]["selectedQuestion12"]=selectedQuestion12
        user_question_cache[session]["selectedQuestion13"]=selectedQuestion13


    except Exception as e:
        return {
            'errorData.message': '백엔드 에러',
            'errorData.detail': str(e),
        }, print(e)
    return {
        'saved in server': user_question_cache[session]
    }, print(user_question_cache[session])


@router.post('/api/paperweightfive', tags=['paperweight'])
async def get_paperweight_five(
    selectedQuestion14: int = Form(None),
    selectedQuestion15: int = Form(None),
    selectedQuestion16: int = Form(None),
    selectedQuestion17: int = Form(None),
    selectedQuestion18: int = Form(None),
    selectedQuestion19: int = Form(None),
    session : str = Form(...)
    ):
    try:
        session=json.loads(session)
        global user_question_cache
        user_question_cache[session]["selectedQuestion14"]=selectedQuestion14
        user_question_cache[session]["selectedQuestion15"]=selectedQuestion15
        user_question_cache[session]["selectedQuestion16"]=selectedQuestion16
        user_question_cache[session]["selectedQuestion17"]=selectedQuestion17
        user_question_cache[session]["selectedQuestion18"]=selectedQuestion18
        user_question_cache[session]["selectedQuestion19"]=selectedQuestion19


    except Exception as e:
        return {
            'errorData.message': '백엔드 에러',
            'errorData.detail': str(e),
        }, print(e)
    return {
        'saved in server': user_question_cache[session]
    }, print(user_question_cache[session])

@router.post('/api/paperweightsix', tags=['paperweight'])
async def get_paperweight_six(
    selectedQuestion20: int = Form(None),
    selectedQuestion21: int = Form(None),
    selectedQuestion22: int = Form(None),
    selectedQuestion23: int = Form(None),
    selectedQuestion24: int = Form(None),
    selectedQuestion25: int = Form(None),
    selectedQuestion26: int = Form(None),
    session : str = Form(...)
    ):
    try:
        session=json.loads(session)
        global user_question_cache

        user_question_cache[session]["selectedQuestion20"]=selectedQuestion20
        user_question_cache[session]["selectedQuestion21"]=selectedQuestion21
        user_question_cache[session]["selectedQuestion22"]=selectedQuestion22
        user_question_cache[session]["selectedQuestion23"]=selectedQuestion23
        user_question_cache[session]["selectedQuestion24"]=selectedQuestion24
        user_question_cache[session]["selectedQuestion25"]=selectedQuestion25
        user_question_cache[session]["selectedQuestion26"]=selectedQuestion26
        

    except Exception as e:
        return {
            'errorData.message': '백엔드 에러',
            'errorData.detail': str(e),
        }, print(e)
    return {
        'saved in server': user_question_cache[session]
    }, print(user_question_cache[session])


@router.post("/api/user_question_list", tags=['skinreport'])
async def user_question_list(session : str = Form(...)):
    session = json.loads(session)
    global user_question_cache

    question_list = user_question_cache[session]


    question_dict = {}
    question_dict['sex'] = user_question_cache[session]['selectedGender']
    question_dict['age'] = user_question_cache[session]['selectedAge']
    for key, value in question_list.items():
        if 'selectedQuestion' in key:
            column_number = int(key.replace('selectedQuestion', ''))
            column_name = f'question{column_number}'
            question_dict[column_name] = value
    question_dict_fields = ','.join(question_dict.keys())
    question_dict_values = ','.join(f"'{value}'" if isinstance(value, str) else str(value) for value in question_dict.values())

    today = date.today().strftime('%Y-%m-%d')
    #DB전송 코드
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM user WHERE username = '{session}';")
    user_id = cursor.fetchone()[0]

# question_dict 딕셔너리에 user_id 값을 추가
    question_dict['user_id'] = user_id
    cursor.execute(f"INSERT INTO user_question ({question_dict_fields})VALUES ({question_dict_values});")
    del question_dict['user_id']
    #whiturl, uvurl, selectedpart 넣어야함.
    db_white=user_question_cache[session]["image1"]
    db_uv=user_question_cache[session]["image2"]
    db_selected_part=user_question_cache[session]["selectedPart"]
    cursor.execute(
        f"INSERT INTO images (white_path, uv_path, part, date, user_id) VALUES ('{db_white}','{db_uv}', '{db_selected_part}', '{today}', {user_id});")
    conn.commit()
    conn.close()
    print(type(question_dict))
    return {
        "user_question_list": question_dict
    }, print()          
    # 질문 리스트 다 보내야함.


#이미지딥러닝분석    

#분석결과 출력
@router.post('/api/skinreport' , tags=['skin_report'])
async def uv_led_process(session : str = Form(...)):
    session=json.loads(session)

    latest_uv_path = user_question_cache[session]['image2']
    latest_white_path = user_question_cache[session]['image1']
    
    if not latest_white_path:
        return {
            "error": "서버에 저장된 이미지가 없습니다."
            }
    currentTime = datetime.datetime.now().strftime(f"%Y%m%d%H%M%S%f")
    blush_masked_array, blush_ratio = mask_blush(latest_white_path)
    blush_array_image = PIL.Image.fromarray(np.uint8(blush_masked_array))
 

    boxes_list = inference(model=model, device=device, img_path=latest_uv_path)
    sebum_width = boxes_area_calculator(boxes_list)
    output_array = draw_bbox(img_path=latest_uv_path, bboxes_list=boxes_list)
        #output_array가 박스쳐진 어레이 배열.
    sebum_masked_array, porphyrin_ratio ,sebum_ratio = mask_sebum(latest_uv_path)
    sebum_array_image = PIL.Image.fromarray(np.uint8(sebum_masked_array))
    dl_image= PIL.Image.fromarray(np.uint8(output_array))
    dl_filename = f"{DL_IMG_DIR}{int(currentTime)}.png"
    sebum_filename = f"{SEBUM_IMG_DIR}{int(currentTime)}.png"
    blush_filename = f"{BLUSH_IMG_DIR}{int(currentTime)}.png"
    sebum_array_image.save(os.path.join(SEBUM_IMG_DIR,sebum_filename))
    blush_array_image.save(os.path.join(BLUSH_IMG_DIR,blush_filename))
    dl_image.save(os.path.join(DL_IMG_DIR,dl_filename))

    moisture = random.randint(35,45)
    temperature = random.randint(29,33)
    sebum_count = len(boxes_list)

    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM user WHERE username = '{session}';")
    user_id_result = cursor.fetchone()

    # 사용자 ID 확인
    if user_id_result is None:
        return {"error": "해당 세션에 대한 사용자를 찾을 수 없습니다."}
    user_id = user_id_result[0]

    # image_id 값을 가져온 후 확인
    cursor.execute(f"SELECT id FROM images WHERE user_id = '{user_id}';")
    image_result = cursor.fetchone()
    if image_result is None:
        return {"error": "해당 사용자에 대한 이미지를 찾을 수 없습니다."}
    image_id = image_result[0]

    
    cursor.execute(
        f"INSERT INTO skin_analyze (image_id, user_id, sebum_ratio, porphyrin_ratio, sebum_count, moisture, temperature) VALUES ('{image_id}','{user_id}', '{sebum_ratio}', '{porphyrin_ratio}', '{sebum_count}', '{moisture}','{temperature}');")
    conn.commit()
    conn.close()
    sebum_score = round(sebum_score_calc(sebum_width, latest_uv_path, sebum_count))
    porphyrin_score = round(porphyrin_score_calc(1-porphyrin_ratio))
    moisture_score = round(moisture_score_calc(moisture))
    temperature_score = round(temperature_score_calc(temperature))
    blush_score = blush_score_function(blush_ratio)
    print(blush_ratio)
    
    print(calc_grade(sebum_score))
    print(calc_grade(porphyrin_score))
    print(moisture_grade(moisture_score))
    print(calc_grade(blush_score))
    print(temp_grade(temperature_score))
    ws_score = (calc_grade(sebum_score)+calc_grade(porphyrin_score)+moisture_grade(moisture_score)+calc_grade(blush_score)+temp_grade(temperature_score))/5
    pattern = re.compile(r'\d+')
    compile_uv_path = pattern.findall(user_question_cache[session]['image2'])
    compile_white_path = pattern.findall(user_question_cache[session]['image1'])
    compiled_uv = "".join(compile_uv_path)
    compiled_white = "".join(compile_white_path)


    return {'skin_data' : {
        #base64로 인코딩한 화이트 LED 이미지
        "white_led" : f"knu-project.withbecon.com/storage/white/{compiled_white}.png",
        #base64로 인코딩한 UV LED 이미지
        "uv_led" : f"knu-project.withbecon.com/storage/uv/{compiled_uv}.png",
        #피지 색칠한 이미지(UV)
        "sebum_masked": f"knu-project.withbecon.com/storage/sebum/{currentTime}.png",
        #홍조 색칠한 이미지 (white)
        "blush_masked": f"knu-project.withbecon.com/storage/blush/{currentTime}.png",
        #DL 모델돌려서 피지 박스친 이미지
        "dlImages" : f"knu-project.withbecon.com/storage/dl/{currentTime}.png",
        #홍조 비율
        "blush_ratio": round((blush_ratio*100),2),
        #피지 비율
        "sebum_ratio": round((sebum_ratio*100),2),
        #포피린 비율
        "porphyrin_ratio": round((porphyrin_ratio*100),2),
        # DL 모델돌려서 나온 피지 갯수
        "sebum_count" : sebum_count,
        #수분
        "moisture" : moisture,
        #피부온도
        "temperature" : temperature,
        #피지점수
        "sebum_score" : round(sebum_score,5),
        #포피린 점수
        "porphyrin_score" :round(porphyrin_score,5),
        #수분점수
        "moisture_score" : round(moisture_score,5),
        #피부온도점수
        "temperature_score" : round(temperature_score,5),
        #홍조점수
        "blush_score" : round(blush_score,5),
        #WS점수
        "WS_score" : round(float(ws_score),1),
        #홍조 등급
        "blush_grade" : calc_grade(blush_score),
        #피지 등급
        "sebum_grade" : calc_grade(sebum_score),
        #수분
        "moisture_grade" : moisture_grade(moisture_score),
        #온도
        "temp_grade" : dummy_temp(temperature),
        #포피린
        "porphyrin_grade" : calc_grade(porphyrin_score)
        }}

@router.post('/api/images')


#회원가입 기능(완성)
@router.post("/api/Register",tags=["users"])
async def register(request: RegisterModel):
    try:
        username = request.username
        email = request.email
        pw = request.password
        real_name = request.name
        birth = request.birthdate
        
        user_count_username, user_count_email = check_username_email(username, email)
        if user_count_username > 0:
            return {
                'errorData.message': 'ID_EXISTS'
            }
        if user_count_email > 0:
            return {
                'errorData.message': 'Email_EXISTS'
            }
            
        conn = create_conn()
        cursor = conn.cursor()

        cursor.execute(
            f"INSERT INTO user (username, email, pw, real_name, birth) VALUES ('{username}', '{email}', '{pw}', '{real_name}', {birth})")
        
        conn.commit()
        conn.close()

        return{
            'message': 'register completed'
        }

    except Exception as e:
        return {
            'errorData.message': 'Error occurred',
            'errorData.detail': str(e),
        }, print(e)

#로그인 기능(완성)
@router.post('/api/Login', tags=['users'])
async def login(response: Response, userModel: UserModel):
    print("Received userModel:", userModel.dict()) 
    conn = create_conn()
    cursor = conn.cursor(DictCursor)

    cursor.execute("SELECT * FROM user WHERE username = %s", (userModel.username,))
    user = cursor.fetchone()
    print("Fetched user data:", user)
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if userModel.password != user['pw']:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # 쿠키 설정 및 응답 상태 코드 설정
    session_key =(f"{userModel.username}")
    response.set_cookie(key="session_key", value=session_key, httponly=False)
    response.status_code = status.HTTP_200_OK
    return {"session": session_key}




#회원 탈퇴 기능
@router.post('/api/unregister', tags=['users'])
async def unregister(request: Request):
    try:
        form_data = await request.form()
        email = form_data.get('email')
        username = form_data.get('username')
        pw = form_data.get('password')

        conn = create_conn()
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM user WHERE email='{email}' AND pw='{pw}' AND username='{username}")
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            return {
                'errorData.message': 'USER_NOT_EXISTS'
            }

        cursor.execute(f"DELETE FROM user WHERE email='{email}' AND pw='{pw}'")
        conn.commit()
        conn.close()

        return {
            'success.message': 'USER_UNREGISTERED'
        }

    except Exception as e:
        return {
            'errorData.message': '백엔드 에러',
            'errorData.detail': str(e)
        },print(e)

