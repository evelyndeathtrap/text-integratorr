  GNU nano 7.2                                          p.py *                                                 
import random
from collections import defaultdict, Counter
import time
# 1. Configuration
CONTEXT_SIZE = 500  # Higher = more coherent, but requires more training text
PREDICTIONS = 150

# 2. Load and Tokenize
try:
    with open("chat.txt", "r") as f:
        tokens = f.read().split()
except FileNotFoundError:
    tokens = "the quick brown fox jumps over the lazy dog".split()

# 3. Build Multi-level Model (Backoff)
# We store counts for all context sizes from 1 up to CONTEXT_SIZE
models = [defaultdict(Counter) for _ in range(CONTEXT_SIZE + 1)]

for i in range(len(tokens)):
    for n in range(1, CONTEXT_SIZE + 1):
        if i + n < len(tokens):
            context = tuple(tokens[i:i+n])
            next_token = tokens[i+n]
            models[n][context][next_token] += 1

def predict_with_backoff(current_sequence):
    # Try the longest context first, then shrink if not found
    for n in range(CONTEXT_SIZE, 0, -1):
        context = tuple(current_sequence[-n:])
        if context in models[n]:
            choices = models[n][context]
            return random.choices(list(choices.keys()), weights=list(choices.values()))[0]
    
    # Absolute fallback: random word from the whole corpus
    return random.choice(tokens)

# 4. Generate Long Context String
# Start with the first CONTEXT_SIZE words
output = tokens[:CONTEXT_SIZE]

while True:
    next_word = predict_with_backoff(output)
    print(next_word, end=" ", flush=True)
    time.sleep(1)
