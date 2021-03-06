import datetime
import json

import requests

def get_time(time):
    std = ["{:04d}".format(i) for i in range(220, 2321, 300)] # len(std) : 8
    # std = ["0220", "0520", "0820", "1120", "1420", "1720", "2020", "2320"]
    data = time.strftime("%H%M")

    for i in range(len(std)):
        if std[i] <= data < std[i + 1]:
            temp = "{:04d}".format(int(std[i]) - 20)
            return time.replace(hour = int(temp[:2]), minute = int(temp[2:]))
    else:
        temp = "{:04d}".format(int(std[-1]) - 20)
        return time.replace(hour = int(temp[:2]), minute = int(temp[2:])) - datetime.timedelta(days = 1)

def get_weather_info(key: str, base_time: datetime.datetime = None) -> dict:
    """기상청 API로부터 날씨 정보를 받아온다.
    현재 시각의 날씨가 아닌 3시간 이내의 날씨 정보이다.

    매개 변수
    ----------
    key: str
        기상청 API 인증키
    base_time: datetime.datetime
        날씨 조회를 원하는 datetime 객체
    
    리턴
    -------
    dict
        기상청 API로부터 받아온 코드값 : 값 으로 구성 되어있음
    """
    base_url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?"
    if base_time:
        today = base_time
    else:
        today = datetime.datetime.today()
    
    url_args = {
        "ServiceKey" : key,
        "base_date" : today.strftime("%Y%m%d"),
        "base_time" : get_time(today).strftime("%H%M"),
        "nx" : "57",
        "ny" : "74",
        "_type" : "json"
    }

    for k, v in url_args.items():
        base_url += (k + "=" + v + "&")

    try:
        result = json.loads(requests.get(base_url).text)["response"]["body"]["items"]["item"]
        ret = {i["category"] : i["fcstValue"] for i in result}
        ret["fcstTime"] = result[0]["fcstTime"]
        return ret
    except:
        return dict()

def save_json(data: dict) -> bool:
    """딕셔너리 데이터를 파일로 저장한다.

    매개 변수
    ----------
    data: dict
        저장하고 싶은 딕셔너리 데이터

    리턴
    -------
    bool
        데이터 저장에 성공했다면 True, 실패했다면 False
    """
    try:
        with open("response.json", "w") as f:
            json.dump(data, f, indent = 4)
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    pass
