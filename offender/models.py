# Create your models here.
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from offender import choices


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    password = models.CharField(max_length=1500, blank=True, null=True)
    mobile = models.CharField(max_length=1500, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True,
                              choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    is_active = models.BooleanField(default=True)
    dob = models.DateField(blank=True, null=True)
    is_judge = models.BooleanField(default=False)
    is_investigator = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Offender(models.Model):
    offender_id = models.CharField(unique=True, blank=False, null=False, max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True,
                              choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    status = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)


class ActionPlan(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE)
    case_worksteps = models.CharField(max_length=1500, blank=True, null=True)
    category = models.CharField(max_length=1500, blank=True, null=True)
    programnotes = models.CharField(max_length=1500, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    action_plan_id = models.CharField(primary_key=True, unique=True, max_length=20, null=False, blank=False, default="")


class CasePlan(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE)
    created_date_time = models.DateField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=100, blank=True, null=True, choices=[("InProgress", "InProgress"),
                                                                              ("Completed", "Completed")])
    location = models.CharField(max_length=100, blank=True, null=True)
    officer = models.CharField(max_length=100, blank=True, null=True)
    custody_location = models.CharField(max_length=100, blank=True, null=True)
    result = models.CharField(max_length=1500, blank=True, null=True)
    case_plan_id = models.CharField(primary_key=True, unique=True, max_length=20, null=False, blank=False, default="")


class PersonalInformation(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)


class Employment(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class Education(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE)
    course_type = models.CharField(max_length=100, blank=True, null=True)
    institute_name = models.CharField(max_length=100, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class Admission(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE)
    admission_date = models.DateField(blank=True, null=True)
    from_location = models.CharField(max_length=100, blank=True, null=True)
    to_location = models.CharField(max_length=100, blank=True, null=True)
    reason = models.CharField(blank=True, null=True, max_length=100)


class MedicalHealth(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE)
    effective_date = models.DateField(blank=True, null=True)
    health_issue = models.CharField(max_length=1500, blank=True, null=True)
    status = models.CharField(max_length=1000, blank=True, null=True,
                              choices=choices.health_status)
    condition = models.CharField(blank=True, null=True, max_length=1000, choices=choices.health_condition)
    medical_id = models.CharField(primary_key=True, unique=True, max_length=20, null=False, blank=False, default="")


class CourtAppointments(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE)
    scheduled_datetime = models.DateTimeField()
    reason = models.CharField(blank=True, null=True, max_length=1500)
    court = models.CharField(blank=True, null=True, max_length=1000)
    judge_name = models.CharField(blank=True, null=True, max_length=1000)
    assigned_officers = models.CharField(blank=True, null=True, max_length=1000)
    appointment_id = models.CharField(primary_key=True, unique=True, max_length=20, null=False, blank=False, default="")
    status = models.CharField(blank=True, null=True, max_length=1000, default="Processed",
                              choices=[("Processed", "Processed"), ("Completed", "Completed"),
                                       ("Cancelled", "Cancelled")])


class Incident(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE)
    incident_type = models.CharField(blank=True, null=True, max_length=1000)
    reported_by = models.CharField(blank=True, null=True, max_length=1000)
    reported_date = models.DateField(blank=True, null=True)
    incident_details = models.CharField(blank=True, null=True, max_length=1500)


class Release(models.Model):
    offender_id = models.ForeignKey(Offender, on_delete=models.CASCADE)
    release_date_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(blank=True, null=True, max_length=100,
                              choices=[("Released", "Released"), ("In-Custody", "In-Custody")])
