<template>
  <div :class="['content', { 'content-expanded': isSidebarCollapsed }]">
    <!-- Template 1: Options Selection -->
    <div v-if="step === 'options'" class="content-inner">
      <!-- Large Gray Bar -->
      <div class="ai-page-header">
        <h4 class="mb-0">Create with AI</h4>
      </div>
      <!-- Options Container -->
      <div class="ai-create-container">
        <!-- 1) Assignment Type -->
        <div class="ai-option-row">
          <span>Assignment Type</span>
          <select v-model="selectedPractice" class="form-select form-select-sm w-auto">
            <option value="Practice">Practice</option>
            <option value="Graded">Graded</option>
            <option value="Mock Exam">Mock Exam</option>
          </select>
        </div>
        <!-- 2) Week (disabled if Mock Exam is selected) -->
        <div class="ai-option-row">
          <span>Week</span>
          <select
            v-model="selectedWeek"
            class="form-select form-select-sm w-auto"
            :disabled="selectedPractice === 'Mock Exam'"
          >
            <option value="Week 1">Week 1</option>
            <option value="Week 2">Week 2</option>
          </select>
        </div>
        <!-- 3) Number of Questions (– 10 +) -->
        <div class="ai-option-row">
          <span>Number of Questions</span>
          <div class="number-spinner d-flex align-items-center">
            <button class="btn btn-sm btn-secondary me-2" @click="decrement">–</button>
            <span>{{ numberOfQuestions }}</span>
            <button
              class="btn btn-sm btn-secondary ms-2"
              @click="increment"
              :disabled="numberOfQuestions >= 10"
            >
              +
            </button>
          </div>
        </div>
        <!-- Create Button -->
        <div class="mt-3">
          <button class="btn btn-primary w-100" @click="createAssignment" :disabled="!canCreate">
            Create
          </button>
        </div>
      </div>
    </div>

    <!-- Template 2: Assignment Editor -->
    <div v-else :class="['content-inner', { 'content-expanded': isSidebarCollapsed }]">
      <div class="content-inner">
        <!-- Header Area -->
        <div class="assignment-header">
          <h5 class="fw-bold">{{ assignmentType }}</h5>
          <p class="mb-1">
            <small>Due: {{ dueDate }}</small
            ><br />
            <small>Last Submitted: {{ lastSubmitted }}</small>
          </p>
          <button
            class="btn btn-sm btn-outline-dark position-absolute"
            style="top: 1rem; right: 1rem"
            @click="editDeadline"
            :disabled="!isGraded"
          >
            Edit Deadline
          </button>
        </div>

        <!-- Question Navigation -->
        <div class="question-buttons mb-2">
          <button
            v-for="n in numberOfQuestions"
            :key="n"
            class="btn"
            :class="{
              'btn-primary': currentQuestion === n,
              'btn-secondary': currentQuestion !== n,
            }"
            @click="changeQuestion(n)"
          >
            {{ n }}
          </button>
        </div>
        <div class="progress mb-3">
          <div
            class="progress-bar bg-primary"
            role="progressbar"
            :style="progressStyle"
            :aria-valuenow="progress"
            aria-valuemin="0"
            aria-valuemax="100"
          ></div>
        </div>

        <!-- Question Box -->
        <div class="question-box">
          <div class="d-flex justify-content-between align-items-start mb-3">
            <p class="fw-bold mb-0">{{ currentQuestion }}. {{ currentQuestionText }}</p>
            <i class="bi bi-pencil" @click="editQuestion()"></i>
          </div>
          <form>
            <div v-for="(option, index) in options" :key="option.id" class="form-check mb-2">
              <input
                class="form-check-input"
                type="radio"
                :name="'question' + currentQuestion"
                :id="option.id"
                v-model="selectedAnswer"
                :value="option.id"
              />
              <label class="form-check-label" :for="option.id">
                {{ option.text }}
              </label>
            </div>
          </form>
          <!-- Inline Mark Adjustment Control -->
          <div class="d-flex justify-content-end align-items-center mt-2">
            <button
              class="btn btn-outline-secondary btn-sm me-2"
              @click="decreaseMarks"
              :disabled="marks <= 1"
            >
              -
            </button>
            <span class="me-2">{{ marks }} Mark</span>
            <button class="btn btn-outline-secondary btn-sm" @click="increaseMarks">+</button>
          </div>
        </div>

        <!-- Stats -->
        <div class="row g-3">
          <div class="col-md-6">
            <div class="stats-box">
              <p class="mb-1">Attempted by – {{ stats.attempted }}%</p>
              <p class="mb-1">Correct – {{ stats.correct }}%</p>
              <p class="mb-0">Incorrect – {{ stats.incorrect }}%</p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="stats-box">
              <p class="mb-1">Average no. of questions attempted – {{ stat.avgAttempted }}%</p>
              <p class="mb-1">Average no. of correct questions – {{ stat.avgCorrect }}%</p>
              <p class="mb-0">Average no. of incorrect questions – {{ stat.avgIncorrect }}%</p>
            </div>
          </div>
        </div>
        <button class="go-back-btn btn btn-outline-secondary" @click="goBack">← Go Back</button>
      </div>

      <!-- Edit Question Modal -->
      <div
        class="modal fade"
        id="editQuestionModal"
        tabindex="-1"
        aria-labelledby="editQuestionModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="editQuestionModalLabel">Edit Question</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveQuestion">
                <!-- Question Text -->
                <div class="mb-3">
                  <label class="form-label">Question Text</label>
                  <textarea
                    class="form-control"
                    v-model="editForm.questionText"
                    rows="3"
                    required
                  ></textarea>
                </div>
                <!-- Options -->
                <div class="mb-3">
                  <label class="form-label">Options</label>
                  <div v-for="(option, index) in editForm.options" :key="option.id" class="mb-2">
                    <div class="input-group">
                      <input
                        type="text"
                        class="form-control"
                        v-model="option.text"
                        :placeholder="'Option ' + (index + 1)"
                        required
                      />
                      <button
                        type="button"
                        class="btn btn-outline-danger"
                        @click="removeOption(index)"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                  <button
                    type="button"
                    class="btn btn-outline-primary btn-sm mt-2"
                    @click="addOption"
                    :disabled="editForm.options.length >= 5"
                  >
                    Add Option
                  </button>
                </div>
                <!-- Correct Answer -->
                <div class="mb-3">
                  <label class="form-label">Correct Answer</label>
                  <select class="form-select" v-model="editForm.correctAnswer" required>
                    <option value="">Select correct answer</option>
                    <option v-for="option in editForm.options" :key="option.id" :value="option.id">
                      {{ option.text }}
                    </option>
                  </select>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                Cancel
              </button>
              <button type="button" class="btn btn-primary" @click="saveQuestion">
                Save changes
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Deadline Modal -->
    <div
      class="modal fade"
      id="editDeadlineModal"
      tabindex="-1"
      aria-labelledby="editDeadlineModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editDeadlineModalLabel">Edit Deadline</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveDeadline">
              <!-- Date Picker -->
              <div class="mb-3">
                <label for="deadlineDate" class="form-label">Select Date</label>
                <input
                  type="date"
                  class="form-control"
                  id="deadlineDate"
                  v-model="editDeadlineForm.date"
                  required
                />
              </div>
              <!-- Time Picker -->
              <div class="mb-3">
                <label for="deadlineTime" class="form-label">Select Time</label>
                <input
                  type="time"
                  class="form-control"
                  id="deadlineTime"
                  v-model="editDeadlineForm.time"
                  required
                />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="saveDeadline">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router'
import assignments from '@/assets/assignments.json'

export default {
  props: {
    isSidebarCollapsed: Boolean,
  },
  setup() {
    const route = useRoute()
    return { route }
  },
  data() {
    return {
      // Step: 'options' for Template 1, 'editor' for Template 2
      step: 'options',
      bookmarked: false,
      // Template 1 selections
      selectedPractice: 'Practice', // Options: Practice, Graded, Mock Exam
      selectedWeek: 'Week 1',
      numberOfQuestions: 10,
      // Template 2 (shared) variables
      currentQuestion: 1,
      progress: 10,
      selectedAnswer: null,
      marks: 1,
      editForm: {
        questionText: '',
        options: [],
        correctAnswer: '',
      },
      editDeadlineForm: {
        date: '',
        time: '',
      },
    }
  },
  computed: {
    // isGraded is true if the assignment type is Graded
    isGraded() {
      return this.selectedPractice === 'Graded' || this.selectedPractice === 'Mock Exam'
    },
    // Compute week number: if Mock Exam is chosen, always use 2; otherwise derive from selectedWeek
    weekNumber() {
      return this.selectedPractice === 'Mock Exam' ? 2 : this.selectedWeek === 'Week 1' ? 1 : 2
    },
    assignmentType() {
      if (this.selectedPractice === 'Mock Exam') {
        return 'Mock Exam'
      }
      return this.selectedPractice === 'Graded' ? 'Graded Assignment' : 'Practice Assignment'
    },
    courseId() {
      return this.route.params.id
    },
    // Retrieve assignment data based on course and week
    assignmentData() {
      const typeKey = this.isGraded ? 'graded_assignments' : 'practice_assignments'
      return (
        (assignments[this.courseId] &&
          assignments[this.courseId][this.weekNumber] &&
          assignments[this.courseId][this.weekNumber][typeKey]) ||
        {}
      )
    },
    dueDate() {
      return this.assignmentData.dueDate || ''
    },
    lastSubmitted() {
      return this.assignmentData.lastSubmitted || ''
    },
    currentQuestionData() {
      return this.assignmentData.questions
        ? this.assignmentData.questions[this.currentQuestion - 1] || {}
        : {}
    },
    currentQuestionText() {
      return this.currentQuestionData.questionText || ''
    },
    options() {
      return this.currentQuestionData.options || []
    },
    stat() {
      return this.assignmentData.stat || {}
    },
    stats() {
      return this.currentQuestionData.stats || {}
    },
    progressStyle() {
      return { width: `${this.progress}%` }
    },
    // Create button enabled only if selections are valid
    canCreate() {
      if (this.selectedPractice !== 'Mock Exam' && !this.selectedWeek) return false
      return this.numberOfQuestions >= 1
    },
  },
  watch: {
    // Reset question state when isGraded changes
    isGraded() {
      this.currentQuestion = 1
      this.progress = 10
      this.selectedAnswer = null
    },
  },
  methods: {
    // Template 1 methods
    increment() {
      if (this.numberOfQuestions < 10) {
        this.numberOfQuestions += 1
      }
    },
    decrement() {
      if (this.numberOfQuestions > 1) {
        this.numberOfQuestions -= 1
      }
    },
    createAssignment() {
      // Switch to editor view (Template 2)
      this.step = 'editor'
    },
    goBack() {
      // Return to options view (Template 1)
      this.step = 'options'
    },
    // Template 2 methods
    changeQuestion(n) {
      this.currentQuestion = n
      this.progress = (n / this.numberOfQuestions) * 100
      this.selectedAnswer = null
    },
    editDeadline() {
      this.editDeadlineForm.date = this.dueDate ? this.dueDate.split(' ')[0] : ''
      this.editDeadlineForm.time = this.dueDate ? this.dueDate.split(' ')[1] : ''
      const modal = new bootstrap.Modal(document.getElementById('editDeadlineModal'))
      modal.show()
    },
    editQuestion() {
      this.editForm = {
        questionText: this.currentQuestionData.questionText,
        options: JSON.parse(JSON.stringify(this.currentQuestionData.options)),
        correctAnswer: this.currentQuestionData.correctAnswer,
      }
      const modal = new bootstrap.Modal(document.getElementById('editQuestionModal'))
      modal.show()
    },
    addOption() {
      if (this.editForm.options.length < 5) {
        this.editForm.options.push({
          id: `option${this.editForm.options.length + 1}`,
          text: '',
        })
      }
    },
    removeOption(index) {
      if (this.editForm.options.length > 2) {
        const removedOption = this.editForm.options[index]
        this.editForm.options.splice(index, 1)
        if (this.editForm.correctAnswer === removedOption.id) {
          this.editForm.correctAnswer = ''
        }
      }
    },
    saveQuestion() {
      try {
        const typeKey = this.isGraded ? 'graded_assignments' : 'practice_assignments'
        const updatedQuestion = {
          ...this.currentQuestionData,
          questionText: this.editForm.questionText,
          options: this.editForm.options,
          correctAnswer: this.editForm.correctAnswer,
        }
        if (this.assignmentData.questions) {
          this.assignmentData.questions[this.currentQuestion - 1] = updatedQuestion
        }
        const modal = bootstrap.Modal.getInstance(document.getElementById('editQuestionModal'))
        modal.hide()
        alert('Question updated successfully')
      } catch (error) {
        console.error('Error updating question:', error)
        alert('Error updating question')
      }
    },
    saveDeadline() {
      if (!this.editDeadlineForm.date || !this.editDeadlineForm.time) {
        alert('Please select both date and time.')
        return
      }
      this.assignmentData.dueDate = `${this.editDeadlineForm.date} ${this.editDeadlineForm.time}`
      const modal = bootstrap.Modal.getInstance(document.getElementById('editDeadlineModal'))
      modal.hide()
      alert('Deadline updated successfully')
    },
    increaseMarks() {
      this.marks += 1
      this.sendUpdatedMarksToBackend()
    },
    decreaseMarks() {
      if (this.marks > 1) {
        this.marks -= 1
        this.sendUpdatedMarksToBackend()
      }
    },
    sendUpdatedMarksToBackend() {
      console.log(`Marks for question ${this.currentQuestion} updated to ${this.marks}`)
      // Replace with an API call if needed
    },
    toggleBookmark() {
      this.bookmarked = !this.bookmarked
      alert(this.bookmarked ? 'Question bookmarked' : 'Bookmark removed')
    },
  },
}
</script>

<style scoped>
.content {
  flex: 1;
  overflow-y: auto;
  transition: margin-left 0.3s ease-in-out;
  margin-left: 250px;
}

.content-expanded {
  margin-left: 50px;
}

.content-inner {
  padding: 1rem;
}

/* Template 1 Styles */
.ai-page-header {
  background-color: #adb5bd;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
}
.ai-page-header h4 {
  margin: 0;
}
.ai-create-container {
  background-color: #d1d5db;
  border-radius: 8px;
  padding: 2rem;
  max-width: 500px;
  margin: 0 auto;
}
.ai-option-row {
  background-color: #adb5bd;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.number-spinner button {
  width: 2.5rem;
}

/* Template 2 Styles */

/* Additional style so the editor takes full available height */
.editor-inner {
  min-height: calc(100vh - 2rem);
}
.assignment-header {
  background-color: #adb5bd;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
  position: relative;
}
.question-buttons .btn {
  width: 2.5rem;
  text-align: center;
  margin-right: 0.5rem;
}
.progress {
  height: 5px;
  background-color: #dcdcdc;
}
.question-box {
  background-color: #ccc;
  border-radius: 4px;
  padding: 1rem;
  position: relative;
  margin-bottom: 1rem;
}
.stats-box {
  background-color: #e2e3e5;
  border-radius: 4px;
  padding: 1rem;
}

.bi-pencil {
  cursor: pointer;
}
.go-back-btn {
  /* position: fixed;
  bottom: 200px;
  right: 50px;
  z-index: 1000; */
  margin-top: 5px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .ai-create-container {
    padding: 1rem;
    max-width: 100%;
  }
  .content {
    margin-left: 0;
  }
}
</style>
