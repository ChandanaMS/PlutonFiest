from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phone_field import PhoneField
from django.core.validators import RegexValidator
import re 
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.  

class UserProfileInfor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    university_name=models.CharField(max_length=200)
    age=models.PositiveIntegerField()
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

def __str__(self):
    return self.user.username

def validate_mail(value): 
    if "@gmail.com" in value: 
        return value 
    else: 
        raise ValidationError("This field accepts mail id of google only")

def validate_phone(value): 
    Pattern = re.compile("(0/91)?[7-9][0-9]{9}") 
    if (Pattern.match(value)):  
        return value
    else : 
        raise ValidationError("Invalid number. The number begins with 0 or 91 followed by 10 digits")

  
class EventRegisterations(models.Model): 
    Male = 'M'
    FeMale = 'F'
    Small='S'
    Medium='M'
    Large='L'
    GENDER_CHOICES = ( 
    (Male, 'Male'), 
    (FeMale, 'Female'), 
    )
    EVENT_CHOICES=(('Culturals','CULTURALS'),('Sci_tech','SCIENCE & TECHNOLOGY'),('Sports','SPORTS'),('ArtLit','ART & LITERATURE'))

    SIZE=((Small,'Small'),(Medium,'Medium'),(Large,'Large')) 
    name = models.CharField( max_length = 20, blank = False, null = False) 
    emailid=models.CharField( max_length = 200, validators =[validate_mail]) 
    gender = models.CharField(max_length = 6, choices = GENDER_CHOICES,default = Male)
    college_name=models.CharField(max_length=200)
    phone_number=models.CharField(max_length = 15,null=False, blank=False, unique=True,validators=[validate_phone ],)
    event=models.CharField(null=True, max_length=30,
        default=None,choices=EVENT_CHOICES)
    members=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])

    project_idea= models.TextField(blank = False, null = False) 
    tshirt_size=models.CharField(max_length = 6, choices = SIZE,default = Medium)
      

     
      
