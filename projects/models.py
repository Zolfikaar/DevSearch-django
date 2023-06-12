from django.db import models
from users.models import Profile
import uuid


class Tag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name



class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True,blank=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to='uploaded-images/projects', default='images/project-default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio','-vote_total','created_at']
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100
        # to update the vote_total and vote_ratio in DB
        self.vote_total = upVotes
        self.vote_ratio = ratio
        self.save()

    @property
    def reviewers(self):
        query_set = self.review_set.all().values_list('owner_id', flat=True)
        return query_set


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=255, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        # To prevent multi-review from same person/profile on one project
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value