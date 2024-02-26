import re

def detect_words_in_text(word_list, text):
    # Change text and words to low mode
    words = [word.lower() for word in word_list]
    text = text.lower()

    # Make pattern By using the words
    pattern = re.compile(rf'\b(?:{"|".join(map(re.escape, words))})\b')

    # Search in text
    matches = re.findall(pattern, text)

    return matches