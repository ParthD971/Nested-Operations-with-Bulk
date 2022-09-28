from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


from api.models import Task, Todo
from .serializers import BulkCreateTodoSerializer, TodoNestedSerializer, TaskNestedSerializer


class TodoAPIView(APIView):
    def get(self, request):
        queryset = Todo.objects.all()
        serializer = TodoNestedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoNestedSerializer(data=request.data)
        if serializer.is_valid():
            todo = serializer.create(serializer.data)
            response = TodoNestedSerializer(todo).data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskAPIView(APIView):
    def get(self, request):
        queryset = Task.objects.all()
        serializer = TaskNestedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TaskNestedSerializer(data=request.data)
        if serializer.is_valid():
            todo = serializer.create(serializer.data)
            response = TaskNestedSerializer(todo).data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkTodoAPIView(APIView):
    def post(self, request):
        data = request.data

        if data:
            if not isinstance(data, list):
                raise ValidationError('Expected list of dict.')

            temp = {}
            for i in data:
                temp[i['title']] = temp.get(i['title'], 0) + 1

            context = {
                'request': request,
                'duplicate_data_count': temp
            }

            serializer = BulkCreateTodoSerializer(
                data=data, context=context, many=True)

            if serializer.is_valid():
                response = serializer.create(serializer.validated_data)
                response = TodoNestedSerializer(response, many=True).data
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('No Data to process', status=status.HTTP_400_BAD_REQUEST)
