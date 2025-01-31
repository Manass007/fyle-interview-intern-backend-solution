from flask import Blueprint
from core import db #added this import
from core.apis import decorators
from core.apis.responses import APIResponse
from core.libs.exceptions import FyleError
from core.models.assignments import Assignment, AssignmentStateEnum # Import AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema #used the existing grade schema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments submitted to this teacher"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal

def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch assignment from database
    assignment = Assignment.get_by_id(grade_assignment_payload.id)

    # FyleError if assignment does not exist
    if not assignment:
        raise FyleError(status_code=404, message="FyleError")

    # FyleError if teacher is not grading their own assignment
    if assignment.teacher_id != p.teacher_id:
        raise FyleError(status_code=400, message="FyleError")

    # FyleError if assignment is not in submitted state
    if assignment.state != AssignmentStateEnum.SUBMITTED:
        raise FyleError(status_code=400, message="FyleError")
    
    # Proceed with grading
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
