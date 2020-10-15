# 任务队列地址
from my_task.main import app

broker_url = 'redis://127.0.0.1:6379/6'
# 结果队列
result_backend = 'redis://127.0.0.1:6379/7'

# 定时任务调度
app.conf.beat_schedule = {
    'check_order_out_time': {
        'task': 'check_order',
        'schedule': 30.0
    },
}
