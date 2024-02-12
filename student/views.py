from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import *  # Importing models from current app
from manager.models import *  # Importing models from manager app

import json

# Create your views here.

# View function for student login
def student_login(request):
    # Redirect to student-main page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('student-main')
    
    # Handling form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            # Check if the user is a student
            if user.role == 'student':
                print("student found")
                # Authenticate user
                authenticated_user = authenticate(request, username=username, password=password)
                print("user authenticated")

                # If authentication successful, login user
                if authenticated_user:
                    print("user authenticated")
                    login(request, authenticated_user)
                    print("user logged in")
                    return redirect('student-main')
                else:
                    messages.error(request, "Invalid login credentials")
                    print("Invalid credentials")
                    return redirect('student-login')

            else:
                messages.error(request, "Invalid Role!")
                return redirect('student-login')
        
        except CustomUser.DoesNotExist:
            # Handle non-existing user
            messages.error(request, "User does not exist")
            print("User does not exist")
            return redirect('student-login')

    # Render login page if request method is GET
    return render(request, 'student_login.html', {})

# View function for student logout
@login_required
def student_logout(request):
    logout(request)
    return redirect('home')

# View function for student main page
@login_required
def student_main(request):
    nameuser = request.user.username

    context = {'nameuser':nameuser}
    return render(request, 'student_main.html', context)

# View function for student initial registration
@login_required
def student_initial(request):
    major = Major.objects.all()
    university = University.objects.all()
    category = Category.objects.all()
    activity = Activity.objects.all()

    category_id_list = []
    activity_id_list = []
    activity_name_list = []

    for act in activity:
        category_id_list.append(act.category.id)
        activity_id_list.append(act.id)
        activity_name_list.append(act.name)

    # Assuming the user is already authenticated
    user_instance = request.user

    if Student.objects.filter(user=user_instance).exists():
        messages.warning(request, "You have already completed the registration.")
        return redirect('student-main')

    if request.method == 'POST':
        grade = request.POST.get('grade')
        university_id = request.POST.get('university')
        major_id = request.POST.get('major')
        category_id_list = request.POST.getlist('category')
        activity_id_list = request.POST.getlist('activity')
        start_date_list = request.POST.getlist('start-date')
        end_date_list = request.POST.getlist('end-date')
        description_list = request.POST.getlist('description')

        if not all([grade, university_id, major_id]):
            messages.error(request, "Please fill out all the required fields!")
            return redirect('student-initial')

        student = Student(user=user_instance,
                          grade=grade,
                          university=get_object_or_404(University, id=university_id),
                          major=get_object_or_404(Major, id=major_id),
                          )
        student.save()

        # add new activity experiences
        for idx in range(len(category_id_list)):
            curr_category = get_object_or_404(Category, id=category_id_list[idx])
            curr_activity = get_object_or_404(Activity, id=activity_id_list[idx])
            curr_start_date = start_date_list[idx]
            curr_end_date = end_date_list[idx]
            curr_description = description_list[idx]
            # print(curr_category)
            # print(curr_activity)
            # print(curr_start_date)
            # print(curr_end_date)
            # print(curr_description)

            ae = ActivityExperience(
                student=student,
                category=curr_category,
                activity=curr_activity,
                start_date=curr_start_date,
                end_date=curr_end_date,
                description=curr_description,
            )
            # student = Student(user=user_instance, grade=grade, university=university_instance, major=major_instance,
            #                   category=cat_instance, start_date=startdate, end_date=enddate, description=description)
            ae.save()



        messages.success(request, "Registration Successful!")
        return redirect('student-main')

    context = {
        'major': major,
        'university': university,
        'category': category,
        'activity': activity,
        'GRADE_CHOICES': Student.GRADE_CHOICES,
        'category_id_list': json.dumps(category_id_list),
        'activity_id_list': json.dumps(activity_id_list),
        'activity_name_list': json.dumps(activity_name_list),
    }
    return render(request, 'student_initial.html', context)

# View function for fetching activities based on category
def fetch_activities(request):
    category_id = request.GET.get('category_id')
    # Fetch activities based on the category_id (implement as needed)
    activities = [{'id': 1, 'name': 'Activity 1'}, {'id': 2, 'name': 'Activity 2'}]
    return JsonResponse({'activities': activities})

# View function for student profile editing
@login_required
def student_edit(request):
    # Assuming the user is already authenticated
    user_instance = request.user

    if not Student.objects.filter(user=user_instance).exists():
        messages.warning(request, "You have not completed the initial registration.")
        return redirect('student-main')

    # Get the student instance for the authenticated user
    student_instance = get_object_or_404(Student, user=user_instance)

    # Get existing record of the student
    existing_activity_experiences = ActivityExperience.objects.filter(student=student_instance).order_by('pk')


    major = Major.objects.all()
    university = University.objects.all()
    category = Category.objects.all()
    activity = Activity.objects.all()
    category_activity_tuples = [(category, category.activity_set.all()) for category in category]
    category_activity_dict = {}
    for t in category_activity_tuples:
        if t[0] in category_activity_dict.keys():
            pass
        else:
            category_activity_dict[t[0]] = []
        for tt in t[1]:
            category_activity_dict[t[0]].append(tt)
    # print(category_activity_dict)



    if request.method == 'POST':
        grade = request.POST.get('grade')
        university_id = request.POST.get('university')
        major_id = request.POST.get('major')
        category_id_list = request.POST.getlist('category')
        activity_id_list = request.POST.getlist('activity')
        start_date_list = request.POST.getlist('start-date')
        end_date_list = request.POST.getlist('end-date')
        description_list = request.POST.getlist('description')

        # Update the student instance with the new data
        student_instance.grade = grade
        student_instance.university_id = university_id
        student_instance.major_id = major_id

        new_activity_experiences = []
        # update existing activity experiences
        eae_cnt = len(existing_activity_experiences)
        for idx in range(eae_cnt):
            curr_eae = existing_activity_experiences[idx]
            curr_category = get_object_or_404(Category, id=category_id_list[idx])
            curr_activity = get_object_or_404(Activity, id=activity_id_list[idx])
            curr_start_date = start_date_list[idx]
            curr_end_date = end_date_list[idx]
            curr_description = description_list[idx]

            curr_eae.category = curr_category
            curr_eae.activity = curr_activity
            curr_eae.start_date = curr_start_date
            curr_eae.end_date = curr_end_date
            curr_eae.description = curr_description
            curr_eae.save()

        # add new activity experiences
        for idx in range(eae_cnt, len(category_id_list)):

            curr_category = get_object_or_404(Category, id=category_id_list[idx])
            curr_activity = get_object_or_404(Activity, id=activity_id_list[idx])
            curr_start_date = start_date_list[idx]
            curr_end_date = end_date_list[idx]
            curr_description = description_list[idx]
            # print(curr_category)
            # print(curr_activity)
            # print(curr_start_date)
            # print(curr_end_date)
            # print(curr_description)

            ae = ActivityExperience(
                student=student_instance,
                category=curr_category,
                activity=curr_activity,
                start_date=curr_start_date,
                end_date=curr_end_date,
                description=curr_description,
            )
            # student = Student(user=user_instance, grade=grade, university=university_instance, major=major_instance,
            #                   category=cat_instance, start_date=startdate, end_date=enddate, description=description)
            ae.save()

        # Save the updated instance
        student_instance.save()

        messages.success(request, "Details updated successfully!")
        return redirect('student-main')

    # Get all activities
    all_activities = Activity.objects.all()

    # Pass selected activities to the template context
    selected_activities = student_instance.activity.all()

    category_id_list = []
    activity_id_list = []
    activity_name_list = []

    for act in activity:
        category_id_list.append(act.category.id)
        activity_id_list.append(act.id)
        activity_name_list.append(act.name)

    print(category_id_list)
    print(activity_id_list)
    print(activity_name_list)
    print(json.dumps(category_id_list))
    context = {
        'GRADE_CHOICES': Student.GRADE_CHOICES,
        'curr_grade': Student.GRADE_CHOICES[student_instance.grade-1],
        'curr_univ': University.objects.get(pk=student_instance.university_id),
        'curr_major': Major.objects.get(pk=student_instance.major_id),
        'major': major,
        'university': university,
        'category': category,
        # 'category_json': json.dumps(category),
        'activity': activity,
        'category_activity_tuples': category_activity_tuples,
        'category_id_list': json.dumps(category_id_list),
        'activity_id_list': json.dumps(activity_id_list),
        'activity_name_list': json.dumps(activity_name_list),
        'student_instance': student_instance,
        'selected_activities': selected_activities,
        'all_activities': all_activities,
        'existing_activity_experiences': existing_activity_experiences,
    }


    return render(request, 'student_edit.html', context)

# View function for student recommendation
@login_required
def student_recommendation(request):
    # Assuming you have a way to get the current user
    user_instance = request.user

    if not Student.objects.filter(user=user_instance).exists():
        messages.warning(request, "You have not completed the initial registration.")
        return redirect('student-main')

    # Assuming you have a way to associate a Student with a user
    student_instance = Student.objects.get(user=user_instance)

    context = {
        'student_instance': student_instance,
        # Add other context variables if needed
    }

    return render(request, 'student_recommendation.html', context)

# View function for generating PDF of student recommendation
@login_required
def student_recommendation_pdf(request):
    # Assuming you have a way to get the current user
    user_instance = request.user

    # Assuming you have a way to associate a Student with a user
    student_instance = get_object_or_404(Student, user=user_instance)

    context = {
        'student_instance': student_instance,
        # Add other context variables if needed
    }

    # Render the recommendation page as PDF
    template = get_template('student_recommendation.html')
    html = template.render(context)

    # Create a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_recommendation.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(
        html, dest=response,
        encoding='utf-8'
    )

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
