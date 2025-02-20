<template>
  <div class="min-vh-100 py-4">
    <NavBar />
    <div class="container-expanded">
      <div class="row">
        <div class="col-12 mb-3">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-white">
              <h2 class="h5 mb-0">Issues Submitted</h2>
            </div>
            <div class="card-body">
              <div v-if="issues.length === 0" class="text-muted">No issues reported.</div>
              <ul class="list-group">
                <li v-for="issue in issues" :key="issue.id" class="list-group-item p-4">
                  <div>
                    <h5 class="mb-1">{{ issue.subject }}</h5>
                    <p class="mb-1 text-muted"><strong>Student:</strong> {{ issue.studentName }}</p>
                    <p class="mb-1"><strong>Course ID:</strong> {{ issue.courseId }}</p>
                    <p class="mb-1"><strong>Description:</strong> {{ issue.description }}</p>
                    <small class="text-muted"> Submitted on: {{ issue.date }} </small>
                  </div>
                  <hr class="my-3 text-muted" />
                  <div class="d-flex justify-content-end">
                    <button
                      class="btn btn-primary btn-md me-2"
                      @click="openModal(issue)"
                      :disabled="issue.instructorNotified"
                    >
                      {{ issue.instructorNotified ? 'Sent to Instructor' : 'Resolve' }}
                    </button>
                    <button
                      class="btn btn-secondary btn-md"
                      @click="askInstructor(issue)"
                      :disabled="issue.instructorNotified"
                    >
                      {{ issue.instructorNotified ? 'Sent to Instructor' : 'Ask Instructor' }}
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Issue Resolution Modal -->
      <div class="modal fade" id="resolveIssueModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Resolve Issue</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <p><strong>Student:</strong> {{ selectedIssue.studentName }}</p>
              <p><strong>Subject:</strong> {{ selectedIssue.subject }}</p>
              <p><strong>Course ID:</strong> {{ selectedIssue.courseId }}</p>
              <p><strong>Description:</strong> {{ selectedIssue.description }}</p>
              <div class="mb-3">
                <label class="form-label">Provide Solution</label>
                <textarea v-model="solutionText" class="form-control" rows="4"></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-success btn-lg" @click="resolveIssue">Done</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Optional: Add Task Modal can go here if needed -->
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/TA/NavBar.vue'
export default {
  name: 'IssuesSummary',
  data() {
    return {
      issues: [
        {
          id: 1,
          studentName: 'John Doe',
          subject: 'Login not working',
          courseId: 'CS101',
          description: 'I cannot login to my account even after resetting my password.',
          date: '2025-02-19',
          instructorNotified: false,
        },
        {
          id: 2,
          studentName: 'Jane Smith',
          subject: 'Video not loading',
          courseId: 'DS102',
          description: 'The video in module 3 keeps buffering and does not load.',
          date: '2025-02-18',
          instructorNotified: false,
        },
      ],
      selectedIssue: {},
      solutionText: '',
    }
  },
  components: { NavBar },
  methods: {
    openModal(issue) {
      this.selectedIssue = { ...issue }
      this.solutionText = ''
      new bootstrap.Modal(document.getElementById('resolveIssueModal')).show()
    },
    resolveIssue() {
      if (!this.solutionText.trim()) {
        alert('Please provide a solution before marking as resolved.')
        return
      }
      // Remove the resolved issue from the list
      this.issues = this.issues.filter((i) => i.id !== this.selectedIssue.id)
      alert('Issue resolved successfully!')
      bootstrap.Modal.getInstance(document.getElementById('resolveIssueModal')).hide()
    },
    askInstructor(issue) {
      alert('Sent to Instructor')
      issue.instructorNotified = true
    },
  },
}
</script>

<style scoped>
.container-expanded {
  max-width: 95vw;
  margin: 0 auto;
  padding: 0 1rem;
  padding-top: 50px;
}
.card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1rem;
}
.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  padding: 1rem;
}
.list-group-item {
  border: none;
  background: transparent;
}
.btn {
  min-width: 150px;
}
</style>
