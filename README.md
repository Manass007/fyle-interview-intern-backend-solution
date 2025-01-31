# fyle-interview-intern-backend-solution
The commands which are mentioned in the challenge repository are specifically for linux like operating system.
The commands for windows and the steps to run this backend flask application is a bit different.(Note: run all the below commands in project directory in vscode terminal)

**Step 1 :**
First, let's ensure the Python version installed. Open the terminal and check
```
python --version
```
**Step 2 :** 
Install virtualenv if haven't already:
```
pip install virtualenv
```
**Step 3 :** 
Create and activate a virtual environment:

**Step a :** Create virtual environment
(Note: if the latest version is installed replace with python3.13)
```
virtualenv env --python=python3.8
```
**Step b :** On Windows, activate using:
```
.env\Scripts\activate
```
**Step 4 :** 
Install project dependencies:
```
pip install -r requirements.txt
```
**Step 5 :** 
Set up the database:

**Set the Flask application On Windows:**
```
$env:FLASK_APP = "core/server.py"
$env:FLASK_ENV = "development"
```
**Remove existing database if it exists:**
```
del core\store.sqlite3
```
**Run database migrations:**
```
flask db upgrade -d core/migrations/
```
**Step 6 :** 
start the Flask development server:
```
python -m flask run
```
## Commands to check all the APIS are working (note: Run all the below commands in Git Bash)
### GET /student/assignments
List all assignments created by a student
```
curl -X GET -H 'X-Principal: {"user_id":1, "student_id":1}' http://127.0.0.1:5000/student/assignments
```
### POST /student/assignments
Create an assignment
```
curl -X POST -H 'X-Principal: {"user_id":2, "student_id":2}' -H "Content-Type: application/json" -d '{"content":"PROJECT P1"}' http://127.0.0.1:5000/student/assignments
```
### POST /student/assignments
Edit an assignment
```
curl -X POST -H 'X-Principal: {"user_id":2, "student_id":2}' -H "Content-Type: application/json" -d '{"id: 5", "content":"REPORT R1"}' http://127.0.0.1:5000/student/assignments
```

### POST /student/assignments/submit
Submit an assignment
```
curl -X POST -H 'X-Principal: {"user_id":1, "student_id":1}' -H "Content-Type: application/json" -d '{"id": 2, "teacher_id": 2}' http://127.0.0.1:5000/student/assignments/submit
```
### GET /teacher/assignments
List all assignments submitted to this teacher
```
curl -X GET -H 'X-Principal: {"user_id":3, "teacher_id":1}' http://127.0.0.1:5000/teacher/assignments
```
### GET /principal/assignments
List all submitted and graded assignments
```
curl -X GET -H 'X-Principal: {"user_id":5, "principal_id":1}' http://127.0.0.1:5000/principal/assignments
```
### POST /principal/assignments/grade
Grade or re-grade an assignment
```
curl -X POST -H 'X-Principal: {"user_id":5, "principal_id":1}' -H "Content-Type: application/json" -d '{"id": 1, "grade": "A"}' http://127.0.0.1:5000/principal/assignments/grade
```
## Missing APIs Implemented
### GET /principal/teachers
List all the teachers
```
curl -X GET -H 'X-Principal: {"user_id":5, "principal_id":1}' http://127.0.0.1:5000/principal/teachers
```
### POST /teacher/assignments/grade
Grade an assignment
```
curl -X POST -H 'X-Principal: {"user_id":3, "teacher_id":1}' -H "Content-Type: application/json" -d '{"id": 1, "grade": "A"}' http://127.0.0.1:5000/teacher/assignments/grade
```
## Bugs I encountered during Implementation and there solution
### Exception in function test_submit_assignment_student_1 in students_test.py
this test can only be run at the first time of running the test command ```pytest -vvv -s tests/``` in the new terminal of vscode in the project directory after activating env enviroment by running this command ```.env\Scripts\activate```
this happens because the student can only submit the assignment once and do not resubmit the assignment so if we try to again run the test second time this test will fails because the assignment which student trying to submit with this payload ```{'id': 2, 'teacher_id': 2}``` is already submitted.

### Use of FlyeError exceptions which are given in libs/exceptions.py
I used the given exception in libs folder to properly pass the error messages and error code to pass the test cases.

### Used AssignmentStateEnum function
This ensures that only submitted assignments can be graded.
If an assignment is in DRAFT or GRADED state, grading is not allowed.

### Use of comments in different files
I have did comments in the code files where I have maked the change you can compare the snippet of that files from the main challenge repository [click here to go to main challenge repo.](https://github.com/fylein/fyle-interview-intern-backend).

