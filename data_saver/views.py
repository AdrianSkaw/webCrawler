
from django.http import HttpResponse
from rest_framework.views import APIView
from data_saver.tasks import save_product_to_db


class DataManager(APIView):

    def post(self, request):
        for product in request.data:
            save_product_to_db.delay(product)
        return HttpResponse("hallo")
