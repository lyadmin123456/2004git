from edu_api2.utils.send_msg import Message
from edu_api2.settings import constanst
from my_task.main import app


@app.task(name="send_sms")
def send_sms(mobile, code):
    print("这是发送短信的方法")
    message = Message(constanst.API_KEY)
    status = message.send_message(mobile, code)

    if not status:
        print("用户发送短信失败，手机号为：%s" % mobile)

    return "hello"
