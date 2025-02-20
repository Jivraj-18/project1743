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
          <small v-if="isGraded">Last Submitted: {{ lastSubmitted }}</small>
        </p>
      </div>

      <!-- QUESTION NAVIGATION (Individual question buttons) -->
      <div class="question-buttons mb-2">
        <button
          v-for="n in totalQuestions"
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

      <!-- QUESTION BOX (original dimensions) -->
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

      <!-- Navigation Buttons and Global Submit for Graded Assignments -->
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
          :disabled="currentQuestion === totalQuestions"
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
      currentQuestion: 1,
      progress: 10,
      selectedAnswers: {},
      totalQuestions: 0,
      bookmarked: false,
    }
  },
  mounted() {
    console.log('Assignment Data:', this.assignmentData)
    console.log('Total Questions:', this.totalQuestions)
    console.log('Current Question Data:', this.currentQuestionData)
    console.log('Current Question Text:', this.currentQuestionText)
  },
  computed: {
    isGraded() {
      return this.route.path.includes('graded_assignments')
    },
    assignmentType() {
      return this.isGraded ? 'Graded Assignment' : 'Practice Assignment'
    },
    courseId() {
      return this.route.params.id
    },
    weekId() {
      return this.route.params.week_id
    },
    weekNumber() {
      return this.weekId
    },
    assignmentData() {
      const typeKey = this.isGraded ? 'graded_assignments' : 'practice_assignments'
      const data = assignments[this.courseId]?.[this.weekId]?.[typeKey] || {}

      console.log('Fetching Assignment Data:', data) // Debug log

      // Set totalQuestions based on the questions array inside assignmentData
      this.totalQuestions = data.questions ? data.questions.length : 0

      return data
    },
    currentQuestionData() {
      return this.assignmentData['questions'][this.currentQuestion - 1] || {}
    },
    dueDate() {
      return this.currentQuestionData.dueDate || 'No Deadline'
    },
    lastSubmitted() {
      return this.currentQuestionData.lastSubmitted || 'Not Applicable'
    },
    currentQuestionText() {
      return this.currentQuestionData.questionText || ''
    },
    options() {
      return this.currentQuestionData.options || []
    },
    stats() {
      return this.currentQuestionData.stats || {}
    },
    progressStyle() {
      return { width: `${this.progress}%` }
    },
  },
  methods: {
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

    submitAssignment() {
      console.log('Submitting entire assignment answers:', this.selectedAnswers)
      alert('assignment submitted')
      // Add API call here if needed.
    },
    checkAnswer() {
      const correctAnswer = this.currentQuestionData.correctAnswer
      const studentAnswer = this.selectedAnswers[this.currentQuestion]
      alert(studentAnswer === correctAnswer ? 'Correct!' : 'Incorrect')
    },
    getAIExplanation() {
      alert('AI explanation feature coming soon!')
    },
    getHint() {
      alert('Hint: ' + (this.currentQuestionData.hint || 'No hint available'))
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

/* QUESTION BOX (original dimensions) */
.question-box {
  background-color: #ccc;
  border-radius: 4px;
  padding: 1rem;
  position: relative;
  margin-bottom: 1rem;
}

.practice-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.question-navigation button {
  margin-right: 0.5rem;
}
</style>
