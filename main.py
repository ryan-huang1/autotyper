import time
import random
import pyautogui

def type_out_paragraph(paragraph, wps=10, typo_chance=0.05, long_pause_chance=0.02, min_word_pause=0.05, max_word_pause=0.15, sentence_pause_min=0.5, sentence_pause_max=1.5):
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

    for word in words:
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

def type_out_paragraphs(paragraphs, wps=10, typo_chance=0.05, long_pause_chance=0.02, min_word_pause=0.05, max_word_pause=0.15, sentence_pause_min=0.5, sentence_pause_max=1.5):
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
    for paragraph in paragraphs:
        type_out_paragraph(paragraph, wps, typo_chance, long_pause_chance, min_word_pause, max_word_pause, sentence_pause_min, sentence_pause_max)
        time.sleep(1)  # Delay between paragraphs for readability

def main():
    # Load text from a file
    with open('textfile.txt', 'r') as file:
        content = file.read()

    # Split content into paragraphs, handling line breaks correctly
    paragraphs = content.split('\n\n')

    # Default typing settings
    wps = 85  # Words per second typing speed
    typo_chance = 0.05
    long_pause_chance = 0.02
    min_word_pause = 0.05
    max_word_pause = 0.15
    sentence_pause_min = 0.5
    sentence_pause_max = 0.8

    # Give yourself a few seconds to focus the target application window
    time.sleep(5)
    type_out_paragraphs(paragraphs, wps, typo_chance, long_pause_chance, min_word_pause, max_word_pause, sentence_pause_min, sentence_pause_max)

if __name__ == "__main__":
    main()
