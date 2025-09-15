from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from datetime import datetime

# Import the necessary model and function
from studentbookadminfrontend.models import SubscriptionOrder, Student
from studentbookadminfrontend.views.dashboard_views import api_response

class PaymentDetailsAPIView(APIView):
    def get(self, request):
        payments = SubscriptionOrder.objects.all().order_by('-created_at')
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        class_filter = request.query_params.get('class')
        status_filter = request.query_params.get('status')
        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                payments = payments.filter(created_at__date__range=[start_date, end_date])
            except ValueError:
                return api_response("Invalid date format. Use YYYY-MM-DD.", "error", status.HTTP_400_BAD_REQUEST)
        if class_filter:
            payments = payments.filter(course__name=class_filter)
        if status_filter:
            payments = payments.filter(payment_status=status_filter)
        total_amount_collected = payments.filter(payment_status='completed').aggregate(total_sum=Sum('price'))['total_sum'] or 0
        pending_payments_count = payments.filter(payment_status='pending').count()
        failed_payments_count = payments.filter(payment_status='failed').count()
        payment_summary = {
            "total_amount_collected": total_amount_collected,
            "pending_payments_count": pending_payments_count,
            "failed_payments_count": failed_payments_count,
        }
        payment_data_list = []
        for payment in payments:
            user = payment.student
            payment_data_list.append({
                'transaction_id': payment.transaction_id,
                # 'start_date': payment.subscription_start,
                # 'end_date': payment.subscription_end,
                'user_name': f"{user.first_name} {user.last_name}",
                'user_email': user.email,
                'class': payment.course.name,
                'status': payment.payment_status,
                'payment_mode': payment.payment_mode,
                'payment_gateway': "Not Available",
            })
        final_data = {
            "summary": payment_summary,
            "payments": payment_data_list
        }
        return api_response("Payment details fetched successfully", "success", status.HTTP_200_OK, data=final_data)