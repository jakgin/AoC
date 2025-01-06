from collections import defaultdict
from functools import cmp_to_key

with open("in") as f:
    lines = f.read().strip().split("\n")
    players = []
    for line in lines:
        hand, bid = line.split()
        players.append((hand, int(bid)))


def score_hand(hand: str) -> int:
    if hand[0] == hand[1] == hand[2] == hand[3] == hand[4]:
        return 6
    cards = defaultdict(int)
    for card in hand:
        cards[card] += 1
    if 4 in cards.values():
        return 5
    if 3 in cards.values() and 2 in cards.values():
        return 4
    if 3 in cards.values():
        return 3
    if list(cards.values()).count(2) == 2:
        return 2
    if 2 in cards.values():
        return 1
    return 0

def sort_players(player1, player2):
    strengths = "23456789TJQKA"

    p1_score = score_hand(player1[0])
    p2_score = score_hand(player2[0])
    if p1_score > p2_score:
        return 1
    elif p2_score > p1_score:
        return -1

    for p1_card, p2_card in zip(player1[0], player2[0]):
        p1_strength = strengths.find(p1_card)
        p2_strength = strengths.find(p2_card)
        if p1_strength > p2_strength:
            return 1
        if p2_strength > p1_strength:
            return -1
        
    # If draw
    return 0

players.sort(key=cmp_to_key(sort_players))
ans = 0
for i, player in enumerate(players):
    ans += (i + 1) * player[1]

print(ans)
