from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class ClienteManager(BaseUserManager):
    def create_user(self, username, email, cpf, password=None):
        if not email:
            raise ValueError("O cliente deve ter um endereço de email")
        if not username:
            raise ValueError("O cliente deve ter um username")
        if not cpf:
            raise ValueError("O cliente deve ter um CPF")

        email = self.normalize_email(email)
        cliente = self.model(username=username, email=email, cpf=cpf)
        cliente.set_password(password)
        cliente.is_active = True  # Necessário para login
        cliente.save(using=self._db)
        return cliente

    def create_superuser(self, username, email, cpf, password=None):
        cliente = self.create_user(username, email, cpf, password)
        cliente.is_superuser = True
        cliente.is_staff = True
        cliente.is_active = True  # Superusuários também devem estar ativos
        cliente.save(using=self._db)
        return cliente

class Cliente(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    cpf = models.CharField(max_length=11, unique=True)  # CPF deve ser único e ter 11 caracteres
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='cliente_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='cliente_permissions',
        blank=True
    )

    objects = ClienteManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'cpf']

    def __str__(self):
        return self.username
