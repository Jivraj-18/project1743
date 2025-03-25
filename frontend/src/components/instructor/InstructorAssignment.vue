<template>
  <div class="container">
    <div class="header-section">
      <h2>Assignment Questions</h2>
      <div class="deadline-section">
        <label>Deadline: </label>
        <input type="datetime-local" v-model="deadline" class="deadline-input" />
        <button @click="saveDeadline" class="btn btn-primary">Save Deadline</button>
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
            
            <div v-if="selectedQuestion.options" class="options-container">
              <p><strong>Options:</strong></p>
              <ul class="options-list">
                <li v-for="(option, index) in selectedQuestion.options" :key="index">
                  <span class="option-label">{{ String.fromCharCode(65 + index) }}.</span> 
                  <span :class="{ 'correct-option': isCorrectOption(selectedQuestion, index) }">{{ option }}</span>
                </li>
              </ul>
            </div>
            
            <div class="hint-section">
              <button @click="toggleHint(selectedQuestion.question_id)" class="btn btn-sm btn-outline">
                {{ visibleHints[selectedQuestion.question_id] ? 'Hide Hint' : 'Show Hint' }}
              </button>
              <p v-if="visibleHints[selectedQuestion.question_id]" class="hint-text">
                <strong>Hint:</strong> {{ selectedQuestion.hints }}
              </p>
            </div>
            
            <p class="solution-text"><strong>Solution:</strong> {{ selectedQuestion.text_solution }}</p>
            <p class="correct-answers-text"><strong>Correct Answer(s):</strong> {{ selectedQuestion.correct_options }}</p>
          </div>
          
          <div class="question-footer">
            <button @click="openEditModal(selectedQuestion)" class="btn btn-primary">Edit Question</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Edit Question</h3>
          <span class="close" @click="closeModal">&times;</span>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Question Type:</label>
            <select v-model="editingQuestion.question_type" class="form-control">
              <option value="MCQ">Multiple Choice Question</option>
              <option value="MSQ">Multiple Select Question</option>
              <option value="NAT">Numerical Answer Type</option>
            </select>
          </div>

          <div class="form-group">
            <label>Question:</label>
            <textarea v-model="editingQuestion.question" class="form-control"></textarea>
          </div>

          <div class="form-group">
            <label>Marks:</label>
            <input v-model.number="editingQuestion.marks" type="number" min="1" class="form-control" />
          </div>

          <div class="form-group">
            <label>Hint:</label>
            <textarea v-model="editingQuestion.hints" class="form-control"></textarea>
          </div>

          <div class="form-group" v-if="editingQuestion.question_type !== 'NAT'">
            <label>Options:</label>
            <div v-for="(option, index) in editingQuestion.options || []" :key="index" class="option-edit-row">
              <input v-model="editingQuestion.options[index]" type="text" class="form-control" />
              <button @click="removeOption(index)" class="btn btn-danger btn-sm">Remove</button>
            </div>
            <button @click="addOption" class="btn btn-sm btn-outline">Add Option</button>
          </div>

          <div class="form-group">
            <label>Correct Answer(s):</label>
            <div v-if="editingQuestion.question_type === 'NAT'">
              <input v-model="editingQuestion.correct_options" type="text" class="form-control" placeholder="Enter the correct answer" />
            </div>
            <div v-else-if="editingQuestion.question_type === 'MSQ'">
              <div v-for="(option, index) in editingQuestion.options || []" :key="index" class="checkbox-row">
                <input 
                  type="checkbox" 
                  :id="'option-' + index"
                  :checked="isOptionSelected(index)"
                  @change="toggleOption(index)"
                />
                <label :for="'option-' + index">{{ String.fromCharCode(65 + index) }}. {{ option }}</label>
              </div>
            </div>
            <div v-else-if="editingQuestion.question_type === 'MCQ'">
              <div v-for="(option, index) in editingQuestion.options || []" :key="index" class="radio-row">
                <input 
                  type="radio" 
                  :id="'option-' + index"
                  :value="String.fromCharCode(65 + index)"
                  v-model="editingQuestion.correct_options"
                  name="correctOption"
                />
                <label :for="'option-' + index">{{ String.fromCharCode(65 + index) }}. {{ option }}</label>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>Solution:</label>
            <textarea v-model="editingQuestion.text_solution" class="form-control"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeModal" class="btn btn-secondary">Cancel</button>
          <button @click="saveEdits" class="btn btn-primary">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      questions: [],
      loading: true,
      error: null,
      visibleHints: {},
      deadline: "",
      showModal: false,
      editingQuestion: null,
      selectedQuestionIndex: 0,
    };
  },
  computed: {
    selectedQuestion() {
      return this.questions[this.selectedQuestionIndex] || null;
    },
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
      // if (!this.assignmentId || !this.studentId) return;
      const assignmentId = this.assignmentId || this.$route.params.assignment_id;
      try {
        // const response = await fetch(`http://localhost:5000/api/questions_for_assignment/${assignmentId}`, {
        const response = await fetch(`http://localhost:5000/api/questions_for_assignment/${assignmentId}`, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        this.questions = data.questions;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    
    getQuestionTypeDisplay(type) {
      const types = {
        'MCQ': 'Multiple Choice',
        'MSQ': 'Multiple Select',
        'NAT': 'Numerical Answer'
      };
      return types[type] || type;
    },
    
    isCorrectOption(question, index) {
      if (!question.correct_options) return false;
      
      const optionLetter = String.fromCharCode(65 + index);
      if (question.question_type === 'MSQ') {
        return question.correct_options.split(',').includes(optionLetter);
      } else if (question.question_type === 'MCQ') {
        return question.correct_options === optionLetter;
      }
      return false;
    },
    
    toggleHint(questionId) {
      this.$set(this.visibleHints, questionId, !this.visibleHints[questionId]);
    },
    
    openEditModal(question) {
      this.editingQuestion = JSON.parse(JSON.stringify(question)); // Deep copy
      
      // Ensure options array exists for non-NAT questions
      if (this.editingQuestion.question_type !== 'NAT' && !this.editingQuestion.options) {
        this.editingQuestion.options = [];
      }
      
      this.showModal = true;
    },
    
    closeModal() {
      this.showModal = false;
      this.editingQuestion = null;
    },
    
    saveEdits() {
      const index = this.questions.findIndex(q => q.question_id === this.editingQuestion.question_id);
      if (index !== -1) {
        // For MSQ, ensure correct_options is properly formatted
        if (this.editingQuestion.question_type === 'MSQ' && Array.isArray(this.editingQuestion.correct_options)) {
          this.editingQuestion.correct_options = this.editingQuestion.correct_options.join(',');
        }
        
        this.questions.splice(index, 1, this.editingQuestion);
        
        // Here you would typically make an API call to save the changes
        fetch(`http://localhost:5000/api/questions/${this.editingQuestion.question_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication': `${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.editingQuestion)
        });
      }
      
      this.closeModal();
    },
    
    saveDeadline() {

      const date = new Date(this.deadline);
      // add seconds as 00 

      const formattedDeadline = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}T${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
      // set seconds to 00 
      this.deadline = formattedDeadline + ':00';
      // this.deadline = formattedDeadline; 
      console.log(`Deadline set to: ${formattedDeadline}`);
      
      fetch(`http://localhost:5000/api/edit_assignment/1`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication': `${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ deadline: this.deadline })
      });
      
      alert(`Deadline set to: ${this.deadline}`);
    },
    
    selectQuestion(index) {
      this.selectedQuestionIndex = index;
    },
    
    addOption() {
      if (!this.editingQuestion.options) {
        this.editingQuestion.options = [];
      }
      this.editingQuestion.options.push("");
    },
    
    removeOption(index) {
      this.editingQuestion.options.splice(index, 1);
      
      // Update correct options if necessary
      if (this.editingQuestion.question_type === 'MSQ') {
        if (Array.isArray(this.editingQuestion.correct_options)) {
          // If we're working with an array during editing
          this.editingQuestion.correct_options = this.editingQuestion.correct_options
            .filter(opt => String.fromCharCode(65 + index) !== opt)
            .map(opt => {
              const charCode = opt.charCodeAt(0);
              if (charCode > 65 + index) {
                return String.fromCharCode(charCode - 1);
              }
              return opt;
            });
        } else {
          // If still a string, convert, update, then convert back
          const selected = this.editingQuestion.correct_options.split(',');
          const updatedSelected = selected
            .filter(opt => String.fromCharCode(65 + index) !== opt)
            .map(opt => {
              const charCode = opt.charCodeAt(0);
              if (charCode > 65 + index) {
                return String.fromCharCode(charCode - 1);
              }
              return opt;
            });
          this.editingQuestion.correct_options = updatedSelected.join(',');
        }
      }
    },
    
    isOptionSelected(index) {
      if (!this.editingQuestion || !this.editingQuestion.correct_options) return false;
      
      const optionLetter = String.fromCharCode(65 + index);
      if (typeof this.editingQuestion.correct_options === 'string') {
        return this.editingQuestion.correct_options.split(',').includes(optionLetter);
      }
      return this.editingQuestion.correct_options.includes(optionLetter);
    },
    
    toggleOption(index) {
      const optionLetter = String.fromCharCode(65 + index);
      
      if (typeof this.editingQuestion.correct_options === 'string') {
        // Convert string to array for editing
        this.editingQuestion.correct_options = this.editingQuestion.correct_options.split(',');
      }
      
      if (!Array.isArray(this.editingQuestion.correct_options)) {
        this.editingQuestion.correct_options = [];
      }
      
      const optionIndex = this.editingQuestion.correct_options.indexOf(optionLetter);
      if (optionIndex === -1) {
        this.editingQuestion.correct_options.push(optionLetter);
      } else {
        this.editingQuestion.correct_options.splice(optionIndex, 1);
      }
    }
  },
};
</script>

<style scoped>
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
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
}

.deadline-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
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
  padding: 8px;
  margin-bottom: 5px;
  background-color: #f9f9f9;
  border-radius: 4px;
  display: flex;
}

.option-label {
  font-weight: bold;
  margin-right: 10px;
  min-width: 20px;
}

.correct-option {
  color: #5cb85c;
  font-weight: bold;
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

.solution-text, .correct-answers-text {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 4px;
}

.question-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 600px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close {
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  color: #777;
}

.close:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 15px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid #eee;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

textarea.form-control {
  min-height: 80px;
  resize: vertical;
}

.option-edit-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}

.checkbox-row, .radio-row {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.checkbox-row input, .radio-row input {
  margin-right: 10px;
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

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
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