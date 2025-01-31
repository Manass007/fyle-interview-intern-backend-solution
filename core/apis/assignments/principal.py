from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum # Import AssignmentStateEnum
from core.libs.exceptions import FyleError # Import FyleError
from .schema import AssignmentSchema, AssignmentGradeSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principals_assignments = Assignment.get_assignments_by_principal()
    principals_assignments_dump = AssignmentSchema().dump(principals_assignments, many=True)
    return APIResponse.respond(data=principals_assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal

def grade_assignment(p, incoming_payload):
    """Grade or Regrade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch assignment from the database
    assignment = Assignment.get_by_id(grade_assignment_payload.id)

    # If assignment doesn't exist, return 404
    if not assignment:
        raise FyleError(status_code=404, message="Assignment not found")

    # Explicitly check for DRAFT state and prevent grading
    if assignment.state == AssignmentStateEnum.DRAFT:
        raise FyleError(status_code=400, message="Cannot grade an assignment in DRAFT state")

    # Grade the assignment
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

# def grade_assignment(p, incoming_payload):
#     """Grade an assignment"""
#     grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
#     assignment = Assignment.get_by_id(grade_assignment_payload.id)
#     if assignment.state != 'SUBMITTED':
#         raise BadRequest('Assignment content cannot be null or empty')
#         return APIResponse.respond(error="INVALID_STATE")

#     graded_assignment = Assignment.mark_grade(
#         _id=grade_assignment_payload.id,
#         grade=grade_assignment_payload.grade,
#         auth_principal=p
#     )
#     db.session.commit()
#     graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
#     return APIResponse.respond(data=graded_assignment_dump)
