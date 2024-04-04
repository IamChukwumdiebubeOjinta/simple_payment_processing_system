

def test_valid_payment_request(self):
    # Arrange
    amount = 100
    card_number = "1234567890123456"
    expiration_date = "12/23"
    cvv = "123"

    # Act
    payment_request = PaymentRequest(amount=amount, card_number=card_number, expiration_date=expiration_date, cvv=cvv)

    # Assert
    assert payment_request.amount == amount
    assert payment_request.card_number == card_number
    assert payment_request.expiration_date == expiration_date
    assert payment_request.cvv == cvv