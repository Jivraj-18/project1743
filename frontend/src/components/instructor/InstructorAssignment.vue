<template>
  <!-- MAIN CONTENT AREA -->
  <div :class="['content', { 'content-expanded': isSidebarCollapsed }]">
    <div class="content-inner">
      <!-- HEADER AREA -->
      <div class="assignment-header">
        <h5 class="fw-bold">{{ assignmentType }} - Week {{ weekNumber }}</h5>
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

      <!-- QUESTION NAVIGATION -->
      <div class="question-buttons mb-2">
        <button
          v-for="n in 10"
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

      <!-- QUESTION -->
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
        <!-- (Inline Mark Adjustment Control moved to the edit question modal) -->
      </div>

      <!-- STATS -->
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
            <p class="mb-1">
              Average no. of questions attempted –
              {{ stat.avgAttempted }}%
            </p>
            <p class="mb-1">Average no. of correct questions – {{ stat.avgCorrect }}%</p>
            <p class="mb-0">
              Average no. of incorrect questions –
              {{ stat.avgIncorrect }}%
            </p>
          </div>
        </div>
      </div>
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

              <!-- Inline Mark Adjustment Control moved here -->
              <div class="d-flex justify-content-end align-items-center mt-2">
                <button
                  class="btn btn-outline-secondary btn-sm me-2"
                  @click="decreaseMarks"
                  :disabled="marks <= 1"
                  type="button"
                >
                  -
                </button>
                <span class="me-2">{{ marks }} Mark</span>
                <button class="btn btn-outline-secondary btn-sm" @click="increaseMarks" type="button">
                  +
                </button>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="saveQuestion">
              Save changes
            </button>
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
            <button type="button" class="btn btn-primary" @click="saveDeadline">Save Changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router'
// Import the assignments JSON file
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
      currentQuestion: 1,
      progress: 10,
      bookmarked: false,
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
      modal: null,
    }
  },
  computed: {
    // Determine whether this is a graded assignment based on the route
    isGraded() {
      return this.route.path.includes('graded_assignments')
    },
    assignmentType() {
      return this.isGraded ? 'Graded Assignment' : 'Practice Assignment'
    },
    // Extract course and week ids from the route params
    courseId() {
      return this.route.params.id
    },
    weekId() {
      return this.route.params.week_id
    },
    weekNumber() {
      return this.weekId
    },
    // Get the array of questions for the current assignment from the JSON file
    assignmentData() {
      const typeKey = this.isGraded ? 'graded_assignments' : 'practice_assignments'
      return (
        (assignments[this.courseId] &&
          assignments[this.courseId][this.weekId] &&
          assignments[this.courseId][this.weekId][typeKey]) ||
        []
      )
    },
    // Get the current question object (array is 0-indexed)
    currentQuestionData() {
      console.log(this.assignmentData)
      return this.assignmentData['questions'][this.currentQuestion - 1] || {}
    },
    dueDate() {
      return this.assignmentData.dueDate || ''
    },
    lastSubmitted() {
      return this.assignmentData.lastSubmitted || ''
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
  },
  watch: {
    // Reset question state when assignment type changes
    isGraded() {
      this.currentQuestion = 1
      this.progress = 10
      this.selectedAnswer = null
    },
  },
  methods: {
    changeQuestion(n) {
      this.currentQuestion = n
      this.progress = (n / 10) * 100
      this.selectedAnswer = null
    },
    editDeadline() {
      // Pre-fill the modal with the current deadline
      this.editDeadlineForm.date = this.dueDate ? this.dueDate.split(' ')[0] : ''
      this.editDeadlineForm.time = this.dueDate ? this.dueDate.split(' ')[1] : ''

      // Open the modal
      const modal = new bootstrap.Modal(document.getElementById('editDeadlineModal'))
      modal.show()
    },
    editQuestion() {
      // Initialize form with current question data
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

        // Create updated question object including the updated marks value
        const updatedQuestion = {
          ...this.currentQuestionData,
          questionText: this.editForm.questionText,
          options: this.editForm.options,
          correctAnswer: this.editForm.correctAnswer,
          marks: this.marks, // Save the updated marks
        }

        // Update local assignments data
        this.assignmentData[this.currentQuestion - 1] = updatedQuestion

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('editQuestionModal'))
        modal.hide()

        // Show success message only after the modal is saved
        alert('Question updated successfully')
      } catch (error) {
        console.error('Error updating question:', error)
        alert('Error updating question')
      }
    },
    saveDeadline() {
      // Ensure both date and time are selected
      if (!this.editDeadlineForm.date || !this.editDeadlineForm.time) {
        alert('Please select both date and time.')
        return
      }

      // Format the new deadline
      this.dueDate = `${this.editDeadlineForm.date} ${this.editDeadlineForm.time}`

      // Close the modal
      const modal = bootstrap.Modal.getInstance(document.getElementById('editDeadlineModal'))
      modal.hide()

      // Show success message
      alert('Deadline updated successfully')
    },
    increaseMarks() {
      // Only update local marks state; do not save or alert yet
      this.marks += 1
    },
    decreaseMarks() {
      if (this.marks > 1) {
        this.marks -= 1
      }
    },
    toggleBookmark() {
      this.bookmarked = !this.bookmarked
      alert(this.bookmarked ? 'Question bookmarked' : 'Bookmark removed')
    },
  },
}
</script>

<style scoped>
/* MAIN CONTENT AREA */
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

/* Assignment Header */
.assignment-header {
  background-color: #adb5bd;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
  position: relative;
}

/* Question Buttons */
.question-buttons .btn {
  width: 2.5rem;
  text-align: center;
  margin-right: 0.5rem;
}

/* Progress Bar */
.progress {
  height: 5px;
  background-color: #dcdcdc;
}

/* Question Box */
.question-box {
  background-color: #ccc;
  border-radius: 4px;
  padding: 1rem;
  position: relative;
  margin-bottom: 1rem;
}

/* Stats Boxes */
.stats-box {
  background-color: #e2e3e5;
  border-radius: 4px;
  padding: 1rem;
}

.bi-pencil {
  cursor: pointer;
}
</style>
