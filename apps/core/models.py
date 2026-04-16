from pyexpat import model

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.
class Staff(models.Model):
    
    DEPARTMENT_CHOICES = [
    ('HR', 'Human Resources'),
    ('IT', 'Information Technology'),
    ('Finance', 'Finance'),
    ('Marketing', 'Marketing'),
    ('Operations', 'Operations'),
]

    staff_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^UBA\d{3}$',
                message='Staff ID must be in the format UBA followed by 3 digits (e.g., UBA001).'
            )
        ]
    )
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='IT')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
            # staff_id is always uppercase
            self.staff_id = self.staff_id.upper()
            super().save(*args, **kwargs)

    def __str__(self):
            return f"{self.staff_id} - {self.full_name}"