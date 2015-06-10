from django.db import models
from django.contrib.auth.models import User 

class Role(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=500)

	def __unicode__(self):
		return self.name
# Create your models here.
class Staff(models.Model):
	mob_no = models.CharField(max_length=20)
	adress = models.CharField(max_length=100)
	role = models.ForeignKey(Role)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return self.user.first_name + " "+self.user.last_name

class Language(models.Model):
	language = models.CharField(max_length=100)
	language_code = models.CharField(max_length=20)

	def __unicode__(self):
		return self.language

class Patient(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	initials = models.CharField(max_length=3)
	original_address = models.CharField(max_length=400)
	bed_no = models.IntegerField()
	ward_no = models.IntegerField()
	pta_cleared = models.BooleanField()
	language = models.ForeignKey(Language)

	def __unicode__(self):
		return self.first_name + " " + self.last_name

class Question(models.Model):
	QUESTION_TYPE = (
      ('location', 'Location'),
      ('time', 'Time'),
      ('visual', 'Visual'),
   )
	name = models.CharField(max_length=500)
	question_type = models.CharField(max_length=50, choices=QUESTION_TYPE)


	def __unicode__(self):
		return self.name

class PictureCard(models.Model):
	image = models.ImageField("Pic card", upload_to="images/", blank=True, null=True)
	name = models.CharField(max_length=100)

	def __unicode__(self):
			return self.name

class PatientPics(models.Model):
	patient = models.ForeignKey(Patient)
	pictureCard = models.ForeignKey(PictureCard)
	date = models.DateTimeField()

	def __unicode__(self):
		return "Picture for patient "+self.patient.first_name+" "+self.last_name

class Answer(models.Model):
	question = models.ForeignKey(Question)
	text = models.CharField(max_length=200)
	isAnswerRight = models.BooleanField()

	def __unicode__(self):
		return self.text

class PatientResponses(models.Model):
	patient = models.ForeignKey(Patient)
	date = models.DateTimeField()
	answer = models.CharField(max_length=200)
	answerStatus = models.BooleanField()
	question = models.ForeignKey(Question)

	def __unicode__(self):
		return self.patient.first_name+" "+ self.patient.last_name+" "+self.question.name

class PTAQuestionaire(models.Model):
	patient = models.ForeignKey(Patient)
	date = models.DateTimeField()
	correctAnswers = models.IntegerField()
	totalQuestions = models.IntegerField()
	staff = models.ForeignKey(User)

	def __unicode__(self):
		return "Patient "+self.patient.initials + " on " + self.date.strftime("%c")+ "  correctly answered "+ str(self.correctAnswers)+"  out of "+ str(self.totalQuestions)+" questions."