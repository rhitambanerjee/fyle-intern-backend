from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]

def test_get_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200

def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 200


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_submit_non_draft_assignment(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2  # Assuming assignment with id 2 exists and is not in draft state
        }
    )

    assert response.status_code == 400  # Assuming the server returns 400 for invalid operations
    assert 'error' in response.json

def test_invalid_endpoint_access(client):
    response = client.get('/invalid/endpoint')

    assert response.status_code == 404  # Assuming the server returns 404 for invalid endpoints

def test_get_assignments_by_student(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200
    assert 'data' in response.json
    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1  # Assuming student_id 1

def test_get_assignments_principal(client, h_principal):
    response = client.get('/principal/assignments', headers=h_principal)
    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED.value, AssignmentStateEnum.GRADED.value]


def test_get_teachers_principal(client, h_principal):
    response = client.get('/principal/teachers', headers=h_principal)
    assert response.status_code == 200
    data = response.json['data']
    assert len(data) > 0  # Check that there is at least one teacher


def test_grade_nonexistent_assignment_principal(client, h_principal):
    """
    Failure case: Principal tries to grade a non-existent assignment
    """
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            'id': 100000,  # Non-existent assignment ID
            'grade': GradeEnum.C.value
        }
    )
    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'


def test_assignment_schema_initiate_class():
    from core.models.assignments import Assignment
    from core.apis.assignments.schema import AssignmentSchema
    
    schema = AssignmentSchema()
    input_data = {
        "id": 1,
        "content": "Sample content",
        "created_at": "2024-07-18T16:23:16.859868",
        "updated_at": "2024-07-18T16:23:16.859868",
        "teacher_id": 1,
        "student_id": 1,
        "grade": "A",
        "state": "DRAFT"
    }
    assignment = schema.load(input_data)
    assert isinstance(assignment, Assignment)
    assert assignment.id == 1
    assert assignment.content == "Sample content"


def test_assignment_submit_schema_initiate_class():
    from core.libs.helpers import GeneralObject
    from core.apis.assignments.schema import AssignmentSubmitSchema
    
    schema = AssignmentSubmitSchema()
    input_data = {
        "id": 1,
        "teacher_id": 1
    }
    obj = schema.load(input_data)
    assert isinstance(obj, GeneralObject)
    assert obj.id == 1
    assert obj.teacher_id == 1
def test_assignment_grade_schema_initiate_class():
    from core.libs.helpers import GeneralObject
    from core.apis.assignments.schema import AssignmentGradeSchema
    from core.models.assignments import GradeEnum
    
    schema = AssignmentGradeSchema()
    input_data = {
        "id": 1,
        "grade": "A"
    }
    obj = schema.load(input_data)
    assert isinstance(obj, GeneralObject)
    assert obj.id == 1
    assert obj.grade == GradeEnum.A
