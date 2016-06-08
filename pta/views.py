from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from pta.models import Question, Patient, PTAQuestionaire, Staff,Answer,PatientResponses,PictureCard
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.db.models.signals import post_save
from django.contrib.auth import login as authLogin
from django.contrib.auth.decorators import login_required
from random import shuffle

def method(sender, **keywords):
	print sender

post_save.connect(method, User)
def logMeOut(request):
	message = "Logged out user "+ request.username
	logout(request)
	return HttpResponse(message)

def error(request):
	return render_to_response("pta/error.html", locals(), context_instance = RequestContext(request)) 

def login(request):
	helper = Helper()
	allPatientTypes = helper.getUnclearedPatientPerf()
	allPatientTypes["user"] = request.user
	if request.user.is_authenticated():
		return render_to_response("pta/index.html",allPatientTypes, context_instance = RequestContext(request))
	else:
		errorMessage = ""
		if request.POST:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password= password)
			if user is not None:
				if user.is_active:
					authLogin(request,user)
					allPatientTypes["user"] = request.user
					return render_to_response("pta/index.html",allPatientTypes, context_instance = RequestContext(request))
				else:
					errorMessage = "The user " +username+ " is no longer active. If this is a mistake, email support@pta.com and notify them."
					return render_to_response("pta/error.html",{"error":errorMessage}, context_instance = RequestContext(request))
			else:
				errorMessage = " Invalid username or password for '" +username+ "'. If this is a mistake, email support@pta.com and notify them."	
				return render_to_response("pta/error.html",{"error":errorMessage}, context_instance = RequestContext(request))
		else:
			return render_to_response("pta/login.html", locals(), context_instance = RequestContext(request)) 

@login_required(redirect_field_name='')
def pictureCards(request):
	pictureCards = PictureCard.objects.all()
	for pic in pictureCards:
		print pic
	return render_to_response("pta/pictureCards.html",{"PictureCards":pictureCards}, context_instance = RequestContext(request))

@login_required(redirect_field_name='', login_url="/pta/login")
def reports(request):

	helper = Helper()
	allPatientTypes = helper.getAllPatientTypes()
	allPatientTypes["staff"] = helper.getAllStaff()
	print allPatientTypes["staff"]
	return render_to_response("pta/reports.html",allPatientTypes, context_instance = RequestContext(request))

@login_required(redirect_field_name='', login_url="/pta/login")
def index(request):
	helper = Helper()
	allPatientTypes = helper.getAllPatientTypes()
	reports = helper.getUnclearedPatientPerf()
	for report in reports:
		print report
	return render_to_response("pta/index.html",allPatientTypes, context_instance = RequestContext(request))

def staffRpt(request,staff, reportType):
	s = Staff.objects.get(pk=staff)
	uniquePatients = set()
	messages  =[]
	
	for entry in PTAQuestionaire.objects.all():
		print entry.staff
	qsDone = PTAQuestionaire.objects.filter(staff = s.user)
	patientsCleared = 0
	patientClearingTime = []
	for qs in qsDone:
		patient = qs.patient
		if patient.pta_cleared:
			patientsCleared+=1
			uniquePatients.add(patient)

	clearingTotal = 0
	patientDict = {}
	
	for patient  in uniquePatients:
		
		patientQuestionnaires = PTAQuestionaire.objects.filter(patient = patient).order_by('-date')[:3]
		dateDiff = patientQuestionnaires[0].date - patientQuestionnaires[2].date
		minutesTaken = int(dateDiff.total_seconds() / 60)
		name  = patient.first_name+" "+ patient.last_name
		patientDict[name] = minutesTaken
		message = "Patient '"+ patient.first_name +" "+patient.last_name +"' took "+str(minutesTaken)+" minutes to celar the PTA assessment"
		messages.append(message)
		clearingTotal += minutesTaken

	
	average = 0
	if len(uniquePatients)>0:
		average = clearingTotal /len(uniquePatients)

	staffSummary = "In summary therapist '"+s.user.first_name+" "+s.user.last_name+"' took an average of "+str(average)+" minutes to clear "+ str(len(uniquePatients))+" patients from their PTA."
	#"patientDict":patientDict}
	return render_to_response("pta/staffReport.html",{"staff":s,"summary":staffSummary, "individualSumaries":messages, "reportType":reportType,"patientDict":patientDict}, context_instance = RequestContext(request))

def questionResponses(request, fromDate, toDate):
	return render_to_response("pta/patientRespDemo.html",locals(), context_instance = RequestContext(request))

def search(request):
	if 'q' in request.POST and request.POST['q']:
		 q = request.POST.get('q', False)
		 v1 = request.POST.get('test', False)
	else:
		print "nothing found"
		print "no param supplied"
	return render_to_response("pta/sample.html", locals(), context_instance = RequestContext(request))

@login_required(redirect_field_name='', login_url="/pta/login")
def questionnaire(request, patient):
	questions = Question.objects.all()
	biPatient = Patient.objects.get(pk=patient)
	
	incorrectAnswers = 0
	totalQuestions = 0
	totalCorrectAnswers= 0
	questionsWithAnswers = []
	
	for q in questions:
		ans = []
		answers = Answer.objects.filter(question = q)
		
		for a  in answers:
			ans.append(a);
		shuffle(ans)
		qDict = {"question": q, "answers": ans}
		questionsWithAnswers.append(qDict)

	questionMap = {}
	
	if request.POST:
		correctAnswers = request.POST.get("correctAnswers", False).split(',')
		if correctAnswers:
			print correctAnswers


		for q in questions:
			totalQuestions+=1
			if str(q.id) in correctAnswers:
				print "true"
				totalCorrectAnswers+=1
				response = PatientResponses(patient = biPatient, date = timezone.now(),answer="Correct", question = q, answerStatus=True)
				response.save()
			else:
				response = PatientResponses(patient = biPatient, date = timezone.now(),answer="Incorrect", question = q, answerStatus=False)
				response.save()


		questionaire = PTAQuestionaire(correctAnswers = str(totalCorrectAnswers),totalQuestions= str(totalQuestions))
		questionaire.patient = biPatient
		questionaire.date = timezone.now()
		questionaire.staff = request.user
		questionaire.save()
		questionsAnswered = PTAQuestionaire.objects.filter(patient= biPatient)
		ptasCleared = 0

		lastClear = False
		for q in questionsAnswered:
			if q.correctAnswers == q.totalQuestions:
				ptasCleared = ptasCleared+1;
			else:
				ptasCleared = 0

		if ptasCleared >= 3:
			biPatient.pta_cleared = True
			biPatient.save()

		helper = Helper()
		allPatientTypes = helper.getUnclearedPatientPerf()
		allPatientTypes["qFinished"]= True
		allPatientTypes["name"] = biPatient.first_name+"("+biPatient.initials+")"
		return render_to_response("pta/index.html", allPatientTypes, context_instance = RequestContext(request))
	return render_to_response("pta/questionnaire.html",{"questions":questionsWithAnswers, "patient":biPatient}, context_instance = RequestContext(request))

@login_required(redirect_field_name='', login_url="/pta/login")
def patientRpt(request, patient, reportType):
	
	biPatient = Patient.objects.get(pk=patient)
	patientInfo = PTAQuestionaire.objects.filter(patient = biPatient).order_by('date')
	return render_to_response("pta/patientRpt.html",{"patient":biPatient, "responses":patientInfo, "reportType":reportType}, context_instance = RequestContext(request))

class Helper:
	def __init__(self):
		return None

	def getAllStaff(self):
		staff = Staff.objects.all()
		return staff

	def getUnclearedPatientPerf(self):
		allPatientTypes = self.getAllPatientTypes()
		perfReport = []
		unclearedPatients = allPatientTypes.get('unclearedPatients')
		patientQuestionnaireMap = {}
		for biPatient in unclearedPatients:
			patientQuestionnaires = PTAQuestionaire.objects.filter(patient = biPatient).order_by('-date')
			patientName =""+biPatient.first_name +" "+ biPatient.last_name+""
			patientQuestionnaireMap[patientName] = len(patientQuestionnaires)
			counter = 0
			totalRightAnswers = 0
			totalQuestions = 0
			for patientQuestionnaire in patientQuestionnaires:
				totalQuestions += patientQuestionnaire.totalQuestions
				totalRightAnswers += patientQuestionnaire.correctAnswers
				counter +=1
				if counter ==3:
					break;
					
			if patientQuestionnaireMap[patientName]:
				perfSummary = "Patient "+ biPatient.first_name +" "+ biPatient.last_name+"  had an average of "+str(totalRightAnswers/3) +" correct answers  in the last 3 assessments"
			else:
				perfSummary = "Patient "+ patientName+"  has not done any PTA assessments so far"
			perfReport.append(perfSummary)
		allPatientTypes['patientPerfSummaries'] = perfReport	

		clearedPatients = allPatientTypes.get('clearedPatients')
		allPatientTypes['clearedPatients'] = clearedPatients[:7]
		return allPatientTypes

	def getAllPatientTypes(self):
		patients = Patient.objects.all()
		unclearedPatients = []
		currentPtaPatients = 0
		clearedPatients = []
		for patient in patients:
			if not patient.pta_cleared:
				unclearedPatients.append(patient)
				currentPtaPatients = currentPtaPatients+1;
			else:
				
				patientQuestionnaires = PTAQuestionaire.objects.filter(patient = patient).order_by('-date')[:1]
				date = patientQuestionnaires[0].date
				patient.clearingDate = str(date.year) +"/"+ str(date.month)+"/"+str(date.day)
				clearedPatients.append(patient)

		return  {"unclearedPatients":unclearedPatients, "allPatients":patients,"currentPtaPatients":currentPtaPatients, "clearedPatients":clearedPatients}



	