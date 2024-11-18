from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from offender import models
from offender import choices
from rest_framework import status


# Create your views here.
def index(request):
    return render(request, "index.html", {})


def dashboard(request):
    offender_queryset = models.Offender.objects.all()
    data = {
        "offender_count": offender_queryset.count(),
        "male_count": offender_queryset.filter(gender="Male").count(),
        "female_count": offender_queryset.filter(gender="Female").count(),
    }
    return render(request, "dashboard.html", {"context": data})


def contact_us(request):
    return render(request, "contact_us.html", {})


def privacy_policy(request):
    return render(request, "privacy_policy.html", {})


def about_us(request):
    return render(request, "about_us.html", {})


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = request.POST
        user = authenticate(username=data["username"], password=data["password"])
        print("USER", user)
        if user is not None:
            # user_obj = models.User.objects.get(username=user)
            if user.is_investigator:
                login(request, user)
                user.last_login = datetime.now()
                user.save()
                messages.success(request, "Investigator Logged In Successfully")
                return redirect('dashboard')
            else:
                messages.error(request, "User is not Investigator")
                return redirect('login')
        else:
            messages.error(request, "Unable to Login")
            return redirect('login')
    else:
        return render(request, "login.html", {})


@csrf_exempt
def judge_login(request):
    if request.method == "POST":
        data = request.POST
        user = authenticate(username=data["username"], password=data["password"])
        print("USER", user)
        if user is not None:
            user_obj = models.User.objects.get(username=user)
            if user_obj.is_judge:
                login(request, user)
                user.last_login = datetime.now()
                user.save()
                messages.success(request, "Judge Logged In Successfully")
                return redirect('dashboard')
            else:
                messages.error(request, "User is not Judge")
                return redirect('judge_login')
        messages.error(request, "Unable to Login")
        return redirect('judge_login')
    else:
        return render(request, "judge_login.html", {})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/')


def logout_ajax(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse(data={"data": None, "message": "Logout Success"}, status=status.HTTP_200_OK)


@login_required(login_url='login')
def create_offender(request):
    if request.method == "POST":
        data = request.POST
        try:
            offender_cnt = models.Offender.objects.all().count()
            offender_id = "OFF{0:0=4d}".format(int(offender_cnt) + 1)
            offender_obj = models.Offender.objects.create(offender_id=offender_id, first_name=data["first_name"],
                                                          dob=data["dob"], last_name=data["last_name"],
                                                          gender=data["gender"])
            if offender_obj:
                messages.success(request, "Offender Added Successfully")
                return redirect('offender')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('create_offender')
    return render(request, "add_offender.html", {})


@login_required(login_url='login')
def change_password(request):
    try:
        if request.method == "POST":
            data = request.POST
            user_obj = models.User.objects.get(user_id=request.user.user_id)
            if user_obj.check_password(data["old_password"].strip()):
                user_obj.password = make_password(data["password"].strip())
                user_obj.save()
                update_session_auth_hash(request, user_obj)  # Important!
                messages.success(request, "Password Changed Successfully")
            else:
                messages.error(request, "Old Password Is Incorrect")
            return redirect('change_password')
        return render(request, "change_password.html", {})
    except Exception as E:
        messages.error(request, str(E))
        return redirect('change_password')


@login_required(login_url='login')
def my_account(request):
    user_obj = models.User.objects.get(user_id=request.user.user_id)
    if request.method == "POST":
        data = request.POST
        user_obj.first_name = data['first_name']
        user_obj.last_name = data['last_name']
        user_obj.mobile = data['mobile']
        user_obj.dob = data['dob']
        user_obj.gender = data['gender']
        user_obj.save()
        messages.success(request, "Account Details Updated Successfully")
        return redirect('my_account')
    return render(request, 'my_account.html', {'user_obj': user_obj})


@login_required(login_url='login')
def personal_information(request):
    if request.method == "POST":
        data = request.POST
        try:
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            personal_obj = models.PersonalInformation.objects.get(offender_id=offender_obj)
            personal_obj.city = data["city"]
            personal_obj.state = data["state"]
            personal_obj.country = data["country"]
            personal_obj.mobile = data["mobile"]
            personal_obj.email = data["email"]
            personal_obj.save()
            messages.success(request, "Offender Personal Information Updated")
            return redirect('personal_information')
        except models.PersonalInformation.DoesNotExist:
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            personal_obj = models.PersonalInformation.objects.create(offender_id=offender_obj,
                                                                     country=data["country"], state=data["state"],
                                                                     city=data["city"], mobile=data["mobile"],
                                                                     email=data["email"])
            messages.success(request, "Offender Personal Information Added")
            return redirect('personal_information')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('personal_information')
    return render(request, "personal_information.html", {})


@login_required(login_url='login')
def offender(request):
    offender_queryset = models.Offender.objects.all()
    return render(request, "offender.html", {"offender_queryset": offender_queryset})


@login_required(login_url='login')
def employment(request):
    if request.method == "POST":
        try:
            data = request.POST
            print("data", data)
            emp_id_list = request.POST.getlist('employee_id')
            designation_list = request.POST.getlist('designation')
            company_name_list = request.POST.getlist('company_name')
            start_date_list = request.POST.getlist('start_date')
            end_date_list = request.POST.getlist('end_date')
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            for i in range(0, len(emp_id_list)):
                print("EMP DAATA", emp_id_list[i], designation_list[i], company_name_list[i], start_date_list[i],
                      end_date_list[i])
                try:
                    employment_obj = models.Employment.objects.get(offender_id=offender_obj, employee_id=emp_id_list[i])
                    employment_obj.employee_id = emp_id_list[i]
                    employment_obj.designation = designation_list[i]
                    employment_obj.company_name = company_name_list[i]
                    employment_obj.start_date = start_date_list[i]
                    employment_obj.end_date = end_date_list[i]
                    employment_obj.save()
                except models.Employment.DoesNotExist:
                    models.Employment.objects.create(offender_id=offender_obj, employee_id=emp_id_list[i],
                                                     designation=designation_list[i],
                                                     company_name=company_name_list[i],
                                                     start_date=start_date_list[i],
                                                     end_date=end_date_list[i])
            messages.success(request, "Offender Employment Information Updated")
            return redirect('employment')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('employment')
    return render(request, "employment.html", {})


@login_required(login_url='login')
def delete_employment(request, id):
    emp_queryset = models.Employment.objects.get(id=id)
    emp_queryset.delete()
    messages.success(request, "Offender Employment Information Deleted")
    return redirect('employment')


@login_required(login_url='login')
def education(request):
    if request.method == "POST":
        try:
            data = request.POST
            print("data", data)
            course_type_list = request.POST.getlist('course_type')
            institute_name_list = request.POST.getlist('institute_name')
            branch_list = request.POST.getlist('branch')
            start_date_list = request.POST.getlist('start_date')
            end_date_list = request.POST.getlist('end_date')
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            for i in range(0, len(course_type_list)):
                try:
                    education_obj = models.Education.objects.get(offender_id=offender_obj,
                                                                 institute_name=institute_name_list[i],
                                                                 course_type=course_type_list[i])
                    education_obj.course_type = course_type_list[i]
                    education_obj.institute_name = institute_name_list[i]
                    education_obj.branch = branch_list[i]
                    education_obj.start_date = start_date_list[i]
                    education_obj.end_date = end_date_list[i]
                    education_obj.save()
                except models.Education.DoesNotExist:
                    models.Education.objects.create(offender_id=offender_obj, course_type=course_type_list[i],
                                                    institute_name=institute_name_list[i],
                                                    branch=branch_list[i], start_date=start_date_list[i],
                                                    end_date=end_date_list[i])
            messages.success(request, "Offender Education Information Updated")
            return redirect('education')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('education')
    return render(request, "education.html", {})


@login_required(login_url='login')
def delete_education(request, id):
    emp_queryset = models.Education.objects.get(id=id)
    emp_queryset.delete()
    messages.success(request, "Offender Education Information Deleted")
    return redirect('education')


@login_required(login_url='login')
def admission(request):
    if request.method == "POST":
        data = request.POST
        try:
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            personal_obj = models.Admission.objects.get(offender_id=offender_obj)
            personal_obj.admission_date = data["admission_date"]
            personal_obj.from_location = data["from_location"]
            personal_obj.to_location = data["to_location"]
            personal_obj.reason = data["reason"]
            personal_obj.save()
            messages.success(request, "Offender Admission Information Updated")
            return redirect('admission')
        except models.Admission.DoesNotExist:
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            models.Admission.objects.create(offender_id=offender_obj,
                                            admission_date=data["admission_date"],
                                            from_location=data["from_location"],
                                            to_location=data["to_location"],
                                            reason=data["reason"])
            messages.success(request, "Offender Admission Information Added")
            return redirect('admission')
        except Exception as e:
            print("EX", str(e))
            messages.error(request, str(e))
            return redirect('admission')
    return render(request, "admission.html", {})


@login_required(login_url='login')
def medical_health(request):
    if request.method == "POST":
        try:
            data = request.POST
            print("data", data)
            medical_id_list = request.POST.getlist('medical_id') or []
            print("MEDICAL LIST", medical_id_list)
            health_issue_list = request.POST.getlist('health_issue')
            status_list = request.POST.getlist('status')
            condition_list = request.POST.getlist('condition')
            effective_date_list = request.POST.getlist('effective_date')
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            for i in range(0, len(health_issue_list)):
                if medical_id_list[i] != "":
                    print("ENTERED IF")
                    employment_obj = models.MedicalHealth.objects.get(offender_id=offender_obj,
                                                                      medical_id=medical_id_list[i])
                    employment_obj.health_issue = health_issue_list[i]
                    employment_obj.status = status_list[i]
                    employment_obj.condition = condition_list[i]
                    employment_obj.effective_date = effective_date_list[i]
                    employment_obj.save()
                else:
                    print("ENTERED ELSE")
                    medical_obj = models.MedicalHealth.objects.last()
                    medical_cnt = 0
                    if medical_obj:
                        medical_cnt = medical_obj.medical_id[3:]
                    print("MEDICA", medical_cnt)
                    medical_id = "MED{0:0=4d}".format(int(medical_cnt) + 1)
                    print("MEDICAL ID", medical_id)
                    models.MedicalHealth.objects.create(offender_id=offender_obj, health_issue=health_issue_list[i],
                                                        status=status_list[i], medical_id=medical_id,
                                                        condition=condition_list[i],
                                                        effective_date=effective_date_list[i])
            messages.success(request, "Offender Medical Health Information Updated")
            return redirect('medical_health')
        except Exception as e:
            print("EXCEPTION", str(e))
            messages.error(request, str(e))
            return redirect('medical_health')
    return render(request, "medical_health.html", {"health_status": choices.health_status_list,
                                                   "health_condition": choices.health_condition_list})


@login_required(login_url='login')
def delete_medical_health(request, medical_id):
    emp_queryset = models.MedicalHealth.objects.get(medical_id=medical_id)
    emp_queryset.delete()
    messages.success(request, "Offender Medical Information Deleted")
    return redirect('medical_health')


def register(request):
    if request.method == 'POST':
        data = request.POST
        user_cnt = models.User.objects.all().count()
        user_id = int(user_cnt) + 1
        investigator, judge = 0, 0
        if data.get("user_type") == "judge":
            judge = 1
        if data.get("user_type") == "investigator":
            investigator = 1
        user_obj = models.User.objects.create(user_id=user_id, first_name=data["first_name"],
                                              last_name=data["last_name"], is_judge=judge, is_investigator=investigator,
                                              username=data["email"], is_active=True, gender=data["gender"],
                                              dob=data["dob"], email=data["email"], last_login=datetime.now(),
                                              password=make_password(data["password"]))
        if user_obj:
            if judge:
                messages.success(request, "Judge Registered Successfully")
                return redirect('judge_login')
            messages.success(request, "Investigator Registered Successfully")
            return redirect('login')
        messages.error(request, "Failed to Register")
        return redirect('login')
    return render(request, 'register.html', {})


@login_required(login_url='login')
def court_appointments(request):
    if request.method == "POST":
        try:
            data = request.POST
            print("data", data)
            appointment_id_list = request.POST.getlist('appointment_id') or []
            print("MEDICAL LIST", appointment_id_list)
            scheduled_datetime_list = request.POST.getlist('scheduled_datetime')
            reason_list = request.POST.getlist('reason')
            court_list = request.POST.getlist('court')
            status_list = request.POST.getlist('status')
            judge_name_list = request.POST.getlist('judge_name')
            assigned_officers_list = request.POST.getlist('assigned_officers')
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            for i in range(0, len(court_list)):
                if appointment_id_list[i] != "":
                    print("ENTERED IF")
                    employment_obj = models.CourtAppointments.objects.get(offender_id=offender_obj,
                                                                          appointment_id=appointment_id_list[i])
                    employment_obj.scheduled_datetime = scheduled_datetime_list[i]
                    employment_obj.reason = reason_list[i]
                    employment_obj.court = court_list[i]
                    employment_obj.judge_name = judge_name_list[i]
                    employment_obj.status = status_list[i]
                    employment_obj.assigned_officers = assigned_officers_list[i]
                    employment_obj.save()
                else:
                    print("ENTERED ELSE")
                    medical_cnt = models.CourtAppointments.objects.all().count()
                    appointment_id = "CA{0:0=4d}".format(int(medical_cnt) + 1)
                    models.CourtAppointments.objects.create(offender_id=offender_obj, appointment_id=appointment_id,
                                                            reason=reason_list[i], status=status_list[i],
                                                            court=court_list[i], judge_name=judge_name_list[i],
                                                            assigned_officers=assigned_officers_list[i],
                                                            scheduled_datetime=scheduled_datetime_list[i])
            messages.success(request, "Court Appointment Information Updated")
            return redirect('court_appointments')
        except Exception as e:
            print("EXCEPTION", str(e))
            messages.error(request, str(e))
            return redirect('court_appointments')
    return render(request, "court_appointments.html", {})


@login_required(login_url='login')
def delete_court_appointment(request, appointment_id):
    emp_queryset = models.CourtAppointments.objects.get(appointment_id=appointment_id)
    emp_queryset.delete()
    messages.success(request, "Offender Court Appointment Deleted")
    return redirect('court_appointments')


@login_required(login_url='login')
def incident(request):
    if request.method == "POST":
        data = request.POST
        try:
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            personal_obj = models.Incident.objects.get(offender_id=offender_obj)
            personal_obj.incident_type = data["incident_type"]
            personal_obj.reported_by = data["reported_by"]
            personal_obj.reported_date = data["reported_date"]
            personal_obj.incident_details = data["incident_details"]
            personal_obj.save()
            messages.success(request, "Offender Incident Details Updated")
            return redirect('incident')
        except models.Incident.DoesNotExist:
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            models.Incident.objects.create(offender_id=offender_obj,
                                           incident_type=data["incident_type"],
                                           reported_by=data["reported_by"],
                                           reported_date=data["reported_date"],
                                           incident_details=data["incident_details"])
            messages.success(request, "Offender Incident Information Added")
            return redirect('incident')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('incident')
    return render(request, "incident.html", {})


@login_required(login_url='login')
def action_plan(request):
    if request.method == "POST":
        try:
            data = request.POST
            print("data", data)
            action_plan_id_list = request.POST.getlist('action_plan_id') or []
            print("MEDICAL LIST", action_plan_id_list)
            startdate_list = request.POST.getlist('startdate')
            enddate_list = request.POST.getlist('enddate')
            programnotes_list = request.POST.getlist('programnotes')
            category_list = request.POST.getlist('category')
            case_worksteps_list = request.POST.getlist('case_worksteps')
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            for i in range(0, len(category_list)):
                if action_plan_id_list[i] != "":
                    print("ENTERED IF")
                    employment_obj = models.ActionPlan.objects.get(offender_id=offender_obj,
                                                                   action_plan_id=action_plan_id_list[i])
                    employment_obj.case_worksteps = case_worksteps_list[i]
                    employment_obj.category = category_list[i]
                    employment_obj.programnotes = programnotes_list[i]
                    employment_obj.startdate = startdate_list[i]
                    employment_obj.enddate = enddate_list[i]
                    employment_obj.save()
                else:
                    print("ENTERED ELSE")
                    medical_obj = models.ActionPlan.objects.last()
                    medical_cnt = 0
                    if medical_obj:
                        medical_cnt = medical_obj.action_plan_id[2:]
                    print("MEDICA", medical_cnt)
                    appointment_id = "AC{0:0=4d}".format(int(medical_cnt) + 1)
                    print("MEDICAL ID", appointment_id)
                    models.ActionPlan.objects.create(offender_id=offender_obj, action_plan_id=appointment_id,
                                                     case_worksteps=case_worksteps_list[i],
                                                     category=category_list[i],
                                                     programnotes=programnotes_list[i], startdate=startdate_list[i],
                                                     enddate=enddate_list[i])
            messages.success(request, "Action Plan Information Updated")
            return redirect('action_plan')
        except Exception as e:
            print("EXCEPTION", str(e))
            messages.error(request, str(e))
            return redirect('action_plan')
    return render(request, "action_plan.html", {})


@login_required(login_url='login')
def delete_action_plan(request, action_plan_id):
    emp_queryset = models.ActionPlan.objects.get(action_plan_id=action_plan_id)
    emp_queryset.delete()
    messages.success(request, "Offender Action Plan Deleted")
    return redirect('action_plan')
    zZZZZxzzzzzzzz


@login_required(login_url='login')
def case_plan(request):
    if request.method == "POST":
        try:
            data = request.POST
            print("data", data)
            case_plan_id_list = request.POST.getlist('case_plan_id') or []
            print("MEDICAL LIST", case_plan_id_list)
            created_date_time_list = request.POST.getlist('created_date_time')
            status_list = request.POST.getlist('status')
            location_list = request.POST.getlist('location')
            officer_list = request.POST.getlist('officer')
            custody_location_list = request.POST.getlist('custody_location')
            result_list = request.POST.getlist('result')
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            for i in range(0, len(officer_list)):
                if case_plan_id_list[i] != "":
                    print("ENTERED IF")
                    employment_obj = models.CasePlan.objects.get(offender_id=offender_obj,
                                                                 case_plan_id=case_plan_id_list[i])
                    employment_obj.created_date_time = created_date_time_list[i]
                    employment_obj.status = status_list[i]
                    employment_obj.location = location_list[i]
                    employment_obj.officer = officer_list[i]
                    employment_obj.custody_location = custody_location_list[i]
                    employment_obj.result = result_list[i]
                    employment_obj.save()
                else:
                    print("ENTERED ELSE")
                    medical_obj = models.CasePlan.objects.last()
                    medical_cnt = 0
                    if medical_obj:
                        medical_cnt = medical_obj.case_plan_id[2:]
                    print("MEDICA", medical_cnt)
                    case_plan_id = "CP{0:0=4d}".format(int(medical_cnt) + 1)
                    print("MEDICAL ID", case_plan_id)
                    models.CasePlan.objects.create(offender_id=offender_obj, case_plan_id=case_plan_id,
                                                   created_date_time=created_date_time_list[i],
                                                   status=status_list[i], result=result_list[i],
                                                   location=location_list[i], officer=officer_list[i],
                                                   custody_location=custody_location_list[i])
            messages.success(request, "Case Plan Information Updated")
            return redirect('case_plan')
        except Exception as e:
            print("EXCEPTION", str(e))
            messages.error(request, str(e))
            return redirect('case_plan')
    return render(request, "case_plan.html", {})


@login_required(login_url='login')
def delete_case_plan(request, case_plan_id):
    emp_queryset = models.CasePlan.objects.get(case_plan_id=case_plan_id)
    emp_queryset.delete()
    messages.success(request, "Offender Case Plan Deleted")
    return redirect('case_plan')


@login_required(login_url='login')
def release(request):
    if request.method == "POST":
        data = request.POST
        try:
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            personal_obj = models.Release.objects.get(offender_id=offender_obj)
            personal_obj.release_date_time = data["release_date_time"]
            personal_obj.status = data["status"]
            personal_obj.save()
            messages.success(request, "Offender Release Details Updated")
            return redirect('incident')
        except models.Release.DoesNotExist:
            offender_obj = models.Offender.objects.get(offender_id=data["offender_id"])
            models.Release.objects.create(offender_id=offender_obj,
                                          release_date_time=data["release_date_time"],
                                          status=data["status"])
            messages.success(request, "Offender Incident Information Added")
            return redirect('release')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('release')
    return render(request, "release.html", {})
