import re
from copy import copy

with open("input.txt") as f:
    lines = f.read().strip().split("\n")

def process_card(card):
    winning, my = card
    matches = 0
    for wn in winning:
        if wn in my:
            matches += 1
    for i in range(matches):
        index = cards.index(card)
        my_cards.append(cards[index + i + 1])
    return matches

cards = []

for i, line in enumerate(lines):
    line = re.sub(r"Card \d: ", "", line)
    winning, my = line.split(" | ")
    winning = winning.split()
    my = my.split()
    cards.append((winning, my))

my_cards = copy(cards)
ans = len(my_cards)

while len(my_cards) > 0:
    card = my_cards.pop()
    ans += process_card(card)

print(ans)