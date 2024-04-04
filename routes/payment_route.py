from fastapi import APIRouter
from controllers.payment_controller import make_payment_request
from models.payment_model import PaymentRequest, PaymentResponse

router = APIRouter(prefix="/v1", tags=["payments"])


@router.post("/make_payment")
def payment_route(req: PaymentRequest):
    """
    Endpoint for making a payment with the specified request data.
    
    Parameters:
    - request: PaymentRequest object
    
    Returns:
    - PaymentResponse object
    """
    return make_payment_request(req)