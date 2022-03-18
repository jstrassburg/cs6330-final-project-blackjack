import Cards


deck = Cards.Deck()
print(f"Deck count: {deck.count()}")

while deck.count() > 0:
    card = deck.draw()
    print(f"Drew the {card.face} of {card.suit} with values: {card.face_values()}")

deck.reset_and_shuffle()
print(f"Deck count: {deck.count()}")