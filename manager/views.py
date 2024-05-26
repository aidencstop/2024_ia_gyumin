from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *;
from student.models import Student

# Create your views here.

# View function for manager login
def manager_login(request):
    # Redirect to manager-main page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('manager-main')
    
    # Handling form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            # Check if the user is a manager
            if user.role == 'manager':
                print("manager found")
                # Authenticate user
                authenticated_user = authenticate(request, username=username, password=password)
                print("user authenticated")

                # If authentication successful, login user
                if authenticated_user:
                    print("user authenticated")
                    login(request, authenticated_user)
                    print("user logged in")
                    return redirect('manager-main')
                else:
                    messages.error(request, "Invalid login credentials")
                    print("Invalid credentials")
                    return redirect('manager-login')

            else:
                messages.error(request, "Invalid Role!")
                return redirect('manager-login')
        
        except CustomUser.DoesNotExist:
            # Handle non-existing user
            messages.error(request, "User does not exist")
            print("User does not exist")
            return redirect('manager-login')

    # Render login page if request method is GET
    return render(request, 'manager_login.html', {})

# View function for counselor logout
@login_required
def manager_logout(request):
    logout(request)
    return redirect('home')

# View function for manager main page
@login_required
def manager_main(request):
    nameuser = request.user.username

    context = {
        'nameuser' : nameuser
    }
    return render(request, 'manager_main.html', context)

# View function for adding a new counselor
@login_required
def manager_addcounselor(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('user-username')
        password = request.POST.get('user-password')
        confirm_password = request.POST.get('user-confirm-password')
        name = request.POST.get('user-name')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('manager-addcounselor')

        # Check if all required fields are filled
        if not all([username, password, confirm_password, name]):
            messages.error(request, "Please fill out all the required fields!")
            return redirect('manager-addcounselor')

        # Check if password matches confirm password
        if password == confirm_password:
            # Hash password and create new user
            hashed_password = make_password(password)
            new_user = CustomUser(username=username, password=hashed_password, name=name, role='counselor')
            new_user.save()
            messages.success(request, "User added successfully!")
            return redirect('manager-addcounselor')

        else:
            messages.error(request, "Password doesn't match. Please try again!")
            return redirect('manager-addcounselor')

    return render(request, 'manager_addcounselor.html', {})


@login_required
def manager_counselorlist(request):
    if request.method == 'POST':
        if 'ok' in request.POST:
            del_pk = request.POST.get('ok')
            del_counselor = CustomUser.objects.get(pk=del_pk)
            del_counselor.is_active = False
            del_counselor.save()
            return redirect('manager-counselorlist')


    counselors = CustomUser.objects.filter(role='counselor', is_active=True)
    for c in counselors:
        print(c.name)
    counselor_pk_list = [c.pk for c in counselors]
    print(counselor_pk_list)
    context = {
        'counselors': counselors,
        'counselor_pk_list': counselor_pk_list,
    }
    return render(request, 'manager_manageuserscounselor.html', context)

@login_required
def manager_studentlist(request):
    if request.method == 'POST':
        if 'ok' in request.POST:
            del_pk = request.POST.get('ok')
            del_student = Student.objects.get(pk=del_pk)
            del_student.is_active = False
            del_student.save()
            return redirect('manager-studentlist')
    students = Student.objects.filter(is_active=True)
    student_pk_list = [s.pk for s in students]
    print(student_pk_list)
    context = {
        'students': students,
        'student_pk_list': student_pk_list,
    }
    return render(request, 'manager_manageusersstudent.html', context)

# View function for adding a new user
@login_required
def manager_addnewuser(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('user-username')
        password = request.POST.get('user-pass')
        confirm_password = request.POST.get('user-confirm-pass')
        name = request.POST.get('user-name')
        role = request.POST.get('class-name')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('manager-addnewuser')

        # Check if all required fields are filled
        if not all([username, password, confirm_password, name, role]):
            messages.error(request, "Please fill out all the required fields!")
            return redirect('manager-addnewuser')

        # Check if password matches confirm password
        if password == confirm_password:
            # Hash password and create new user
            hashed_password = make_password(password)
            new_user = CustomUser(username=username, password=hashed_password, name=name, role=role)
            new_user.save()
            messages.success(request, "User added successfully!")
            return redirect('manager-addnewuser')

        else:
            messages.error(request, "Password doesn't match. Please try again!")
            return redirect('manager-addnewuser')

    return render(request, 'manager_addnewuser.html', {})

# View function for managing users
@login_required
def manager_manageusers(request):
    users = CustomUser.objects.all()

    context = {'users' : users}
    return render(request, 'manager_manageusers.html', context)

# View function for managing universities
@login_required
def manager_manageuni(request):
    uni = University.objects.all()

    context = {'uni': uni}
    return render(request, 'manager_manageuni.html',context)

# View function for managing majors
@login_required
def manager_managemajors(request):
    major = Major.objects.all()

    context = {'major' : major}
    return render(request, 'manager_managemajors.html', context)

# View function for managing categories and activities
@login_required
def manager_managecatact(request):
    categories = Category.objects.all()
    category_activity_tuples = []
    for category in categories:
        activities = Activity.objects.filter(category=category, is_active=True)
        category_activity_tuples.append((category, activities))
    print(category_activity_tuples)

    context = {
        'category_activity_tuples': category_activity_tuples,
    }

    return render(request, 'manager_managecatact.html', context)

# View function for adding a category
@login_required
def manager_addcat(request):
    if request.method == 'POST':
        cat_name = request.POST.get('cat-name')
        Category.objects.create(name = cat_name)
        return redirect('manager-managecatact')

    return render(request, 'manager_addcat.html', {})

# View function for adding an activity
@login_required
def manager_addact(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        act_name = request.POST.get('act-name')
        cat_id = request.POST.get('cat-name')  # Get the selected category ID from the form

        # Check if the selected category ID is valid
        if cat_id:
            category = Category.objects.get(pk=cat_id)
            print(category)
            # Create a new Activity associated with the selected category
            new_activity = Activity.objects.create(name=act_name)
            new_activity.category=category  # Use set() to manage many-to-many relationship
            new_activity.save()
            return redirect('manager-managecatact')

    context = {
        'categories': categories,
    }

    return render(request, 'manager_addact.html', context)

# View function for adding a major
@login_required
def manager_addmajors(request):
    if request.method == 'POST':
        major_name = request.POST.get('major-name')
        Major.objects.create(name = major_name)
        return redirect('manager-managemajors')

    return render(request, 'manager_addmajors.html', {})

# View function for adding a university
@login_required
def manager_adduni(request):
    if request.method == 'POST':
        uni_name = request.POST.get('uni-name')
        University.objects.create(name = uni_name)
        return redirect('manager-manageuni')

    return render(request, 'manager_adduni.html', {})

# View class for deleting a university
class Delete_uni(View):
    def post(self, request, *args, **kwargs):
        uni_ids = request.POST.getlist('id[]')
        for id in uni_ids:
            uni = University.objects.get(pk=id)
            uni.delete()
        return redirect('manager-manageuni')

# View class for deleting a major
class Delete_major(View):
    def post(self, request, *args, **kwargs):
        major_ids = request.POST.getlist('id[]')
        for id in major_ids:
            major = Major.objects.get(pk=id)
            major.delete()
        return redirect('manager-managemajors')

# View class for deleting a category and its associated activities
class Delete_catact(View):
    def post(self, request, *args, **kwargs):
        cat_ids = request.POST.getlist('id[]')
        for id in cat_ids:
            cat = Category.objects.get(pk = id)
            cat.delete()
        return redirect('manager-managecatact')

# View class for deleting a user
class Delete_user(View):
    def post(self, request, *args, **kwargs):
        users_ids = request.POST.getlist('id[]')
        for id in users_ids:
            user = CustomUser.objects.get(pk=id)
            user.delete()
        return redirect('manager-manageusers')

@login_required
def manager_deletecounselor(request, id):
    del_counselor = CustomUser.objects.get(pk=id)
    del_counselor.is_active = False
    del_counselor.save()
    return redirect('manager-counselorlist')

@login_required
def manager_deletestudent(request, id):
    del_student = Student.objects.get(pk=id)
    del_student.is_active = False
    del_student.save()
    return redirect('manager-studentlist')

@login_required
def manager_deleteactivity(request, id):
    del_activity = Activity.objects.get(pk=id)
    del_activity.is_active = False
    del_activity.save()
    return redirect('manager-managecatact')

@login_required
def manager_editactivity(request, id):
    if request.method == 'POST':
        new_activity_name = request.POST.get('new_name')
        activity = Activity.objects.get(pk=id)
        activity.name = new_activity_name
        activity.save()
        return redirect('manager-managecatact')
    activity = Activity.objects.get(pk=id)
    return render(request, 'manager_editactivity.html', {'activity': activity})

@login_required
def manager_addactivity(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = Category.objects.get(pk=category_id)
        new_activity_name = request.POST.get('new_name')
        activity = Activity(name=new_activity_name, category=category)
        activity.save()
        return redirect('manager-managecatact')
    categories = Category.objects.all()
    return render(request, 'manager_addactivity.html', {'categories': categories})