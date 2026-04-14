from django.db import models

# Create your models here.
class Staff(models.Model):
    staff_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.staff_id} - {self.full_name}"
    
    
    # class Attendance(models.Model):
        staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
        date = models.DateField()
        check_in_time = models.TimeField()
        check_out_time = models.TimeField(null=True, blank=True)
        
        def __str__(self):
            return f"{self.staff.full_name} - {self.date}"