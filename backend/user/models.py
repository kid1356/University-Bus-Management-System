from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.



class Manager(BaseUserManager):
    def create_user(self, username,email, role=None,password= None, confirm_password =None):
        if not email:
            raise ("Email should be provided")
        
        user = self.model(
            username =username,
            email=email,
            role=role
        )

        user.set_password(password)
        user.save(using = self._db)
        return user
    

    def create_superuser(self,username,email,password):
        if not email:
            raise ("Email should be provided")
        
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using =self._db)
        return user
    

class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('Student','student'),
        ('University_admin','university_admin')
    )

    email = models.EmailField(max_length=254,unique=True)
    username = models.CharField(max_length=30, null=True,blank=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to='images/', null=True,blank=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,null=True,blank=True)
    university = models.ForeignKey('University', on_delete= models.CASCADE,null= True, blank=True)
    otp = models.CharField(max_length=10, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin =models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = Manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email
    

    def has_perm(self, perm, obj=None):
     "Does the user have a specific permission?"
      
     return self.is_admin

    def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
     
      return True

    @property
    def is_staff(self):
      "Is the user a member of staff?"
      
      return self.is_admin
    

class University(models.Model):
   university_name = models.CharField(max_length=100, null=True,blank=True)
   location = models.CharField(max_length=255, null=True,blank=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now_add=True)
   
   def __str__(self) -> str:
      return self.university_name