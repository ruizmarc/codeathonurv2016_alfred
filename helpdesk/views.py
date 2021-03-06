from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import UpdateView
from django.db.models import Avg
from helpdesk.models import *
from helpdesk.tables import *
from django.core.urlresolvers import reverse
from django.db.models import Q
from .forms import *
from django_tables2   import RequestConfig

# Create your views here.
@login_required
def pdi_topics(request):
    try:
        request.user.pdi
    except:
        return HttpResponse('Unauthorized', status=401)

    sent = 'False'
    if request.method == 'GET':
        if 'sent' in request.GET.keys():
            sent = 'True'

    if sent=='True':
        table = SentTopicsTable(Topic.objects.filter(author__id=request.user.id))
    else:
        table = ReceivedTopicsTable(Topic.objects.filter(receiver__id=request.user.id))

    # topic_author = Topic.objects.filter(author__id=request.user.id)
    # topic_receiver = Topic.objects.filter(receiver__id=request.user.id)
    RequestConfig(request).configure(table)
    return render(request,'helpdesk/topics.html', {'sent':sent, 'section': 'topics', 'rol' : 'pdi', 'table':table})

@login_required
def pdi_new_topic_for_pas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = NewTopicForPas(request.POST, dynamic_choices=Department.objects.all())
        # check whether it's valid:

        if form.is_valid():
            department = form.cleaned_data['department']
            pas_set = department.pas_set.all()
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            priority = form.cleaned_data["priority"]

            if(len(pas_set) == 1):
                teacher = pas_set[0]
                topic = Topic(title=title, content=content, priority=priority, receiver=teacher.user, department=True, author=request.user).save()
                return HttpResponseRedirect('/helpdesk/pdi/topics')
            else:
                topic = Topic(title=title, content=content, priority=priority, department=True, author=request.user)
                topic.save()
                request.session["topic"] = topic.id
                request.session["department"] = department.id
                return HttpResponseRedirect('/helpdesk/pdi/ask/employee')

    # if a GET (or any other method) we'll create a blank form
    departments = Department.objects.all()
    form = NewTopicForPas(dynamic_choices=departments)

    return render(request, 'helpdesk/create_topic_for_pas.html', {'rol':'pdi','form': form})

@login_required
def pdi_choose_pas(request):
    # if this is a POST request we need to process the form data
    department = Department.objects.get(pk=request.session['department'])
    teachers = department.pas_set.all()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmployeeChooser(request.POST, dynamic_choices=teachers)
        # check whether it's valid:

        if form.is_valid():
            teacher = form.cleaned_data["employee"]
            topic = Topic.objects.get(pk=request.session['topic'])
            topic.receiver = teacher.user
            topic.save()
            return HttpResponseRedirect('/helpdesk/pdi/topics')


    # if a GET (or any other method) we'll create a blank form
    form = EmployeeChooser(dynamic_choices=teachers)
    return render(request, 'helpdesk/choose_teacher_pas.html', {'rol': 'pdi', 'form': form})

@login_required
def pdi_ask(request):
    try:
        request.user.pdi
    except:
        return HttpResponse('Unauthorized', status=401)
    return render(request,'helpdesk/create_topic_for_pdi.html', {'section': 'ask', 'rol' : 'pdi'})

@login_required
def pdi_profile(request, pk):
    try:
        request.user.pdi
    except:
        return HttpResponse('Unauthorized', status=401)

    pdi = Pdi.objects.get(pk=pk)

    subjects = pdi.subjects.all()

    return render(request,'helpdesk/pdi_profile.html', {'pdi': pdi, 'subjects': subjects, 'section': 'profile', 'rol' : 'pdi'})

@login_required
def pas_topics(request):
    try:
        request.user.pas
    except:
        return HttpResponse('Unauthorized', status=401)

    sent = 'False'
    if request.method == 'GET':
        if 'sent' in request.GET.keys():
            sent = 'True'

    if sent=='True':
        table = SentTopicsTable(Topic.objects.filter(author__id=request.user.id))
    else:
        table = ReceivedTopicsTable(Topic.objects.filter(receiver__id=request.user.id))

    # topic_author = Topic.objects.filter(author__id=request.user.id)
    # topic_receiver = Topic.objects.filter(receiver__id=request.user.id)
    RequestConfig(request).configure(table)
    return render(request,'helpdesk/topics.html', {'sent':sent, 'section': 'topics', 'rol' : 'pas', 'table':table})

@login_required
def pas_new_topic_for_pas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = NewTopicForPas(request.POST, dynamic_choices=Department.objects.all())
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            department = form.cleaned_data['department']
            pas_set = department.pas_set.all()
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            priority = form.cleaned_data["priority"]

            if(len(pas_set) == 1):
                teacher = pas_set[0]
                topic = Topic(title=title, content=content, priority=priority, receiver=teacher.user, department=True, author=request.user).save()
                return HttpResponseRedirect('/helpdesk/pas/topics')
            else:
                topic = Topic(title=title, content=content, priority=priority, department=True, author=request.user)
                topic.save()
                request.session["topic"] = topic.id
                request.session["department"] = department.id
                return HttpResponseRedirect('/helpdesk/pas/ask/employee')

    # if a GET (or any other method) we'll create a blank form
    departments = Department.objects.all()
    form = NewTopicForPas(dynamic_choices=departments)

    return render(request, 'helpdesk/create_topic_for_pas.html', {'rol':'pas','form': form})

@login_required
def pas_choose_pas(request):
    # if this is a POST request we need to process the form data
    department = Department.objects.get(pk=request.session['department'])
    teachers = department.pas_set.all()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmployeeChooser(request.POST, dynamic_choices=teachers)
        # check whether it's valid:

        if form.is_valid():
            teacher = form.cleaned_data["employee"]
            topic = Topic.objects.get(pk=request.session['topic'])
            topic.receiver = teacher.user
            topic.save()
            return HttpResponseRedirect('/helpdesk/pas/topics')


    # if a GET (or any other method) we'll create a blank form
    form = EmployeeChooser(dynamic_choices=teachers)
    return render(request, 'helpdesk/choose_teacher_pas.html', {'rol': 'pas', 'form': form})

@login_required
def pas_ask(request):
    try:
        request.user.pas
    except:
        return HttpResponse('Unauthorized', status=401)
    return render(request,'helpdesk/create_topic_for_pdi.html', {'section': 'ask', 'rol' : 'pas'})

@login_required
def ranking(request):

    if request.method == 'GET':
        if 'user_type' in request.GET.keys():
            user_type = request.GET['user_type']
        else:
            user_type = 'pdi'

        if user_type == 'pdi':
            users = Pdi.objects.all()
        elif user_type == 'pas':
            users = Pas.objects.all()
        else:
            return HttpResponse('Unauthorized', status=401)

        reputation_ranking = {}
        speed_ranking = {}
        closed_ranking = {}

        topics = {}

        for user in users:
            reputation_ranking[user] = Comment.objects.filter(author=user.user).aggregate(Avg("rating")).values()[0]
            closed_ranking[user] = Topic.objects.filter(receiver=user.user, status='CLOSED').count()

            topics[user] = Topic.objects.filter(receiver=user.user)
            time = 0
            counter = 0
            for topic in topics[user]:
                topic_comments = Comment.objects.filter(topic=topic, author=user.user).order_by('date_published')
                if(topic_comments.count()):
                    time += (Comment.objects.filter(topic=topic.id).order_by('date_published')[0].date_published - topic.creation_date).total_seconds()
                    counter += 1

            if(counter!=0):
                speed_ranking[user] = time / counter

        import operator

        reputation = sorted(reputation_ranking.items(), key=operator.itemgetter(1), reverse=True)
        speed = sorted(speed_ranking.items(), key=operator.itemgetter(1), reverse=True)
        closed = sorted(closed_ranking.items(), key=operator.itemgetter(1), reverse=True)

        try:
            request.user.student
            rol = 'student'
        except:
            try:
                request.user.pdi
                rol = 'pdi'
            except:
                    try:
                        request.user.pas
                        rol = 'pas'
                    except:
                        return HttpResponse('Unauthorized', status=401)

        return render(request,'helpdesk/ranking.html', {'section': 'ranking', 'rol' : rol, 'user_type':user_type, 'reputation_ranking':reputation, 'closed_ranking' : closed, 'speed_ranking': speed})

@login_required
def pas_profile(request, pk):
    try:
        request.user.pas
    except:
        return HttpResponse('Unauthorized', status=401)

    pas = Pas.objects.get(pk=pk)

    return render(request,'helpdesk/pas_profile.html', {'pas': pas, 'section': 'profile', 'rol' : 'pas'})


@login_required
def student_topics(request):
    try:
        request.user.student
    except:
        return HttpResponse('Unauthorized', status=401)
    table = SentTopicsTable(Topic.objects.filter(author__id=request.user.id))
    RequestConfig(request).configure(table)
    return render(request,'helpdesk/topics.html', {'sent':'True', 'section': 'topics', 'rol':'student', 'table':table})

@login_required
def  student_new_topic_for_pdi(request):
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = NewTopicForPdi(request.POST, dynamic_choices=request.user.student.subjects.all())
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            subject = form.cleaned_data['subject']


            pdi_set = subject.pdi_set.all()
            title = form.cleaned_data["title"]
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]
            priority = form.cleaned_data["priority"]

            if(len(pdi_set) == 1):
                teacher = pdi_set[0]
                topic = Topic(title=title, content=content, priority=priority, receiver=teacher.user, author=request.user).save()
                return HttpResponseRedirect('/helpdesk/student/topics')
            else:
                topic = Topic(title=title, content=content, priority=priority, author=request.user)
                topic.save()
                request.session["topic"] = topic.id
                request.session["subject"] = subject.id
                return HttpResponseRedirect('/helpdesk/student/ask/pdi/teacher')

    # if a GET (or any other method) we'll create a blank form
    subjects = request.user.student.subjects.all()
    form = NewTopicForPdi(dynamic_choices=subjects)

    return render(request, 'helpdesk/create_topic_for_pdi.html', {'rol':'student','form': form})

@login_required
def  student_choose_teacher(request):
    # if this is a POST request we need to process the form data
    subject = Subject.objects.get(pk=request.session['subject'])
    teachers = subject.pdi_set.all()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TeacherChooser(request.POST, dynamic_choices=teachers)
        # check whether it's valid:

        if form.is_valid():
            teacher = form.cleaned_data["teacher"]
            topic = Topic.objects.get(pk=request.session['topic'])
            topic.receiver = teacher.user
            topic.save()
            return HttpResponseRedirect('/helpdesk/student/topics')
    # if a GET (or any other method) we'll create a blank form


    form = TeacherChooser(dynamic_choices=teachers)

    return render(request, 'helpdesk/choose_teacher_pdi.html', {'rol': 'student', 'form': form})

@login_required
def  student_new_topic_for_pas(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = NewTopicForPas(request.POST, dynamic_choices=Department.objects.all())
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            department = form.cleaned_data['department']
            pas_set = department.pas_set.all()
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            priority = form.cleaned_data["priority"]

            if(len(pas_set) == 1):
                teacher = pas_set[0]
                topic = Topic(title=title, content=content, priority=priority, receiver=teacher.user, department=True, author=request.user).save()
                return HttpResponseRedirect('/helpdesk/student/topics')
            else:
                topic = Topic(title=title, content=content, priority=priority, department=True, author=request.user)
                topic.save()
                request.session["topic"] = topic.id
                request.session["department"] = department.id
                return HttpResponseRedirect('/helpdesk/student/ask/pas/employee')

    # if a GET (or any other method) we'll create a blank form
    departments = Department.objects.all()
    form = NewTopicForPas(dynamic_choices=departments)

    return render(request, 'helpdesk/create_topic_for_pas.html', {'rol':'student','form': form})

@login_required
def  student_choose_pas(request):
    # if this is a POST request we need to process the form data
    department = Department.objects.get(pk=request.session['department'])
    teachers = department.pas_set.all()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmployeeChooser(request.POST, dynamic_choices=teachers)
        # check whether it's valid:

        if form.is_valid():
            teacher = form.cleaned_data["employee"]
            topic = Topic.objects.get(pk=request.session['topic'])
            topic.receiver = teacher.user
            topic.save()
            return HttpResponseRedirect('/helpdesk/student/topics')


    # if a GET (or any other method) we'll create a blank form
    form = EmployeeChooser(dynamic_choices=teachers)
    return render(request, 'helpdesk/choose_teacher_pas.html', {'rol': 'student', 'form': form})

@login_required
def get_queryset(request):
    result = ""
    query = request.GET.get('q')
    try:
        request.user.student
        rol = 'student'
    except Exception:
        try:
            request.user.pdi
            rol = 'pdi'
        except Exception:
            try:
                request.user.pas
                rol = 'pas'
            except Exception:
                return HttpResponse('Unauthorized', status=401)
    if query:
        result = Topic.objects.filter(is_public=True).filter(Q(title__icontains=query)).order_by('last_update')
        print 'result', type(result), result
        subjects = result.filter(department=False)[:10]
        departments = result.filter(department=True)[:10]
        return render(request,'helpdesk/search.html', {'empty': False, 'section': 'ask_faq', 'rol': rol, 'subjects' : subjects, 'departments' : departments  })
    else:
        return render(request,'helpdesk/search.html', {'empty': True, 'section': 'ask_faq', 'rol': rol, 'subjects' : {}, 'departments' : {}  })

@login_required
def student_ask(request):
    try:
        request.user.student
    except:
        return HttpResponse('Unauthorized', status=401)
    return render(request,'helpdesk/create_topic_for_pdi.html', {'section': 'ask', 'rol' : 'student'})

@login_required
def topic(request, topic_id):
    #TODO: Fix the way to assign roles to users.
    try:
        request.user.student
        rol = 'student'
    except Exception:
        try:
            request.user.pdi
            rol = 'pdi'
        except Exception:
            try:
                request.user.pas
                rol = 'pas'
            except Exception:
                return HttpResponse('Unauthorized', status=401)
    topic = Topic.objects.get(pk=topic_id)
    if request.method == "GET":
        comments = Comment.objects.filter(topic__id=topic_id).order_by('date_published')
        form = NewComment()
        return render(request,'helpdesk/topic.html', {'comment_form':form, 'section': 'topic', 'rol' : rol, 'topic':topic, 'comments':comments})
    if request.method == "POST":
        return render(request,'helpdesk/make_topic_public.html', {'section': 'topic', 'rol' : rol, 'topic':topic})

@login_required
def topic_close(request, topic_id):
    #TODO: Fix the way to assign roles to users.
    try:
        request.user.student
        rol = 'student'
    except Exception:
        try:
            request.user.pdi
            rol = 'pdi'
        except Exception:
            try:
                request.user.pas
                rol = 'pas'
            except Exception:
                return HttpResponse('Unauthorized', status=401)
    topic = Topic.objects.get(pk=topic_id)
    if "is_public" in request.POST.keys():
        topic.is_public = True
    topic.status = "CLOSED"
    topic.save()
    comments = Comment.objects.filter(topic__id=topic_id).order_by('date_published')
    form = NewComment()
    return render(request,'helpdesk/topic.html', {'comment_form':form, 'section': 'topic', 'rol' : rol, 'topic':topic, 'comments':comments})

@login_required
def topic_comment(request, topic_id):
    #TODO: Fix the way to assign roles to users.

    try:
        request.user.student
        rol = 'student'
    except Exception:
        try:
            request.user.pdi
            rol = 'pdi'
        except Exception:
            try:
                request.user.pas
                rol = 'pas'
            except Exception:
                return HttpResponse('Unauthorized', status=401)

    if request.method == 'POST':
        form = NewComment(request.POST, request.FILES)

        if form.is_valid():
            topic = Topic.objects.get(pk=topic_id)
            comment = Comment(content=form.cleaned_data['content'], author=request.user, topic=topic).save()

    return HttpResponseRedirect('/helpdesk/topics/'+str(topic_id)+'/')


@login_required
def student_profile(request, pk):
    try:
        request.user.student
    except:
        return HttpResponse('Unauthorized', status=401)

    student = Student.objects.get(pk=pk)

    subjects = student.subjects.all()

    return render(request,'helpdesk/student_profile.html', {'student': student, 'subjects': subjects, 'section': 'profile', 'rol' : 'student'})

@login_required
def vote_comment(request):

    comment_id = None
    rating = 0
    if request.method == 'GET':
        comment_id = request.GET['comment_id']
        rating = request.GET['rating']
    if comment_id:
        comment = Comment.objects.get(id=int(comment_id))
        if comment:
            comment.rating =  rating
            comment.save()

    return HttpResponse(rating)
