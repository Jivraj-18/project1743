<template>
  <div class="container">
    <div class="header-section">
      <h2>Assignment Questions</h2>
      <div class="deadline-section">
        <label>Deadline: {{ formattedDeadline }}</label>
      </div>
    </div>
    <div class="navbar">
      <ul>
        <li v-for="(question, index) in questions" :key="question.question_id" 
            @click="selectQuestion(index)" 
            :class="{ active: selectedQuestionIndex === index }">
          Q{{ index + 1 }}
        </li>
      </ul>
    </div>
    <div class="content">
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else-if="error" class="error-message">Error: {{ error }}</div>
      <div v-else>
        <div v-if="selectedQuestion" class="question-card">
          <div class="question-header">
            <span class="question-type-badge" :class="selectedQuestion.question_type.toLowerCase()">
              {{ getQuestionTypeDisplay(selectedQuestion.question_type) }}
            </span>
            <span class="question-marks">{{ selectedQuestion.marks }} marks</span>
          </div>
          <div class="question-body">
            <p class="question-text"><strong>Q:</strong> {{ selectedQuestion.question }}</p>
            
            <!-- Options for MCQ and MSQ -->
            <div v-if="selectedQuestion.options" class="options-container">
              <p><strong>Options:</strong></p>
              <ul class="options-list">
                <li v-for="(option, index) in selectedQuestion.options" :key="index"
                    :class="{ 'submitted-answer': isSubmittedAnswer(selectedQuestion.question_id, String.fromCharCode(65 + index)) }">
                  
                  <!-- MCQ type (radio buttons) -->
                  <div v-if="selectedQuestion.question_type === 'MCQ'" class="option-select mcq">
                    <input type="radio" 
                           :id="`option-${selectedQuestion.question_id}-${index}`"
                           :name="`question-${selectedQuestion.question_id}`"
                           :value="String.fromCharCode(65 + index)"
                           v-model="answers[selectedQuestion.question_id]"
                           :disabled="submitted">
                    <label :for="`option-${selectedQuestion.question_id}-${index}`">
                      <span class="option-label">{{ String.fromCharCode(65 + index) }}.</span> 
                      <span>{{ option }}</span>
                    </label>
                  </div>
                  
                  <!-- MSQ type (checkboxes) -->
                  <div v-else-if="selectedQuestion.question_type === 'MSQ'" class="option-select msq">
                    <input type="checkbox"
                           :id="`option-${selectedQuestion.question_id}-${index}`"
                           :value="String.fromCharCode(65 + index)"
                           v-model="multiSelectAnswers[selectedQuestion.question_id]"
                           @change="updateMSQAnswer(selectedQuestion.question_id)"
                           :disabled="submitted">
                    <label :for="`option-${selectedQuestion.question_id}-${index}`">
                      <span class="option-label">{{ String.fromCharCode(65 + index) }}.</span> 
                      <span>{{ option }}</span>
                    </label>
                  </div>
                  
                  <!-- Default display for other question types -->
                  <div v-else>
                    <span class="option-label">{{ String.fromCharCode(65 + index) }}.</span> 
                    <span>{{ option }}</span>
                  </div>
                  
                  <span v-if="isSubmittedAnswer(selectedQuestion.question_id, String.fromCharCode(65 + index))" class="submitted-badge">Your Answer</span>
                </li>
              </ul>
            </div>
            
            <!-- NAT question (numeric input) -->
            <div v-if="selectedQuestion.question_type === 'NAT'" class="nat-answer-input">
              <p><strong>Your Answer:</strong></p>
              <input type="text" 
                     v-model="answers[selectedQuestion.question_id]" 
                     placeholder="Enter your answer" 
                     :disabled="submitted"
                     class="nat-input">
              <p v-if="getSubmittedAnswer(selectedQuestion.question_id)" class="submitted-nat-answer">
                <strong>Submitted Answer:</strong> {{ getSubmittedAnswer(selectedQuestion.question_id) }}
              </p>
            </div>
            
            <div class="submission-info" v-if="getSubmittedMarks(selectedQuestion.question_id) !== null">
              <p class="marks-obtained">
                <strong>Marks Obtained:</strong> 
                {{ getSubmittedMarks(selectedQuestion.question_id) }} / {{ selectedQuestion.marks }}
              </p>
            </div>
            
            <div class="hint-section">
              <button @click="toggleHint(selectedQuestion.question_id)" class="btn btn-sm btn-outline">
                {{ visibleHints[selectedQuestion.question_id] ? 'Hide Hint' : 'Show Hint' }}
              </button>
              <p v-if="visibleHints[selectedQuestion.question_id]" class="hint-text">
                <strong>Hint:</strong> {{ selectedQuestion.hints }}
              </p>
            </div>
          </div>
        </div>
        
        <div class="submission-actions" v-if="!submitted">
          <button @click="saveProgress" class="btn btn-secondary">Save Progress</button>
          <button @click="submitAssignment" class="btn btn-primary">Submit Answers</button>
        </div>
        
        <div class="submission-summary" v-if="submission">
          <h3>Submission Summary</h3>
          <p><strong>Submitted on:</strong> {{ formatDate(submission.submission_date) }}</p>
          <p><strong>Total Score:</strong> {{ submission.marks_obtained }} / {{ getTotalMarks() }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue';

export default {
  data() {
    return {
      questions: [],
      loading: true,
      error: null,
      visibleHints: reactive({}),
      deadline: "",
      selectedQuestionIndex: 0,
      submission: null,
      answers: reactive({}), // For MCQ and NAT answers
      multiSelectAnswers: reactive({}), // For MSQ answers (checkboxes)
      submitted: false
    };
  },
  computed: {
    selectedQuestion() {
      return this.questions[this.selectedQuestionIndex] || null;
    },
    formattedDeadline() {
      if (!this.deadline) return "Not set";
      const date = new Date(this.deadline);
      return date.toLocaleString();
    }
  },
  props: {
    assignmentId: String,
    studentId: String,
  },
  mounted() {
    this.fetchData();
  },
  watch: {
    assignmentId: "fetchData",
    studentId: "fetchData",
  },
  methods: {
    async fetchData() {
      const assignmentId = this.$route.params.assignment_id;
      try {
        // Get user data from localStorage
        const userData = JSON.parse(localStorage.getItem('userdata'));
        const studentId = userData.student_id;
        
        const assignmentResponse = await fetch(`http://localhost:5000/api/assignments/${assignmentId}/${studentId}`, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
         
        if (!assignmentResponse.ok) {
          throw new Error(`HTTP error! Status: ${assignmentResponse.status}`);
        }
        
        const data = await assignmentResponse.json();
        this.questions = data.questions;
        this.submission = data.submission;
        
        // Initialize the multiSelectAnswers for MSQ questions
        this.questions.forEach(question => {
          if (question.question_type === 'MSQ') {
            this.multiSelectAnswers[question.question_id] = [];
          }
        });
        
        // Preload student answers if available
        this.preloadStudentAnswers();
        
        // Set submitted flag if there's a submission
        this.submitted = !!this.submission;
        
        // Get deadline from the response if available
        if (data.deadline) {
          this.deadline = data.deadline;
        }
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    
    preloadStudentAnswers() {
      if (!this.submission || !this.submission.marks_answers) return;
      
      // For each question that has a submitted answer
      Object.keys(this.submission.marks_answers).forEach(questionId => {
        const question = this.questions.find(q => q.question_id == questionId);
        const markedAnswer = this.submission.marks_answers[questionId].marked_answers;
        
        if (!question) return;
        
        if (question.question_type === 'MSQ') {
          // For MSQ, split the comma-separated answers and set them in multiSelectAnswers
          const selectedOptions = markedAnswer.split(',');
          this.multiSelectAnswers[questionId] = selectedOptions;
        } else {
          // For MCQ and NAT, set the answer directly
          this.answers[questionId] = markedAnswer;
        }
      });
    },
    
    updateMSQAnswer(questionId) {
      // When MSQ checkboxes change, update the answers object with comma-separated values
      const selected = this.multiSelectAnswers[questionId] || [];
      this.answers[questionId] = selected.join(',');
    },
    
    getQuestionTypeDisplay(type) {
      const types = {
        'MCQ': 'Multiple Choice',
        'MSQ': 'Multiple Select',
        'NAT': 'Numerical Answer'
      };
      return types[type] || type;
    },
    
    toggleHint(questionId) {
      this.visibleHints[questionId] = !this.visibleHints[questionId];
    },
    
    selectQuestion(index) {
      this.selectedQuestionIndex = index;
    },
    
    getSubmittedAnswer(questionId) {
      if (!this.submission || !this.submission.marks_answers || !this.submission.marks_answers[questionId]) {
        return null;
      }
      return this.submission.marks_answers[questionId].marked_answers;
    },
    
    getSubmittedMarks(questionId) {
      if (!this.submission || !this.submission.marks_answers || !this.submission.marks_answers[questionId]) {
        return null;
      }
      return this.submission.marks_answers[questionId].marks;
    },
    
    isSubmittedAnswer(questionId, option) {
      const submittedAnswer = this.getSubmittedAnswer(questionId);
      if (!submittedAnswer) return false;
      
      if (submittedAnswer.includes(',')) {
        // For MSQ questions (multiple answers)
        return submittedAnswer.split(',').includes(option);
      }
      
      // For MCQ questions (single answer)
      return submittedAnswer === option;
    },
    
    formatDate(dateString) {
      if (!dateString) return "Not submitted";
      const date = new Date(dateString);
      return date.toLocaleString();
    },
    
    getTotalMarks() {
      return this.questions.reduce((total, question) => total + question.marks, 0);
    },
    
    async saveProgress() {
      const assignmentId = this.$route.params.assignment_id;
      const userData = JSON.parse(localStorage.getItem('userdata'));
      const studentId = userData.student_id;
      
      try {
        const response = await fetch(`http://localhost:5000/api/assignments/${assignmentId}/${studentId}/save`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({ answers: this.answers })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        alert("Your progress has been saved!");
      } catch (err) {
        alert(`Error saving progress: ${err.message}`);
      }
    },
    
    async submitAssignment() {
      // Check if all questions have answers
      const unanswered = this.questions.filter(question => 
        !this.answers[question.question_id] || this.answers[question.question_id] === ""
      );
      
      if (unanswered.length > 0) {
        const confirm = window.confirm(`You have ${unanswered.length} unanswered question(s). Do you still want to submit?`);
        if (!confirm) return;
      }
      
      const assignmentId = this.$route.params.assignment_id;
      const userData = JSON.parse(localStorage.getItem('userdata'));
      const studentId = userData.student_id;
      
      try {
        const response = await fetch(`http://localhost:5000/api/assignments`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
        student_id: studentId,
        assignment_id: assignmentId,
        student_answers: this.answers,
        code: "" // Empty for non-programming assignments
      })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const result = await response.json();
        this.submission = result.submission;
        this.submitted = true;
        
        alert("Your assignment has been submitted successfully!");
      } catch (err) {
        alert(`Error submitting assignment: ${err.message}`);
      }
    }
  },
};
</script>

<style scoped>
/* CSS remains unchanged */
.container {
  display: flex;
  flex-direction: column;
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.header-section h2 {
  margin: 0;
  color: #333;
}

.deadline-section {
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
  font-weight: bold;
}

.navbar {
  display: flex;
  justify-content: center;
  background-color: #fff;
  padding: 10px;
  margin-bottom: 20px;
  border-radius: 6px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.05);
  overflow-x: auto;
}

.navbar ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 8px;
  margin: 0;
}

.navbar li {
  padding: 8px 15px;
  cursor: pointer;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.2s;
}

.navbar li:hover {
  background-color: #f5f5f5;
}

.navbar li.active {
  background-color: #4a6fa5;
  color: white;
  border-color: #4a6fa5;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.05);
}

.loading {
  text-align: center;
  padding: 40px;
  font-style: italic;
  color: #666;
}

.error-message {
  color: #d9534f;
  padding: 20px;
  border: 1px solid #d9534f;
  border-radius: 4px;
  background-color: #f9f2f2;
}

.question-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.question-type-badge {
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.question-type-badge.mcq {
  background-color: #5bc0de;
}

.question-type-badge.msq {
  background-color: #5cb85c;
}

.question-type-badge.nat {
  background-color: #f0ad4e;
}

.question-marks {
  color: #666;
  font-weight: bold;
}

.question-body {
  margin-bottom: 20px;
}

.question-text {
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 20px;
}

.options-container {
  margin-bottom: 20px;
}

.options-list {
  list-style-type: none;
  padding-left: 0;
}

.options-list li {
  padding: 12px;
  margin-bottom: 8px;
  background-color: #f9f9f9;
  border-radius: 4px;
  display: flex;
  align-items: center;
  position: relative;
}

.option-select {
  display: flex;
  align-items: center;
  flex: 1;
}

.option-select label {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin: 0;
  flex: 1;
}

.option-select input[type="radio"],
.option-select input[type="checkbox"] {
  margin-right: 10px;
}

.option-label {
  font-weight: bold;
  margin-right: 10px;
  min-width: 20px;
}

.submitted-answer {
  background-color: #e8f4fc;
  border-left: 3px solid #4a6fa5;
}

.submitted-badge {
  margin-left: auto;
  background-color: #4a6fa5;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.nat-answer-input {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.nat-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  margin-top: 5px;
}

.submitted-nat-answer {
  margin-top: 10px;
  padding: 8px;
  background-color: #e8f4fc;
  border-left: 3px solid #4a6fa5;
  border-radius: 4px;
}

.hint-section {
  margin-bottom: 15px;
}

.hint-text {
  padding: 10px;
  background-color: #f8f9fa;
  border-left: 3px solid #ffc107;
  margin-top: 10px;
}

.marks-obtained {
  padding: 10px;
  background-color: #f0f8ff;
  border-radius: 4px;
  font-weight: 500;
}

.submission-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin: 20px 0;
}

.submission-summary {
  margin-top: 30px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #4a6fa5;
}

.submission-summary h3 {
  margin-top: 0;
  color: #4a6fa5;
}

.btn {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #4a6fa5;
  color: white;
}

.btn-primary:hover {
  background-color: #3c5c8c;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-outline {
  background-color: transparent;
  border: 1px solid #4a6fa5;
  color: #4a6fa5;
}

.btn-outline:hover {
  background-color: #f0f5ff;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}
</style>