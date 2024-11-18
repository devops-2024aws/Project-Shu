from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from offender import models, choices


@login_required(login_url='login')
def get_personal_information(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            personal_obj = models.PersonalInformation.objects.get(offender_id=offender_obj)
        except models.PersonalInformation.DoesNotExist:
            personal_obj = False
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('personal_information')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('personal_information')
    return render(request, "personal_information.html", {"offender_obj": offender_obj, "personal_obj": personal_obj})


@login_required(login_url='login')
def get_employment_information(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            employment_obj = models.Employment.objects.filter(offender_id=offender_obj)
        except models.Employment.DoesNotExist:
            employment_obj = False
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('employment')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('employment')
    return render(request, "employment.html", {"offender_obj": offender_obj, "employment_obj": employment_obj})


@login_required(login_url='login')
def get_education_information(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            education_obj = models.Education.objects.filter(offender_id=offender_obj)
        except models.Education.DoesNotExist:
            education_obj = False
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('education')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('education')
    return render(request, "education.html", {"offender_obj": offender_obj, "education_obj": education_obj})


@login_required(login_url='login')
def get_admission_information(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            admission_obj = models.Admission.objects.get(offender_id=offender_obj)
            print("ADMIS", admission_obj)
        except models.Admission.DoesNotExist:
            admission_obj = False
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('admission')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('admission')
    return render(request, "admission.html", {"offender_obj": offender_obj, "admission_obj": admission_obj})


@login_required(login_url='login')
def get_medical_health_information(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            medical_health_obj = models.MedicalHealth.objects.filter(offender_id=offender_obj)
        except models.MedicalHealth.DoesNotExist:
            medical_health_obj = []
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('medical_health')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('medical_health')
    return render(request, "medical_health.html",
                  {"offender_obj": offender_obj, "medical_health_obj": medical_health_obj,
                   "health_status": choices.health_status_list, "health_condition": choices.health_condition_list
                   })


@login_required(login_url='login')
def get_court_appointments(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            court_appointments_queryset = models.CourtAppointments.objects.filter(offender_id=offender_obj)
        except models.CourtAppointments.DoesNotExist:
            court_appointments_queryset = False
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('court_appointments')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('court_appointments')
    return render(request, "court_appointments.html",
                  {"offender_obj": offender_obj, "court_appointments": court_appointments_queryset})


@login_required(login_url='login')
def get_incident_information(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            incident_obj = models.Incident.objects.get(offender_id=offender_obj)
        except models.Incident.DoesNotExist:
            incident_obj = False
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('incident')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('incident')
    return render(request, "incident.html", {"offender_obj": offender_obj, "incident_obj": incident_obj})


@login_required(login_url='login')
def get_action_plan(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            court_appointments_queryset = models.ActionPlan.objects.filter(offender_id=offender_obj)
        except models.ActionPlan.DoesNotExist:
            court_appointments_queryset = False
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('action_plan')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('action_plan')
    return render(request, "action_plan.html",
                  {"offender_obj": offender_obj, "action_plans": court_appointments_queryset})


@login_required(login_url='login')
def get_case_plan(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            court_appointments_queryset = models.CasePlan.objects.filter(offender_id=offender_obj)
        except models.CasePlan.DoesNotExist:
            court_appointments_queryset = False
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('case_plan')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('case_plan')
    return render(request, "case_plan.html",
                  {"offender_obj": offender_obj, "case_plans": court_appointments_queryset})


@login_required(login_url='login')
def get_release_information(request):
    data = request.POST
    try:
        offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
        try:
            release_obj = models.Release.objects.get(offender_id=offender_obj)
        except models.Release.DoesNotExist:
            release_obj = False
    except models.Offender.DoesNotExist:
        messages.error(request, "Offender Not Found with Provided ID")
        return redirect('release')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('release')
    return render(request, "release.html", {"offender_obj": offender_obj, "release_obj": release_obj})
