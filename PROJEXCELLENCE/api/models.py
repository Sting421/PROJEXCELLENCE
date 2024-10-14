from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    status = models.CharField(max_length=20)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Member: {self.user}"


class Project(models.Model):
    project_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.project_name


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.team_name


class Role(models.Model):
    role_name = models.CharField(max_length=50)
    permission = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name


class Resources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=50)

    def __str__(self):
        return self.filename


class Task(models.Model):
    task_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.task_name


class File(models.Model):
    filename = models.CharField(max_length=50)
    time_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resources, on_delete=models.CASCADE)

    def __str__(self):
        return self.filename


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user} on {self.project} posted on {self.time_posted}"
