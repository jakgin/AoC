from itertools import combinations_with_replacement
from collections import defaultdict
from functools import cmp_to_key

with open("in") as f:
    lines = f.read().strip().split("\n")
    players = []
    for line in lines:
        hand, bid = line.split()
        players.append((hand, int(bid)))

strengths = "J23456789TQKA"


def score_hand(hand: list[str]) -> int:
    cards = defaultdict(int)
    for card in hand:
        cards[card] += 1

    if hand[0] == hand[1] == hand[2] == hand[3] == hand[4]:
        return 6
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


def score_player(hand: str) -> int:
    non_jokers = set()
    for card in hand:
        if card != "J":
            non_jokers.add(card)

    jokers_comb = combinations_with_replacement(non_jokers, r=hand.count("J"))
    max_score = -1
    hand: list[str] = [ch for ch in hand]
    
    for comb in jokers_comb:
        new_hand = [val for val in hand]
        for val in comb:
            new_hand[new_hand.index("J")] = val
        max_score = max(max_score, score_hand(new_hand))
    if max_score == -1:
        return 6
        
    return max_score


def sort_players(player1, player2):
    p1_score = score_player(player1[0])
    p2_score = score_player(player2[0])
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


print(players)
print(ans)
