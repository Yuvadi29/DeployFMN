import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager




class register_user_manager(BaseUserManager):
    def create_user(self,username,mail,first_name,mid_name,last_name,gender,password=None):
        # if not mail:
        #     raise ValueError("Email required")
        
        if not username:
            raise ValueError("username required")

        user = self.model(
            mail = mail,
            first_name=first_name,
            mid_name=mid_name,
            last_name=last_name,
            gender=gender,
            username = username,
            password = password,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self,username,mail,first_name,mid_name,last_name,gender,password=None):
        user = self.create_user(
            mail = mail,
            first_name=first_name,
            mid_name=mid_name,
            last_name=last_name,
            gender=gender,
            username = username,
            password = password,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using = self._db)
        return user      

class user_details(AbstractBaseUser):
    unique_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30,null=False)
    last_name = models.CharField(max_length=30,null=False)

    gender = models.CharField(max_length=6,null = False)
    dob = models.DateField()

    mail = models.CharField(max_length=50,null = False,unique=True)
    phone = models.BigIntegerField(null = False,default=None)

    username = models.CharField(max_length=30,null=False,unique=True,default=None)
    password = models.CharField(max_length=1000,null=False)

    is_active = models.BooleanField(default = False,null=False)
    is_banned = models.BooleanField(default = False,null=False)
    is_admin = models.BooleanField(default = False,null=False)
    is_faculty = models.BooleanField(default = False,null=False)
    is_student = models.BooleanField(default = False,null=False)
    is_content_writer = models.BooleanField(default = False,null=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    MAIL_FIELD = 'mail'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mail','first_name','mid_name','last_name','gender']
    objects = register_user_manager()

    def __str__(self):
        return self.mail
    
    def has_perm(self,perm,obj=None):
        return self.is_admin    

    def has_module_perm(self , app_label):
        return True

    class Meta:
        db_table = "users"


class extra_details(models.Model):
    user_id = models.ForeignKey(user_details,on_delete=models.CASCADE,default=None,verbose_name='user_unique_id')
    github = models.URLField(max_length=300)
    insta = models.URLField(max_length=300)
    twitter = models.URLField(max_length=300)
    website = models.URLField(max_length=300)
    profile = models.CharField(max_length=200)
    other_link = models.URLField(max_length=300)
    
    class meta:
        db_table = "user_extra_details"

class file_upload(models.Model):
    file_type = models.CharField(max_length=6,null=False,default=None)
    file_name = models.CharField(max_length=50,null = False,default=None)
    file_title = models.CharField(max_length=50,null = False,default=None)
    file_url = models.CharField(max_length=200,default=None)
    tags = models.CharField(max_length=200,default=None)
    description = models.CharField(max_length=500,default=None)
    uploading_time = models.DateTimeField(auto_now_add=True)
    likes = models.BigIntegerField(null = False,default=None)
    user = models.ForeignKey(user_details,on_delete=models.CASCADE,default=None,verbose_name='user_unique_id')

    class Meta:
        db_table = "file_details"

class file_likes(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE,default=None,verbose_name='user_unique_id')
    file = models.ForeignKey(file_upload,on_delete=models.CASCADE,default=None,verbose_name='file_uniqque_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "likes"
        unique_together = ('user','file')



class bookmarked_files(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE,default=None,verbose_name='user_unique_id')
    file = models.ForeignKey(file_upload,on_delete=models.CASCADE,default=None,verbose_name='file_uniqque_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "bookmarked_files"
        unique_together = ('user','file')


class reported_file(models.Model):
    reason = models.CharField(max_length=50,blank=False,null=False)
    reason_message = models.CharField(max_length=400,blank=True,null=True)
    file = models.ForeignKey(file_upload,on_delete=models.CASCADE,default=None,verbose_name='file_unique_id',related_name='file_id')
    user_reported_issue = models.ForeignKey(user_details,on_delete=models.CASCADE,verbose_name='user_reported_issue',related_name='user_reported_issue')
    user_posted = models.ForeignKey(user_details,on_delete=models.CASCADE,default=None,verbose_name='user_posted',related_name='user_posted')
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "reported_file"
        unique_together = ('user_posted','user_reported_issue','file')