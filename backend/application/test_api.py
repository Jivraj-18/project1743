import pytest
import requests
from datetime import datetime

# Base URL of the API
BASE_URL = "http://localhost:5000/api"

# Test user credentials
TEST_STUDENT = {"email": "test_student@gmail.com"}  # Ensure this user has 'student' role
TEST_INSTRUCTOR = {"email": "test_instructor@gmail.com"}
TEST_TA = {"email": "test_ta@gmail.com"}
TEST_UNAUTHORIZED_USER = {"email": "unauthorized_user@gmail.com"}

@pytest.fixture
def sample_task(get_auth_token):
    """Creates a sample task and returns its ID, ensuring deletion afterward."""
    task_data = {
        "title": "Sample Task",
        "description": "This is a sample task for testing.",
        "task_date": datetime.now().strftime("%Y-%m-%d"),
    }
    headers = {"Authentication": get_auth_token["Authorization"]}
    response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201, f"Task creation failed: {response.text}"
    task_id = response.json()["task_id"]
    
    yield task_id  # Provide the task ID to tests
    
    # Cleanup: Delete the created task after test
    requests.delete(f"{BASE_URL}/tasks/{task_id}")

@pytest.fixture
def get_instructor_auth_token():
    """Login as an instructor and return an authorization token."""
    response = requests.post(f"{BASE_URL}/login", json=TEST_INSTRUCTOR)
    assert response.status_code == 200, f"Login failed: {response.text}"

    data = response.json()
    token = data.get("token")
    user_id = data.get("id")
    roles = data.get("roles", [])

    assert "instructor" in roles, f"ERROR: This user does NOT have the 'instructor' role. Roles: {roles}"

    return {"Authorization": f"{token}", "user_id": user_id, "roles": roles}

@pytest.fixture
def get_ta_auth_token():
    """Login as a TA and return an authorization token."""
    response = requests.post(f"{BASE_URL}/login", json=TEST_TA)
    assert response.status_code == 200, f"Login failed: {response.text}"

    data = response.json()
    token = data.get("token")
    user_id = data.get("id")
    roles = data.get("roles", [])

    assert "ta" in roles, f"ERROR: This user does NOT have the 'ta' role. Roles: {roles}"

    return {"Authorization": f"{token}", "user_id": user_id, "roles": roles}

@pytest.fixture
def get_auth_token():
    """Login as a student and return an authorization token."""
    response = requests.post(f"{BASE_URL}/login", json=TEST_STUDENT)
    assert response.status_code == 200, f"Login failed: {response.text}"
    
    data = response.json()
    token = data.get("token")
    student_id = data.get("student_id")
    user_id = data.get("id")
    roles = data.get("roles", [])  # Retrieve roles explicitly

    print(f"🟢 Login Successful: Token Received, Student ID = {student_id}, User id = {user_id}, Roles = {roles}")

    assert "student" in roles, f"❌ ERROR: This user does NOT have the 'student' role. Roles: {roles}"

    return {"Authorization": f"{token}", "student_id": student_id, "user_id": user_id, "roles": roles}

# User Login - Student
def test_login_student():
    response = requests.post(f"{BASE_URL}/login", json=TEST_STUDENT)
    assert response.status_code == 200
    assert "token" in response.json()

# User Login - Instructor
def test_login_instructor():
    response = requests.post(f"{BASE_URL}/login", json=TEST_INSTRUCTOR)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "roles" in data
    assert "id" in data
    assert "instructor_id" in data

# Login Failure - Invalid Email
def test_login_invalid_email():
    payload = {"email": "invalid@example.com"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code == 401
    assert response.json()["message"] == "Invalid credentials"

# User Logout
def test_logout(get_auth_token):
    response = requests.get(f"{BASE_URL}/logout", headers={"Authorization": get_auth_token["Authorization"]})
    assert response.status_code == 200, f"Logout failed: {response.text}"

# Get Student Details
def test_get_student_details(get_auth_token):
    """Test fetching a valid student's details."""
    headers = {"Authentication": get_auth_token["Authorization"]}

    response = requests.get(f"{BASE_URL}/studinfo", headers=headers)
    assert response.status_code == 200, f"Failed: {response.text}"

    data = response.json()
    
    # Ensure all expected fields are present
    expected_fields = [
        "student_name", "enroll_date", "current_level", "dob", "about_me",
        "phone", "address", "email"
    ]
    
    for field in expected_fields:
        assert field in data, f"Missing field: {field}"

# Report an Issue (Valid Data)
def test_report_issue_valid(get_auth_token):
    """Test reporting an issue with valid data."""
    issue_data = {
        "issue_type": "content",
        "user_id": get_auth_token["user_id"],
        "course_id": 2,
        "subject": "API Test",
        "description": "API Testing working"
    }
    
    headers = {
        "Authentication": get_auth_token["Authorization"],
        "Content-Type": "application/json"
    }

    response = requests.post(f"{BASE_URL}/report", json=issue_data, headers=headers)
    assert response.status_code == 200, f"Failed: {response.text}"

    data = response.json()
    assert "message" in data, "Missing 'message' in response"
    assert "issue_id" in data, "Missing 'issue_id' in response"


# Report an Issue as an Unauthorized User
def test_report_issue_unauthorized():
    """Test reporting an issue without authentication."""
    issue_data = {
        "issue_type": "content",
        "user_id": 1,
        "course_id": 2,
        "subject": "Unauthorized Test",
        "description": "This should fail"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(f"{BASE_URL}/report", json=issue_data, headers=headers)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"


# Get Reported Issues for a Valid User
def test_get_reported_issues_valid(get_auth_token):
    """Test fetching reported issues for a valid user."""
    user_id = get_auth_token["user_id"]

    response = requests.get(f"{BASE_URL}/report/{user_id}", headers={"Authentication": get_auth_token["Authorization"]})
    assert response.status_code == 200, f"Failed: {response.text}"

    data = response.json()
    assert isinstance(data, list), "Expected a list of issues"
    if data:
        assert "issue_id" in data[0], "Expected 'issue_id' in response"


# Get Reported Issues for a Non-Existent User
def test_get_reported_issues_invalid():
    """Test fetching reported issues for a non-existent user."""
    invalid_user_id = "999999"

    response = requests.get(f"{BASE_URL}/report/{invalid_user_id}", headers={"Authentication": "InvalidToken"})
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"


# Verify response type is a list
def test_events_response_type():
    response = requests.get(f"{BASE_URL}/events")
    data = response.json()
    assert isinstance(data, list), "Expected a list in response"

# View Reports as an Authorized User
def test_view_reports_authorized(get_instructor_auth_token):
    """Test fetching unresolved reports as an authorized instructor/TA."""
    headers = {
        "Authentication": get_instructor_auth_token["Authorization"]
    }

    response = requests.get(f"{BASE_URL}/view_reports", headers=headers)
    assert response.status_code == 200, f"Failed: {response.text}"

    data = response.json()
    assert isinstance(data, list), "Expected response to be a list"

    if data:  # If there are reports, validate the expected fields
        expected_fields = ["issue_id", "issue_type", "course_name", "user_email", "subject", "description", "issue_date"]
        for field in expected_fields:
            assert field in data[0], f"Missing field: {field}"


# View Reports as an Unauthorized User
def test_view_reports_unauthorized(get_auth_token):
    """Test fetching reports as a student (unauthorized role)."""
    headers = {
        "Authentication": get_auth_token["Authorization"]
    }

    response = requests.get(f"{BASE_URL}/view_reports", headers=headers)
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"


def test_view_reports_no_issues(get_instructor_auth_token):
    """Test viewing reports when unresolved issues exist."""
    headers = {
        "Authentication": get_instructor_auth_token["Authorization"]
    }

    response = requests.get(f"{BASE_URL}/view_reports", headers=headers)
    assert response.status_code == 200, f"Failed: {response.text}"

    data = response.json()
    assert isinstance(data, list), "Expected a list"
    assert all("issue_id" in issue for issue in data), "Expected 'issue_id' in all responses"


# Verify each event contains required fields
def test_events_fields():
    response = requests.get(f"{BASE_URL}/events")
    data = response.json()
    
    if data:  # Only run checks if events exist
        for event in data:
            assert "event_id" in event, "Missing 'event_id' in event"
            assert "title" in event, "Missing 'title' in event"
            assert "date" in event, "Missing 'date' in event"
            assert "description" in event, "Missing 'description' in event"

# Verify empty response when no events exist
def test_events_empty_response():
    response = requests.get(f"{BASE_URL}/events")
    data = response.json()
    assert isinstance(data, list), "Expected a list even if empty"
    if not data:
        assert len(data) == 0, "Response should be an empty list when no events exist"

# Validate Date Format (Ensure Date is ISO 8601)
def test_events_date_format():
    response = requests.get(f"{BASE_URL}/events")
    data = response.json()

    if data:
        for event in data:
            date = event["date"]
            assert isinstance(date, str), "Date should be a string"
            assert "T" in date, "Date format should be ISO 8601 (YYYY-MM-DDTHH:MM:SS)"

# Handle Unexpected HTTP Methods (Ensure DELETE is blocked)
def test_events_invalid_method():
    response = requests.delete(f"{BASE_URL}/events")
    assert response.status_code in [400, 405], f"Unexpected behavior on DELETE request: {response.status_code}"

# Get Tasks for a Specific User
def test_get_tasks(get_auth_token):
    headers = {"Authentication": get_auth_token["Authorization"]}
    response = requests.get(f"{BASE_URL}/tasks", headers=headers)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert isinstance(response.json(), list), "Response should be a list of tasks"

# Create a New Task
def test_add_task(get_auth_token):
    task_data = {
        "title": "New Task",
        "description": "Testing task addition",
        "task_date": datetime.now().strftime("%Y-%m-%d"),
    }
    headers = {"Authentication": get_auth_token["Authorization"]}
    response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
    assert response.status_code == 201, f"Task creation failed: {response.text}"
    assert "task_id" in response.json(), "Response should contain task_id"

# Test: Delete an Existing Task (Uses Fixture)
def test_delete_task(get_auth_token, sample_task):
    headers = {"Authentication": get_auth_token["Authorization"]}

    response = requests.delete(f"{BASE_URL}/tasks/delete/{sample_task}", headers=headers)
    
    assert response.status_code == 200, f"Task deletion failed: {response.text}"
    assert response.json().get("message") == "Task deleted successfully", "Incorrect success message"

# Test: Delete a Non-Existent Task
def test_delete_non_existent_task(get_auth_token):
    headers = {"Authentication": get_auth_token["Authorization"]}

    response = requests.delete(f"{BASE_URL}/tasks/delete/999999", headers=headers)  # Assuming this task ID doesn't exist

    assert response.status_code == 404, f"Expected 404 for non-existent task: {response.text}"
    assert response.json().get("message") == "Task not found", "Incorrect error message"

# API Rejects Invalid Request Method (PUT)
def test_invalid_method():
    response = requests.put(f"{BASE_URL}/tasks")
    assert response.status_code == 405, f"Expected 405 Method Not Allowed, got {response.status_code}"

def test_get_non_existent_courses():
    student_id = 999
    response = requests.get(f"{BASE_URL}/mycourses/{student_id}")    
    assert response.status_code == 404, f"Expected 404, got : {response.text}"

def test_get_courses_for_student():
    student_id = 2
    response = requests.get(f"{BASE_URL}/mycourses/{student_id}")
    assert response.status_code == 200, f"Failed to fetch courses: {response.text}"
    assert isinstance(response.json(), dict), "Expected dictionary response"    

# to get course content  
def test_get_non_existent_course_content():
    course_id = 999  # Non-existent course ID
    response = requests.get(f"{BASE_URL}/content/{course_id}")  
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    assert response.json().get("message") == "Course not found", f"Unexpected response: {response.json()}"

def test_add_questions_valid(get_instructor_auth_token):
    print("from function", get_instructor_auth_token)

    data = {
        "category": "Math",
        "course_id": 1,
        "which_week": 2,
        "questions": [
            {
                "question_type": "MCQ",
                "question": "What is 2+2?",
                "options": ["1", "2", "3", "4"],
                "correct_options": "D",
                "marks": 5,
                "hints": "Think about addition.",
                "text_solution": "2+2 is 4."
            }
        ]
    }

    headers = {
        "Authentication": get_instructor_auth_token["Authorization"],  # Use Authentication instead of Authorization
        "Content-Type": "application/json"
    }

    response = requests.post(f"{BASE_URL}/questions", json=data, headers=headers)

    if response.status_code == 403:
        print(f"🔴 Authorization Failed: {response.json()}")
    elif response.status_code == 400:
        print(f"⚠ Validation Error: {response.json()}")

    assert response.status_code == 201, f"Failed: {response.text}"
    data = response.json()
    assert "message" in data
    assert data["message"] == "Assignment and questions added successfully"

# ✅ Test: Starred Questions Found for Student
def test_starred_questions_found(get_auth_token):
    student_id = get_auth_token["student_id"]
    headers = {
        "Authentication": get_auth_token["Authorization"],
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/starred_questions/{student_id}", headers=headers)
    
    if response.status_code == 404:
        pytest.skip("No starred questions found for this student; seed test data appropriately.")
    
    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()
    assert isinstance(data, list), "Expected response to be a list of starred questions"
    
    expected_keys = [
        "question_id", "question_type", "assignment_id", "assignment_category",
        "which_week", "question", "options", "correct_options", "marks", "hints", "text_solution"
    ]
    for question in data:
        for key in expected_keys:
            assert key in question, f"Missing key '{key}' in question: {question}"

# ✅ Test: Starred Questions Not Found for Student
def test_starred_questions_not_found():
    # Use a student ID that is not expected to have any starred questions
    non_existing_student_id = 9999
    headers = {
        "Authentication": "Bearer some_invalid_token",  # Adjust token if necessary
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/starred_questions/{non_existing_student_id}", headers=headers)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    data = response.json()
    assert data.get("message") == "No starred questions found", f"Unexpected response: {data}"

# ✅ Test: Get Students Scores Info (Assignment Submissions)
def test_assignment_submissions(get_instructor_auth_token):
    headers = {
        "Authentication": get_instructor_auth_token["Authorization"],
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/submissions", headers=headers)
    assert response.status_code == 200, f"Failed: {response.text}"
    
    data = response.json()
    assert isinstance(data, list), "Expected response to be a list"
    
    # If there are submissions, verify each entry's structure.
    if data:
        for course in data:
            assert "course_id" in course, f"Missing 'course_id' in {course}"
            assert "assignments" in course, f"Missing 'assignments' in {course}"
            assert isinstance(course["assignments"], list), f"'assignments' should be a list in {course}"
            
            for assignment in course["assignments"]:
                expected_keys = [
                    "assignment_id", "which_week", "category", "id",
                    "student_id", "marks_answers", "marks_obtained", "code", "submission_date"
                ]
                for key in expected_keys:
                    assert key in assignment, f"Missing key '{key}' in assignment: {assignment}"

def test_submit_assignment(get_auth_token):
    student_id = get_auth_token["student_id"]
    assignment_id = 4  # Ensure this assignment exists
    student_answers = {"8":"D"}  # Ensure valid question IDs

    submission_data = {
        "student_id": student_id,
        "assignment_id": assignment_id,
        "student_answers": student_answers,
        "code": ""
    }

    headers = {
        "Authentication": get_auth_token["Authorization"],
        "Content-Type": "application/json"
    }

    response = requests.post(f"{BASE_URL}/assignments", json=submission_data, headers=headers)
    
    assert response.status_code == 201, f"Assignment submission failed: {response.text}"
    data = response.json()
    assert "message" in data
    assert data["message"] == "Assignment submitted successfully"
    assert "total_marks" in data
    assert "details" in data

def test_get_non_existent_assignment_submission(get_auth_token):
    student_id = get_auth_token["student_id"]
    assignment_id = 99999  # Non-existent assignment

    headers = {
        "Authentication": get_auth_token["Authorization"],
        "Content-Type": "application/json"
    }

    response = requests.get(f"{BASE_URL}/assignments/{assignment_id}/{student_id}", headers=headers)
    assert response.status_code == 200, f"Expected 200 even for non-existent assignment, got {response.status_code}"
    
    data = response.json()
    assert "questions" in data
    assert "submission" in data
    assert data["submission"] is None, "Submission data should be None for non-existent assignments"

def test_update_assignment_deadline(get_instructor_auth_token):
    assignment_id = 1  # Ensure this assignment exists
    new_deadline = "2025-12-31T23:59:59"

    update_data = {"deadline": new_deadline}

    headers = {
        "Authentication": get_instructor_auth_token["Authorization"],
        "Content-Type": "application/json"
    }

    response = requests.put(f"{BASE_URL}/edit_assignment/{assignment_id}", json=update_data, headers=headers)

    assert response.status_code == 200, f"Failed to update deadline: {response.text}"
    assert response.json()["message"] == "Assignment updated successfully"

def test_update_deadline_non_existent_assignment(get_instructor_auth_token):
    assignment_id = 99999  # Ensure this assignment doesn't exist
    new_deadline = "2025-12-31T23:59:59"

    update_data = {"deadline": new_deadline}

    headers = {
        "Authentication": get_instructor_auth_token["Authorization"],
        "Content-Type": "application/json"
    }

    response = requests.put(f"{BASE_URL}/edit_assignment/{assignment_id}", json=update_data, headers=headers)

    # Ensure we get 404 Not Found
    assert response.status_code == 404, f"Expected 404, got {response.status_code}, Response: {response.json()}"
    assert response.json().get("error") == "Assignment not found", f"Unexpected response: {response.json()}"

def test_update_deadline_invalid_format(get_instructor_auth_token):
    assignment_id = 1  # Ensure assignment exists
    invalid_deadline = "31-12-2025 23:59"  # Wrong format

    update_data = {"deadline": invalid_deadline}

    headers = {
        "Authentication": get_instructor_auth_token["Authorization"],
        "Content-Type": "application/json"
    }

    response = requests.put(f"{BASE_URL}/edit_assignment/{assignment_id}", json=update_data, headers=headers)

    # Debugging logs
    print(f"Response Status: {response.status_code}")
    print(f"Response Data: {response.text}")

    assert response.status_code == 400, f"Expected 400 for invalid datetime format, got {response.status_code}"
    assert response.json().get("error") == "Invalid datetime format", f"Unexpected response: {response.json()}"


def test_remove_assignment_deadline(get_instructor_auth_token):
    assignment_id = 1  # Ensure this assignment exists

    update_data = {"deadline": None}

    headers = {
        "Authentication": get_instructor_auth_token["Authorization"],
        "Content-Type": "application/json"
    }

    response = requests.put(f"{BASE_URL}/edit_assignment/{assignment_id}", json=update_data, headers=headers)

    assert response.status_code == 200, f"Failed to remove deadline: {response.text}"
    assert response.json()["message"] == "Assignment updated successfully"

def test_instructor_cannot_fetch_student_details(get_instructor_auth_token):
    headers = {"Authentication": get_instructor_auth_token["Authorization"]}

    response = requests.get(f"{BASE_URL}/studinfo", headers=headers)
    
    assert response.status_code == 403, f"Expected 403 Forbidden, got {response.status_code}"
    assert response.json().get("message") == "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.", f"Unexpected response: {response.json()}"


def test_student_cannot_delete_another_students_task(get_auth_token):
    other_student_task_id = 5  # Task created by another student
    headers = {"Authentication": get_auth_token["Authorization"]}

    response = requests.delete(f"{BASE_URL}/tasks/delete/{other_student_task_id}", headers=headers)
    
    assert response.status_code == 403, f"Expected 403 Forbidden, got {response.status_code}"
    assert response.json().get("error") == "Unauthorized to delete this task", f"Unexpected response: {response.json()}"

def test_submit_assignment_without_answers(get_auth_token):
    student_id = get_auth_token["student_id"]
    assignment_id = 1  # Ensure this assignment exists

    submission_data = {
        "student_id": student_id,
        "assignment_id": assignment_id,
        "student_answers": {},  # Empty answers
        "code": ""
    }

    headers = {"Authentication": get_auth_token["Authorization"], "Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/assignments", json=submission_data, headers=headers)

    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
    assert response.json().get("error") == "No answers provided", f"Unexpected response: {response.json()}"

def test_student_cannot_add_course_content(get_auth_token):
    content_data = {
        "course_id": 1,
        "content_type": "video",
        "content_name": "Test Video",
        "url": "http://test.com/video.mp4",
        "transcript_url": "http://test.com/transcript.txt"
    }

    headers = {"Authorization": get_auth_token["Authorization"], "Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/content", json=content_data, headers=headers)
    
    assert response.status_code == 403, f"Expected 403 Forbidden, got {response.status_code}"

def test_unauthorized_user_cannot_edit_course_content():
    content_id = 1  # Ensure this content exists
    update_data = {"content_name": "Updated Content"}

    response = requests.put(f"{BASE_URL}/content/edit/{content_id}", json=update_data, headers={"Authorization": "InvalidToken"})
    
    assert response.status_code == 403, f"Expected 403 Forbidden, got {response.status_code}"

def test_create_task_invalid_date(get_auth_token):
    task_data = {
        "title": "Invalid Date Task",
        "description": "Should fail",
        "task_date": "32-13-2025",  # Invalid date format
        "user_id": get_auth_token["user_id"]
    }

    headers = {"Authentication": get_auth_token["Authorization"], "Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)

    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
    assert response.json().get("error") == "Invalid date format, expected YYYY-MM-DD", f"Unexpected response: {response.json()}"
