from rest_framework import generics, status
from rest_framework.response import Response

from .helper import custom_query
from .models import Transaction, TransactionCache
from .pagination import CustomPagination
from .serializers import DaySerializer, WeekSerializer, MonthSerializer, CacheSerializer


class TransactionView(generics.ListAPIView):
    """
    This Api is for view transactions and have mandatory params (type,mode)
    and base on them use different query and serializer
    if user input merchantId , query will filter on it if not default query
    contain all users data
    """
    queryset = Transaction.objects.all()
    serializer_class = DaySerializer

    def list(self, request, *args, **kwargs):
        if not (self.request.query_params.get('type') and self.request.query_params.get('mode')):
            return Response({'Error': 'type/mode query params is mandatory'}, status=status.HTTP_404_NOT_FOUND)
        type = self.request.query_params.get('type')
        mode = self.request.query_params.get('mode')
        merchantId = self.request.query_params.get('merchantId')
        if mode == 'week':
            query = custom_query(mode, merchantId)
            serial = WeekSerializer(query, many=True, context={'type': type})
            return Response(serial.data, status=status.HTTP_200_OK)
        elif mode == 'month':
            query = custom_query(mode, merchantId)
            serial = MonthSerializer(query, many=True, context={'type': type})
            return Response(serial.data, status=status.HTTP_200_OK)
        elif mode == 'day':
            query = custom_query(mode, merchantId)
            serial = DaySerializer(query, many=True, context={'type': type})
            return Response(serial.data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'mode value is incorrect'}, status=status.HTTP_404_NOT_FOUND)


class CacheView(generics.ListAPIView):
    """
    This API is for use cache data after calculations and behavior like TransactionView API
    Use other collection (TransactionCache)
    """
    queryset = TransactionCache.objects.all()
    serializer_class = CacheSerializer

    def get_queryset(self):
        merchantId = self.request.query_params.get('merchantId')
        mode = self.request.query_params.get('mode')
        query = self.queryset.filter(mode=mode, type='All')
        if merchantId:
            query = self.queryset.filter(mode=mode, merchantId=merchantId)
        return query

    def list(self, request, *args, **kwargs):
        if not (self.request.query_params.get('type') and self.request.query_params.get('mode')):
            return Response({'Error': 'type/mode query params is mandatory'}, status=status.HTTP_404_NOT_FOUND)
        type = self.request.query_params.get('type')
        mode = self.request.query_params.get('mode')
        paginator = CustomPagination()
        context = paginator.paginate_queryset(self.get_queryset(), request)
        serial = CacheSerializer(context, many=True, context={'type': type, 'mode': mode})
        return paginator.get_paginated_response(serial.data)
