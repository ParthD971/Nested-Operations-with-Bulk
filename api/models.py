from email.policy import default
from django.db import models

def make_string(data_dict):
    return " | ".join([k + ": " + str(v) for k, v in data_dict.items()])


class Todo(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        data = {
            'ID': self.id,
            'TodoTitle': self.title,

        }
        return make_string(data)


class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    todo = models.ForeignKey(Todo, related_name='tasks', on_delete=models.CASCADE)


    def __str__(self):
        data = {
            'ID': self.id,
            'TaskTitle': self.title,
            'todo': self.todo.id,
        }
        return make_string(data)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        data = {
            'ID': self.id,
            'Name': self.name,
        }
        return make_string(data)


class Post(models.Model):
    title = models.CharField(max_length=500, unique=True)
    description = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, through='PostTag', related_name='posts')

    def __str__(self):
        data = {
            'ID': self.id,
            'PostTitle': self.title,
        }
        return make_string(data)


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        data = {
            'ID': self.id,
            'PostTitle': self.post.title,
            'TagName': self.tag.name,
        }
        return make_string(data)


class Book(models.Model):
    name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)

    def __str__(self):
        data = {
            'ID': self.id,
            'BookName': self.name,
        }
        return make_string(data)


class BookDetails(models.Model):
    book = models.OneToOneField(Book, related_name='book_details', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)
    price = models.IntegerField()
    publish_date = models.DateField()

    def __str__(self):
        data = {
            'ID': self.id,
            'book': self.book.id,
        }
        return make_string(data)

