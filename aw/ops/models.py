from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Race(models.Model):
    name = models.CharField(max_length=100)

    # Shows up in the admin list
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Base(models.Model) :
    name = models.CharField(max_length=100)

    # Shows up in the admin list
    def __str__(self):
        return self.name

class Clas(models.Model):
    name = models.CharField(max_length=100)

    # Shows up in the admin list
    def __str__(self):
        return self.name

class Operator(models.Model) :
    name = models.CharField(
            max_length=50,
            validators=[MinLengthValidator(1, "Name must be greater than 1 characters")]
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    rarity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many to One Fields
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='operator_owned', default=1)
    RACE_DEFAULT_ID = 35
    race = models.ForeignKey(Race, on_delete=models.CASCADE, default=RACE_DEFAULT_ID)
    BASE_DEFAULT_ID = 1
    base_type_1 = models.ForeignKey(Base, on_delete=models.CASCADE, related_name="base1", default=BASE_DEFAULT_ID)
    base_type_2 = models.ForeignKey(Base, on_delete=models.CASCADE, related_name="base2", default=BASE_DEFAULT_ID)
    CLAS_DEFAULT_ID = 1
    clas = models.ForeignKey(Clas, on_delete=models.CASCADE, verbose_name="class", default=CLAS_DEFAULT_ID)

    #Many To Many Fields
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comment', related_name='comments_owned')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Fav', related_name='favorite_operators')
    #ratings = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Rating', related_name='ratings_owned')

    # Shows up in the admin list
    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )
    num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )

    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text + '; rating = ' + self.num
        return self.text[:11] + ' ...; rating = ' + self.num

class Fav(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('operator', 'user')

    def __str__(self):
        return '%s has %s'%(self.user.username, self.operator.name)

'''class Rating(models.Model):
    num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return num'''