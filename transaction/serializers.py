import jdatetime
from rest_framework import serializers

from .models import Transaction, TransactionCache


class DaySerializer(serializers.ModelSerializer):
    """
    This serializer use when query group by on day of year
    """
    value = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()

    def get_value(self, obj):
        if self.context.get('type') == 'amount':
            return obj.get('totalAmount')
        return obj.get('Count')

    def get_createdAt(self, obj):
        date = jdatetime.date.fromgregorian(day=obj.get('createdAt').day, month=obj.get('createdAt').month,
                                            year=obj.get('createdAt').year)
        return str(date)

    class Meta:
        model = Transaction
        fields = ('value', 'createdAt')


class WeekSerializer(serializers.ModelSerializer):
    """
    This serializer use when query group by on week of year
    """
    value = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()

    def get_value(self, obj):
        if self.context.get('type') == 'amount':
            return obj.get('totalAmount')
        return obj.get('Count')

    def get_createdAt(self, obj):
        date = jdatetime.date.fromgregorian(day=obj.get('createdAt').day, month=obj.get('createdAt').month,
                                            year=obj.get('createdAt').year)
        return "هفته {0} سال {1}".format(date.weeknumber(), date.year)

    class Meta:
        model = Transaction
        fields = ('value', 'createdAt',)


class MonthSerializer(serializers.ModelSerializer):
    """
    This serializer use when query group by on month of year
    """
    value = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()

    def get_value(self, obj):
        if self.context.get('type') == 'amount':
            return obj.get('totalAmount')
        return obj.get('Count')

    def get_createdAt(self, obj):
        date = jdatetime.date.fromgregorian(day=obj.get('createdAt').day, month=obj.get('createdAt').month,
                                            year=obj.get('createdAt').year)
        return "{0} سال {1}".format(date.j_months_fa[date.month - 1], date.year)

    class Meta:
        model = Transaction
        fields = ('value', 'createdAt',)


class CacheSerializer(serializers.ModelSerializer):
    """
    This serializer use when use TransactionCache collection and base on type or mode change response
    """
    value = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()

    def get_value(self, obj):
        if self.context.get('type') == 'amount':
            return obj.data.get('totalAmount')
        return obj.data.get('Count')

    def get_createdAt(self, obj):
        date = jdatetime.date.fromgregorian(day=obj.data.get('createdAt').day, month=obj.data.get('createdAt').month,
                                            year=obj.data.get('createdAt').year)
        if self.context.get('mode') == 'week':
            return "هفته {0} سال {1}".format(date.weeknumber(), date.year)
        if self.context.get('mode') == 'month':
            return "{0} سال {1}".format(date.j_months_fa[date.month - 1], date.year)
        return str(date)

    class Meta:
        model = TransactionCache
        fields = ('value', 'createdAt',)
