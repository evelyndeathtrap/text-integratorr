from collections import defaultdict, Counter
import random

# 1. Training Text
f = open("chat.txt", "r")
text = f.read()
f.close()

# 2. Tokenization
tokens = text.split()

# 3. Build a Trigram Model (Frequency Table)
# Structure: {(word1, word2): {next_word: count}}
trigram_counts = defaultdict(Counter)

for i in range(len(tokens) - 2):
    context = (tokens[i], tokens[i+1])
    next_word = tokens[i+2]
    trigram_counts[context][next_word] += 1

# 4. Improved Prediction
def predict_next_word(current_context):
    """
    Takes a tuple of (word1, word2) and returns 
    the next word based on highest frequency.
    """
    if current_context in trigram_counts:
        # Get the most common next word
        prediction = trigram_counts[current_context].most_common(1)[0][0]
        return prediction
    else:
        # Fallback: if context not found, return a random word from the whole text
        return random.choice(tokens)

# Generate a sequence using trigrams
# Start with two words
start_context = ("the", "cat")
generated_sequence = [start_context[0], start_context[1]]

for _ in range(256):
    # Get current context (the last two words generated)
    context = (generated_sequence[-2], generated_sequence[-1])
    
    next_w = predict_next_word(context)
    generated_sequence.append(next_w)

# Join and print
print(" ".join(generated_sequence))
