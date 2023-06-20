import pymysql, os


#db 연결 함수
def create_conn():
    db_path="./db_host.txt"
    abs_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_path)
    with open(abs_db_path, 'r') as f:
        host_name = f.read()
    host_port = 3306
    username = 'root'
    password = 'knu-withbecon-2023'
    database_name = 'knu_main'

    conn = pymysql.connect(
                            host = host_name,
                            port = host_port, 
                            user = username, 
                            passwd = password,
                            db=database_name,
                            charset='utf8')
    
    return conn

# 결과로 반환된 출현 횟수를 변수에 저장.
def check_username_email(username: str, email: str):
    conn = create_conn()
    cursor = conn.cursor()
    #유저 닉네임 확인
    cursor.execute(f"SELECT count(*) FROM user WHERE username = '{username}'")
    user_count_username = cursor.fetchone()[0]
    #유저 이메일 확인
    cursor.execute(f"SELECT count(*) FROM user WHERE email = '{email}'")
    user_count_email = cursor.fetchone()[0]

    conn.close()

    return user_count_username, user_count_email

# 문진정보 db에 삽입하는 코드. 이거 함수화해서 마지막에 결과창 리턴하면서 db에 넣어야함.
# user_question_data = [('sex', '1'), ('age', '19'),
#  ('question1', '0'), ('question2', '2'),
#  ('question3', '2'), ('question4', '0'),
#  ('question5', '1'), ('question6', '2'),
#  ('question7', '2'), ('question8', '1'),
#  ('question9', '1'), ('question10', '2'),
#  ('question11', '0'), ('question12', '0'),
#  ('question13', '2'), ('question14', '2'),
#  ('question15', '2'), ('question16', '1'),
#  ('question17', '2'), ('question18', '2'),
#  ('question19', '2'), ('question20', '1'),
#  ('question21', '1'), ('question22', '1')]

# def put_question_in_db(user_question_data):

#     try:
#         # 커서 생성 (데이터의 입력과 수정을 하려면 커서 객체를 사용해야 함)
#         with db.cursor() as cursor:
#             # user_question_data에 있는 데이터를 한 줄씩 데이터베이스에 삽입
#             sql_insert_data = f'''
#             INSERT INTO user_question (
#                 sex, age, question1, question2, question3, question4,
#                 question5, question6, question7, question8, question9,
#                 question10, question11, question12, question13, question14,
#                 question15, question16, question17, question18, question19,
#                 question20, question21, question22
#             ) VALUES (
#                 %(sex)s, %(age)s, %(question1)s, %(question2)s, %(question3)s, %(question4)s,
#                 %(question5)s, %(question6)s, %(question7)s, %(question8)s, %(question9)s,
#                 %(question10)s, %(question11)s, %(question12)s, %(question13)s, %(question14)s,
#                 %(question15)s, %(question16)s, %(question17)s, %(question18)s, %(question19)s,
#                 %(question20)s, %(question21)s, %(question22)s
#             )
#             '''

    #         # 튜플 형태의 데이터를 딕셔너리로 변환
    #         dict_data = {k: v for (k, v) in user_question_data}
    #         cursor.execute(sql_insert_data, dict_data)

    #         # 커밋: 데이터베이스에 변경 사항 저장
    #         db.commit()

    # finally:
    #     # 데이터베이스 연결 종료
    #     db.close()

