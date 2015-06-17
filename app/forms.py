from wtforms import Form, StringField, IntegerField, validators

class UserForm(Form):
    id = StringField('id')
    name = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Email(message='Enter a valid email id')])

class DoctorForm(Form):
	id = StringField('id')
	name = StringField('Name',[validators.Length(min=4, max=100)])
	email = StringField('Email Address',[validators.Email(message='Enter a valid email id')])
	phone = IntegerField('Phone Number',[validators.required()])
	description = StringField('Description')
	experience = StringField('Experience')
	#qualification
	qualification = StringField('Qualification')
	#services
	services = StringField('Services')

class ClinicForm(Form):
	#Clinic
	id = StringField('id')
	clinicName = StringField('Clinic Name')
	area = StringField('Area')
	address = StringField('Address')
	startTime = StringField('Start Time')
	endTime = StringField('End Time')
	doctor_id = IntegerField('Doctor Id')

class SpecialityForm(Form):
	id = StringField('id')
	specialityName = StringField('Speciality Name')
	doctor_id = IntegerField('Doctor Id')