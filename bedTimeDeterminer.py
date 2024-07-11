import random
from datetime import datetime, timedelta, timezone
import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def calculate_times():
    # Set the timezone to UTC+8
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    current_hour = now.hour
    current_minute = now.minute

    # Generate random bedtime that is before the current time
    hour = random.randint(0, current_hour)
    minute = random.randint(0, 59) if hour < current_hour else random.randint(0, current_minute)

    def bedtime(hour, minute):
        global bedtime_datetime
        bedtime_datetime = datetime(now.year, now.month, now.day, hour, minute, tzinfo=tz)
        period = "下午" if hour >= 12 else "上午"
        formatted_hour = hour if hour <= 12 else hour - 12
        return f"樂多今天{period} {formatted_hour:02}點{minute:02}分要去睡覺"

    def awake():
        global awake_datetime, day
        awake_datetime = bedtime_datetime + timedelta(hours=8, minutes=random.randint(0, 960))
        day = "隔天" if awake_datetime.day > bedtime_datetime.day else "今天"
        period = "下午" if awake_datetime.hour >= 12 else "上午"
        formatted_hour = awake_datetime.hour if awake_datetime.hour <= 12 else awake_datetime.hour - 12
        return f"樂多{day}{period} {formatted_hour:02}點{awake_datetime.minute:02}分要起床"

    def duration():
        duration = awake_datetime - bedtime_datetime
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60
        return f"樂多共睡了{hours:02}小時{minutes:02}分鐘"

    bedtime_message = bedtime(hour, minute)
    awake_message = awake()
    duration_message = duration()
    return now.strftime('%Y-%m-%d %H:%M:%S'), bedtime_message, awake_message, duration_message

def show_sleep_times():
    pygame.mixer.music.load(resource_path("ZNJSM.mp3"))
    pygame.mixer.music.play()

    current_time, bedtime_message, awake_message, duration_message = calculate_times()
    current_time_label.config(text=f"現在時間：{current_time}")
    bedtime_label.config(text=bedtime_message)
    awake_label.config(text=awake_message)
    duration_label.config(text=duration_message)

pygame.mixer.init()


# Create the main window
root = tk.Tk()
root.title("古希臘掌管睡覺的神")

# Set minimum size for the window
root.minsize(400, 400)


# Load an image using Pillow
image_path = "LD.JPG"  # Replace with your image path
image = Image.open(resource_path("LD.JPG"))
image = image.resize((262,465))  # Resize the image as needed
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = tk.Label(root, image=photo)
image_label.pack(pady=5)

# Create labels to display the information
current_time_label = tk.Label(root, text="")
current_time_label.pack(pady=5)

bedtime_label = tk.Label(root, text="")
bedtime_label.pack(pady=5)

awake_label = tk.Label(root, text="")
awake_label.pack(pady=5)

duration_label = tk.Label(root, text="")
duration_label.pack(pady=5)

# Create and place the button
btn = tk.Button(root, text="累累病又發作了，真的點點點", command=show_sleep_times)
btn.pack(pady=20)

# Keep a reference to the image to prevent it from being garbage collected
image_label.image = photo



# Start the GUI event loop
root.mainloop()
