from flask import Flask, render_template, request, session, redirect, url_for
from database import init_db, db_session
from models import Doctors,Clinic,Speciality
from forms import UserForm, DoctorForm,ClinicForm,SpecialityForm
import json
from sqlalchemy import func
init_db()
 
app = Flask('app')


@app.route('/', methods=['GET', 'POST'])
def home():
	#return "Hello Doctor"
	doctors = Doctors.query.all()
	form = DoctorForm(request.form)
	if request.method == 'POST':
		if form.validate():
			if form.id.data == '':
				doc = Doctors(name=form.name.data,email=form.email.data,phone=form.phone.data,description=form.description.data,qualification=form.qualification.data,experience=form.experience.data)
				db_session.add(doc)
				db_session.commit()
			else:
				doctor = Doctors.query.get(int(form.id.data))
				doctor.name = form.name.data
				doctor.email = form.email.data
				doctor.phone = form.phone.data
				doctor.description = form.description
				db_session.commit()
	doctors = Doctors.query.all()
	return render_template('index.html',doctors = doctors)

@app.route('/search',methods = ['GET','POST'])
def my_form():
	if request.method == 'POST':
		dictionary = {}
		docList,clinicList,spcltList = [],[],[]
		special = request.form['specialization']
		#special = special[0].upper() + special[1:]
		location = request.form['location']
		specialities = Speciality.query.filter(func.lower(Speciality.specialityName)==func.lower(special))
		if location == '':
			onlyDoctors = []
			for spclt in specialities:
				doctor = Doctors.query.get(int(spclt.doctor_id))
				clinicForEachDoctor = Clinic.query.filter_by(doctor_id=int(spclt.doctor_id))
				for clnc in clinicForEachDoctor:
					onlyDoctors.append((doctor,clnc))
			return render_template("show.html",onlyDoctors = onlyDoctors)
		clinics = Clinic.query.filter(func.lower(Clinic.area)==func.lower(location))
		for spclt in specialities:
			for clinic in clinics:
				if spclt.doctor_id == clinic.doctor_id:
					docRow = Doctors.query.get(int(spclt.doctor_id))
					docList.append((docRow,clinic,spclt))
		dictionary['docList'] = docList
		if len(docList) == 0:
			return "No Results Found"
		return render_template('show.html', dictionary = dictionary)

	rows=Speciality.query.all()
 	specialities=[]
	[specialities.append(row.specialityName) for row in rows]

	rows=Clinic.query.all()
 	locations=[]
	[locations.append(row.area) for row in rows]	
	
	return render_template('search.html',specialities=json.dumps(list(set(specialities))),locations=json.dumps(list(set(locations))))


@app.route('/addDoctor/new',methods=['GET','POST'])
def doctor():
	form = DoctorForm(request.form)
	return render_template('addDoctor.html',form = form)

@app.route('/addDoctor/<doctor_id>',methods=['GET','POST'])
def newDoctor(doctor_id):
	doctors = Doctors.query.all()
	if doctor_id == "new":
		form = DoctorForm(request.form)
	else:
		form = None
	return render_template('index.html',form=form)

@app.route('/doctor/qualification/<doctor_id>')
def getDoctor(doctor_id):
	doctor = Doctors.query.filter_by(id=doctor_id).first()
	docs = Doctors.query.all()
	d = Doctors.query.filter_by(name="Aditya",)
	qual = Qualification.query.filter_by(doctor_id = doctor.id).first()
	clinic = Clinic.query.filter_by(doctor_id = doctor.id).first()
	dic = {}
	dic['name'] = doctor.name
	dic['email'] = doctor.email
	dic['degree'] = qual.degree
	dic['clinicName'] = clinic.clinicName
	#dic['college'] = qual.college
	#dic['year'] = qual.degree
	return render_template('quals.html',dic = dic)

@app.route('/addClinic/<doctor_id>')
def addClinic(doctor_id):
	if doctor_id != '':
		form = ClinicForm(request.form)
		form.doctor_id.data = doctor_id
		return render_template("addClinic.html",form=form)


@app.route('/clinic',methods = ['GET','POST'])
def clinic():
	#return "dasds"
	form = ClinicForm(request.form)
	if request.method == 'POST':
		if form.validate():
			if form.id.data == '':
				doctor = Doctors.query.get(int(form.doctor_id.data))
				_id = doctor.id
				clinic = Clinic(clinicName=form.clinicName.data,area=form.area.data,address=form.address.data,startTime=form.startTime.data,endTime=form.endTime.data)
				db_session.add(clinic)
				doctor.clinics.append(clinic)
				db_session.commit()
				clinicList = doctor.clinics
	doctors = Doctors.query.all()
	return render_template("index.html",doctors = doctors)

@app.route('/addSpeciality/<doctor_id>')
def addSpeciality(doctor_id):
	if doctor_id != '':
		form = SpecialityForm(request.form)
		form.doctor_id.data = doctor_id
		return render_template("speciality.html",form=form)

@app.route('/speciality',methods = ['GET','POST'])
def speciality():
	form = SpecialityForm(request.form)
	if request.method == 'POST':
		if form.validate():
			if form.id.data == '':
				doctor = Doctors.query.get(int(form.doctor_id.data))
				_id = doctor.id
				speciality = Speciality(specialityName=form.specialityName.data)
				db_session.add(speciality)
				doctor.specialities.append(speciality)
				db_session.commit()
				specialityList = doctor.specialities
				return render_template("specialities.html",specialities = specialityList)



@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user_obj = User.query.get(user_id)
    db_session.delete(user_obj)
    b_session.commit()
    #addDoctor redirect(url_for('home'))


@app.route('/add/<user_id>')
def add_user(user_id):
    if user_id == 'new':
        form = UserForm(request.form)
    else:
        user_obj = User.query.get(int(user_id))
        form = UserForm(obj=user_obj)
    return render_template('user_form.html', form=form)
