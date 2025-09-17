# studentbookadminfrontend/views/calculator_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Ensure you have this api_response function available.
# It can be in a separate utils file or in the same views file.
def api_response(message, message_type, status_code, data=None):
    return Response(
        {
            "message": message,
            "message_type": message_type,
            "status_code": status_code,
            "data": data,
        },
        status=status_code,
    )

class PriceCalculatorAPIView(APIView):
    def post(self, request, format=None):
        try:
            original_price = float(request.data.get('original_price'))
            discount_percentage = float(request.data.get('discount_percentage'))
            
            
            # Simple validation to check for valid numbers
            if original_price is None or discount_percentage is None or original_price < 0 or discount_percentage < 0:
                return api_response(
                    "Invalid input. Please provide valid original price and discount percentage.",
                    "error",
                    status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate the final price
            discount_amount = original_price * (discount_percentage / 100)
            final_price = original_price - discount_amount

            # Return the result
            return api_response(
                message="Final price calculated successfully.",
                message_type="success",
                status_code=status.HTTP_200_OK,
                data={
                    "final_price": final_price
                }
            )
        
        except (ValueError, TypeError):
            return api_response(
                message="ValueError or TypeError",
                message_type="Error",
                status_code=status.HTTP_400_BAD_REQUEST,
                # "Invalid data types. Original price and discount must be numbers.",
                # "error",
                # status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return api_response(
                message="An Error Occurred.",
                message_type="Error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                # f"An error occurred: {str(e)}",
                # "error",
                # status.HTTP_500_INTERNAL_SERVER_ERROR
            )