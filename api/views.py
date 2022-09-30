from re import search
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


from api.models import Book, BookDetails, Post, Task, Todo
from .serializers import BookDetailsSerailzer, BulkCreateTodoSerializer, PostSerializer, TodoNestedSerializer, TaskNestedSerializer

# Forward Relation Nested CRUD Operations
class TodoAPIView(APIView):
    def get(self, request):
        queryset = Todo.objects.all()
        serializer = TodoNestedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoNestedSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response = TodoNestedSerializer(instance).data
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        todo_filter = Todo.objects.filter(title=request.data.get('title'))
        if not todo_filter:
            raise ValidationError('Title for todo does not exists.')

        if not isinstance(request.data.get('tasks'), dict):
            ValidationError('tasks field must be dictionary.')

        try:
            context_data = [i.id for i in todo_filter.first().tasks.all()]
        except KeyError:
            ValidationError('tasks object must have id field.')
        
        serializer = TodoNestedSerializer(todo_filter.first(), data=request.data, context=context_data)
        if serializer.is_valid():
            response = serializer.validated_data.copy()
            instance = serializer.save()
            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        todo_filter = Todo.objects.filter(title=request.data.get('title'))
        if not todo_filter:
            raise ValidationError('Title for todo does not exists.')

        if not isinstance(request.data.get('tasks'), dict):
            ValidationError('tasks field must be dictionary.')
        
        context_data = [i.id for i in todo_filter.first().tasks.all()]
        
        # except KeyError:
        #     ValidationError('tasks object must have id field.')
        
        def is_valid_data(data, context=None):
            errors = []
            validated_data = []
            is_valid = True
            tasks = data.pop('tasks')
            for task in tasks:
                error = {}
                if not task.get('id'):
                    is_valid = False
                    error = {'id': f"This field is required."}
                elif task['id'] not in context:
                    is_valid = False
                    error = {'id': f"The Id {task['id']} is invalid."}
                else:
                    validated_data.append(task)
                errors.append(error)
            return errors, is_valid, validated_data
        
        errors, is_valid, validated_data = is_valid_data(request.data, context=context_data)
        if is_valid:
            ids = [task['id'] for task in validated_data]
            Task.objects.filter(id__in=ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Reverse Relation Nested CR Operations
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


# Forward Relation Bulk Nested CR Operations
class BulkTodoAPIView(APIView):
    def get(self, request):
        queryset = Todo.objects.all()
        serializer = BulkCreateTodoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


# Forward Relation Nested R Operations with manytomanyfield
class PostAPIView(APIView):
    def get(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        if data:
            if not data.get('tags'):
                raise ValidationError('tags attribute is required.')
                
            tags = data.get('tags')

            if not isinstance(tags, list):
                raise ValidationError('Expected tags to be list of dict.')

            temp = {}
            for i in tags:
                if not i.get('name'):
                    raise ValidationError('Invalid data: Every tag must have name attribute.')
                temp[i['name']] = temp.get(i['name'], 0) + 1

            context = {
                'request': request,
                'duplicate_data_count': temp
            }

            serializer = PostSerializer(data=request.data, context=context)
            if serializer.is_valid():
                instance = serializer.save()
                response = PostSerializer(instance).data
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('No Data to process', status=status.HTTP_400_BAD_REQUEST)



# Forward Relation Nested R Operations with onetoonefield
class BookDetailsAPIView(APIView):
    def get(self, request):
        queryset = BookDetails.objects.all()
        serializer = BookDetailsSerailzer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        
        data = request.data

        if data:
            # if not data.get('tags'):
            #     raise ValidationError('tags attribute is required.')
                
            # tags = data.get('tags')

            # if not isinstance(tags, list):
            #     raise ValidationError('Expected tags to be list of dict.')

            # temp = {}
            # for i in tags:
            #     if not i.get('name'):
            #         raise ValidationError('Invalid data: Every tag must have name attribute.')
            #     temp[i['name']] = temp.get(i['name'], 0) + 1

            # context = {
            #     'request': request,
            #     'duplicate_data_count': temp
            # }

            serializer = BookDetailsSerailzer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                response = BookDetailsSerailzer(instance).data
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('No Data to process', status=status.HTTP_400_BAD_REQUEST)

