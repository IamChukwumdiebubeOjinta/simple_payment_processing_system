import re
from enum import Enum
from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field, PositiveFloat, field_validator

def validate_expiration_date(date_str):
    """
    Validate the expiration date in the format MM/YY.
    
    Args:
        date_str (str): The expiration date string.
        
    Returns:
        bool: True if the date is valid and not in the past, False otherwise.
    """
    try:
        expiration_date = datetime.strptime(date_str, "%m/%y")
        if expiration_date < datetime.now():
            return False
        return True
    except ValueError:
        return False

class PaymentRequest(BaseModel):
    """
    A class representing a payment request.

    Attributes:
        amount (float): The amount of the payment.
        card_number (str): The card number used for the payment.
        expiration_date (str): The expiration date of the card.
        cvv (str): The CVV number of the card.

    Raises:
        HTTPException: If the card number is not 16 digits long.

    """
    amount: PositiveFloat = Field(description="amount")
    card_number: str = Field(pattern=r"\d{16}", min_length=16, max_length=16, description="card number")
    expiration_date: str = Field(default_factory=lambda: datetime.now().strftime('%m/%y'),pattern=r"^(0[1-9]|1[0-2])\/\d{2}$", description="exp-date")
    cvv: str = Field(pattern=r"\d{3}", min_length=3, max_length=3, description="cvv")
    
    @field_validator("card_number")
    def validate_card_number(cls, card_number: str) -> str:
        """
        Validate the card_number field by checking that it is a valid credit card number.

        Args:
            card_number (str): The card number to validate.

        Raises:
            HTTPException: If the card number is not valid.

        Returns:
            str: The valid card number.
        """
        card_prefix_regex: dict[str, str] = {
            "Mastercard": r"^5[1-5]\d{14}$",
            "Visa": r"^4\d{12}(?:\d{3})?$",
            "American Express": r"^3[47]\d{13}$",
            "Discover": r"^6(?:011|5[0-9]{2})\d{12}$",
        }

        if len(card_number) != 16:
            raise HTTPException(
                status_code=400, detail="Card number must be 16 digits long."
            )

        valid_prefix = next(
            (prefix for prefix, regex in card_prefix_regex.items() if re.match(regex, card_number)),
            None,
        )

        if valid_prefix is None:
            raise HTTPException(
                status_code=400, detail="Card number does not match any known prefix."
            )

        return card_number

    @field_validator("expiration_date")
    def validate_expiration_date(cls, expiration_date: str) -> str:
        """Validate the format of the expiration date field."""
        try:
            datetime.strptime(expiration_date, "%m/%y")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid expiration date format. It should be in the format MM/YY, not {value}",
            )
        return expiration_date



class StatusCode(Enum):
    SUCCESS = 200
    ERROR = 400
    NOT_FOUND = 404

class PaymentData(BaseModel):
    amount: PositiveFloat
    card_number: str
    expiration_date: str
    cvv: str

class PaymentResponse(BaseModel):
    message: str = Field(description="message", example="Payment successful", default="message") 
    data: Optional[PaymentData] = Field(description="data", example={"field1": "value1", "field2": 100})
    status_code: StatusCode = Field(description="status code", default=StatusCode.SUCCESS)  