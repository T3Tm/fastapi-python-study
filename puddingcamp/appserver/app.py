from fastapi import FastAPI

app = FastAPI()
'''
약속 잡기 서비스 기능 기획
'''

'''
명세
호스트 : 약속 일정을 열어 약속 신청을 받는 주최 사용자
게스트 : 호스트가 열어 놓은 시간대로 약속 신청을 하는 손님
타임슬롯 : 호스트가 약속 신청을 받을 시간대
부킹 : 타임슬롯 단위로 호스트와 게스트가 맺은 약속
캘린더 : 달력
'''
@app.get("/")
def hello_world() -> dict:
    return {"message" : "Hello_world"}