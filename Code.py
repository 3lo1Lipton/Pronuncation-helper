from builtins import Exception

import requests
from gtts import gTTS
from playsound import playsound
import os
import tkinter as tk
from tkinter import messagebox
from googletrans import Translator

translator = Translator()

def get_word_data(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        meanings = data[0]["meanings"]
        phonetic = data[0].get("phonetic", "")
        definition = meanings[0]["definitions"][0]["definition"]
        synonyms = meanings[0]["definitions"][0].get("synonyms", [])
        return {
            "word": word,
            "phonetic": phonetic,
            "definition": definition,
            "synonyms": synonyms[:5]
        }
    except Exception:
        return None

def translate_word(word):
    try:
        result = translator.translate(word, src='en', dest='ru')
        return result.text
    except:
        return "Не удалось перевести"

def speak_word(word):
    try:
        tts = gTTS(word, lang='en')
        tts.save("word.mp3")
        playsound("word.mp3")
        os.remove("word.mp3")
    except:
        messagebox.showerror("Ошибка", "Произошла ошибка при озвучивании слова.")

def search():
    word = entry.get().strip().lower()
    if not word:
        messagebox.showwarning("Пустой ввод", "Введите слово.")
        return
    data = get_word_data(word)
    if data:
        result_text.set(f"Слово: {data['word']}\n"
                        f"Фонетика: {data['phonetic']}\n"
                        f"Определение: {data['definition']}\n"
                        f"Синонимы: {', '.join(data['synonyms']) if data['synonyms'] else '—'}\n"
                        f"Перевод: {translate_word(word)}")
    else:
        result_text.set("❌ Слово не найдено.")

def speak():
    word = entry.get().strip().lower()
    if word:
        speak_word(word)

# GUI
root = tk.Tk()
root.title("📚 Умный Словарь")
root.geometry("450x300")
root.resizable(False, False)

entry = tk.Entry(root, font=("Arial", 16), width=25)
entry.pack(pady=10)

tk.Button(root, text="🔍 Найти", font=("Arial", 12), command=search).pack()
tk.Button(root, text="🔊 Озвучить", font=("Arial", 12), command=speak).pack(pady=5)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", font=("Arial", 12), wraplength=400)
result_label.pack(pady=10)

root.mainloop()
