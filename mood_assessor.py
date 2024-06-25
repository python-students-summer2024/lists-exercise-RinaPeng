import datetime
import os

MOODS = {
    "happy": 2,
    "relaxed": 1,
    "apathetic": 0,
    "sad": -1,
    "angry": -2
}

def get_current_date():
    return str(datetime.date.today())

def read_mood_diary():
    if not os.path.exists('data/mood_diary.txt'):
        return []
    with open('data/mood_diary.txt', 'r') as file:
        return file.readlines()

def write_mood_diary(entry):
    with open('data/mood_diary.txt', 'a') as file:
        file.write(entry + "\n")

def validate_mood(mood):
    return mood.lower() in MOODS

def get_mood_input():
    while True:
        mood = input("Enter your current mood (happy, relaxed, apathetic, sad, angry): ").strip().lower()
        if validate_mood(mood):
            return MOODS[mood]
        else:
            print("Invalid mood. Please try again.")

def already_entered_today(entries):
    today = get_current_date()
    for entry in entries:
        if entry.startswith(today):
            return True
    return False

def diagnose_mood(moods):
    last_seven_days = moods[-7:]
    mood_count = {
        "happy": 0,
        "relaxed": 0,
        "apathetic": 0,
        "sad": 0,
        "angry": 0
    }

    for mood in last_seven_days:
        for mood_str, mood_int in MOODS.items():
            if mood_int == int(mood.strip().split(",")[1]):
                mood_count[mood_str] += 1

    if mood_count["happy"] >= 5:
        return "manic"
    elif mood_count["sad"] >= 4:
        return "depressive"
    elif mood_count["apathetic"] >= 6:
        return "schizoid"

    average_mood = round(sum(int(mood.strip().split(",")[1]) for mood in last_seven_days) / 7)
    for mood_str, mood_int in MOODS.items():
        if mood_int == average_mood:
            return mood_str

def assess_mood():
    entries = read_mood_diary()
    if already_entered_today(entries):
        print("Sorry, you have already entered your mood today.")
        return

    current_date = get_current_date()
    mood = get_mood_input()
    write_mood_diary(f"{current_date},{mood}")

    if len(entries) >= 6:
        diagnosis = diagnose_mood(entries + [f"{current_date},{mood}"])
        print(f"Your diagnosis: {diagnosis}!")


