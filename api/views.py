from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


from api.models import (
    Book, 
    BookDetails,
    Post,
    Task,
    Todo
)

from .serializers import (
    BookDetailsSerailzer,
    BulkCreateTodoSerializer,
    PostSerializer,
    TodoNestedSerializer,
    TaskNestedSerializer
)


class TodoAPIView(APIView):
    """
    description: This is for Nested Todo for reverse relation - CRUD operations | Foreign Key Relation
    """
    def get(self, request):
        """
        response:
        {
            "id": integer,
            "title": string,
            "tasks": [
                {
                    "id": integer,
                    "title": string,
                    "description": string
                },
                ...
            ]
        }
        """
        queryset = Todo.objects.all()
        serializer = TodoNestedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        data:
        {
            "title": string,
            "description": string,
            "todo": {
                "title": string
            }
        }
        response:
        {
            "id": integer,
            "title": string,
            "description": string,
            "todo": {
                "id": integer,
                "title": string
            }
        }
        """
        serializer = TodoNestedSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response = TodoNestedSerializer(instance).data
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        """
        data:
        {
            "title": string,
            "tasks": [
                {
                    "id": integer,
                    "title": string,
                    "description": string
                },
                ...
            ]
        }
        response:
        {
            "title": string,
            "tasks": [
                {
                    "title": string,
                    "description": string
                },
                ...
            ]
        }
        """
        todo_filter = Todo.objects.filter(title=request.data.get('title'))
        if not todo_filter.exists():
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
        """
        description: It deletes all task provided in data related to todo given in data.
        data:
        {
            "title": string,
            "tasks": [
                {
                    "id": integer
                },
                ...
            ]
        }
        """
        todo_filter = Todo.objects.filter(title=request.data.get('title'))
        if not todo_filter:
            raise ValidationError('Title for todo does not exists.')

        if not isinstance(request.data.get('tasks'), dict):
            ValidationError('tasks field must be dictionary.')
        
        context_data = [i.id for i in todo_filter.first().tasks.all()]
        
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


class TaskAPIView(APIView):
    """
    description: This is for Nested Todo for forward relation - CRUD operations | Foreign Key Relation
    """
    def get(self, request):
        """
        response:
        [
            {
                "id": integer,
                "title": string,
                "description": string,
                "todo": {
                    "id": inger,
                    "title": string
                }
            },
            ...
        ]
        """
        queryset = Task.objects.all()
        serializer = TaskNestedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        data:
        {
            "title": string,
            "description": string,
            "todo": {
                "title": string
            }
        }
        response:
        {
            "id": integer,
            "title": string,
            "description": string,
            "todo": {
                "id": integer,
                "title": string
            }
        }
        """
        serializer = TaskNestedSerializer(data=request.data)
        if serializer.is_valid():
            todo = serializer.create(serializer.data)
            response = TaskNestedSerializer(todo).data
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkTodoAPIView(APIView):
    """
    description: This is for Bulk Nested Todo for reverse relation - CR operations | Foreign Key Relation
    """
    def get(self, request):
        """
        response:
        [
            {
                "id": integer,
                "title": string,
                "tasks": [
                    {
                        "id": integer,
                        "title": string,
                        "description": string
                    },
                    ...
                ]
            },
            ...
        ]
        """
        queryset = Todo.objects.all()
        serializer = BulkCreateTodoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        """
        data:
        [
            {
                "title": string,
                "tasks": [
                    {
                        "title": string,
                        "description": string
                    },
                    ...
                ]
            },
            ...
        ]
        response:
        [
            {
                "id": integer,
                "title": string,
                "tasks": [
                    {
                        "id": integer,
                        "title": string,
                        "description": string
                    },
                    ...
                ]
            },
            ...
        ]
        """
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


class PostAPIView(APIView):
    """
    description: This is for Nested Post for forward relation - CR operations | ManytoMany Key Relation
    """
    def get(self, request):
        """
        response:
        [
            {
                "id": integer,
                "title": string,
                "description": string,
                "published": true,
                "tags": [
                    {
                        "id": integer,
                        "name": string
                    }
                    ...
                ]
            },
            ...
        ]
        """
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        data:
        {
            "title": string,
            "tags": [
                {
                    "name": string
                }, 
                ...
            ]
        }
        response:
        {
            "id": integer,
            "title": string,
            "description": string,
            "published": boolean,
            "tags": [
                {
                    "id": integer,
                    "name": string
                },
                ...
            ]
        }
        """
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



class BookDetailsAPIView(APIView):
    """
    description: This is for BookDetails Nested Todo for forward relation - CRU operations | OnetoOne Key Relation
    """
    def get(self, request):
        """
        response:
        [
            {
                "id": integer,
                "category": string,
                "rating": integer,
                "price": integer,
                "publish_date": Date("YYYY-MM-DD"),
                "book": {
                    "id": integer,
                    "name": string,
                    "author_name": string
                }
            },
            ...
        ]
        """
        queryset = BookDetails.objects.all()
        serializer = BookDetailsSerailzer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        """
        data:
        {
            "category": string,
            "rating": integer,
            "price": integer,
            "publish_date": Date("YYYY-MM-DD"),
            "book": {
                "name": string,
                "author_name": string
            }    
        }
        response:
        {
            "id": integer,
            "category": string,
            "rating": integer,
            "price": integer,
            "publish_date": Date("YYYY-MM-DD"),
            "book": {
                "id": integer,
                "name": string,
                "author_name": string
            }
        }
        """
        data = request.data

        if data:
            serializer = BookDetailsSerailzer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                response = BookDetailsSerailzer(instance).data
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('No Data to process', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        data:
            {
            "category": string,
            "rating": integer,
            "price": integer,
            "publish_date": Date("YYYY-MM-DD"),
            "book": {
                "name": string,
                "author_name": string
            }
        }
        response:
        {
            "id": integer,
            "category": string,
            "rating": integer,
            "price": integer,
            "publish_date": Date("YYYY-MM-DD"),
            "book": {
                "id": integer,
                "name": string,
                "author_name": string
            }
        }
        """
        if not isinstance(request.data.get('book'), dict):
            ValidationError('book field must be dictionary.')

        book = request.data.get('book')
        if not book:
            raise ValidationError('book attribute is not found.')

        book_name = book.get('name')
        if not book_name:
            raise ValidationError('book object has no name attribute.')

        book_filter = Book.objects.filter(name=book_name)
        if not book_filter.exists():
            raise ValidationError('Book does not exists.')
        
        serializer = BookDetailsSerailzer(BookDetails(), data=request.data)
        if serializer.is_valid():
            # response = serializer.validated_data.copy()
            instance = serializer.save()
            response = BookDetailsSerailzer(instance).data
            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)