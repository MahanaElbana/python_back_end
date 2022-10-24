from django.db import models

from helper.models import TrackingModel
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib.auth.models import ( 
    AbstractBaseUser ,
    UserManager ,
    PermissionsMixin)

class MyUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        
        if not email:
            raise ValueError("The given email must be set")
        
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin ,TrackingModel) :

    username_validator = UnicodeUsernameValidator()

    username = models.CharField( verbose_name ="username" ,
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        verbose_name = "email address", blank=False  ,unique = True ,
        help_text=(
            "Required. example@mail.come"
        ),
        error_messages={
            "unique": ("A user with that email already exists."),
        },
        )
    
    is_staff = models.BooleanField(
        verbose_name =("staff status"),
        default=False,
        help_text= ("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        verbose_name =("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    email_verified = models.BooleanField(
        verbose_name =("email verification"),
        default=False,
        help_text=(
            "Designates whether this user should be treated as verification. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(verbose_name= "date joined", default=timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property   
    def token():
        return ''