<template>
  <!-- Renders only if we have an assignment -->
  <div
    v-if="assignment"
    class="assignment-page"
    :class="{ 'content-expanded': isSidebarCollapsed }"
  >
    <!-- A header that will not scroll within this component -->
    <div class="assignment-header">
      <h4>{{ assignment.title }}</h4>
      <p>
        <small>Due: {{ assignment.due_date }}</small
        ><br />
        <small>Last Submitted: {{ assignment.last_submitted_date }}</small>
      </p>
    </div>

    <!-- Main content area: row with two columns -->
    <div class="row columns-container">
      <!-- Left Column -->
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

          <!-- Tab content (clipped if too large, no scrolling) -->
          <div class="tab-content no-scroll">
            <!-- Question Tab -->
            <div class="tab-pane fade show active" id="question-pane" role="tabpanel">
              <p class="mt-2">{{ assignment.question_text }}</p>
            </div>
            <!-- Public Test Tab -->
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
                    <td><i class="bi-question-circle-fill"></i></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Private Test Tab -->
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
                    <td><i class="bi-question-circle-fill"></i></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column -->
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

          <!-- Tab content (clipped if too large, no scrolling) -->
          <div class="tab-content no-scroll">
            <!-- Code Tab -->
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
            <!-- AI Help Tab -->
            <div class="tab-pane fade" id="ai-pane" role="tabpanel">
              <p class="mt-2"><strong>AI Chat / Help Section</strong></p>
              <textarea class="form-control" rows="3" placeholder="Ask the AI..."></textarea>
              <button class="btn btn-secondary mt-1">Send</button>
            </div>
            <!-- Solution Tab -->
            <div class="tab-pane fade" id="solution-pane" role="tabpanel">
              <p class="mt-2"><strong>Official Solution:</strong></p>
              <pre class="bg-light p-2 rounded">{{ assignment.solution }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Fallback if assignment is not found -->
  <div v-else class="p-3">
    <h5>Assignment not found!</h5>
    <p>Please check your URL or contact support.</p>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import assignmentsData from '@/assets/programmingassignment.json'

export default {
  name: 'StudentProgrammingAssignment',
  props: {
    // If you have a collapsible sidebar
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

    // Example logic to find the correct assignment
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

    return {
      assignment,
      courseId,
      weekId,
      assignmentId,
    }
  },
}
</script>

<style scoped>
/* 
  1) The component is given a fixed height (e.g., 600px).
  2) Overflow is hidden so it won't scroll.
  3) The rest of the page can still scroll if there's more content outside this component.
*/
html,
body {
  margin: 0;
  height: 100%;
  overflow: hidden;
}
.assignment-page {
  height: 600px; /* or any fixed height you want for this component */
  overflow: hidden; /* no scrolling within the component */
  margin-left: 280px; /* expanded sidebar width, if you have a sidebar */
  width: calc(100% - 280px);
  transition:
    margin-left 0.3s ease-in-out,
    width 0.3s ease-in-out;
}

.assignment-page.content-expanded {
  margin-left: 60px;
  width: calc(100% - 60px);
}

/* Header styling */
.assignment-header {
  background-color: #d1d5db;
  padding: 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

/* Just basic row/column styling if using Bootstrap classes */
.columns-container {
  margin: 0;
}

/* We add a class "no-scroll" to the tab-content to ensure no overflow */
.tab-content.no-scroll {
  height: 400px; /* or another fixed height inside the component */
  overflow: hidden !important; /* no scrolling in the tab content */
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 0.5rem;
  font-size: 0.85rem;
}

/* Table styling */
.table-test-cases td {
  vertical-align: middle;
  font-size: 0.8rem;
}

/* Example for the embedded editor container */
#onecompiler-embed {
  width: 100%;
  height: 400px;
  border: 1px solid #ccc;
  border-radius: 4px;
  overflow: hidden;
}
</style>
