from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from studentbookadminfrontend.views.dashboard_views import api_response
from studentbookadminfrontend.serializers.content_management_serializer import *
from studentbookadminfrontend.models import *
from studentbookadminfrontend.views.content_management_views import api_response





class ClassWIthSubjectsView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        classes = Class.objects.all().order_by('id')
        data = []
        for cls in classes:
            subjects = Subject.objects.filter(course=cls.id).order_by('id')
            subject_data = []
            for subject in subjects:
                subject_data.append({
                    'subject_id': subject.id,
                    'subject_name': subject.name,
                    # 'subject_image': subject.image.url if subject.image else None
                })
            # subject_serializer = SubjectSerializer(subjects, many=True)
 
            class_data = {
                'class_id': cls.id,
                'class_name': cls.name,
                'subjects': subject_data
            }
            data.append(class_data)
       
        return api_response(
            message="Classes with subjects fetched successfully",
            message_type="success",
            status_code=status.HTTP_200_OK,
            data=data
        )
 

# class PriceCalculatorAPIView(APIView):
#     def post(self, request, format=None):
#         try:
#             original_price = float(request.data.get('original_price'))
#             discount_percentage = float(request.data.get('discount_percentage'))
            
            
#             # Simple validation to check for valid numbers
#             if original_price is None or discount_percentage is None or original_price < 0 or discount_percentage < 0:
#                 return api_response(
#                     "Invalid input. Please provide valid original price and discount percentage.",
#                     "error",
#                     status.HTTP_400_BAD_REQUEST
#                 )
            
#             # Calculate the final price
#             discount_amount = original_price * (discount_percentage / 100)
#             final_price = original_price - discount_amount

#             # Return the result
#             return api_response(
#                 message="Final price calculated successfully.",
#                 message_type="success",
#                 status_code=status.HTTP_200_OK,
#                 data={
#                     "final_price": final_price
#                 }
#             )
        
#         except (ValueError, TypeError):
#             return api_response(
#                 message="ValueError or TypeError",
#                 message_type="Error",
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 # "Invalid data types. Original price and discount must be numbers.",
#                 # "error",
#                 # status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             return api_response(
#                 message="An Error Occurred.",
#                 message_type="Error",
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 # f"An error occurred: {str(e)}",
#                 # "error",
#                 # status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
        


# class PriceCalculatorGETAPIView(APIView):
#     def get(self, request):
#         try:
#             # Get data from URL query parameters
#             original_price = float(request.query_params.get('original_price'))
#             discount_percentage = float(request.query_params.get('discount_percentage'))
            
#             # Simple validation
#             if original_price is None or discount_percentage is None:
#                 return api_response(
#                     "Both original_price and discount_percentage are required.",
#                     "error",
#                     status.HTTP_400_BAD_REQUEST
#                 )
            
#             # Calculate the final price
#             discount_amount = original_price * (discount_percentage / 100)
#             final_price = original_price - discount_amount

#             # Return the result
#             return api_response(
#                 message="Final price calculated successfully.",
#                 message_type="success",
#                 status_code=status.HTTP_200_OK,
#                 data={"final_price": final_price}
#             )
        
#         except (ValueError, TypeError):
#             return api_response(
#                 "Invalid data types. Please provide numbers.",
#                 "error",
#                 status.HTTP_400_BAD_REQUEST
#             )



class PriceCalculatorAPIView(APIView):
    
    # --- GET Method: To retrieve all past calculations ---
    def get(self, request, *args, **kwargs):
        try:
            # Fetch all records, ordered by creation date
            records = Class.objects.all().order_by('id')
            
            data = [
                {
                    # "id": record.id,
                    'class':record.name,
                    "base_price": float(record.amount),
                    "discount_percentage": float(record.discount_percentage),
                    "final_price": float(record.final_price),
                    "created_date": record.created_at,
                    "updated_date": record.updated_at,
                }
                for record in records
            ]
            
            return api_response(
                message="Class Price List fetched sucessfully",
                message_type="success",
                status_code=status.HTTP_200_OK,
                data={"calculations": data}
            )
        except Exception as e:
            return api_response(
                message=f"Error fetching class prices: {str(e)}",
                message_type="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    # --- POST Method: To perform and save a calculation ---
    def post(self, request, format=None):
        try:
            # 1. Get and convert data
            original_price = float(request.data.get('original_price'))
            discount_percentage = float(request.data.get('discount_percentage'))
            class_id = request.data.get('class_id') # Add a class_id to uniquely identify the record
            
            # Simple validation
            if not all([original_price, discount_percentage, class_id]):
                return api_response(
                    "Invalid input. Please provide original price, discount percentage, and class ID.",
                    "error",
                    status.HTTP_400_BAD_REQUEST
                )
            
            
            # 2. Calculate the final price
            discount_amount = original_price * (discount_percentage / 100)
            final_price = original_price - discount_amount

            record = Class.objects.get(id =class_id)
            record.amount = original_price
            record.discount_percentage = discount_percentage
            record.final_price = final_price
            record.created_at = timezone.now() if record.created_at is None else record.created_at
            record.updated_at = timezone.now()
            record.save()



            # 4. Return the result including the dates
            return api_response(
                message="Price updated successfully",
                message_type="success",
                status_code=status.HTTP_200_OK,
                data={
                    "id": record.id,
                    "final_price": float(record.final_price),
                    "original_price": float(record.amount),
                    "discount_percentage": float(record.discount_percentage),
                    "created_date": record.created_at,
                    "updated_date": record.updated_at,
                }
            )
        
        except (ValueError, TypeError):
            return api_response(
                message="Invalid data types. Original price, discount, and class ID must be numbers.",
                message_type="error",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return api_response(
                message=f"An error occurred: {str(e)}",
                message_type="error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        




