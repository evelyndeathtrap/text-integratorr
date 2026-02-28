from collections import defaultdict, Counter
import random

# 1. Training Text
try:
    with open("chat.txt", "r") as f:
        text = f.read()
except FileNotFoundError:
    print("Please create 'chat.txt' first.")
    exit()

# 2. Tokenization
tokens = text.split()

# 3. Build the Bigram Model
bigram_counts = defaultdict(Counter)
for i in range(len(tokens) - 1):
    bigram_counts[tokens[i]][tokens[i+1]] += 1

# 4. Improved Prediction: Probabilistic Sampling
def predict_next_word(current_word):
    if current_word in bigram_counts:
        choices = bigram_counts[current_word]
        # Instead of most_common(1), we pick based on frequency weights
        words = list(choices.keys())
        weights = list(choices.values())
        return random.choices(words, weights=weights)[0]
    else:
        # Fallback to random word if dead end
        return random.choice(tokens)

# Generate a sequence
current = "the"
generated_sequence = [current]
print(f"Sequence: {current}", end=" ")

for _ in range(256):
    next_w = predict_next_word(current)
    print(f"-> {next_w}", end=" ")
    generated_sequence.append(next_w)
    current = next_w

print("\n")
