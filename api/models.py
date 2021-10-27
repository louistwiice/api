from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy

# Create your models here.

class Userstype(models.Model):
    '''
    Basically there are 4 types of user:
    -0- client
    -1- coach
    -2- doctor
    -3- nutritioniste
    -4- other
    '''
    user_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user_type}'


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, firstname, lastname, password, **others_fields):

        if not email:
            raise ValueError( gettext_lazy('You must provide an email address') )

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, firstname=firstname, lastname=lastname, **others_fields)

        user.set_password(password)
        user.save(using= self._db)

        return user


    def create_superuser(self,  email, username, firstname, lastname, password, **others_fields):
        others_fields.setdefault('is_staff', True)
        others_fields.setdefault('is_superuser', True)
        others_fields.setdefault('is_active', True)

        if others_fields.get('is_staff') is not True:
            raise ValueError( 'Superuser must be assigned to is_staff=True' )

        if others_fields.get( 'is_superuser' ) is not True:
            raise ValueError( 'Superuser must be assigned to is_superuser=True' )

        return self.create_user(email, username, firstname, lastname, password, **others_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    '''
    The users of the plateform
    '''
    Male = 'M'
    Femele = 'F'
    SEXE = [
        ('M', 'Male'),
        ('F', 'Femele'),
    ]


    email = models.EmailField( ('email address'), unique=True )
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    startdate = models.DateTimeField(auto_now=True)
    about = models.TextField( ('about'), max_length=500, blank=True )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    phone = PhoneNumberField(blank=True)
    address = models.CharField(max_length=350)
    user_type = models.ForeignKey('Userstype', null=True, on_delete=models.CASCADE)
    born_date = models.DateField(default=timezone.now)
    height = models.IntegerField( default=150, validators=[MinValueValidator(100), MaxValueValidator(400)])
    sexe = models.CharField(max_length=10, choices=SEXE)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname', 'lastname']

    def __str__(self):
        return f'{self.username}'

    def number_of_rating(self):
        '''
        This function returns the number of rating specific to a fitness program
        :return:
        '''

        ratings = AccountRating.objects.filter(account_to_rate=self)
        return len(ratings)



    def avg_rating(self):
        ratings = AccountRating.objects.filter(account_to_rate=self)

        sum = 0
        for rating in ratings:
            sum += rating.stars

        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0



class FitnessProgram(models.Model):
    BOTH_GENDERS = 'B'
    POPULATION = [
        ('M', 'Male'),
        ('F', 'Femele'),
        ('B', 'Both genders'),
    ]

    name = models.CharField(max_length=100)
    duree = models.IntegerField(('Number of time, in minute, for this Program'),validators=[MinValueValidator(30)])
    target = models.CharField(max_length=150,default=BOTH_GENDERS, choices=POPULATION)
    description = models.TextField(default='NULL')

    def number_of_rating(self):
        '''
        This function returns the number of rating specific to a fitness program
        :return:
        '''
        ratings = FitnessProgramsRating.objects.filter(fitprog=self)
        return len(ratings)

    def avg_rating(self):
        sum= 0
        ratings = FitnessProgramsRating.objects.filter(fitprog=self)

        for rating in ratings:
            sum += rating.stars

        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0

    def number_of_comments(self):
        comments = FitnessProgramsComment.objects.filter(fitprog=self)
        return len(comments)


    def __str__(self):
        return f'{self.name}'


class UsersFitnessPrograms(models.Model):
    account = models.OneToOneField('Account', on_delete=models.CASCADE)
    fitprog = models.ForeignKey('FitnessProgram', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now=True)


class FitnessProgramsComment(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    fitprog = models.ForeignKey( 'FitnessProgram', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=1000)


    class Meta:
        ordering = ['-created_on']





class FitnessProgramsRating(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    fitprog = models.ForeignKey( 'FitnessProgram', on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_date = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together= (('account', 'fitprog'),)
        index_together= (('account', 'fitprog'),)


class AccountRating(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

    #As It is a Coach Rating model, we filter account by user_type='coach'
    account_to_rate = models.ForeignKey('Account', on_delete=models.CASCADE ,related_name='account_to_rate')
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together= (('account', 'account_to_rate'),)
        index_together= (('account', 'account_to_rate'),)



class Blog(models.Model):
    title = models.CharField(max_length=400)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(default=timezone.now)
    published = models.BooleanField()
    content = models.TextField(max_length=8000)
    tags = models.CharField(max_length=1000, blank=True)
    source = models.CharField(max_length=1000, blank=True)

    class Meta:
        ordering = ['-created_on']


    def __str__(self):
        return f'{self.title} from {self.account}'

    def clean(self):
        FORBIDDEN_CHARACTER = ['-', ';', ':', '/', '+', '\\']
        for c in FORBIDDEN_CHARACTER:
            if c in self.tags:
                raise ValidationError(gettext_lazy("Tag can't contain following characters: - ; : / + \\"))


    def number_of_rating(self):
        '''
        This function returns the number of rating specific to a fitness program
        :return:
        '''
        ratings = BlogRating.objects.filter(blog=self)
        return len(ratings)

    def avg_rating(self):
        sum= 0
        ratings = BlogRating.objects.filter(blog=self)

        for rating in ratings:
            sum += rating.stars

        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0

    def number_of_comments(self):
        comments = BlogComment.objects.filter(blog=self)
        return len(comments)



class BlogRating(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating_date']
        unique_together= (('account', 'blog'),)
        index_together= (('account', 'blog'),)


class BlogComment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment of {self.account}'


class Workout(models.Model):
    '''
    This model is to create a program. A coach can create a workout.
    After creating a workout, he can associate the workout to a Fitness programm

    '''
    WORKOUT_TYPE = [
        ('C', 'Challenge'),
        ('P', 'Program')
    ]

    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    fitprog = models.ForeignKey( 'FitnessProgram', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=500) #he name of the workout
    about = models.TextField(max_length=7000) #The overview of the workout
    price = models.IntegerField(blank=True, default=0) #The price of the workout
    nb_of_weeks = models.IntegerField()
    day_per_week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    difficulty = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    body_focus = models.CharField(max_length=500)
    equipments = models.CharField(max_length=500, blank=True)
    training_type = models.CharField(max_length=800) # Example Cardiovascular, HIIT, Strength Training, Toning
    workout_type = models.CharField(choices=WORKOUT_TYPE, default=WORKOUT_TYPE[0], max_length=30)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.title} from {self.account}'

    def number_of_rating(self):
        '''
        This function returns the number of rating specific to a fitness program
        :return:
        '''
        ratings = WorkoutsRating.objects.filter(workout=self)
        return len(ratings)

    def avg_rating(self):
        sum= 0
        ratings = WorkoutsRating.objects.filter(workout=self)

        for rating in ratings:
            sum += rating.stars

        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0

    def number_of_comments(self):
        comments = WorkoutComment.objects.filter(workout=self)
        return len(comments)


class WorkoutsRating(models.Model):
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_date = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-rating_date']
        unique_together= (('account', 'workout'),)
        index_together= (('account', 'workout'),)


class WorkoutComment(models.Model):
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment of {self.account}'

