<template>
  <div :class="['content', { 'content-expanded': isSidebarCollapsed }]">
    <!-- Template 1: Options Selection -->
    <div v-if="step === 'options'" class="content-inner">
      <!-- Large Gray Bar -->
      <div class="ai-page-header">
        <h4 class="mb-0">Practice with AI</h4>
      </div>
      <!-- Options Container -->
      <div class="ai-create-container">
        <!-- Week Selection -->
        <div class="ai-option-row">
          <span>Week</span>
          <select v-model="selectedWeek" class="form-select form-select-sm w-auto">
            <option value="Week 1">Week 1</option>
            <option value="Week 2">Week 2</option>
          </select>
        </div>
        <!-- Number of Questions (– 10 +) -->
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
    <div v-else class="content-inner">
      <!-- HEADER AREA -->
      <div class="assignment-header">
        <h5 class="fw-bold">{{ assignmentType }}</h5>
        <p class="mb-1">
          <small>Due: {{ dueDate }}</small
          ><br />
        </p>
      </div>

      <!-- QUESTION NAVIGATION -->
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

      <!-- QUESTION BOX -->
      <div class="question-box">
        <div class="d-flex justify-content-between align-items-start mb-3">
          <p class="fw-bold mb-0">{{ currentQuestion }}. {{ currentQuestionText }}</p>

          <i
            :class="bookmarked ? 'fa-solid fa-bookmark' : 'fa-regular fa-bookmark'"
            @click="toggleBookmark"
            style="cursor: pointer"
          ></i>
        </div>

        <form>
          <div v-for="(option, index) in options" :key="option.id" class="form-check mb-2">
            <input
              class="form-check-input"
              type="radio"
              :name="'question' + currentQuestion"
              :id="option.id"
              v-model="selectedAnswers[currentQuestion]"
              :value="option.id"
            />
            <label class="form-check-label" :for="option.id">
              {{ option.text }}
            </label>
          </div>
        </form>

        <!-- Student Actions for Practice Assignments -->
        <div v-if="!isGraded" class="mt-4 practice-actions">
          <button
            class="btn btn-success me-2"
            @click="checkAnswer"
            :disabled="!selectedAnswers[currentQuestion]"
          >
            Check Answer
          </button>
          <button class="btn btn-info me-2" @click="getAIExplanation">AI Explanation</button>
          <button class="btn btn-warning" @click="getHint">Get Hint</button>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="question-navigation mt-3">
        <button
          class="btn btn-secondary me-2"
          @click="prevQuestion"
          :disabled="currentQuestion === 1"
        >
          Previous Question
        </button>
        <button
          class="btn btn-secondary me-2"
          @click="nextQuestion"
          :disabled="currentQuestion === numberOfQuestions"
        >
          Next Question
        </button>
        <!-- Global submit button shown only for graded assignments -->
        <button
          v-if="isGraded && !route.path.includes('/ta')"
          class="btn btn-primary"
          @click="submitAssignment"
        >
          Submit Assignment
        </button>
      </div>
      <!-- Go Back Button -->
      <button class="go-back-btn btn btn-outline-secondary" @click="goBack">← Go Back</button>
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

import {sb} from "../sb.js"

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
      // Step: 'options' for Options view, 'editor' for Editor view
      step: 'options',
      // Template 1 selections
      selectedWeek: 'Week 1',
      bookmarked: false,
      numberOfQuestions: 10,
      // Template 2 shared variables
      currentQuestion: 1,
      progress: 10,
      selectedAnswers: {},
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
    isGraded() {
      // Since assignment type is always Practice now
      return false
    },
    assignmentType() {
      return 'Practice Assignment'
    },
    courseId() {
      return this.route.params.id
    },
    weekId() {
      // Use the numeric week value from selectedWeek
      return this.selectedWeek === 'Week 1' ? 1 : 2
    },
    weekNumber() {
      return this.weekId
    },
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
      // Accessing questions from the generated data
      return this.assignmentData.questions
        ? this.assignmentData.questions.find(q => q.questionId === this.currentQuestion) || {}
        : {}
    },
    currentQuestionText() {
      return this.currentQuestionData.question || ''
    },
    options() {
      const options = this.currentQuestionData.options || {};
      return Object.entries(options).map(([key, value]) => ({
        id: key,
        text: value
      }));
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
    canCreate() {
      // Options are valid if week is chosen and at least one question is specified.
      return this.selectedWeek && this.numberOfQuestions >= 1
    },
    totalQuestions() {
      return this.numberOfQuestions
    },
  },
  watch: {
    // Reset question state when the week changes
    selectedWeek() {
      this.currentQuestion = 1
      this.progress = 10
      this.selectedAnswers = {}
    },
  },
  methods: {
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
    async createAssignment() {

      var ques = await sb.gen( {
          N : this.numberOfQuestions,
          week : this.selectedWeek
      } )
      alert(ques)

      this.assignmentData.questions = ques;

      this.step = 'editor'
    },
    goBack() {
      this.step = 'options'
    },
    changeQuestion(n) {
      if (n < 1 || n > this.totalQuestions) return
      this.currentQuestion = n
      this.progress = (n / this.totalQuestions) * 100
    },
    prevQuestion() {
      if (this.currentQuestion > 1) {
        this.currentQuestion--
        this.progress = (this.currentQuestion / this.totalQuestions) * 100
      }
    },
    nextQuestion() {
      if (this.currentQuestion < this.totalQuestions) {
        this.currentQuestion++
        this.progress = (this.currentQuestion / this.totalQuestions) * 100
      }
    },
    openChat() {
      // Implement chat opening as needed
    },
    submitAssignment() {
      console.log('Submitting assignment answers:', this.selectedAnswers)
      alert('Assignment submitted')
    },
    checkAnswer() {
      const correctAnswer = this.currentQuestionData.answer;
      const studentAnswer = this.selectedAnswers[this.currentQuestion];
      alert(studentAnswer === correctAnswer ? 'Correct!' : 'Incorrect');
    },
    getAIExplanation() {
      alert('AI explanation feature coming soon!')
    },
    getHint() {
      alert('Hint: ' + (this.currentQuestionData.hint || 'No hint available'))
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
  position: fixed;
  bottom: 200px;
  right: 50px;
  z-index: 1000;
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
