from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        data = {
            'Todo': self.id,
            'Title': self.title,

        }
        return " | ".join([k+": "+str(v) for k, v in data.items()])




class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    todo = models.ForeignKey(Todo, related_name='tasks', on_delete=models.CASCADE)


    def __str__(self):
        data = {
            'Todo': self.todo.id,
            'Current-task': self.id,
        }
        return " | ".join([k + ": " + str(v) for k, v in data.items()])
