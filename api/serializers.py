from rest_framework import serializers

from api.models import Task, Todo

# Expected input
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


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description']


class TodoNestedSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'tasks']

    def create(self, validated_data):
        tasks = validated_data.pop('tasks')

        todo, created = Todo.objects.get_or_create(**validated_data)
        for task in tasks:
            Task.objects.create(todo=todo, **task)

        return todo

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
