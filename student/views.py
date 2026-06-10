from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import models
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from . models import Student, Attendance
from django.shortcuts import get_object_or_404

# Create your views here.

def homePage(request):

    # Total Students
    total_students = Student.objects.count()

    # Year Wise Count
    first_year_students = Student.objects.filter(year=1).count()
    second_year_students = Student.objects.filter(year=2).count()
    third_year_students = Student.objects.filter(year=3).count()
    final_year_students = Student.objects.filter(year=4).count()

    # Branch Wise Count
    cse_students = Student.objects.filter(branch='CSE').count()
    csm_students = Student.objects.filter(branch='CSM').count()
    csd_students = Student.objects.filter(branch='CSD').count()
    it_students = Student.objects.filter(branch='IT').count()
    ece_students = Student.objects.filter(branch='ECE').count()
    eee_students = Student.objects.filter(branch='EEE').count()
    mech_students = Student.objects.filter(branch='MECH').count()
    civil_students = Student.objects.filter(branch='CIVIL').count()

    context = {
        'total_students': total_students,

        'first_year_students': first_year_students,
        'second_year_students': second_year_students,
        'third_year_students': third_year_students,
        'final_year_students': final_year_students,

        'cse_students': cse_students,
        'csm_students': csm_students,
        'csd_students': csd_students,
        'it_students': it_students,

        'ece_students': ece_students,
        'eee_students': eee_students,
        'mech_students': mech_students,
        'civil_students': civil_students,
    }

    return render(request, 'student/index.html', context)

@login_required(login_url='login')
def addStudent(request):

    if request.method == "POST":
        student_name = request.POST.get("student_name")
        roll_no = request.POST.get("roll_no")
        branch = request.POST.get("branch")
        year = request.POST.get("year")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        print(student_name, roll_no, branch, year, email, phone)

        if student_name and roll_no and branch and year and email and phone:
            Student.objects.create(
                student_name=student_name,
                roll_no=roll_no,
                branch=branch,
                year = int(request.POST.get("year")),
                email=email,
                phone=phone
            )
        
        messages.success(request, "Student Details Added Successfully !")
        return redirect('homePage')

    return render(request, 'student/add_student.html')

@login_required(login_url='login')
def studentList(request):

    students = Student.objects.none()

    selected_branch = request.GET.get('branch')
    selected_year = request.GET.get('year')
    search_query = request.GET.get('search')

    filter_applied = False

    # FILTERS
    if selected_branch or selected_year or search_query:
        filter_applied = True
        students = Student.objects.all()

        if selected_branch:
            students = students.filter(branch=selected_branch)

        if selected_year:
            students = students.filter(year=selected_year)

        # ONLY ROLL NO SEARCH
        if search_query:
            students = students.filter(roll_no__icontains=search_query)

    # ORDERING
    students = students.order_by('roll_no')

    # PAGINATION
    paginator = Paginator(students, 10)  # 10 per page
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)

    context = {
        'students': students,
        'selected_branch': selected_branch,
        'selected_year': selected_year,
        'search_query': search_query,
        'filter_applied': filter_applied
    }

    return render(request, 'student/student_list.html', context)

@login_required(login_url='login')
def deleteStudent(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('studentList')

@login_required(login_url='login')
def editStudent(request, id):
    student = Student.objects.get(id=id)
    return render(request, 'student/edit_student.html', {'student': student})

@login_required(login_url='login')
def updateStudent(request, id):
    student = Student.objects.get(id=id)

    if request.method == "POST":
        student.student_name = request.POST.get('student_name')
        student.roll_no = request.POST.get('roll_no')
        student.branch = request.POST.get('branch')
        student.year = request.POST.get('year')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')

        student.save()

         # SUCCESS MESSAGE
        messages.success(request, "Student Details updated successfully!")

        return redirect('studentList')
    
    return render(request, 'student/edit_student.html', {'student': student})

@login_required(login_url='login')
def studentDetails(request, id):
    student = Student.objects.get(id=id)

    context = {
        'student': student
    }

    return render(request, 'student/student_details.html', context)

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('studentList')
        else:
            return render(request, 'student/login.html', {'error': 'Invalid credentials'})
        
    return render(request, 'student/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def addAttendance(request):

    students = Student.objects.none()
    selected_branch = request.GET.get('branch')
    selected_year = request.GET.get('year')
    date = request.GET.get('date')

    filter_applied = False

    # STEP 1: FILTER STUDENTS
    if selected_branch or selected_year:
        filter_applied = True
        students = Student.objects.all()

        if selected_branch:
            students = students.filter(branch=selected_branch)

        if selected_year:
            students = students.filter(year=selected_year)

        students = students.order_by('roll_no')

    # STEP 2: SAVE ATTENDANCE
    if request.method == "POST":

        # take date safely (prefer GET because filter controls it)
        date = request.GET.get('date')

        # fallback safety (if GET missing)
        if not date:
            date = request.POST.get('date')

        # 🚨 VALIDATION: prevent empty date crash
        if not date:
            messages.error(request, "Date is required to mark attendance")
            return redirect('addAttendance')

        # loop through ONLY filtered students
        for student in students:

            status = request.POST.get(f'attendance_{student.id}')

            # SKIP if no status selected
            if not status:
                continue

            # DUPLICATE CHECK (safe)
            exists = Attendance.objects.filter(
                student=student,
                date=date
            ).exists()

            if exists:
                messages.error(
                    request,
                    f"Attendance already marked for {date}"
                )
                return redirect('addAttendance')

            # SAVE
            Attendance.objects.create(
                student=student,
                date=date,
                status=status
            )

        messages.success(request, "Attendance saved successfully")
        return redirect('addAttendance')

    context = {
        'students': students,
        'selected_branch': selected_branch,
        'selected_year': selected_year,
        'date': date,
        'filter_applied': filter_applied
    }

    return render(request, 'student/add_attendance.html', context)

def attendanceHistory(request, student_id):

    student = Student.objects.get(id=student_id)

    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by('-date')

    total_classes = attendance_records.count()

    present_days = attendance_records.filter(
        status='Present'
    ).count()

    absent_days = attendance_records.filter(
        status='Absent'
    ).count()

    if total_classes > 0:
        attendance_percentage = int(
            (present_days / total_classes) * 100
        )
    else:
        attendance_percentage = 0

    next_url = request.GET.get('next')

    context = {
        'student': student,
        'attendance_records': attendance_records,
        'next_url': next_url,

        'total_classes': total_classes,
        'present_days': present_days,
        'absent_days': absent_days,
        'attendance_percentage': attendance_percentage,
    }

    print("TOTAL =", total_classes)
    print("PRESENT =", present_days)
    print("ABSENT =", absent_days)
    print("PERCENT =", attendance_percentage)

    return render(request, 'student/attendance_history.html', context)

def studentSearch(request):

    roll_no = request.GET.get('roll_no')

    try:
        student = Student.objects.get(roll_no=roll_no)

        return redirect('studentDetails', id=student.id)

    except Student.DoesNotExist:

        messages.error(request, "Student not found")

        return redirect('homePage')




