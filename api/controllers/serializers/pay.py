# coding=utf-8
from rest_framework import serializers

from api.models.pay import Pay
from api.models.task_filled import TaskFilled
from agent import AgentSerializer


class PaySerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели Pay для получения связанных с ней 
    данных
    '''
    promos = serializers.CharField(source='agent.group.promos.title')
    request_dt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    agent = serializers.CharField(source='agent.name')

    class Meta:
        model = Pay
        fields = ('id', 'agent', 'request_dt', 'promos')


class PayDetailWebSerializer(PaySerializer):
    tasks = serializers.SerializerMethodField()
    last_pay = serializers.SerializerMethodField()
    description = serializers.CharField(source='agent.group.promos.description')
    agent = AgentSerializer()

    class Meta:
        model = Pay
        fields = ('id', 'agent', 'request_dt', 'promos', 'description', 'last_pay', 'tasks')


    def get_tasks(self, obj):
        data = []
        tasks_f = TaskFilled.objects.filter(status=3, 
                                            executer=obj.agent).order_by('-check_dt')
        for task_f in tasks_f:
            data.append({
                'task': task_f.task_address.task.title,
                'check_dt': task_f.check_dt.strftime("%Y-%m-%d %H:%M:%S"),
                'price': task_f.task_address.task.price
            })
        return data


    def get_last_pay(self, obj):
        try:
            pay = Pay.objects.filter(status=1, 
                                     agent=obj.agent).order_by('-check_dt')[0]
        except IndexError:
            return None
        return pay.check_dt.strftime("%Y-%m-%d %H:%M:%S")


class PayHistoryWebSerializer(PaySerializer):

    status = serializers.SerializerMethodField()
    check_dt = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Pay
        fields = ('id', 'agent', 'status', 'check_dt', 'promos')

    def get_status(self,obj):
        return obj.get_status_display()


class PayListMobileSerializer(PayHistoryWebSerializer):
    class Meta:
        model = Pay
        fields = ('id', 'status', 'check_dt', 'request_dt', 'promos')

class PayDetailMobileSerializer(PayDetailWebSerializer, PayHistoryWebSerializer):
    comment = serializers.CharField()
    class Meta:
        model = Pay
        fields = ('id', 'status', 'request_dt', 'check_dt', 'promos', 'description', 
                  'comment')


class PayUpdateSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    comment = serializers.CharField(required=False)

