from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from student.models import Student, ActivityExperience  # Importing Student model from student app
from manager.models import CustomUser  # Importing CustomUser model from manager app

# Create your views here.

# View function for counselor login
def counselor_login(request):
    # Redirect to counselor-main page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('counselor-main')
    
    # Handling form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            # Check if the user is a counselor
            if user.role == 'counselor':
                print("counselor found !!")
                # Authenticate user
                authenticated_user = authenticate(request, username=username, password=password)
                print("user authenticated")

                # If authentication successful, login user
                if authenticated_user:
                    print("user authenticated")
                    login(request, authenticated_user)
                    print("user logged in")
                    return redirect('counselor-main')
                else:
                    messages.error(request, "Invalid login credentials")
                    print("Invalid credentials")
                    return redirect('counselor-login')

            else:
                messages.error(request, "Invalid Role!")
                return redirect('counselor-login')
        
        except CustomUser.DoesNotExist:
            # Handle non-existing user
            messages.error(request, "User does not exist")
            print("User does not exist")
            return redirect('counselor-login')

    # Render login page if request method is GET
    return render(request, 'counselor_login.html', {})

# View function for counselor logout
@login_required
def counselor_logout(request):
    logout(request)
    return redirect('home')

# View function for counselor main page
@login_required
def counselor_main(request):
    nameuser = request.user.username

    context = {
        'nameuser' : nameuser,
    }
    return render(request, 'counselor_main.html', context)

# View function for checking students
@login_required
def counselor_checkstudents(request):
    students = Student.objects.all()

    context ={
        'students' : students,
    }
    return render(request, 'counselor_checkstudents.html', context)

# View function for checking details of a student
@login_required
def counselor_checkdetails(request, id):
    students = Student.objects.get(id = id)
    # Get existing record of the student
    existing_activity_experiences = ActivityExperience.objects.filter(student=students).order_by('pk')
    context = {
        'students' : students,
        'existing_activity_experiences': existing_activity_experiences,
    }
    return render(request, 'counselor_checkdetails.html', context)

# View function for displaying student dashboard
@login_required
def counselor_studentdashboard(request):
    students = Student.objects.all()

    context = {
        'students' : students
    }
    return render(request, 'counselor_studentdashboard.html', context)

# View function for displaying detailed information of a student in dashboard
@login_required
def counselor_studdashboarddetail(request, id):
    students = Student.objects.get(id = id)

    context = {
        'students' : students,
    }
    return render(request, 'counselor_studdashboarddetail.html', context)
