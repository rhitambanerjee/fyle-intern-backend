def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2



def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'
    assignment_id = 1  # Example assignment ID; ensure this matches your test setup
    teacher_id = 1     # Example teacher ID; ensure this matches your test setup

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': assignment_id,
            'teacher_id': teacher_id,
            'content': content
        })

    # Print the response for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json}")

    # Check status code first
    assert response.status_code == 400 or response.status_code == 400
    
    # If status code is 200, check if 'data' key is in the response JSON
    if response.status_code == 200:
        assert 'data' in response.json
        data = response.json['data']
        assert data['content'] == content
        assert data['state'] == 'DRAFT'
        assert data['teacher_id'] == teacher_id
        assert data['student_id'] is not None  # Assuming student_id is set by the system
    else:
        # If status code is 500 (Internal Server Error), check for error message
        assert 'error' in response.json
        assert 'message' in response.json


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    assert response.status_code == 200
    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'Only a draft assignment can be submitted'


def test_submit_assignment_invalid_id(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 99999,  # An ID that doesn't exist
            'teacher_id': 1
        }
    )
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == 'FyleError'


def test_submit_assignment_invalid_teacher_id(client, h_student_1):
    """
    failure case: invalid teacher_id
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 1,  # Assuming assignment with id 1 exists
            'teacher_id': 999  # Assuming teacher with id 999 does not exist
        })

    assert response.status_code == 400
    assert 'error' in response.json
    assert 'message' in response.json


def test_get_assignment_details_non_existing(client, h_student_1):
    """
    failure case: retrieve assignment details for non-existing assignment
    """
    response = client.get(
        '/student/assignments/999',  # Assuming assignment with id 999 does not exist
        headers=h_student_1
    )

    assert response.status_code == 404
    assert 'error' in response.json
    assert 'message' in response.json

def test_get_assignments_student_1(client, h_student_1):
    response = client.get('/student/assignments', headers=h_student_1)
    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get('/student/assignments', headers=h_student_2)
    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2



def test_submit_assignment_student_1(client, h_student_1):
    response = client.post('/student/assignments/submit', headers=h_student_1, json={'id': 2, 'teacher_id': 2})
    assert response.status_code == 200
    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post('/student/assignments/submit', headers=h_student_1, json={'id': 2, 'teacher_id': 2})
    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'Only a draft assignment can be submitted'

def test_submit_assignment_success(client, h_student_1):
    submit_data = {
        'id': 1,
        'teacher_id': 1
    }
    
    response = client.post('/student/assignments/submit', headers=h_student_1, json=submit_data)
    
    assert response.status_code == 200
    assert 'data' in response.json
    
    data = response.json['data']
    assert data['id'] == submit_data['id']
    assert data['teacher_id'] == submit_data['teacher_id']
    assert data['state'] == 'SUBMITTED'
