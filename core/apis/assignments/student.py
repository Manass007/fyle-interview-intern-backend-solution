from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum  # Import AssignmentStateEnum
from core.libs.exceptions import FyleError # Import FyleError
from .schema import AssignmentSchema, AssignmentSubmitSchema
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal

def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""

    # Validate that 'content' is not null or empty
    if 'content' not in incoming_payload or not incoming_payload['content']:
        raise FyleError(status_code=400, message="Assignment content cannot be null or empty")

    assignment = AssignmentSchema().load(incoming_payload)
    assignment.student_id = p.student_id

    upserted_assignment = Assignment.upsert(assignment)
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
    return APIResponse.respond(data=upserted_assignment_dump)



@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal

def submit_assignment(p, incoming_payload):
    """Submit an assignment"""

    submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    # Fetch the assignment from the database
    assignment = Assignment.get_by_id(submit_assignment_payload.id)

    # If assignment doesn't exist, return a 404 error
    if not assignment:
        raise FyleError(status_code=404, message="Assignment not found")


    # Check if the assignment belongs to the student making the request
    if assignment.student_id != p.student_id:
        raise FyleError(status_code=400, message="You can only submit your own assignments")

    # Check if assignment is already submitted or graded
    if assignment.state != AssignmentStateEnum.DRAFT:
        raise FyleError(status_code=400, message="only a draft assignment can be submitted")

    # Check if assignment has content
    if not assignment.content:
        raise FyleError(status_code=400, message="Cannot submit assignment without content") 
    
    # Submit the assignment
    submitted_assignment = Assignment.submit(
        _id=submit_assignment_payload.id,
        teacher_id=submit_assignment_payload.teacher_id,
        auth_principal=p
    )
    db.session.commit()
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
    return APIResponse.respond(data=submitted_assignment_dump)

