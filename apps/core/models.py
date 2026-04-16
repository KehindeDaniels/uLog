from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Staff(models.Model):
    DEPARTMENT_CHOICES = [
        ("operations", "Operations"),
        ("it", "IT"),
        ("hr", "HR"),
        ("finance", "Finance"),
        ("retail", "Retail Banking"),
    ]

    staff_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^UBA\d{3}$',
                message="Staff ID must be like UBA001"
            )
        ]
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default="operations"
    )

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        #  store staff_id in uppercase
        self.staff_id = self.staff_id.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.staff_id} - {self.full_name}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("late", "Late"),
        ("absent", "Absent"),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    date = models.DateField(default=timezone.now)

    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="absent"
    )

    def save(self, *args, **kwargs):
        if self.clock_in:
            bank_open = self.clock_in.replace(hour=9, minute=0, second=0)

            if self.clock_in > bank_open:
                self.status = "late"
            else:
                self.status = "present"
        else:
            self.status = "absent"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.staff.full_name} - {self.date} ({self.status})"


    class Meta:
        ordering = ['-date']