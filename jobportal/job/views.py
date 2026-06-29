from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
# Create your views here.


def index(request):
    return render(request, 'index.html')



def admin_login(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        try:
            if user.is_active:
                login(request, user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    context = {"error": error}
    return render(request, 'admin_login.html',context)


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount=Recruiter.objects.all().count()
    ucount=ApplicantUser.objects.all().count()
    jcount=Job.objects.all().count()
    mcount=Contact.objects.all().count()
    context = {'rcount': rcount, 'ucount': ucount,'jcount': jcount,'mcount': mcount}
    return render(request, 'admin_home.html',context)



def recruiter_login(request):

    error = ""

    if request.method == "POST":

        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status!="pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    context = {'error': error}

    return render(request, 'recruiter_login.html',context)






def user_login(request):

    error = ""

    if request.method == "POST":

        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            try:
                user1 = ApplicantUser.objects.get(user=user)
                if user1.type == "Applicant":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    context = {'error': error}
    return render(request, 'user_login.html', context)



from .models import ApplicantUser

def user_signup(request):

    error = ""

    if request.method == "POST":

        f = request.POST.get('first_name')
        l = request.POST.get('last_name')
        e = request.POST.get('email')
        p = request.POST.get('password')
        con = request.POST.get('contact')
        gen = request.POST.get('gender')

        i = request.FILES.get('image')

        try:

            if User.objects.filter(username=e).exists():
                error = "already"

            else:

                user = User.objects.create_user(
                    username=e,
                    first_name=f,
                    last_name=l,
                    email=e,
                    password=p)

                ApplicantUser.objects.create(
                    user=user,
                    phone=con,
                    image=i,
                    gender=gen,
                    type="Applicant")

                error = "no"

        except Exception as ex:
            print(ex)
            error = "yes"

    return render(request, 'user_signup.html', {'error': error})


def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    user = request.user
    applicant = ApplicantUser.objects.get(user=user)

    error = ""

    if request.method == "POST":

        f = request.POST.get('first_name')
        l = request.POST.get('last_name')
        con = request.POST.get('contact')
        gen = request.POST.get('gender')

        applicant.user.first_name = f
        applicant.user.last_name = l
        applicant.phone = con
        applicant.gender = gen

        if request.FILES.get('image'):
            applicant.image = request.FILES.get('image')

        try:
            applicant.user.save()
            applicant.save()
            error = "no"

        except Exception as ex:
            print(ex)
            error = "yes"

    context = {'applicant': applicant, 'error': error}
    return render(request, 'user_home.html',context)



def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)

    error = ""

    if request.method == "POST":

        f = request.POST.get('first_name')
        l = request.POST.get('last_name')
        con = request.POST.get('contact')
        gen = request.POST.get('gender')



        recruiter.user.first_name = f
        recruiter.user.last_name = l
        recruiter.phone = con
        recruiter.gender = gen

        if request.FILES.get('image'):
            recruiter.image = request.FILES.get('image')

        try:
            recruiter.user.save()
            recruiter.save()
            error = "no"

        except Exception as ex:
            print(ex)
            error = "yes"


    context = {'recruiter':recruiter,'error':error}
    return render(request, 'recruiter_home.html',context)




def recruiter_signup(request):
    error = ""
    if request.method == "POST":

        f = request.POST.get('first_name')
        l = request.POST.get('last_name')
        e = request.POST.get('email')
        p = request.POST.get('password')
        con = request.POST.get('contact')
        com=request.POST.get('company')
        gen = request.POST.get('gender')

        i = request.FILES.get('image')

        try:
            if User.objects.filter(username=e).exists():
                error = "already"
            else:
                user = User.objects.create_user(
                    username=e,
                    first_name=f,
                    last_name=l,
                    email=e,
                    password=p)

                Recruiter.objects.create(
                    user=user,
                    phone=con,
                    image=i,
                    gender=gen,
                    company=com,
                    type="recruiter",
                    status="pending"
                )

                error = "no"

        except Exception as ex:
            print(ex)
            error = "yes"

    return render(request, 'recruiter_signup.html',{'error': error})



def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=ApplicantUser.objects.all()
    context = {'data': data}
    return render(request, 'view_users.html',context)


def delete_user(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=id)
    user.delete()
    return redirect('view_users')


def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    sta= Recruiter.objects.filter(status__iexact="pending")
    s= {'sta':sta}
    return render(request, 'recruiter_pending.html',s)



def view_recruiters(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    context = {'data': data}
    return render(request, 'view_recruiters.html',context)




def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    sta= Recruiter.objects.filter(status__iexact="accept")
    s= {'sta':sta}
    return render(request, 'recruiter_accepted.html',s)



def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    sta= Recruiter.objects.filter(status__iexact="reject")
    s= {'sta':sta}
    return render(request, 'recruiter_rejected.html',s)




def delete_recruiter(request,id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=id)
    user.delete()
    return redirect('view_recruiters')



def change_status(request, id):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter = Recruiter.objects.get(id=id)
    if request.method == "POST":
        s=request.POST.get('status')
        recruiter.status = s
        try:
            recruiter.save()
            error = "no"
        except:
            error = "yes"
    d={'recruiter':recruiter,'error':error}
    return render(request, 'change_status.html',d)



def adminchange_password(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":

        old = request.POST.get('currentpassword')
        new = request.POST.get('newpassword')

        try:
            user = User.objects.get(id=request.user.id)

            if user.check_password(old):

                if old == new:
                    error = "same"
                else:
                    user.set_password(new)
                    user.save()
                    error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'adminchange_password.html', d)



def applicantchange_password(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    if request.method == "POST":

        old = request.POST.get('currentpassword')
        new = request.POST.get('newpassword')

        try:
            user = User.objects.get(id=request.user.id)

            if user.check_password(old):


                if old == new:
                    error = "same"
                else:
                    user.set_password(new)
                    user.save()
                    error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'applicantchange_password.html', d)




def recruiterchange_password(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == "POST":

        old = request.POST.get('currentpassword')
        new = request.POST.get('newpassword')

        try:
            user = User.objects.get(id=request.user.id)

            if user.check_password(old):


                if old == new:
                    error = "same"
                else:
                    user.set_password(new)
                    user.save()
                    error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'recruiterchange_password.html', d)



def addjob(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == "POST":

            jt = request.POST.get('jobtitle')
            sd= request.POST.get('startdate')
            ed= request.POST.get('enddate')
            sal= request.POST.get('salary')
            lo= request.FILES.get('logo')
            exp = request.POST.get('experience')
            loc = request.POST.get('location')
            ski = request.POST.get('skills')
            desc = request.POST.get('description')
            user=request.user

            recruiter=Recruiter.objects.get(user=user)
            try:
                  Job.objects.create(recruiter=recruiter,start_date=sd,
                                     end_date=ed,title=jt,
                                     salary=sal,image=lo,
                                     experience=exp,location=loc,
                                     skills=ski,description=desc,
                                     creation_date=date.today())

                  error = "no"

            except Exception as ex:
                print(ex)
                error = "yes"
    context={'error': error}
    return render(request, 'addjob.html',context)



def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    jobs=Job.objects.filter(recruiter=recruiter)
    context={'jobs':jobs}

    return render(request, 'job_list.html',context)



def editjob(request,id):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job=Job.objects.get(id=id)
    if request.method == "POST":

            jt = request.POST.get('jobtitle')
            sd= request.POST.get('startdate')
            ed= request.POST.get('enddate')
            sal= request.POST.get('salary')
            lo= request.FILES.get('logo')
            exp = request.POST.get('experience')
            loc = request.POST.get('location')
            ski = request.POST.get('skills')
            desc = request.POST.get('description')

            job.title=jt
            job.salary=sal
            job.experience=exp
            job.location=loc
            job.skills=ski
            job.description=desc

            try:
                  job.save()
                  error = "no"

            except Exception as ex:
                print(ex)
                error = "yes"

            if sd:
                try:
                    job.start_date=sd
                    job.save()

                except:
                     pass
            else:
                pass

            if ed:
                try:
                    job.end_date=ed
                    job.save()

                except:
                    pass
            else:
                pass

    context={'error': error,'job':job}
    return render(request, 'editjob.html',context)



def changecompanylogo(request,id):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job=Job.objects.get(id=id)
    if request.method == "POST":

            lo= request.FILES.get('logo')
            job.image=lo

            try:
                  job.save()
                  error = "no"

            except Exception as ex:
                print(ex)
                error = "yes"


    context={'error': error,'job':job}
    return render(request, 'changecompanylogo.html',context)


def latestjobs(request):
    data=Job.objects.all().order_by('-start_date')
    context = {'data': data}
    return render(request, 'latestjobs.html',context)



def userjobs(request):
    job=Job.objects.all().order_by('-start_date')
    user=request.user
    applicant=ApplicantUser.objects.get(user=user)
    data=Appliedjob.objects.filter(applicant=applicant)
    li=[]
    for i in data:
        li.append(i.job.id)

    context = {'job': job,'li':li}
    return render(request, 'userjobs.html',context)



def jobdetails(request,id):
    job=Job.objects.get(id=id)

    context = {'job': job}
    return render(request, 'jobdetails.html',context)




def applyjob(request,id):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    user=request.user
    applicant=ApplicantUser.objects.get(user=user)
    job = Job.objects.get(id=id)
    date1 = date.today()
    if job.end_date < date1:
        error = "Closed"
    elif job.start_date > date1:
        error = "Not opened for applying"
    else:

         if request.method == "POST":
            res = request.FILES.get('resume')
            Appliedjob.objects.create(applicant=applicant,job=job,resume=res,applied_date=date.today())

            error="Done"

    context={'error': error}
    return render(request, 'applyjob.html',context)





def candidates(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    data=Appliedjob.objects.all()
    context={'data':data}
    return render(request, 'candidates.html',context)


def delete_candidates(request,id):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    application = Appliedjob.objects.get(id=id)
    application.delete()
    return redirect('candidates')


from django.shortcuts import render, redirect
from .models import Contact

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        return redirect('contact')

    return render(request, 'contact.html')


def view_contacts(request):
        if not request.user.is_authenticated:
            return redirect('admin_login')

        data = Contact.objects.all().order_by('-created_at')
        return render(request, 'view_contacts.html', {'data': data})


def Logout(request):
    logout(request)
    return redirect('index')



