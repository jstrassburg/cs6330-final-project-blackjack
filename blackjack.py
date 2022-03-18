import Cards


deck = Cards.Deck()
print(f"Deck count: {deck.count()}")

while deck.count() > 0:
    card = deck.draw()
    print(f"Drew the {card.face} of {card.suit} with values: {card.face_values()}")

deck.reset_and_shuffle()
print(f"Deck count: {deck.count()}")

next_card = deck.peek()
print(f"Peeked at next card which is the {card.face} of {card.suit}")

drawn_card = deck.draw()
print(f"Drew {card.face} of {card.suit}")
