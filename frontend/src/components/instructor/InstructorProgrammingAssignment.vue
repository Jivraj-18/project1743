<template>
  <div
    v-if="assignment"
    class="assignment-page"
    :class="{ 'content-expanded': isSidebarCollapsed }"
  >
    <!-- HEADER -->
    <div class="assignment-header">
      <div class="header-left">
        <h5 class="fw-bold">{{ assignmentType }} - Week {{ weekNumber }}</h5>
        <p class="deadline-text">
          <small>Due: {{ dueDate }}</small
          ><br />
          <small>Last Submitted: {{ lastSubmitted }}</small>
        </p>
      </div>
      <div class="header-right">
        <button
          class="btn btn-sm btn-outline-dark position-absolute edit-deadline-btn"
          style="top: 1rem; right: 1rem"
          @click="openDeadlineModal"
          :disabled="!isGraded"
        >
          Edit Deadline
        </button>
      </div>
    </div>

    <!-- MAIN CONTENT: Two Columns -->
    <div class="row columns-container">
      <!-- LEFT COLUMN -->
      <div class="col-md-6 left-column">
        <div class="column-content">
          <ul class="nav nav-tabs" role="tablist">
            <li class="nav-item">
              <button
                class="nav-link active"
                data-bs-toggle="tab"
                data-bs-target="#question-pane"
                type="button"
                role="tab"
              >
                Question
              </button>
            </li>
            <li class="nav-item">
              <button
                class="nav-link"
                data-bs-toggle="tab"
                data-bs-target="#public-pane"
                type="button"
                role="tab"
              >
                Public Test
              </button>
            </li>
            <li class="nav-item">
              <button
                class="nav-link"
                data-bs-toggle="tab"
                data-bs-target="#private-pane"
                type="button"
                role="tab"
              >
                Private Test
              </button>
            </li>
          </ul>
          <div class="tab-content no-scroll">
            <!-- QUESTION TAB -->
            <div class="tab-pane fade show active question-pane" id="question-pane" role="tabpanel">
              <!-- Edit Question Icon at Top-Right of the tab content -->
              <span class="edit-icon" @click="openQuestionModal">
                <i class="bi bi-pencil"></i>
              </span>
              <p class="mt-2">{{ assignment.question_text }}</p>
            </div>
            <!-- PUBLIC TEST TAB -->
            <div class="tab-pane fade" id="public-pane" role="tabpanel">
              <table class="table table-bordered table-test-cases mt-2">
                <thead>
                  <tr>
                    <th>Input</th>
                    <th>Expected</th>
                    <th>Actual</th>
                    <th>Result</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(test, idx) in assignment.public_test_cases" :key="idx">
                    <td>{{ test.input }}</td>
                    <td>{{ test.expected_output }}</td>
                    <td>-</td>
                    <td><i class="bi-check-circle-fill"></i></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- PRIVATE TEST TAB -->
            <div class="tab-pane fade" id="private-pane" role="tabpanel">
              <table class="table table-bordered table-test-cases mt-2">
                <thead>
                  <tr>
                    <th>Input</th>
                    <th>Expected</th>
                    <th>Actual</th>
                    <th>Result</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(test, idx) in assignment.private_test_cases" :key="idx">
                    <td>{{ test.input }}</td>
                    <td>{{ test.expected_output }}</td>
                    <td>-</td>
                    <td><i class="bi-check-circle-fill"></i></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN -->
      <div class="col-md-6 right-column">
        <div class="column-content">
          <ul class="nav nav-tabs" role="tablist">
            <li class="nav-item">
              <button
                class="nav-link active"
                data-bs-toggle="tab"
                data-bs-target="#code-pane"
                type="button"
                role="tab"
              >
                Your Code
              </button>
            </li>
            <li class="nav-item">
              <button
                class="nav-link"
                data-bs-toggle="tab"
                data-bs-target="#ai-pane"
                type="button"
                role="tab"
              >
                AI Help
              </button>
            </li>
            <li class="nav-item">
              <button
                class="nav-link"
                data-bs-toggle="tab"
                data-bs-target="#solution-pane"
                type="button"
                role="tab"
              >
                Solution
              </button>
            </li>
          </ul>
          <div class="tab-content no-scroll">
            <!-- CODE TAB -->
            <div class="tab-pane fade show active" id="code-pane" role="tabpanel">
              <h5 class="mt-2">OneCompiler Embedded Editor</h5>
              <div id="onecompiler-embed">
                <iframe
                  src="https://onecompiler.com/embed/python?hideLanguageSelection=true&hideTitle=true&code=print('Hello World')"
                  width="100%"
                  height="400px"
                  frameborder="0"
                  style="border-radius: 4px"
                ></iframe>
              </div>
            </div>
            <!-- AI HELP TAB -->
            <div class="tab-pane fade" id="ai-pane" role="tabpanel">
              <p class="mt-2"><strong>AI Chat / Help Section</strong></p>
              <textarea class="form-control" rows="3" placeholder="Ask the AI..."></textarea>
              <button class="btn btn-secondary mt-1">Send</button>
            </div>
            <!-- SOLUTION TAB -->
            <div class="tab-pane fade solution-pane" id="solution-pane" role="tabpanel">
              <!-- Edit Solution Icon at Top-Right -->
              <span class="edit-icon" @click="openSolutionModal">
                <i class="bi bi-pencil"></i>
              </span>
              <p class="mt-2"><strong>Official Solution:</strong></p>
              <pre class="bg-light p-2 rounded">{{ assignment.solution }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODALS -->

    <!-- Question Edit Modal -->
    <div v-if="showQuestionModal" class="modal-overlay">
      <div class="modal-content">
        <h5>Edit Question and Test Cases</h5>
        <label>Question Text:</label>
        <textarea v-model="editedQuestionText" rows="3" class="form-control"></textarea>

        <h6 class="mt-3">Public Test Cases:</h6>
        <div v-for="(test, index) in editedPublicTestCases" :key="index" class="mb-2">
          <input v-model="test.input" placeholder="Input" class="form-control mb-1" />
          <input
            v-model="test.expected_output"
            placeholder="Expected Output"
            class="form-control"
          />
        </div>

        <h6 class="mt-3">Private Test Cases:</h6>
        <div v-for="(test, index) in editedPrivateTestCases" :key="index" class="mb-2">
          <input v-model="test.input" placeholder="Input" class="form-control mb-1" />
          <input
            v-model="test.expected_output"
            placeholder="Expected Output"
            class="form-control"
          />
        </div>

        <div class="modal-actions">
          <button class="btn btn-primary" @click="saveQuestionEdits">Save</button>
          <button class="btn btn-secondary" @click="closeQuestionModal">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Solution Edit Modal -->
    <div v-if="showSolutionModal" class="modal-overlay">
      <div class="modal-content">
        <h5>Edit Solution</h5>
        <textarea v-model="editedSolution" rows="6" class="form-control"></textarea>
        <div class="modal-actions">
          <button class="btn btn-primary" @click="saveSolutionEdits">Save</button>
          <button class="btn btn-secondary" @click="closeSolutionModal">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Deadline Edit Modal -->
    <div v-if="showDeadlineModal" class="modal-overlay">
      <div class="modal-content">
        <h5>Edit Deadline</h5>
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
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Save</button>
            <button class="btn btn-secondary" @click="closeDeadlineModal">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Fallback if assignment not found -->
  <div v-else class="p-3">
    <h5>Assignment not found!</h5>
    <p>Please check your URL or contact support.</p>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import assignmentsData from '@/assets/programmingassignment.json'

export default {
  name: 'InstructorProgrammingAssignment',
  props: {
    isSidebarCollapsed: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    const route = useRoute()
    const courseId = computed(() => route.params.id)
    const weekId = computed(() => route.params.week_id)
    const assignmentId = computed(() => route.params.programming_assignment_id)

    // Find assignment based on JSON data
    const assignment = computed(() => {
      if (courseId.value !== assignmentsData.id) return null
      const week = assignmentsData.weeks.find((w) => w.id === weekId.value)
      if (!week) return null
      if (route.path.includes('practice_programming')) {
        return week.pp_assignments.find((a) => a.ppa_id === assignmentId.value) || null
      } else if (route.path.includes('graded_programming')) {
        return week.grp_assignments.find((a) => a.grpa_id === assignmentId.value) || null
      }
      return null
    })

    // Determine assignment type and related properties
    const isGraded = computed(() => route.path.includes('graded_programming'))
    const assignmentType = computed(() =>
      isGraded.value ? 'Graded Programming Assignment' : 'Practice Programming Assignment',
    )
    const weekNumber = computed(() => weekId.value)
    const dueDate = computed(() => (assignment.value ? assignment.value.due_date : ''))
    const lastSubmitted = computed(() =>
      assignment.value ? assignment.value.last_submitted_date : '',
    )

    // Modal state for Question, Solution, and Deadline
    const showQuestionModal = ref(false)
    const showSolutionModal = ref(false)
    const showDeadlineModal = ref(false)

    // Local state for editing question
    const editedQuestionText = ref('')
    const editedPublicTestCases = ref([])
    const editedPrivateTestCases = ref([])

    const openQuestionModal = () => {
      if (assignment.value) {
        editedQuestionText.value = assignment.value.question_text
        editedPublicTestCases.value = assignment.value.public_test_cases.map((tc) => ({ ...tc }))
        editedPrivateTestCases.value = assignment.value.private_test_cases.map((tc) => ({ ...tc }))
      }
      showQuestionModal.value = true
    }
    const closeQuestionModal = () => {
      showQuestionModal.value = false
    }
    const saveQuestionEdits = () => {
      if (assignment.value) {
        assignment.value.question_text = editedQuestionText.value
        assignment.value.public_test_cases = editedPublicTestCases.value
        assignment.value.private_test_cases = editedPrivateTestCases.value
      }
      showQuestionModal.value = false
    }

    // Local state for editing solution
    const editedSolution = ref('')
    const openSolutionModal = () => {
      if (assignment.value) {
        editedSolution.value = assignment.value.solution
      }
      showSolutionModal.value = true
    }
    const closeSolutionModal = () => {
      showSolutionModal.value = false
    }
    const saveSolutionEdits = () => {
      if (assignment.value) {
        assignment.value.solution = editedSolution.value
      }
      showSolutionModal.value = false
    }

    // Local state for editing deadline
    const editDeadlineForm = ref({ date: '', time: '' })
    const openDeadlineModal = () => {
      if (assignment.value) {
        // Assume the due_date is in "YYYY-MM-DD HH:MM" format.
        const parts = assignment.value.due_date.split(' ')
        editDeadlineForm.value.date = parts[0] || ''
        editDeadlineForm.value.time = parts[1] || ''
      }
      showDeadlineModal.value = true
    }
    const closeDeadlineModal = () => {
      showDeadlineModal.value = false
    }
    const saveDeadline = () => {
      if (assignment.value) {
        assignment.value.due_date = `${editDeadlineForm.value.date} ${editDeadlineForm.value.time}`
      }
      showDeadlineModal.value = false
    }

    return {
      assignment,
      isGraded,
      assignmentType,
      weekNumber,
      dueDate,
      lastSubmitted,
      showQuestionModal,
      showSolutionModal,
      showDeadlineModal,
      editedQuestionText,
      editedPublicTestCases,
      editedPrivateTestCases,
      editedSolution,
      editDeadlineForm,
      openQuestionModal,
      closeQuestionModal,
      saveQuestionEdits,
      openSolutionModal,
      closeSolutionModal,
      saveSolutionEdits,
      openDeadlineModal,
      closeDeadlineModal,
      saveDeadline,
    }
  },
}
</script>

<style scoped>
/* MAIN CONTAINER */
.assignment-page {
  height: 600px; /* fixed height for the component */
  overflow: hidden;
  margin-left: 280px; /* width of expanded sidebar */
  width: calc(100% - 280px);
  transition:
    margin-left 0.3s ease-in-out,
    width 0.3s ease-in-out;
}
.assignment-page.content-expanded {
  margin-left: 60px;
  width: calc(100% - 60px);
}

/* HEADER */
.assignment-header {
  background-color: #adb5bd;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}
.header-left {
  display: flex;
  flex-direction: column;
}
.assignment-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: bold;
}
.deadline-text {
  margin: 0.25rem 0 0 0;
  font-size: 0.9rem;
  line-height: 1.2;
}

/* The Edit Deadline button is positioned absolutely via inline styles */

/* COLUMNS */
.columns-container {
  margin: 0;
}

/* Column content container */
.column-content {
  overflow: hidden;
}

/* Fixed height tab content with no scrolling */
.tab-content.no-scroll {
  height: 400px; /* adjust as needed */
  overflow: hidden !important;
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 0.5rem;
  font-size: 0.85rem;
  position: relative;
}

/* For positioning the edit icons within a tab pane */
.question-pane,
.solution-pane {
  position: relative;
}

/* Edit icon for question & solution: positioned at top-right of tab content */
.edit-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.2rem;
  color: #333;
  cursor: pointer;
  z-index: 10;
}

/* TABLES */
.table-test-cases td {
  vertical-align: middle;
  font-size: 0.8rem;
}

/* Embedded editor */
#onecompiler-embed {
  width: 100%;
  height: 400px;
  border: 1px solid #ccc;
  border-radius: 4px;
  overflow: hidden;
}

/* MODALS */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 2000;
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: #fff;
  padding: 1rem;
  border-radius: 4px;
  width: 90%;
  max-width: 600px;
}
.modal-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* Additional spacing for the Edit Deadline button if needed */
/* .edit-deadline-btn { */
/* Already positioned via inline style in template */
/* } */
</style>
