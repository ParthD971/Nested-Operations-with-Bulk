from logging.config import valid_ident
from wsgiref import validate
from rest_framework import serializers

from api.models import Book, BookDetails, Post, Tag, Task, Todo

# Expected input for create
# {
#     "title": "Title of todo",
#     "tasks": [
#         {
#             "title": "Title of task 1",
#             "description": ""
#         },
#         {
#             "title": "Title of task 1",
#             "description": ""
#         }
#     ]
# }

# Expected input for update
# {
#     "title": "Title of todo",
#     "tasks": [
#         {
#             "id": 1,
#             "title": "Title of task 1",
#             "description": ""
#         },
#         {
#             "id": 2,
#             "title": "Title of task 1",
#             "description": ""
#         }
#     ]
# }

# Expected input for delete
# {
#     "title": "Todo 13",
#     "tasks": [
#         {
#             "id": 45
#         },
#         {
#             "id": 46
#         },
        
#     ]
# }


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description']


class TodoNestedSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'tasks']
        extra_kwargs = {
            'title': {
                'validators': []
            }
        }


    def create(self, validated_data):
        tasks = validated_data.pop('tasks')

        todo, created = Todo.objects.get_or_create(**validated_data)
        for task in tasks:
            task.pop('id', None)
            Task.objects.create(todo=todo, **task)

        return todo

    def validate(self, attrs):
        attrs = super().validate(attrs)
        context_data = self.context
        if self.instance:
            errors = []
            is_error_exists = False
            for i in attrs.get('tasks'):
                error = {}
                if i['id'] not in context_data:
                    is_error_exists = True
                    error = {'id': f"id: {i['id']} is not valid"}
                errors.append(error)

            if is_error_exists:
                raise serializers.ValidationError({'tasks': errors})


        return attrs

    def update(self, instance, validated_data):
        # response = validated_data.copy()
        tasks = validated_data.pop('tasks')
        for task in tasks:
            task_id = task.pop('id')
            Task.objects.filter(id=task_id).update(**task)

        return self.instance

    # def delete(self, ):
    #     ids = [task['id'] for task in self.validated_data['tasks']]
    #     Task.objects.filter(id__in=ids).delete()
    #     return self.instance
            


# Expected Input
# {
#     'title': 'Task 1',
#     'description': 'This is django task.',
#     'todo': {
#         'title': 'Todo 5'
#     }
# }


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title']
        extra_kwargs = {
            'title': {
                'validators': []
            }
        }


class TaskNestedSerializer(serializers.ModelSerializer):
    todo = TodoSerializer()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'todo']

    def create(self, validated_data):
        todo = validated_data.pop('todo')
        todo, created = Todo.objects.get_or_create(title=todo['title'])

        task = Task.objects.create(todo=todo, **validated_data)

        return task


class BulkCreateTodoSerializer(TodoNestedSerializer):

    def validate(self, attrs):
        attrs = super(BulkCreateTodoSerializer, self).validate(attrs)
        duplicate_data_count = self.context.get('duplicate_data_count')

        if duplicate_data_count and attrs['title'] and duplicate_data_count[attrs['title']] > 1:
            raise serializers.ValidationError(
                {'non_field_error': 'Title must be unique.'})

        return attrs


# Expected Input
# {
#     "title": "post 1",
#     "tags": [
#         {
#             "name": "tag 1"
#         }, 
#         {
#             "name": "tag 2"
#         }
#     ]
# }

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {
                'validators': []
            }
        }


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'published', 'tags']

    def validate_tags(self, attrs):

        duplicate_data_count = self.context.get('duplicate_data_count')

        errors = []
        is_error_present = False
        for tag in attrs:
            error = {}
            if duplicate_data_count[tag['name']] > 1:
                is_error_present = True
                error = {'name': f'This field with value {tag["name"]} is duplicate.'} 
            errors.append(error)
        if is_error_present:
            raise serializers.ValidationError({'tasks': errors})


        return attrs
    
    def create(self, validated_data):
        tags = validated_data.pop('tags')

        instance = Post.objects.create(**validated_data)

        for tag in tags:
            tag.pop('id', None)
            tag_obj, created = Tag.objects.get_or_create(**tag)
            instance.tags.add(tag_obj)

        return instance

# Expected Input
# {
#     "category": "Category 1",
#     "rating": 2,
#     "price": 20,
#     "publish_date": "12-09-2022",
#     "book": {
#         "name": "Book 1",
#         "author_name": "Author 1",
#     }
    
# }

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'author_name']


class BookDetailsSerailzer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookDetails
        fields = ['id', 'category', 'rating', 'price', 'publish_date', 'book']

    def validate(self, attrs):
        book_name = attrs['book']['name']
        if Book.objects.filter(name=book_name).exists() and BookDetails.objects.filter(book__name=book_name).exists():
            raise serializers.ValidationError({'details': 'Book details are already set.'})

        return attrs
    
    def create(self, validated_data):
        book = validated_data.pop('book')
        book_obj, created = Book.objects.get_or_create(name=book['name'])
        return BookDetails.objects.create(book=book_obj, **validated_data)
