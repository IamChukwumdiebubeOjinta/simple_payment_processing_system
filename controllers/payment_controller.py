from models.payment_model import PaymentRequest, PaymentResponse, PaymentData, StatusCode
from fastapi.encoders import jsonable_encoder

def make_payment_request(payment: PaymentRequest) -> dict:
    """
    Creates a payment request and returns a payment response.

    Args:
        payment (PaymentRequest): An object representing a payment request.

    Returns:
        dict: A dictionary containing the payment response object wrapped in a 'msg' key.
    """
    payment_data = PaymentData(
        amount=payment.amount,
        card_number=payment.card_number,
        expiration_date=payment.expiration_date,
        cvv=payment.cvv
    )
    
    try:
        if not luhn_algorithm(payment.card_number):
            raise ValueError

        response_data = PaymentResponse(
        message="Payment successful",
        data=payment_data,
        status_code=StatusCode.SUCCESS
        )
    except ValueError:
        response_data = PaymentResponse(
            message="Invalid card number",
            data=payment_data,
            status_code=StatusCode.ERROR
        )

    return response_data

def luhn_algorithm(card_number: str) -> bool:
    """
    Check the validity of a credit card number using the Luhn algorithm.

    Args:
        card_number (str): The credit card number to be checked for validity.

    Returns:
        bool: True if the credit card number is valid, False otherwise.
    """

    # Remove any spaces or dashes from the card number
    card_number = ''.join(filter(str.isdigit, card_number))

    # Double every second digit starting from the right
    doubled_digits = [int(card_number[i]) * 2 if i % 2 == len(card_number) % 2 else int(card_number[i]) for i in range(len(card_number))]

    # Subtract 9 from doubled digits greater than 9
    doubled_digits = [digit - 9 if digit > 9 else digit for digit in doubled_digits]

    # Calculate the sum of all digits
    total_sum = sum(doubled_digits)

    # Check if the sum is divisible by 10
    return total_sum % 10 == 0
