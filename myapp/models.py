from django.db import models

# Create your models here.
roles = (
    ('doctor','doctor'),
    ('patient','patient'),
)

class User(models.Model):
    role = models.CharField(max_length=10 , choices = roles)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=20)
    picture = models.ImageField(default="user.jpg",upload_to="images/")
    
    def __str__(self):
        return self.f_name + " " + self.l_name + " || " + self.role
    
genders = (
    ('Male','Male'),
    ('Female','Female'),
)

specialitys = (
    ('Cardiologist','Cardiologist'),
    ('Nephrologiest','Nephrologiest'),
    ('Pulmonologist','Pulmonologist'),
    ('Ophthalmologist','Ophthalmologist'),
    ('Neurologist','Neurologist'),
    ('Rheumatologist','Rheumatologist'),
    ('Dermatologist','Dermatologist'),
    ('Hematologist','Hematologist'),
    ('Somnologist','Somnologist'),
)

class Doctor_info(models.Model):
    user_id = models.ForeignKey(User,on_delete = models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=10 , choices=genders)
    speciality = models.CharField(max_length=30 , choices=specialitys)
    city = models.CharField(max_length=20)
    Hospital_Affiliations = models.TextField()
    Medical_School = models.TextField()
    Experience = models.TextField()
    Internship = models.TextField()
    country = models.CharField(max_length=20)
    address = models.TextField()
    contact = models.PositiveIntegerField()
    certificate = models.ImageField(null=True,upload_to="doc/")
    about = models.TextField()
    
    def __str__(self):
        return self.user_id.f_name + " || " +self.speciality
countries = (
    ('America','America'),
    ('Australia','Australia'),
    ('Canada','Canada'),
    ('India','India'),
    ('UK','UK'),
    ('Other','Other'),
)    
    
class Patient_info(models.Model):
    user_id = models.ForeignKey(User,on_delete = models.CASCADE)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20,choices=countries)
    address = models.TextField()
    contact = models.PositiveIntegerField()
    
    def __str__(self):
        return self.user_id.f_name
    
services = (
    #cardiologiest
    ('heart Problem','heart Problem'),
    ('Diagnostic Testing','Diagnostic Testing'),
    #Nephrologiest
    ('kidneys Problem','kidneys Problem'),
    ('Treatment of Acute Kidney Injury','Treatment of Acute Kidney Injury'),
    #Pulmonologist
    ('Lung Problem','Lung Problem'),
    ('Sleep Medicine Services','Sleep Medicine Services'),
    ('Respiratory Disease Diagnosis','Respiratory Disease Diagnosis'),
    #Ophthalmologist
    ('Retina and Vitreous Services','Retina and Vitreous Services'),
    ('Eye Problem','Eye Problem'),
    ('Cornea and External Disease Services','Cornea and External Disease Services'),
    #Neurologist
    ('Epilepsy Management and Seizure Disorders','Epilepsy Management and Seizure Disorders'),
    ('Stroke Care and Management','Stroke Care and Management'),
    ('brain Problem','brain Problem'),
    #Rheumatologist
    ('Management of Autoimmune Diseases','Management of Autoimmune Diseases'),
    ('Management of Musculoskeletal Conditions','Management of Musculoskeletal Conditions'),
    #Dermatologist
    ('Diagnosis and Treatment of Skin Conditions','Diagnosis and Treatment of Skin Conditions'),
    ('Cosmetic Dermatology Services','Cosmetic Dermatology Services'),
    #Hematologist
    ('Management of Blood Disorders','Management of Blood Disorders'),
    ('Management of Hematologic Malignancies','Management of Hematologic Malignancies'),
    #Somnologist
    ('Diagnosis and Management of Sleep Disorders','Diagnosis and Management of Sleep Disorders'),
    ('Treatment and Management of Sleep Disorders','Treatment and Management of Sleep Disorders'), 
)
    
class Appointment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    doctor_info = models.ForeignKey(Doctor_info,on_delete=models.CASCADE)
    patient_info = models.ForeignKey(Patient_info,on_delete=models.CASCADE)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=20 , choices=genders)
    service = models.CharField(max_length=50 , choices=services)
    appointment_date = models.DateTimeField()
    email = models.EmailField()
    phone = models.BigIntegerField()
    info = models.TextField()
    appointment_status_approved = models.BooleanField(default=False)
    appointment_status_cancle = models.BooleanField(default=False)
    appointment_status_pandding = models.BooleanField(default=True)

    def __str__(self):
        return self.user.f_name + " || " + self.service + " || Dr." + self.doctor_info.user_id.f_name
    