from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, request
from .models import Answer, Question, QuizModel, User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
import pyotp

# Views here
number = 0
Email = ""
real_otp = 0
"""def signup(request):
    
    View for Registration Form display and sending OTP"
    if request.method == "POST":
        form = MyUserForm(request.POST)
        if form.is_valid():
            # If form data is valid, send OTP and redirect to verification page
            form.save()
            global Email 
            Email = request.POST.get('email')
            base32secret = pyotp.random_base32()
            totp = pyotp.TOTP(base32secret, digits=4, interval=120)
            #print("TOTP-------------------------------",totp.now())
            global real_otp
            real_otp = totp.now()
            sender = "er.gaganraj@gmail.com"
            receiver = Email
            message = "
                        From: From {sender}
                        #To: To {receiver}
                        Hey Buddy, 
                        Thanks for signing up. Your OTP is {real_otp}.
                        It is valid for 2 minutes. Be quick!
                    "
            try:
                send_mail(
                    'OTP verification',
                    message,
                    sender,
                    [receiver],
                    fail_silently=False,
                )
            except:
                User.objects.filter(email=Email).delete()
                msg = "<h1>Failed to send email Try again</h1><a href = '/'><button>Try again</button></a>"
                return HttpResponse(msg)
            return HttpResponseRedirect("Verification")
    else:
        form = MyUserForm()
    return render(request, "Registration_form.html",{"form":form})"""

def otp(request):
    """
    This view deals with OTP verification display
    """
    try:
        verified_obj = User.objects.get(email=Email)
    except:
        return HttpResponseNotFound("<h3>Page Not found!!</h3>")
    if not verified_obj.is_verified:
        if request.method == 'POST':
            user_input = request.POST.get("otp")
            if user_input != real_otp:
                User.objects.filter(email=Email).delete()
                error = "Verification Failed! Try again."
                return HttpResponse(error)
            else:
                message = "Congrats!!! You are a verfied User! <a href='/Login'>Login Now</a>"
                verified_obj.is_verified = True
                verified_obj.save()
                return HttpResponse(message)
        return render(request, "Verification.html")
    else:
        return HttpResponseRedirect("/Login")
    
def logging(request):
    """
    This view deals with the login functionality verifying the credentials of the user.
    """
    if request.method == "POST":
        form = LoggingForm(request.POST)
        this_user = request.POST.get("username")
        this_user_pass = request.POST.get("password")
        print(this_user,this_user_pass)
        user = authenticate(request, username=this_user, password=this_user_pass)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect("/Home/")
        else:
            return HttpResponse("Invalid Credentials")
    else:
        form = LoggingForm()
    return render(request, "LogInform.html", {"form":form}) 

#@login_required
def home(request):
    """
    Home view here deals with the display and logic behind the HomePage
    It's showing all the quizzes being created.
    """
    request.session["question_number"] = 0
    all_quizzes = QuizModel.objects.all()
    return render(request, "HomePage.html", {"quizzes":all_quizzes})

#This decorator works with inbuilt authentication system
#@login_required
def question_page(request, page_number):
    """
    This view renders the template for display of each particular quiz.
    """
    for i in range(len(page_number)):
        if page_number[i].isdigit():
            break
    quiz_number = int(page_number[i:])
    if quiz_number > len(QuizModel.objects.all()):
        return HttpResponse("The Quiz with this ID doesn't exist!!")
    this_quiz = QuizModel.objects.all().filter(id = quiz_number).first()
    quiz_questions = Question.objects.all().filter(quiz = quiz_number)
    print("----------------",request.session["question_number"],"----------------")
    #Logical Error when user presses the back button
    if request.method == "POST":
        request.session["question_number"] += 1
        if request.session["question_number"] > len(quiz_questions)-1:
            return render(request, "result.html")
        return HttpResponseRedirect(f"/Home/quiz{this_quiz.id}")
    this_question = quiz_questions[request.session["question_number"]]
    answers = Answer.objects.all().filter(question = this_question.id)
    return render(request, "onequestion.html", {
        "this_quiz":this_quiz, "question":this_question, "answers":answers
        })
