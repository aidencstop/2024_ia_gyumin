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

    # Assuming the user is already authenticated
    user_instance = request.user

    if Student.objects.filter(user=user_instance).exists():
        messages.warning(request, "You have already completed the registration.")
        return redirect('student-main')

    if request.method == 'POST':
        grade = request.POST.get('grade')
        uni = request.POST.get('university')
        mjr = request.POST.get('major')
        cat = request.POST.get('category')
        act = request.POST.getlist('activity')
        startdate = request.POST.get('start-date')
        enddate = request.POST.get('end-date')
        description = request.POST.get('description')

        if not all([grade, uni, mjr]):
            messages.error(request, "Please fill out all the required fields!")
            return redirect('student-initial')

        startdate = datetime.strptime(startdate, '%d-%m-%Y').date()
        enddate = datetime.strptime(enddate, '%d-%m-%Y').date()

        university_instance = get_object_or_404(University, name=uni)
        major_instance = get_object_or_404(Major, name=mjr)
        cat_instance = get_object_or_404(Category, name=cat)
        activities = [get_object_or_404(Activity, name=name) for name in act]

        student = Student(user=user_instance, grade=grade, university=university_instance, major=major_instance, category=cat_instance, start_date=startdate, end_date=enddate, description=description)
        student.save()

        student.activity.set(activities)

        messages.success(request, "Registration Successful!")
        return redirect('student-main')

    context = {
        'major': major,
        'university': university,
        'category': category,
        'activity': activity,
        'GRADE_CHOICES': Student.GRADE_CHOICES,
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

    # Get the student instance for the authenticated user
    student_instance = get_object_or_404(Student, user=user_instance)

    if request.method == 'POST':
        grade = request.POST.get('grade')
        university_id = request.POST.get('university')
        major_id = request.POST.get('major')
        category_id = request.POST.get('category')
        activity_ids = request.POST.getlist('activity')
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        description = request.POST.get('description')

        # Update the student instance with the new data
        student_instance.grade = grade
        student_instance.university_id = university_id
        student_instance.major_id = major_id
        student_instance.category_id = category_id
        student_instance.activity.set(activity_ids)
        student_instance.start_date = start_date
        student_instance.end_date = end_date
        student_instance.description = description

        # Save the updated instance
        student_instance.save()

        messages.success(request, "Details updated successfully!")
        return redirect('student-main')

    # Get all activities
    all_activities = Activity.objects.all()

    # Pass selected activities to the template context
    selected_activities = student_instance.activity.all()

    context = {
        'student_instance': student_instance,
        'selected_activities': selected_activities,
        'all_activities': all_activities,
    }
    return render(request, 'student_edit.html', context)

# View function for student recommendation
@login_required
def student_recommendation(request):
    # Assuming you have a way to get the current user
    user_instance = request.user

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
