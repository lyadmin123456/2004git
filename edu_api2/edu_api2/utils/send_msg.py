import requests


class Message(object):

    def __init__(self, api_key):
        # 账号的唯一标识
        self.api_key = api_key
        # 单条发送短息的接口
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_message(self, phone, code):
        params = {
            "apikey": self.api_key,
            "mobile": phone,
            "text": "【刘洋test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        # 将包含参数的请求发送出去
        res = requests.post(self.single_send_url, data=params)
        print(res)


if __name__ == '__main__':
    message = Message("ab0346f606ab7883bd7285cd5ed197c0")
    message.send_message("18237068250", "123456")

