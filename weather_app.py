import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from config import API_KEY

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", data["message"])
        else:
            weather = data["weather"][0]["description"].title()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            # Update text
            result_label.config(
                text=f"Weather: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%\nWind Speed: {wind} m/s"
            )

            # Get icon code and load icon
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url, stream=True)
            icon_img = Image.open(icon_response.raw)
            icon_photo = ImageTk.PhotoImage(icon_img)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo  # prevent garbage collection

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ===== GUI Setup =====
root = tk.Tk()
root.title("Weather App")
root.state('zoomed')  # Maximize window

# ===== Background Image =====
try:
    bg_image = Image.open("background.jpg")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print("Error loading background image:", e)

# ===== Fonts =====
FONT_TITLE = ("Segoe UI", 30, "bold")
FONT_INPUT = ("Segoe UI", 16)
FONT_OUTPUT = ("Segoe UI", 18)

# ===== Widgets =====
title_label = tk.Label(root, text="Weather Forecast", font=FONT_TITLE, bg="#ffffff", fg="#003366")
title_label.pack(pady=40)

city_entry = tk.Entry(root, font=FONT_INPUT, width=40, bd=3)
city_entry.pack(pady=10)

get_button = tk.Button(root, text="Get Weather", font=FONT_INPUT, bg="#3399ff", fg="white", command=get_weather)
get_button.pack(pady=20)

icon_label = tk.Label(root, bg="#ffffff")
icon_label.pack(pady=10)

result_label = tk.Label(root, text="", font=FONT_OUTPUT, bg="#ffffff", justify="left")
result_label.pack(pady=10)

root.mainloop()
