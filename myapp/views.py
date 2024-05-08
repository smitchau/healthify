from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
import random
from django.conf import settings


# Create your views here.
def login(request):
    try:
        if request.POST:
            try:
                user = User.objects.get(email = request.POST['email'])
                if user.password == request.POST['password']:
                    request.session['role'] = user.role
                    request.session['fname'] = user.f_name
                    request.session['lname'] = user.l_name
                    request.session['email'] = user.email  
                    request.session['password'] = user.password
                    request.session['picture'] = user.picture.url
                    
                    if user.role == "doctor":
                        return redirect('home')
                    else:
                        print("hello")
                        return redirect("doctors")
                else:
                    return render(request,"login.html")
            except:
                msg = "Email is not register !!"
                return render(request,"login.html",{'msg':msg})
        else:
            return render(request,"login.html")
    except Exception as e:
        print("======================",e)
        return render(request,"login.html")
    
def logout(request):
    if 'email' in request.session:
        del request.session['role'] 
        del request.session['fname'] 
        del request.session['lname'] 
        del request.session['email'] 
        del request.session['password'] 
        del request.session['picture'] 
        msg1 = "Logout Successfully"
        return render(request,"login.html",{'msg1':msg1})

def forgot_password(request):
    if request.method=="POST":
        try:
            user= User.objects.get(email = request.POST['email'])
            request.session['email'] = user.email
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
            subject = 'OTP For Forgot Password'
            message = 'Hello '+user.f_name+" , Your OTP : "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'otp.html',{'email':user.email,'otp':otp})
        except:
            msg = "Email Does Not Exist !!!"
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",msg)
            return render(request,'forgot-password.html',{'msg':msg})
    else:
        return render(request,'forgot-password.html')
    
def otp(request):
    if request.POST:
        uotp=int(request.POST['otp'])
        print("uotp",type(uotp))
        print(request.session['otp'],type(request.session['otp']))
        
        if uotp == request.session['otp']:
            return render(request,'password.html')
        else:
            msg="Invalid OTP"
            return render(request,'otp.html',{'msg':msg})
    
def password(request):
    if request.POST:
        np = request.POST['password']
    
        user=User.objects.get(email = request.session['email'])
        user.password=np
        user.save()
        del request.session['email']
        del request.session['otp']
        msg1="Password Updated :) "
        return render(request, 'login.html',{'msg1':msg1})

    else:
        msg="please enter password !!!"
        return render(request,"password.html",{'msg':msg})

def signup(request):
    if request.POST:
        try:
            user = User.objects.get(email = request.POST['email'])
            msg = "Email is Already Exists !!"
            return render(request,"login.html",{'msg':msg})
        except:
            user = User.objects.create(
                role = request.POST['role'],
                f_name = request.POST['fname'],
                l_name = request.POST['lname'],
                email = request.POST['email'],
                password = request.POST['password']
            )
            msg1 = "Signup Successfully !!"
            return render(request,"login.html",{'msg1':msg1})
    else:
        return render(request,"signup.html")

def home(request):
    if 'email' in request.session:
        user = User.objects.get(email = request.session['email'])
        print("======",user)
        try:
            doctor_info = Doctor_info.objects.get(user_id = user)
            print("=====",doctor_info)
            appointment = Appointment.objects.filter(doctor_info = doctor_info)
            print("===============>",appointment)
            d = User.objects.all()
            patient_info = Patient_info.objects.all()
            America = 0
            India = 0
            Australia = 0
            Canada = 0
            UK = 0
            Other = 0
        
            for i in patient_info:
                if i.country == 'india':
                    India = India + 1
                    print("=========>india",India)
                    
                elif i.country == 'America':
                    America = America + 1
                    
                elif i.country == 'Australia':
                    Australia = Australia + 1
                    
                elif i.country == 'Canada':
                    Canada = Canada + 1
                    
                elif i.country == 'UK':
                    UK = UK + 1
                    
                elif i.country == 'Other':
                    Other = Other + 1
                    
                #print(i.user_id.f_name)
            print("============>d",d)
            #all patient
            b = 0
            for i in patient_info:
                    b = b + 1
            #Your patient
            a = 0
        
            print("Your patient")
            try:
                list = []
                for i in appointment:
                    if i.user.f_name not in list:
                        list.append(i.user.f_name)
                print('list',list)
                for i in list:
                    a = a + 1
                print(a)
            except Exception as e:
                print(e)
                
            #Total Doctor
            if user.role == "doctor":
                u = User.objects.all()
                c = 0
                for i in u:
                    if i.role == 'doctor':
                        c = c + 1
                return render(request,"index.html",{'c':c,'a':a,'b':b,'appointment':appointment,'India':India,'America':America,'Australia':Australia,'Canada':Canada,'UK':UK,'Other':Other})
            else:    
                user = User.objects.all()  
                return render(request, "doctors.html", {"user": user})
        except Exception as e:
            print(e)
            return render(request,"index.html")    
    else:
        return redirect("login")

def book_appointment(request,pk):
    if 'email' in request.session:
        user = User.objects.get(email = request.session['email'])
        print("==================>user",user)
        try:
            patient_info = Patient_info.objects.get(user_id = user)
            print("==================>patient_info",patient_info.user_id.f_name)
        except Exception as e:
            print(e)
            msg1 = "Fill Up The Information And You can Book Appointment"
            return render(request,"update_profile.html",{'msg1':msg1,'user':user})
    
    

        doctor = User.objects.get(pk = pk)
        doctor_info = Doctor_info.objects.get(user_id = doctor) 
        print("==============123",doctor)
        print("==============456",doctor_info.speciality)
        try:
            if request.POST:
                appointment = Appointment.objects.create(
                    user = user,
                    doctor_info = doctor_info,
                    patient_info = patient_info,
                    fname = request.POST['fname'],
                    lname = request.POST['lname'],
                    dob = request.POST['dob'],
                    gender = request.POST['gender'],
                    service = request.POST['service'],
                    appointment_date = request.POST['appoinment_date'],
                    email = request.POST['email'],
                    phone = request.POST['phone'],
                    info = request.POST['info'],
                    age = request.POST['age']
                )
                print("=============>appointment",appointment)
                return render(request,"book_appointment.html",{'doctor_info':doctor_info,'doctor':doctor})
            else:
                return render(request,"book_appointment.html",{'doctor_info':doctor_info,'doctor':doctor})
        except Exception as e:
            print("=============",e)
            return render(request,"book_appointment.html",{'doctor_info':doctor_info,'doctor':doctor})
    else:
        return redirect("login")

# def add_patients(request):
#     return render(request,"add-patients.html")

def all_patients(request):
    if 'email' in request.session:
        user = User.objects.get(email = request.session['email'])    
        try:
            doctor = Doctor_info.objects.get(user_id = user)
            print("doctor",doctor)
            appointment = Appointment.objects.filter(doctor_info = doctor)
            print("====",appointment)
            
            return render(request,"all-patients.html",{'appointment':appointment})
        except Exception as e:
            print(e)
            return render(request,"all-patients.html")
    else:
        return redirect("login")
    
def invoice(request):
    if 'email' in request.session:
        user = User.objects.get(email = request.session['email'])
        print("=================>",user)
        appointment = Appointment.objects.filter(user = user)
        print("===========>",appointment)
        return render(request,"invoice.html",{'appointment':appointment})
    else:
        return redirect("login")

def approved(request,pk):
    print("hiiiiiiiiiiiiiiiii")
    a = Appointment.objects.get(pk = pk)
    print("appointment",a)
    a.appointment_status_approved = True
    a.appointment_status_cancle = False
    a.appointment_status_pandding = False
    a.save()
    print("done")
    user = User.objects.get(email = request.session['email'])
    doctor = Doctor_info.objects.get(user_id = user)
    print("doctor",doctor)
    
    
    appointment = Appointment.objects.filter(doctor_info = doctor)
    print("====",appointment)
        
    return render(request,"all-patients.html",{'appointment':appointment})

def rejected(request,pk):
    print("hiiiiiiiiiiiiiiiii")
    a = Appointment.objects.get(pk = pk)
    print("appointment",a)
    a.appointment_status_cancle = True
    a.appointment_status_approved = False
    a.appointment_status_pandding = False
    a.save()
    print("done")
    user = User.objects.get(email = request.session['email'])
    doctor = Doctor_info.objects.get(user_id = user)
    print("doctor",doctor)
    
    
    appointment = Appointment.objects.filter(doctor_info = doctor)
    print("====",appointment)
        
    return render(request,"all-patients.html",{'appointment':appointment})


def patients_profile(request,pk):
    if 'email' in request.session:
        appointment = Appointment.objects.get(pk = pk)
        print(appointment)
        
        user = User.objects.get(email = request.session['email'])
        print("============>",user)
        
        a = Appointment.objects.filter(user = appointment.user)
        print(a)
        
        return render(request,"patients-profile.html",{'appointment':appointment,'a':a,'user':user})
    else:
        return redirect("login")

def add_doctor(request):
    if 'email' in request.session:
        try:
            user = User.objects.get(email = request.session['email'])
            doctor_info = Doctor_info.objects.get(user_id = user)
            print("-----------",doctor_info)
        
            if request.POST:

                user.f_name = request.POST['fname']
                user.l_name = request.POST['lname']
                user.email = request.POST['email']
                user.save()

                request.session['fname'] = user.f_name
                request.session['lname'] = user.l_name
                request.session['email'] = user.email
                
                doctor_info.gender = request.POST['gender']

                doctor_info.speciality = request.POST['speciality']
                doctor_info.city = request.POST['city']
                doctor_info.country = request.POST['country']
                doctor_info.address = request.POST['address']
                doctor_info.contact = request.POST['contact']
                
                doctor_info.Hospital_Affiliations = request.POST['Hospital_Affiliations']
                doctor_info.Medical_School = request.POST['Medical_School']
                doctor_info.Experience = request.POST['Experience']
                doctor_info.Internship = request.POST['Internship']


                if request.POST['dob']:
                    doctor_info.dob = request.POST['dob']
                if request.POST['file']:
                    doctor_info.certificate = request.FILES.get('file')
                doctor_info.about = request.POST['about']
                doctor_info.save()
                
                return render(request,"add-doctor.html",{"doctor_info":doctor_info})            
            else:
                return render(request,"add-doctor.html",{"doctor_info":doctor_info})
        except Exception as e: 
            print("exception===================",e)
            if request.POST:
                user = User.objects.get(email = request.session['email'])
                print("============",user)
                user.f_name = request.POST['fname']
                user.l_name = request.POST['lname']
                user.email = request.POST['email']
                user.save()
                request.session['fname'] = user.f_name
                request.session['lname'] = user.l_name
                request.session['email'] = user.email
                
                doctor_info = Doctor_info.objects.create(
                    user_id = user,
                    dob = request.POST['dob'],
                    gender = request.POST['gender'],
                    speciality = request.POST['speciality'],
                    city = request.POST['city'],
                    country = request.POST['country'],
                    address = request.POST['address'],
                    contact = request.POST['contact'],
                    certificate = request.FILES.get('file'),
                    about = request.POST['about'],
                    Hospital_Affiliations = request.POST['Hospital_Affiliations'],
                    Medical_School = request.POST['Medical_School'],
                    Experience = request.POST['Experience'],
                    Internship = request.POST['Internship']
                )
                print('done')
                try:
                    doctor_info = Doctor_info.objects.get(user_id = user)
                    print("hrffffffffffff",doctor_info)
                    return render(request,"add-doctor.html",{'doctor_info':doctor_info})
                    
                except Exception as e:
                    print(e)
                    return render(request,"add-doctor.html")
            else:
                return render(request,"add-doctor.html")
    else:
        return redirect("login")
    
def change_pass(request):
    if 'email' in request.session:
        if request.POST:
            try:
                user = User.objects.get(email = request.session['email'])
                if user.email == request.POST['email']:
                    print("hello")
                    if request.POST['password'] == request.POST['cpassword']:
                        user.password = request.POST['password']
                        user.save()
                        return redirect("logout")
                    else:
                        if user.role == "doctor":
                            msg = "your password and confirm password does not match"
                            return render(request,"add-doctor.html",{'msg':msg})
                        else:
                            msg = "your password and confirm password does not match"
                            return render(request,"update_profile.html",{'msg':msg})
                else:
                    if user.role == "doctor":
                        msg = "Your Email is Wrong Please Enter valid Email id"
                        return render(request,"add-doctor.html",{'msg':msg})
                    else:
                        msg = "Email is Wrong Please Enter valid Email id"
                        return render(request,"update_profile.html",{'msg':msg})
            except Exception as e:
                if user.role == "doctor":
                    print(e)
                    return render(request,"add-doctor.html")
                else:
                    return render(request,"update_profile.html")
        else:
            if user.role == "doctor":
                    print(e)
                    return render(request,"add-doctor.html")
            else:
                return render(request,"update_profile.html")
    else:
        return redirect("login")
        
def doctors(request):
    if 'email' in request.session:
        user = User.objects.all()  
        return render(request, "doctors.html", {"user": user})
    else:
        return redirect("login")
   
# def events(request):
#     return render(request,"events.html")

def myprofile(request):
    if 'email' in request.session:
        user = User.objects.get(email = request.session['email'])
        if user.role == "doctor":
            doctors = Doctor_info.objects.get(user_id = user)
            return render(request,"profile.html",{"doctors":doctors,"user":user})
        else:
            try:
                patient_info = Patient_info.objects.get(user_id = user)
                return render(request,"user_profile.html",{"user":user,"patient_info":patient_info})
            except:
                return render(request,"user_profile.html",{"user":user})
    else:
        return redirect("login")

def profile(request,pk):
    if 'email' in request.session:
        try:
            patient = User.objects.get(email = request.session['email'])
            print("=====",patient)
            user = User.objects.get(pk = pk)
            print("user=================",user)
            doctors = Doctor_info.objects.get(user_id = user)
            print("doctors===============================================",doctors)
            return render(request,"profile.html",{"doctors":doctors,"user":user,"patient":patient})
        except Exception as e:
            print("helo==============",e)
            user = User.objects.get(pk = pk)
            print("user=================",user)
            return render(request,"profile.html",{"user":user})
    else:
        return redirect("login")

def user_profile(request):
    if 'email' in request.session:
        try:
            user = User.objects.get(email = request.session['email'])
            if user.role == "patient":
                patient_info = Patient_info.objects.get(user_id = user)
                return render(request,"user_profile.html",{"user":user,"patient_info":patient_info})
        except Exception as e:
            print("======",e)
            return render(request,"user_profile.html")
    else:
        return redirect("login")
    
def update_profile(request):
    if 'email' in request.session:
        try:
            user = User.objects.get(email = request.session['email'])
            patient_info = Patient_info.objects.get(user_id = user)
            print("Patient_info==========",Patient_info)
            if user.role == "patient":  
                if request.POST:
                    user.f_name = request.POST['f_name']
                    user.l_name = request.POST['l_name']
                    user.email = request.POST['email']
                    user.save()
                    patient_info.city = request.POST['city']
                    patient_info.country = request.POST['country']
                    patient_info.address = request.POST['address']
                    patient_info.contact = request.POST['contact']
                    patient_info.save()
                    
                    request.session['fname'] = user.f_name
                    request.session['lname'] = user.l_name
                    request.session['email'] = user.email  
                    
                    return render(request,"update_profile.html",{"user":user,"patient_info":patient_info})
                else:
                    return render(request,"update_profile.html",{"user":user,"patient_info":patient_info})

        except Exception as e:
            print("==========",e)
            user = User.objects.get(email = request.session['email'])
            if request.POST:
                patient_info = Patient_info.objects.create(
                    user_id = user,
                    city = request.POST['city'],
                    contact = request.POST['contact'],
                    country = request.POST['country'],
                    address = request.POST['address']
                )
                return render(request,"update_profile.html",{"user":user,"patient_info":patient_info})
            else:
                return render(request,"update_profile.html",{"user":user})
    else:
        return redirect("login")

def Change_Picture(request):
    print("==========hii")
    if request.POST:
        print("hello")
        user = User.objects.get(email = request.session['email'])
        if 'picture' in request.FILES:
            user.picture = request.FILES["picture"]
            user.save()
            request.session['picture'] = user.picture.url
            if user.role == "doctor":
                return redirect("home")
            else:
                return redirect("user_profile")
        else:
            # Handle the case where 'picture' is not found in request.FILES
            return HttpResponse('No picture found in the request', status=400)
    else:
        return redirect("user_profile")