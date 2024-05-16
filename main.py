import time
import random
import pyautogui

def type_out_paragraph(paragraph, wps=3, typo_chance=0.05, long_pause_chance=0.02):
    """
    Types out a given paragraph with natural typing delays, typos, and corrections.

    :param paragraph: The paragraph to type out.
    :param wps: Words per second typing speed.
    :param typo_chance: Probability of making a typo.
    :param long_pause_chance: Probability of a longer thinking pause.
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
                time.sleep(random.uniform(0.5, 1.0) * word_delay)  # Longer pause at the end of sentences
            elif char in ",;":
                time.sleep(random.uniform(0.3, 0.5) * word_delay)  # Medium pause for commas and semicolons
            else:
                time.sleep(word_delay / len(word))
        
        pyautogui.typewrite(' ')  # Add space after each word
        time.sleep(word_delay)  # Delay between words

    print()  # Move to the next line after the paragraph is typed out.

def type_out_paragraphs(paragraphs, wps=3, typo_chance=0.05, long_pause_chance=0.02):
    """
    Types out a list of paragraphs with natural typing delays, typos, and corrections.

    :param paragraphs: A list of paragraphs to type out.
    :param wps: Words per second typing speed.
    :param typo_chance: Probability of making a typo.
    :param long_pause_chance: Probability of a longer thinking pause.
    """
    for paragraph in paragraphs:
        type_out_paragraph(paragraph, wps, typo_chance, long_pause_chance)
        time.sleep(1)  # Delay between paragraphs for readability.

def main():
    # Example usage
    paragraphs = [
        "Once upon a time in a land far, far away, there lived a wise old owl.\n\n",
        "The owl was known throughout the kingdom for its knowledge and wisdom.\n\n",
        "People from all over would come to seek the owl's advice on various matters.\n\n"
    ]

    # Default typing settings
    wps = 60  # Words per second typing speed
    typo_chance = 0.05
    long_pause_chance = 0.02

    # Give yourself a few seconds to focus the target application window
    time.sleep(5)
    type_out_paragraphs(paragraphs, wps, typo_chance, long_pause_chance)

if __name__ == "__main__":
    main()
