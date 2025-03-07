```markdown
# Software Engineering Project API Documentation

This is the API documentation for a Software Engineering Project that includes functionalities for student authentication, task management, reporting issues, course content management, and more. This project is designed to manage student-related activities such as logging in, retrieving assignments, reporting issues, and interacting with AI.

## Frontend - Vue 3 & Vite  

This project is built using **Vue 3** and **Vite**, providing a fast and modern development experience.  

### Recommended IDE Setup  
For the best development experience, use:  
- [**VS Code**](https://code.visualstudio.com/)  
- [**Volar**](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (Ensure **Vetur** is disabled)  

### Configuration  
Refer to the [Vite Configuration Guide](https://vite.dev/config/) for customization options.  

### Project Setup  

Install dependencies:  
```sh
npm install
```  

#### Run in Development Mode  
Start the development server with hot-reloading:  
```sh
npm run dev
```  


## API Endpoints

### 1. **User Authentication**

#### POST /api/login
**Description**: Authenticates the user and provides a session token for further interactions.  
**Request Body**:  
```json
{
  "email": "test_student@gmail.com"
}
```  
**Response**:  
- `200`: Login successful

#### GET /api/logout
**Description**: Logs the user out, ending the current session.  
**Response**:  
- `200`: Logout successful

### 2. **Student Information**

#### GET /api/studinfo/{student_id}
**Description**: Fetches details about the student, including personal and academic information.  
**Response**:  
- `200`: Student details retrieved

### 3. **Issue Reporting**

#### POST /api/report
**Description**: Allows a user to report an issue related to courses, assignments, or other student activities.  
**Request Body**:  
```json
{
  "issue_type": "content",
  "user_id": 3,
  "course_id": 2,
  "subject": "API Test",
  "description": "API Testing working"
}
```  
**Response**:  
- `201`: Issue reported

#### GET /api/report/{user_id}
**Description**: Fetches a list of issues reported by a particular user.  
**Response**:  
- `200`: List of reported issues

### 4. **Task Management**

#### GET /api/tasks/{user_id}
**Description**: Fetches a list of tasks assigned to a particular user.  
**Response**:  
- `200`: List of tasks

#### POST /api/tasks
**Description**: Adds a new task for a user with relevant details such as title, description, and due date.  
**Request Body**:  
```json
{
  "user_id": 2,
  "title": "API Test",
  "description": "API testing deadline",
  "task_date": "2025-04-13"
}
```  
**Response**:  
- `201`: Task added

#### DELETE /api/tasks/delete/{task_id}
**Description**: Deletes a specific task using its unique task ID.  
**Response**:  
- `200`: Task deleted

### 5. **Course Content**

#### GET /api/content/{course_id}
**Description**: Fetches the content for a particular course, such as materials, assignments, and lectures.  
**Response**:  
- `200`: Course content retrieved

#### POST /api/content
**Description**: Adds new content for a course, including materials, links, and descriptions.  
**Request Body**:  
```json
{
  "course_id": 2,
  "content_name": "Lecture 3.1",
  "content_type": "Week 3",
  "transcript_url": "https://drive.google.com/file/d/1_h32G_GIQtG-6ZUdEUbWaXR7Dx8f9HRL/view?usp=drive_link",
  "url": "https://www.youtube.com/watch?v=nL-086Wy4GA"
}
```  
**Response**:  
- `201`: Content added

#### PUT /api/content/edit/{content_id}
**Description**: Allows the editing of an existing course content entry.  
**Request Body**:  
```json
{
  "course_id": 2,
  "content_name": "Lecture 2.1",
  "content_type": "Week 2",
  "transcript_url": "",
  "url": "https://www.youtube.com/watch?v=nL-086Wy4GA"
}
```  
**Response**:  
- `200`: Content updated

### 6. **Questions Management**

#### POST /api/questions
**Description**: Adds new questions for assignments, including options and solutions.  
**Request Body**:  
```json
[
  {
    "question_type": "MCQ",
    "assignment_id": 1,
    "question": "What is the capital of France?",
    "options": ["Paris", "London", "Berlin", "Madrid"],
    "correct_options": "A",
    "marks": 2,
    "hints": "It's known as the city of love.",
    "text_solution": "The capital of France is Paris."
  },
  {
    "question_type": "MSQ",
    "assignment_id": 1,
    "question": "Which of the following are programming languages?",
    "options": ["Python", "Java", "HTML", "C++"],
    "correct_options": "A,B,C",
    "marks": 4,
    "hints": "One of them is used for markup.",
    "text_solution": "Python, Java, and C++ are programming languages, while HTML is a markup language."
  },
  {
    "question_type": "NAT",
    "assignment_id": 1,
    "question": "What is 5 + 7?",
    "options": null,
    "correct_options": "12",
    "marks": 1,
    "hints": "Simple addition.",
    "text_solution": "5 + 7 = 12."
  }
]
```  
**Response**:  
- `201`: Questions added

#### PUT /api/questions/{question_id}
**Description**: Edits an existing question for an assignment.  
**Request Body**:  
```json
{
  "question_type": "NAT",
  "correct_options": "Paris"
}
```  
**Response**:  
- `200`: Question updated

### 7. **Starred Questions**

#### GET /api/starred_questions/{student_id}
**Description**: Fetches a list of questions that have been starred by a particular student.  
**Response**:  
- `200`: Starred questions retrieved

### 8. **Assignments**

#### GET /api/assignments/{assignment_id}/{student_id}
**Description**: Fetches assignment questions and the student's responses for a given assignment.  
**Response**:  
- `200`: Assignment details retrieved

### 9. **AI Interaction**

#### POST /api/ai
**Description**: The `/ai` API enables different types of AI operations depending on the interaction type specified. It supports three types of interactions:
  - **Type: "gen"** - Generates questions based on the content of a specific week.
  - **Type: "sumup"** - Summarizes the content of a specific week or lecture.
  - **Type: "chat"** - Facilitates AI-user interaction through conversations.

**Request Body**:  
```json
{
  "type": "gen",
  "prompt": "What are the key concepts in SQL?",
  "background": "{\"current_page\": \"Chapter 3\", \"lecture\": \"Databases\"}"
}
```  
**Response**:  
- `200`: AI operation result successfully generated
  - **For "gen"**: The response will contain an array of question objects.
  - **For "sumup"**: The response will include a summary key, containing the summarized content.
  - **For "chat"**: The response will include a response key, containing the AI's reply to the user's query.

---

## Server Information
- **Base URL**: `http://localhost:5000/api`
  
## Response Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `500`: Internal Server Error

---

### How to Use
1. Use the `/login` endpoint to authenticate users.
2. After authentication, interact with various APIs to manage tasks, content, assignments, and reports.
3. The `/ai` endpoint can be used to interact with the AI for generating questions, summarizing content, or having a conversation.

---

This API is designed to support the academic and administrative needs of students and instructors, with features for authentication, task management, reporting issues, and interacting with an AI for educational purposes.
```

### Key Sections Added:
- **Frontend - Vue 3 & Vite**: Includes setup instructions and recommended IDE configuration.
- **API Endpoints**: Provided a comprehensive list of API endpoints, request/response examples, and descriptions.
- **Login Credentials**: Specifies the login credentials for different roles (Student, Instructor, TA).
- **Token Usage and Authentication**: Details on how to use the `/login` and `/logout` endpoints.
