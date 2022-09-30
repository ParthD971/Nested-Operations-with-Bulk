from email.policy import default
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
    description = models.TextField(null=True, blank=True)
    todo = models.ForeignKey(Todo, related_name='tasks', on_delete=models.CASCADE)


    def __str__(self):
        data = {
            'Todo': self.todo.id,
            'Current-task': self.id,
        }
        return " | ".join([k + ": " + str(v) for k, v in data.items()])


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=500, unique=True)
    description = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, through='PostTag', related_name='posts')


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Book(models.Model):
    name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)


class BookDetails(models.Model):
    book = models.OneToOneField(Book, related_name='book_details', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)
    price = models.IntegerField()
    publish_date = models.DateField()

