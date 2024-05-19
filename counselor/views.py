from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from student.models import Student, ActivityExperience  # Importing Student model from student app
from manager.models import *  # Importing CustomUser model from manager app
import json

import os
from openai import OpenAI


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
def counselor_checkstudents(request, year):
    students = Student.objects.all()

    if year==0:
        pass
    else:
        students = Student.objects.filter(grade=year).order_by('pk')
    context ={
        'students' : students,
        'year': year,
        'year_list': [0, 10, 11, 12, 13],
    }
    return render(request, 'counselor_studentlist.html', context)


# View function for edit students
@login_required
@csrf_exempt
def counselor_editstudents(request, id):
    # Assuming the user is already authenticated
    students = Student.objects.get(id = id)



    # Get the student instance for the authenticated user
    student_instance = students

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
        if 'save' in request.POST:
            grade = request.POST.get('grade')
            university_id = request.POST.get('university')
            major_id = request.POST.get('major')
            category_id_list = request.POST.getlist('category')
            activity_id_list = request.POST.getlist('activity')
            start_date_list = request.POST.getlist('start-date')
            end_date_list = request.POST.getlist('end-date')
            description_list = request.POST.getlist('description')
            print("" in start_date_list)
            if "" in start_date_list or "" in end_date_list or "" in description_list:
                messages.success(request, "You should fill all the details of activities.")
                redirect('counselor-checkstudents',0)
            print(category_id_list)
            print(activity_id_list)
            print(start_date_list)
            print(end_date_list)
            print(description_list)
            # Update the student instance with the new data
            student_instance.grade = grade
            student_instance.university_id = university_id
            student_instance.major_id = major_id

            new_activity_experiences = []
            # update existing activity experiences
            eae_cnt = len(existing_activity_experiences)
            print(eae_cnt)
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
            return redirect('counselor-checkstudents',0)

    # Get all activities
    all_activities = Activity.objects.all()

    # Pass selected activities to the template context
    # selected_activities = student_instance.activity.all()

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
        'curr_name': student_instance.name,
        'GRADE_CHOICES': Student.GRADE_CHOICES,
        'curr_grade': Student.GRADE_CHOICES[student_instance.grade-10],
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
        # 'selected_activities': selected_activities,
        'all_activities': all_activities,
        'existing_activity_experiences': existing_activity_experiences,
    }

    return render(request, 'counselor_editstudents.html', context)

# View function for checking details of a student
@login_required
def counselor_checkdetails(request, id):
    student = Student.objects.get(id = id)
    # Get existing record of the student
    existing_activity_experiences = ActivityExperience.objects.filter(student=student).order_by('pk')
    category = Category.objects.all().order_by('pk')
    eae_categories = []
    for eae in existing_activity_experiences:
        if eae.category in eae_categories:
            continue
        else:
            eae_categories.append(eae.category)
    categories = []
    for cat in category:
        if cat in eae_categories:
            categories.append(cat)

    context = {
        'student': student,
        'categories': categories,
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


def calculate_strength_with_subjects(major, subject_list):
    major_subject_dict = {
        'Statistics': ['Analysis and approaches', 'Applications and interpretation'],
        'Business': ['Business management'],
        'Computer Science': ['Computer science'],
        'Psychology': ['Psychology'],
    }
    fail_list = []
    for major_subject in major_subject_dict[major]:
        if major_subject not in subject_list:
            fail_list.append(major_subject)

    if len(fail_list) == 0:
        return 1, fail_list
    else:
        return 0, fail_list


# View function for displaying detailed information of a student in dashboard
@login_required
def counselor_studdashboarddetail(request, id):
    student = Student.objects.get(id = id)
    ib_subject_dict = {
        "Psychology": "Group 3: Psychology",
        "Statistics": "Group 5: Applications and Interpretation",
        "Business": "Group 3: Business management",
        "Computer Science": "Group 4: Computer Science",
    }
    ib_subject = ib_subject_dict[student.major.name]

    activity_trait_dict = {
        "subjects": "\'getting interest in one's career path and actively seeks to learn related knowledge\'",
        "awards": "\'making an efforts to achieve a goal and achieve results\'",
        "isa": "\'showing interest in community problems and trying to solve them together\'",
        "ea": "\'seeking self-directed development beyond the given curriculum\'",
        "va": "\'willingness to dedicate oneself to helping others\'",
    }

    OPENAI_API_KEY = "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"
    client = OpenAI(
        # This is the default and can be omitted
        # api_key=os.environ.get("OPENAI_API_KEY"),
        api_key="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"
    )

    # get IB IA title
    title_query ="Recommend me a title for IB IA for "+ib_subject+". The subject should be appropriate for high-school student to research and should be related with "+student.major.name.lower()+". Just answer one clear title only(it must not have anything like '[specific topic]'), and don't say anything else."

    title_chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": json.dumps(title_query),
            }
        ],
        model="gpt-3.5-turbo",
    )
    ib_ia_title = title_chat_completion.choices[0].message.content.strip("\"")

    existing_activity_experiences = ActivityExperience.objects.filter(student=student).order_by('pk')

    category_subjects = Category.objects.get(name='Subjects')
    category_awards = Category.objects.get(name='Awards')
    category_isa = Category.objects.get(name='In-school Activities')
    category_ea = Category.objects.get(name='Extracurricular Activities')
    category_va = Category.objects.get(name='Volunteer Activities')

    existing_subjects = ActivityExperience.objects.filter(student=student, category=category_subjects).order_by('pk')
    existing_awards = ActivityExperience.objects.filter(student=student, category=category_awards).order_by('pk')
    existing_isa = ActivityExperience.objects.filter(student=student, category=category_isa).order_by('pk')
    existing_ea = ActivityExperience.objects.filter(student=student, category=category_ea).order_by('pk')
    existing_va = ActivityExperience.objects.filter(student=student, category=category_va).order_by('pk')


    existing_subjects_names = [es.activity.name for es in existing_subjects]
    subjects_strength, fail_subject_list = calculate_strength_with_subjects(student.major.name, existing_subjects_names)
    awards_strength = 1 if len(existing_awards) > 0 else 0
    isa_strength = 1 if len(existing_isa) > 0 else 0
    ea_strength = 1 if len(existing_ea) > 0 else 0
    va_strength = 1 if len(existing_va) > 0 else 0

    strength = []
    weakness = []

    total_query = '''Now I'm giving you five questions. Answer for each question.
    '''

    # subjects strength/weakness text
    if subjects_strength == 1:
        subjects_query = "1. Please write a sentence stating that the courses the student has currently completed are sufficient to apply to the desired major, \'"+student.major.name+"\'. You must also mention that the student's "+activity_trait_dict['subjects']+" is clearly revealed through the subjects completed."
    else:
        subjects_query = "1. Please write a sentence stating that the courses the student has currently completed are not sufficient to apply to the desired major, \'"+student.major.name+"\'. You must also mention that the student's "+activity_trait_dict['subjects']+" will be well revealed if the student completes the subject, especially \'"+fail_subject_list[0]+"\'."

    total_query += subjects_query
    # subjects_chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": json.dumps(subjects_query),
    #         }
    #     ],
    #     model="gpt-3.5-turbo",
    # )
    # subjects_result = subjects_chat_completion.choices[0].message.content.strip("\"")
    #
    # if subjects_strength == 1:
    #     strength.append(subjects_result)
    # else:
    #     weakness.append(subjects_result)

    # awards strength/weakness text
    if awards_strength == 1:
        awards_query = "2. Please write a sentence stating that the current student's awards are sufficient to apply to the desired school, "+student.university.name+". Please also mention that the student's award history reflects the student's "+activity_trait_dict['awards']+"."
    else:
        awards_query = "2. Please write a sentence stating that the current student's award history is not sufficient to apply to the desired school, "+student.university.name+". Please also mention that adding a few more awards will highlight the student's "+activity_trait_dict['awards']+"."

    total_query += awards_query

    # awards_chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": json.dumps(awards_query),
    #         }
    #     ],
    #     model="gpt-3.5-turbo",
    # )
    # awards_result = awards_chat_completion.choices[0].message.content.strip("\"")
    #
    # if awards_strength == 1:
    #     strength.append(awards_result)
    # else:
    #     weakness.append(awards_result)

    # isa strength/weakness text
    if isa_strength == 1:
        isa_query = "3. Please write a sentence explaining that the student's in-school activities meet the standards of the desired school, "+student.university.name+". Please also mention that the student's in-school activities can show the student's "+activity_trait_dict['isa']+"."
    else:
        isa_query = "3. Please write a sentence explaining that the student's in-school activities are somewhat lacking compared to the standards of the desired school, "+student.university.name+". Please also mention that if the student adds in-school activities, the student can show the student's "+activity_trait_dict['isa']+"."

    total_query += isa_query

    # isa_chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": json.dumps(isa_query),
    #         }
    #     ],
    #     model="gpt-3.5-turbo",
    # )
    # isa_result = isa_chat_completion.choices[0].message.content.strip("\"")
    #
    # if isa_strength == 1:
    #     strength.append(isa_result)
    # else:
    #     weakness.append(isa_result)

    # ea strength/weakness text
    if ea_strength == 1:
        ea_query = "4. Write a sentence explaining that the student's extracurricular activities meet the standards of the desired school, "+student.university.name+". Also mention that the student's extracurricular activities can show the student's "+activity_trait_dict['ea']+"."
    else:
        ea_query = "4. Write a sentence explaining why the student's extracurricular activities fall short of the standards of the desired school, "+student.university.name+". Please also mention that if the student adds extracurricular activities, it can show the student's "+activity_trait_dict['ea']+"."

    total_query += ea_query

    # ea_chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": json.dumps(ea_query),
    #         }
    #     ],
    #     model="gpt-3.5-turbo",
    # )
    # ea_result = ea_chat_completion.choices[0].message.content.strip("\"")
    #
    # if ea_strength == 1:
    #     strength.append(ea_result)
    # else:
    #     weakness.append(ea_result)

    # va strength/weakness text
    if va_strength == 1:
        va_query = "5. Please write a sentence explaining that your student's volunteer activities meet the standards of the desired school, "+student.university.name+". Also mention that the student's volunteer activities show the student's "+activity_trait_dict['va']+"."
    else:
        va_query = "5. Please write a sentence explaining why the student's volunteer activities do not meet the standards of the desired school, "+student.university.name+". Please also mention that if the student adds volunteer activities, it can show the student's "+activity_trait_dict['va']+"."

    total_query += va_query

    # va_chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": json.dumps(va_query),
    #         }
    #     ],
    #     model="gpt-3.5-turbo",
    # )
    # va_result = va_chat_completion.choices[0].message.content.strip("\"")
    #
    # if va_strength == 1:
    #     strength.append(va_result)
    # else:
    #     weakness.append(va_result)

    #get recommendation
    recommendation_query = "I decided to write IB IA for the subject \'"+ib_subject+"\' with the following title.\n\'"+ib_ia_title+"\'\n And the university major I want to pursue is "+student.major.name+"."+" At this time, write a sentence explaining why the IA topic you have chosen is suitable for the subject and the major you are applying for, and explaining what kind of content you should write about. The format of the sentence should be as follows(must follow the line-breakings):\n The topic chosen is ~~in one respect~~ suitable as an IA topic for the subject.\n Also, in one respect, it is largely related to the major that the student is pursuing.\n If student conducts research and writes in a way that ~~, the student will be able to produce good results."

    recommendation_chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": json.dumps(recommendation_query),
            }
        ],
        model="gpt-3.5-turbo",
    )

    recommendation = recommendation_chat_completion.choices[0].message.content.strip("\"")

    print(total_query)

    total_chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": json.dumps(total_query),
                }
            ],
            model="gpt-3.5-turbo",
        )

    total = total_chat_completion.choices[0].message.content.strip("\"")

    total_split = [t[3:] for t in total.split("\n") if t != '']

    if subjects_strength==1:
        strength.append(total_split[0])
    else:
        weakness.append(total_split[0])
    if awards_strength==1:
        strength.append(total_split[1])
    else:
        weakness.append(total_split[1])
    if isa_strength==1:
        strength.append(total_split[2])
    else:
        weakness.append(total_split[2])
    if ea_strength==1:
        strength.append(total_split[3])
    else:
        weakness.append(total_split[3])
    if va_strength==1:
        strength.append(total_split[4])
    else:
        weakness.append(total_split[4])

    context = {
        'student': student,
        'ib_subject': ib_subject,
        'ib_ia_title': ib_ia_title,
        'strength': strength,
        'weakness': weakness,
        'recommendation': recommendation,
    }
    return render(request, 'counselor_studdashboarddetail.html', context)
