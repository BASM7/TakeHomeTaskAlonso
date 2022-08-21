def mask_card_number(card_number):
    return card_number[-4:].rjust(len(card_number), 'X')


def mask_card_cvv(card_cvv):
    return 'X' * len(card_cvv)
