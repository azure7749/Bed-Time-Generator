import random
from datetime import datetime, timedelta, timezone

def sleep():
    # Set the timezone to UTC+8
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    current_hour = now.hour
    current_minute = now.minute

    # Print current time
    print(f"現在時間：{now.strftime('%Y-%m-%d %H:%M:%S')}")

    # Generate random bedtime that is before the current time
    hour = random.randint(0, current_hour)
    minute = random.randint(0, 59) if hour < current_hour else random.randint(0, current_minute)

    def bedtime(hour, minute):
        global bedtime_datetime
        bedtime_datetime = datetime(now.year, now.month, now.day, hour, minute, tzinfo=tz)
        period = "下午" if hour >= 12 else "上午"
        formatted_hour = hour if hour <= 12 else hour - 12
        print(f"樂多今天{period} {formatted_hour:02}點{minute:02}分要去睡覺")

    def awake():
        global awake_datetime, day
        awake_datetime = bedtime_datetime + timedelta(hours=8, minutes=random.randint(0, 960))
        day = "隔天" if awake_datetime.day > bedtime_datetime.day else "今天"
        period = "下午" if awake_datetime.hour >= 12 else "上午"
        formatted_hour = awake_datetime.hour if awake_datetime.hour <= 12 else awake_datetime.hour - 12
        print(f"樂多{day}{period} {formatted_hour:02}點{awake_datetime.minute:02}分要起床")

    def duration():
        duration = awake_datetime - bedtime_datetime
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60
        print(f"樂多共睡了{hours:02}小時{minutes:02}分鐘")

    bedtime(hour, minute)
    awake()
    duration()

sleep()
