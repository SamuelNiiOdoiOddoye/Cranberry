"""
Absolute Excelling College School Management System API 

The AECSMS API provides a CRUD(create, read, update, 
delete) interface to AECSMS database.

The various tables in the database to interface include:

Access, Staff, Student, Course, ExamResult, 
Property, Level, Department, and Subject. ## Remove

The api will also initialize the database before any 
transactions take place and commit changes to the 
database before closing it.

Author\t: Prince Asiedu
Email \t: prince14asiedu@gmail.com
Date   \t: May 30, 2019
Copyright : (c) Phelsy Inc. 2019

\n\t\t\tpowered by Phelsy.
"""

import sqlite3 as sql
import wx 
import aecsms_utils as utils


db = None
cursor = None

############################################
# Functions for creating various entities ##
############################################

def reg_access(access_id,user_id,username,passphrase):
 	# Function for registering admin.
 	try:
 		if access_id == 'apo190411' or access_id == 'gdq190241':
 			hashed_pass = utils.make_passhash(passphrase)
 			salt, passwd = hashed_pass

 			query = """insert into Access (StaffID, Name, Passphrase) values (?,?,?,?)"""
 			cursor.execute(query, (user_id, username, passwd))
 		
 		else:
 			pass

 	except Exception as error:
 		raise ValueError('Staff ID Incorrect.\n Contact System Administrator')


def reg_student(new_student_data):
	
 	# Function for registering a student.
 	query = """
 	insert into Student (Name,Gender,Age,Address,Phone,SchAttended,Email,DateOfBirth,
 	GuardianName,GuardianPhone,GuardianEmail,Course,StudentLevel,AdmissionDate)
	values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
 	"""
 	name,sex,age,addr,num,sch,email,dob,g_name,g_num,g_mail,course,level,adm_date = new_student_data 

 	cursor.execute(query,(name,sex,age,addr,num,sch,email,dob,g_name,g_num,g_mail,course,level,adm_date))

def reg_staff(staff_data):

 	# Function for registering a staff member.
 	query = """
 	insert into Staff (Name,Gender,Address,DateOfHiring,YearsOfService,Department
 	,Specialty,Category,Salary,Phone,Email)
 	values (?,?,?,?,?,?,?,?,?,?,?)
 	"""
 	name,sex,addr,hiredate,yrsofserv,dept,category,specialty,salary,phone,email = staff_data

 	cursor.execute(query, (name,sex,addr,hiredate,yrsofserv,dept,category,specialty,salary,phone,email))

def reg_course(course_details):
	# Function for registering a course.
	query = """
	insert into Course (Name, Duration, CourseLevel, Fee, Status)
	values (?,?,?,?,?)
 	"""
	coursename, duration, course_level, price, status = course_details
	cursor.execute(query, (coursename, duration, course_level, price, status))

def reg_exam(examname, coursename):
	# Function for registering an exam.
	query = """insert into Exam (ExamName, CourseName) values (?,?)"""
	cursor.execute(query,(examname, coursename))

def reg_exam_result(student_id, exam_id, exam_date, result):
	# Function for saving student exam results.
	query = """
	insert into ExamResult (StudentID, ExamID, ExamDate, Result)
	values (?,?,?,?)
 	"""
	cursor.execute(query, (student_id, exam_id, exam_date, result)) 

def reg_property(description, name, condition):
	# Function for registering a school property.
	query = """
	insert into Property (Description, Name, Condition)
	values (?,?,?)
 	"""
	cursor.execute(query, (description, name, condition))

def reg_level(level_details):
	# Function for registering a student-course level.
	query = """ insert into Level (Name, Grade) values (?,?)"""
	name, grade = level_details
	cursor.execute(query, (name, grade))

def reg_department(name):
	# Function for registering school department
	query = """
	insert into Department (Name)
	values (?)
	"""
	cursor.execute(query, (name))

def reg_subject(name, course_id):
	# Function for registering a subject.
	query = """
	insert into Subject (Name, CourseID)
	values (?,?)
 	"""
	cursor.execute(query, (name, course_id))


############################################
# Functions for reading various entities ###
#############################################

def get_staff():
	# Function for getting details on all staff members.
	query = """
	select ID,Name,Gender,Address,DateOfHiring,YearsOfService,Department,Specialty,
 	Category,Salary,Phone,Email from Staff 
 	"""
	return cursor.execute(query).fetchall()[0:]

def get_staff_member(staff_id):
	# Function for getting a staff member's details.
	query = """
	select ID,Name,Gender,Address,DateOfHiring,YearsOfService,DeptID,Specialty,
 	Category,Salary,Phone,Email from Staff 
 	where ID = ?
 	"""
	return cursor.execute(query, (staff_id,)).fetchall()[0]

def get_students():
	# Function for getting details on all students.
	query = """
	select * from Student 
 	"""
	return cursor.execute(query).fetchall()[0:]

def get_student(student_id):
	# Function for getting a student's details.
	query = """
	select Name,Gender,Phone,Email,Address,DateOfBirth,GuardianName,GuardianPhone,
	GuardianProfession,GuardianPlaceOfWork,CourseID,StudentLevel,photo,AdmissionDate,
	CompletionDate,Remarks from staff
	where ID = ?
 	"""
	return cursor.execute(query, (student_id,)).fetchall()[0]

def get_student_min_details():
	# Funtion for getting minute student details.
	query = """select ID, Name, Phone, Email, GuadianEmail, 
	CourseID, photo from Student"""
	
	details = cursor.execute(query).fetchall()[0:]
	return details

def get_courses():
	# Function for getting details on all courses.
	query = """
	select ID, Name, Duration, CourseLevel, Fee, Status from Course 
 	"""
	return cursor.execute(query).fetchall()[0:]

def get_course(course_id):
	# Function for getting details on a particular course.
	query = """
	select Name, CourseLevel, Instructor, Fee, Status from Course
	where ID = ?
	"""
	return cursor.execute(query, (course_id,)).fetchall()[0]

def get_access(username):
	query = """
	select Name, Passphrase from Access
	where Name = ?
	"""
	access_details = cursor.execute(query,(username,)).fetchall()
	try:
		access_details = access_details[0]
		access_details = {'name':access_details[0],'password':access_details[1]}
		return access_details
	except Exception as error:
		raise ValueError('User not found')

########## FIXME! FIXME! FIXME! FIXME! FIXME! ###############
def get_student_exam_result(student_id, exam_id):
	# Function for getting a student's exam results.
	query = """
	select Result from ExamResult where student_id = ?  and exam_id = ?
 	"""
	return cursor.execute(query, (student_id,exam_id,)).fetchall()[0]

########## FIXME! FIXME! FIXME! FIXME! FIXME! ###############
def get_students_results(students_level, course_id, exam_id):
	# Function for getting results of students on a particular exam.
	query = """
	select Result from ExamResult where student_level = ? and course_id = ? and exam_id = ?
 	"""
	return cursor.execute(query, (student_level, course_id, exam_id,)).fetchall()[0:]

def get_subject(subject_id):
	# Function for getting subject details.
	query ="""
	select Name, Abbreviation, SubjectAreaID from Subject 
	where ID = ? 
	"""
	return cursor.execute(query, (subject_id,)).fetchall()[0]

def get_subjects():
	# Retrieve info on all subjects.
	query = """
	select ID, Name, Abbreviation, SubjectAreaID from Subject 
	"""
	return cursor.execute(query).fetchall()[0:]

def get_sch_property(property_id):
	# Function for getting details on a particular school property.
	query = """
	select Description, Name, Condition from Property
	where ID = ?
 	"""
	return cursor.execute(query, (property_id,)).fetchall()[0]

def get_sch_properties():
	# Function for getting details on a particular all school properties/assets.
	query = """
	select ID, Description, Name, Condition from Property
 	"""
	return cursor.execute(query).fetchall()[0:]

def get_department(department_id):
	# Function for getting department details 
	query = """
	select Name, Description 
	where ID = ?
	"""

	return cursor.execute(query, (department_id,)).fetchall()[0]

def get_deparments():
	# Function for getting all departmental details
	query = """

	"""


#############################################
# Functions for updating various entities ###
#############################################

def update_staff(staff_id, name=None,gender=None,address=None,photo=None,date_of_hiring=None,
			years_of_service=None,department_id=None,category=None,specialty=None,
			salary=None,phone=None,email=None):

	# Function for making changes to a staff member's details.
	query = """
	update Staff
	set Name = ?,Gender = ?,Address = ?,DateOfHiring = ?,YearsOfService = ?,
	DeptID = ?,Specialty = ?,Category = ?,Salary = ?,Phone = ?,Email = ?
 	where ID = ?
 	"""
	staff_data = get_staff_member(staff_id)

	if not name: name = staff_data[0]
	if not gender: gender = staff_data[1]
	if not address: address = staff_data[2]
	if not photo: photo = staff_data[3]
	if not date_of_hiring: date_of_hiring = staff_data[4]
	if not years_of_service: years_of_service = staff_data[5]
	if not department_id: department_id = staff_data[6]
	if not category: category = staff_data[7]
	if not specialty: specialty = staff_data[8]
	if not salary: salary = staff_data[9]
	if not phone: phone = staff_data[10]
	if not email: email = staff_data[11]

	return cursor.execute(query,(name,gender,address,photo,date_of_hiring,years_of_service,
						  department_id,category,specialty,salary,phone,email))

def update_Student(student_id,name=None,gender=None, phone=None,email=None,address=None, 
	 			birth_date=None,guardian_name=None,guardian_phone=None,guardian_email=None,
	 			guardian_profession=None,guardian_place_of_work=None,
	 			course_id=None,student_level=None,photo=None, enrollment_date=None, 
	 			completion_date=None,remarks=None):
	# Function for making changes to a student's details.
	query = """
	update Student 
	set ID,Name = ?,Gender = ?,Phone = ?,Email = ?,Address = ?,DateOfBirth = ?,
	GuardianName = ?,GuardianPhone = ?,GuardianEmail = ?,GuardianProfession = ?,
	GuardianPlaceOfWork = ?,CourseID = ?,StudentLevel = ?,photo = ?,AdmissionDate = ?,
	CompletionDate = ?,Remarks = ?
 	"""
	student_data = get_student(student_id)

	if not name : name = student_data[0]
	if not gender : gender = student_data[1]
	if not phone : phone = student_data[2]
	if not email : email = student_data[3]
	if not address : address = student_data[4] 
	if not birth_date : birth_date = student_data[5]
	if not guardian_name : guardian_name = student_data[6]
	if not guardian_phone : guardian_phone = student_data[7]
	if not guardian_email : guardian_email = student_data
	if not guardian_profession : guardian_profession = student_data[8]
	if not guardian_place_of_work : guardian_place_of_work = student_data[9]
	if not course_id : course_id = student_data[10]
	if not student_id : student_id = student_data[11]
	if not photo : photo = student_data[12]
	if not enrollment_date : enrollment_date = student_data[13]
	if not completion_date : completion_date = student_data[14]
	if not remarks : remarks = student_data[15]

	return cursor.execute(query, (name,gender,phone,email,address,birth_date,
		guardian_name,guardian_phone,guardian_profession,guardian_place_of_work,course_id,
		student_id,photo,enrollment_date,completion_date,remarks))

def update_course(course_id, name=None, course_level = None,instructor=None, fee=None, status=None):
	# Function for making changes to a staff member's details.
	query = """
	update Course 
	set Name = ?, CourseLevel = ?, Instructor = ?, Fee = ?, Status = ?
 	"""
	course_data = get_course(course_id)

	if not name : name = course_data[0]
	if not instructor : instructor = course_data[2]
	if not course_level : course_level = course_data[1]
	if not fee : fee = course_data[3]
	if not status : status = course_data[4]

	return cursor.execute(query, (name,course_level,instructor,fee,status))


def update_property(property_id, description=None, name = None, condition=None):
	# Function for making changes to school property details.
	query = """
	update Property 
	set Description = ?, Name = ?, Condition = ?
 	"""
	property_data = get_sch_property(property_id)

	if not description : description = property_data[0]
	if not name : name = property_data[1]
	if not condition : condition = property_data[2]

	return cursor.execute(query, (description, name, condition))

def update_student_exam_result(exam_id, student_id, exam_date=None, result=None):
	# Function for modifying a student's exam results.
	query = """
	update ExamResult 
	set ExamDate, Result
 	"""
	exam_data = get_student_exam_result(exam_id, student_id)

	if not exam_date : exam_date = exam_data[0]
	if not result : result = exam_data[1]

	return cursor.execute(query, (exam_date,result))

	########### FIXME! FIXME! FIXME! ##############################

def update_access(staff_id, username, passphrase, new_username=None, new_passphrase=None):
	# Function for modifying access.
	query = """
 	"""
	pass

def update_department(department_id, name = None, abbreviation = None):
	# Function for modifying department details.
	query = """
	update Department
	set Name = ?, Abbreviation = ?
	"""
	department_data = get_department(department_id)

	if not name : name = department_id[0]
	if not abbreviation : abbreviation = department_id[1]

	return cursor.execute(query, (name,abbreviation))

def update_subject(subject_id, name, abbreviation, course_id):
	# Function for updating subject details.
	query = """
	update Subject 
	set Name = ?, Abbreviation = ?, SubjectAreaID
	"""
	subject_data = get_subject(subject_id)

	if not name : name = subject_data[0]
	if not abbreviation : abbreviation = subject_data[1]
	if not course_id : course_id = subject_data[2]

	return cursor.execute(query, (name, abbreviation, course_id))

#############################################
# Functions for deleting various entities ###
#############################################

def del_staff(staff_id):
	# Function for deleting a staff member.
	query = """
	delete from Staff
	where id = ?
 	"""
	cursor.execute(query, (staff_id,))

def del_student(student_id):
	# Function for unregistering a student.
	query = """
	delete from Student 
	where id = ?
 	"""
	cursor.execute(query, (student_id,))

def del_course(course_id):
	# Function for deleting a course.
	query = """
	delete from Course
	where id = ?
 	"""
	cursor.execute(query, (course_id,))

def del_exam(exam_id):
	# Function for deleting an exam.
	query = """
	delete from Exam
	where ID = ?
 	"""
	cursor.execute(query, (exam_id))

def del_property(property_id):
	# Function for deleting a school porperty.
	query = """
	delete from Property
	where ID = ?
 	"""
	cursor.execute(query, (property_id))

#############################################################################################

# The initDB function will intialize the database, 
# while the closeDB function will commit to and 
# close the database. 

def initDB(filename=None):
	global db, cursor
	if not filename:
		filename = 'aecsmsdb.db'
	try:
		db = sql.connect(filename)
		cursor = db.cursor()
	except:
		app = wx.App()
		wx.MessageBox("Problem connecting to the database.\n Try Again" + str(error),
			"Database Error!")
		cursor = None

def closeDB():
	try:
		cursor.close()
		db.commit()
		db.close()
	except Exception as error:
		app = wx.App()
		wx.MessageBox("Problem closing the database.\n Try Again" + str(error),
			"Database Error!")
		pass