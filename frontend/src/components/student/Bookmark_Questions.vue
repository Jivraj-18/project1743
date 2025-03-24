<template>
  <div :class="['content', { 'content-expanded': isSidebarCollapsed }]">
    <div class="content-inner">
      <!-- HEADER AREA -->
      <div class="assignment-header">
        <h5 class="fw-bold">Bookmarked Questions</h5>
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
          <div
            v-for="(option, index) in options"
            :key="option.id"
            class="form-check mb-2"
          >
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

        <!-- Display answer result below options -->
        <div v-if="answerResult" class="mt-2" :style="{ color: answerResultColor }">
          {{ answerResult }}
        </div>

        <!-- Student Actions -->
        <div class="mt-4 practice-actions">
          <button
            class="btn btn-success me-2"
            @click="checkAnswer"
            :disabled="!selectedAnswers[currentQuestion]"
          >
            Check Answer
          </button>
          <button class="btn btn-info me-2" @click="getAIExplanation">
            AI Explanation
          </button>
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
          :disabled="currentQuestion === totalQuestions"
        >
          Next Question
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute } from 'vue-router'

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
      bookmarked: false,
      // Array to store only bookmarked questions
      bookmarkedQuestions: [],
      // Property to hold the answer result text and correctness flag
      answerResult: '',
      answerIsCorrect: false,
    }
  },
  computed: {
    // Total questions is determined by the number of bookmarked questions fetched
    totalQuestions() {
      return this.bookmarkedQuestions.length
    },
    // Get the current question object from bookmarkedQuestions array
    currentQuestionData() {
      return this.bookmarkedQuestions[this.currentQuestion - 1] || {}
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
    // Compute color based on whether the answer is correct
    answerResultColor() {
      return this.answerIsCorrect ? 'green' : 'red'
    },
  },
  mounted() {
    // Call dummy function to fetch bookmarked questions from backend
    this.fetchBookmarkedQuestions()
  },
  methods: {
    fetchBookmarkedQuestions() {
      // Dummy function simulating backend fetch with 3 dummy bookmarked questions
      this.bookmarkedQuestions = [
        {
          id: 1,
          questionText: "What is the capital of France?",
          options: [
            { id: "a", text: "Paris" },
            { id: "b", text: "London" },
            { id: "c", text: "Berlin" },
          ],
          correctAnswer: "a",
          dueDate: "2025-04-01",
          lastSubmitted: "2025-03-30",
          stats: { attempted: 70, correct: 60, incorrect: 10 },
          hint: "It's known as the city of love.",
        },
        {
          id: 2,
          questionText: "Which planet is known as the Red Planet?",
          options: [
            { id: "a", text: "Earth" },
            { id: "b", text: "Mars" },
            { id: "c", text: "Jupiter" },
          ],
          correctAnswer: "b",
          dueDate: "2025-04-05",
          lastSubmitted: "2025-04-02",
          stats: { attempted: 80, correct: 75, incorrect: 5 },
          hint: "It's the fourth planet from the Sun.",
        },
        {
          id: 3,
          questionText: "Who wrote 'Hamlet'?",
          options: [
            { id: "a", text: "Charles Dickens" },
            { id: "b", text: "William Shakespeare" },
            { id: "c", text: "Mark Twain" },
          ],
          correctAnswer: "b",
          dueDate: "2025-04-10",
          lastSubmitted: "2025-04-08",
          stats: { attempted: 65, correct: 50, incorrect: 15 },
          hint: "He is widely regarded as the greatest writer in English.",
        },
      ]
      // Reset current question and progress based on the fetched data
      this.currentQuestion = 1
      this.progress = this.totalQuestions ? (1 / this.totalQuestions) * 100 : 0
      // Clear any previous answer result
      this.answerResult = ''
    },
    changeQuestion(n) {
      if (n < 1 || n > this.totalQuestions) return
      this.currentQuestion = n
      this.progress = (n / this.totalQuestions) * 100
      // Clear answer result when switching questions
      this.answerResult = ''
    },
    prevQuestion() {
      if (this.currentQuestion > 1) {
        this.currentQuestion--
        this.progress = (this.currentQuestion / this.totalQuestions) * 100
        this.answerResult = ''
      }
    },
    nextQuestion() {
      if (this.currentQuestion < this.totalQuestions) {
        this.currentQuestion++
        this.progress = (this.currentQuestion / this.totalQuestions) * 100
        this.answerResult = ''
      }
    },
    checkAnswer() {
      const correctAnswer = this.currentQuestionData.correctAnswer
      const studentAnswer = this.selectedAnswers[this.currentQuestion]
      const correctOption = this.options.find(
        (option) => option.id === correctAnswer
      )
      if (studentAnswer === correctAnswer) {
        this.answerResult = `Correct! \n The correct answer is: ${
          correctOption ? correctOption.text : correctAnswer
        }`
        this.answerIsCorrect = true
      } else {
        this.answerResult = `Incorrect. \n The correct answer is: ${
          correctOption ? correctOption.text : correctAnswer
        }`
        this.answerIsCorrect = false
      }
    },
    getAIExplanation() {
      alert("AI explanation feature coming soon!")
    },
    getHint() {
      alert("Hint: " + (this.currentQuestionData.hint || "No hint available"))
    },
    toggleBookmark() {
      this.bookmarked = !this.bookmarked
      alert(this.bookmarked ? "Question bookmarked" : "Bookmark removed")
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
.practice-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.question-navigation button {
  margin-right: 0.5rem;
}
</style>
