from plyer import gyroscope
import time
import json
import openai
from plyer import notification

class StepCounter:
    def __init__(self):
        self.steps = 0
        self.last_reading = None

    def start(self):
        gyroscope.enable()
        while True:
            current_reading = gyroscope.rotation
            if self.last_reading is not None:
                # این قسمت را می‌توانید برای حساسیت گام‌ها تنظیم کنید
                if abs(current_reading[0] - self.last_reading[0]) > 0.1:
                    self.steps += 1
                    print(f'Steps: {self.steps}')
            self.last_reading = current_reading
            time.sleep(1)

step_counter = StepCounter()
step_counter.start()

class CalorieTracker:
    def __init__(self):
        self.meals = {
            "breakfast": [],
            "lunch": [],
            "snack": [],
            "dinner": []
        }
        # دیتابیس غذاها به صورت JSON
        with open('food_database.json', 'r') as f:
            self.food_db = json.load(f)

    def add_food(self, meal_type, food_item):
        if food_item in self.food_db:
            self.meals[meal_type].append(self.food_db[food_item])
        else:
            print(f'{food_item} not found in the database.')

    def calculate_calories(self):
        total_calories = 0
        for meal in self.meals.values():
            total_calories += sum(meal)
        return total_calories

calorie_tracker = CalorieTracker()
calorie_tracker.add_food("breakfast", "egg")
calorie_tracker.add_food("lunch", "chicken breast")
print(f'Total Calories: {calorie_tracker.calculate_calories()}')

# کلید API را از سایت OpenAI دریافت کنید
openai.api_key = 'sk-proj-8fFYEh7iApCj03p9wZZJT3BlbkFJcC9dA6KDBRB0NRJtSBcJ'

def send_data_to_chatgpt(steps, calories):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"User walked {steps} steps and consumed {calories} calories today. Please provide a health analysis.",
        max_tokens=150
    )
    return response.choices[0].text

steps = 5000
calories = 1500
analysis = send_data_to_chatgpt(steps, calories)
print(f'Health Analysis: {analysis}')

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Health Tracker",
        timeout=10
    )

send_notification("Daily Health Summary", analysis)