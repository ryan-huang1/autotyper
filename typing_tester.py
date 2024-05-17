import time
import threading
import json
from pynput import keyboard
from statistics import mean, variance
import sys

# Initialize global variables
start_time = None
end_time = None
typed_data = []
typing_stats = {
    "total_words": 0,
    "total_sentences": 0,
    "total_typos": 0,
    "typing_speed": [],
    "pause_after_letter": [],
    "pause_after_word": [],
    "pause_after_sentence": [],
    "keystroke_durations": [],
    "character_frequencies": {},
    "word_frequencies": {},
    "sentence_lengths": [],
    "corrections": 0
}
current_word = ""
current_sentence = ""
last_key_time = None
typos = 0
key_press_time = {}
session_duration = 60  # 2 minutes

# Function to end the typing session after 2 minutes
def end_typing_session():
    global end_time
    end_time = time.time()
    listener.stop()

# Function to calculate typing statistics
def calculate_statistics():
    global typing_stats
    if end_time is None:
        return
    typing_stats["total_words"] = len([word for word in typed_data if word.endswith(' ')])
    typing_stats["total_sentences"] = len([sentence for sentence in typed_data if sentence.endswith(('.', '!', '?'))])
    typing_stats["total_typos"] = typos

    # Calculate typing speed (words per minute)
    total_time = (end_time - start_time) / 60 if start_time else 1
    if total_time > 0:
        wpm = typing_stats["total_words"] / total_time
        typing_stats["typing_speed"].append(wpm)

    # Calculate average and variance of pauses
    if typing_stats["pause_after_letter"]:
        typing_stats["avg_pause_after_letter"] = mean(typing_stats["pause_after_letter"])
        typing_stats["var_pause_after_letter"] = variance(typing_stats["pause_after_letter"])
    if typing_stats["pause_after_word"]:
        typing_stats["avg_pause_after_word"] = mean(typing_stats["pause_after_word"])
        typing_stats["var_pause_after_word"] = variance(typing_stats["pause_after_word"])
    if typing_stats["pause_after_sentence"]:
        typing_stats["avg_pause_after_sentence"] = mean(typing_stats["pause_after_sentence"])
        typing_stats["var_pause_after_sentence"] = variance(typing_stats["pause_after_sentence"])

    # Calculate average and variance of keystroke durations
    if typing_stats["keystroke_durations"]:
        typing_stats["avg_keystroke_duration"] = mean(typing_stats["keystroke_durations"])
        typing_stats["var_keystroke_duration"] = variance(typing_stats["keystroke_durations"])

    # Save statistics to a JSON file
    with open('typing_statistics.json', 'w') as json_file:
        json.dump(typing_stats, json_file, indent=4)

    print("\nTyping Statistics saved to typing_statistics.json")
    print_statistics()

# Function to print the typing statistics
def print_statistics():
    print("Typing Statistics:")
    for stat, value in typing_stats.items():
        if isinstance(value, list):
            print(f"{stat}: {value[:5]}... (and more)")  # Print first 5 values for brevity
        else:
            print(f"{stat}: {value}")

# Function to handle key press events
def on_press(key):
    global start_time, last_key_time, current_word, current_sentence, typos, key_press_time

    if start_time is None:
        start_time = time.time()

    current_time = time.time()

    # Calculate pauses
    if last_key_time is not None:
        pause_duration = current_time - last_key_time
        typing_stats["pause_after_letter"].append(pause_duration)
    
    last_key_time = current_time

    # Record the key press time
    key_press_time[key] = current_time

    try:
        char = key.char
    except AttributeError:
        char = str(key)

    if char == 'Key.space':
        typed_data.append(current_word + ' ')
        typing_stats["pause_after_word"].append(pause_duration)
        typing_stats["word_frequencies"][current_word] = typing_stats["word_frequencies"].get(current_word, 0) + 1
        current_word = ""
    elif char in ('.', '!', '?'):
        typed_data.append(current_sentence + char)
        typing_stats["pause_after_sentence"].append(pause_duration)
        typing_stats["sentence_lengths"].append(len(current_sentence + char))
        current_sentence = ""
    elif char == 'Key.backspace':
        typos += 1
        typing_stats["corrections"] += 1
        if current_word:
            current_word = current_word[:-1]
        if current_sentence:
            current_sentence = current_sentence[:-1]
    else:
        current_word += char
        current_sentence += char
        typing_stats["character_frequencies"][char] = typing_stats["character_frequencies"].get(char, 0) + 1

# Function to handle key release events
def on_release(key):
    global key_press_time
    current_time = time.time()
    if key in key_press_time:
        press_duration = current_time - key_press_time[key]
        typing_stats["keystroke_durations"].append(press_duration)
        del key_press_time[key]
    if key == keyboard.Key.esc:
        return False

# Main function to start the typing test
def start_typing_test():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    timer = threading.Timer(session_duration, end_typing_session)
    timer.start()
    listener.join()
    calculate_statistics()

# Start the typing test
if __name__ == "__main__":
    start_typing_test()
