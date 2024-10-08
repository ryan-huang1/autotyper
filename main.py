import time
import random
import pyautogui
import json
from tqdm import tqdm

def load_typing_statistics(file_path):
    with open(file_path, 'r') as file:
        stats = json.load(file)
    return stats

def type_out_paragraph(paragraph, wps, typo_chance, long_pause_chance, min_word_pause, max_word_pause, sentence_pause_min, sentence_pause_max):
    """
    Types out a given paragraph with natural typing delays, typos, and corrections.

    :param paragraph: The paragraph to type out.
    :param wps: Words per second typing speed.
    :param typo_chance: Probability of making a typo.
    :param long_pause_chance: Probability of a longer thinking pause.
    :param min_word_pause: Minimum pause between words.
    :param max_word_pause: Maximum pause between words.
    :param sentence_pause_min: Minimum pause after a sentence.
    :param sentence_pause_max: Maximum pause after a sentence.
    """
    words = paragraph.split()
    word_delay = 1 / wps

    for word in tqdm(words, desc="Typing words", leave=False):
        for char in word:
            # Introduce thinking pauses
            if random.random() < long_pause_chance and char not in ".!?":
                time.sleep(random.uniform(0.5 * word_delay, 2 * word_delay))
            
            # Introduce a typo with a certain probability
            if random.random() < typo_chance and char.isalpha():
                typo_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                pyautogui.typewrite(typo_char)
                time.sleep(word_delay / len(word))
                pyautogui.press('backspace')
                pyautogui.typewrite(char)
            else:
                pyautogui.typewrite(char)
            
            # Add different delays based on the character
            if char in ".!?":
                time.sleep(random.uniform(sentence_pause_min, sentence_pause_max))  # Longer pause at the end of sentences
            elif char in ",;":
                time.sleep(random.uniform(0.3, 0.5) * word_delay)  # Medium pause for commas and semicolons
            else:
                time.sleep(word_delay / len(word))
        
        pyautogui.typewrite(' ')  # Add space after each word
        time.sleep(random.uniform(min_word_pause, max_word_pause))  # Random pause between words

    pyautogui.typewrite('\n\n')  # Add two newlines at the end of each paragraph for an empty line between paragraphs

def type_out_paragraphs(paragraphs, wps, typo_chance, long_pause_chance, min_word_pause, max_word_pause, sentence_pause_min, sentence_pause_max):
    """
    Types out a list of paragraphs with natural typing delays, typos, and corrections.

    :param paragraphs: A list of paragraphs to type out.
    :param wps: Words per second typing speed.
    :param typo_chance: Probability of making a typo.
    :param long_pause_chance: Probability of a longer thinking pause.
    :param min_word_pause: Minimum pause between words.
    :param max_word_pause: Maximum pause between words.
    :param sentence_pause_min: Minimum pause after a sentence.
    :param sentence_pause_max: Maximum pause after a sentence.
    """
    for paragraph in tqdm(paragraphs, desc="Typing paragraphs"):
        type_out_paragraph(paragraph, wps, typo_chance, long_pause_chance, min_word_pause, max_word_pause, sentence_pause_min, sentence_pause_max)
        time.sleep(1)  # Delay between paragraphs for readability

def main():
    # Load text from a file
    with open('textfile.txt', 'r') as file:
        content = file.read()

    # Split content into paragraphs, handling line breaks correctly
    paragraphs = content.split('\n\n')

    # Load typing statistics from JSON file
    stats = load_typing_statistics('typing_statistics.json')

    # Extracting realistic typing settings from the stats
    wps = stats['typing_speed'][0] if stats['typing_speed'] else 85  # Words per minute typing speed
    typo_chance = stats['total_typos'] / (stats['total_words'] * 5) if stats['total_words'] else 0.05
    long_pause_chance = 0.02  # You can derive this from the pause statistics if desired
    min_word_pause = min(stats['pause_after_word']) if stats['pause_after_word'] else 0.05
    max_word_pause = max(stats['pause_after_word']) if stats['pause_after_word'] else 0.15
    sentence_pause_min = min(stats['pause_after_sentence']) if stats['pause_after_sentence'] else 0.5
    sentence_pause_max = max(stats['pause_after_sentence']) if stats['pause_after_sentence'] else 1.5

    # Give yourself a few seconds to focus the target application window
    time.sleep(5)
    type_out_paragraphs(paragraphs, wps, typo_chance, long_pause_chance, min_word_pause, max_word_pause, sentence_pause_min, sentence_pause_max)

if __name__ == "__main__":
    main()
