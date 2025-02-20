<!-- ReportIssues.vue -->
<template>
  <div>
    <NavBar />
    <!-- Main Content Area -->
    <div class="min-vh-100 py-4">
      <div class="container">
        <!-- Issue Reporting Form -->
        <div class="mb-4">
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h2 class="h5 mb-0">Submit New Issue</h2>
            </div>
            <div class="card-body">
              <!-- Issue Type Selection -->
              <div class="row g-3 mb-4">
                <div class="col-6">
                  <div
                    :class="[
                      'card h-100 cursor-pointer',
                      {
                        'border-primary bg-light': selectedIssue === 'technical',
                        'border-gray': selectedIssue !== 'technical',
                      },
                    ]"
                    @click="selectIssue('technical')"
                  >
                    <div class="card-body d-flex align-items-center">
                      <i class="bi bi-exclamation-circle text-primary me-2"></i>
                      <span class="fw-medium">Technical Issue</span>
                    </div>
                  </div>
                </div>
                <div class="col-6">
                  <div
                    :class="[
                      'card h-100 cursor-pointer',
                      {
                        'border-primary bg-light': selectedIssue === 'content',
                        'border-gray': selectedIssue !== 'content',
                      },
                    ]"
                    @click="selectIssue('content')"
                  >
                    <div class="card-body d-flex align-items-center">
                      <i class="bi bi-exclamation-circle text-primary me-2"></i>
                      <span class="fw-medium">Content Issue</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Form -->
              <form @submit.prevent="handleSubmit">
                <div class="mb-3">
                  <label for="subject" class="form-label">Subject</label>
                  <input
                    type="text"
                    class="form-control"
                    id="subject"
                    v-model="form.subject"
                    required
                  />
                </div>

                <div v-if="selectedIssue === 'content'" class="mb-3">
                  <label for="course" class="form-label">Course</label>
                  <select class="form-select" id="course" v-model="form.course" required>
                    <option value="" disabled>Select a course</option>
                    <option v-for="course in courses" :key="course.id" :value="course.name">
                      {{ course.name }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <label for="description" class="form-label">Description</label>
                  <textarea
                    class="form-control"
                    id="description"
                    rows="6"
                    v-model="form.description"
                    required
                  ></textarea>
                </div>

                <button type="submit" class="btn btn-primary w-100" :disabled="!selectedIssue">
                  Submit
                </button>
              </form>
            </div>
          </div>
        </div>

        <!-- Submitted Issues List -->
        <div>
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h2 class="h5 mb-0">Previously Submitted Issues</h2>
            </div>
            <div class="card-body">
              <div class="accordion" id="issuesAccordion">
                <div v-for="issue in submittedIssues" :key="issue.id" class="accordion-item">
                  <div class="accordion-header">
                    <button
                      class="accordion-button d-flex justify-content-between py-3"
                      :class="{ collapsed: !expandedIssues.includes(issue.id) }"
                      @click="toggleIssue(issue.id)"
                      type="button"
                    >
                      <div class="d-flex align-items-center flex-grow-1">
                        <i
                          :class="[
                            'bi me-2',
                            issue.status === 'Resolved'
                              ? 'bi-check-circle-fill text-success'
                              : 'bi-clock-fill text-warning',
                          ]"
                        ></i>
                        <span class="fw-medium me-2">{{ issue.subject }}</span>
                        <span
                          :class="[
                            'badge rounded-pill ms-2',
                            issue.status === 'Resolved' ? 'bg-success' : 'bg-warning text-dark',
                          ]"
                        >
                          {{ issue.status }}
                        </span>
                      </div>
                      <small class="text-muted ms-3">{{ issue.date }}</small>
                    </button>
                  </div>
                  <div
                    v-show="expandedIssues.includes(issue.id)"
                    class="accordion-collapse collapse show"
                  >
                    <div class="accordion-body">
                      <p class="mb-3">{{ issue.description }}</p>
                      <div
                        v-if="issue.status === 'Resolved' && issue.solution"
                        class="alert alert-success mb-0"
                      >
                        <div class="d-flex align-items-center mb-2">
                          <i class="bi bi-check-circle-fill me-2"></i>
                          <span class="fw-medium">Solution</span>
                        </div>
                        <p class="mb-0">{{ issue.solution }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="submittedIssues.length === 0" class="text-muted">
                No issues submitted yet.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/student/NavBar.vue'
export default {
  components: { NavBar },
  data() {
    return {
      selectedIssue: null,
      courses: [
        { id: 1, name: 'Course 1' },
        { id: 2, name: 'Course 2' },
        { id: 3, name: 'Course 3' },
      ],
      submittedIssues: [
        {
          id: 1,
          subject: 'Login not working',
          status: 'Submitted',
          description:
            'I cannot login to my account. I tried resetting my password but still no luck.',
          date: '2025-01-15',
        },
        {
          id: 2,
          subject: 'Module 2 Content Error',
          status: 'Resolved',
          description:
            'The video in module 2 does not load. I noticed it fails after buffering for a while.',
          solution:
            "The video CDN was experiencing temporary issues. We've moved the content to a backup server and implemented automatic failover to prevent future incidents.",
          date: '2025-01-20',
        },
      ],
      expandedIssues: [],
      form: {
        subject: '',
        course: '',
        description: '',
      },
    }
  },
  methods: {
    selectIssue(issueType) {
      this.selectedIssue = issueType
      if (issueType !== 'content') {
        this.form.course = ''
      }
    },
    toggleIssue(issueId) {
      if (this.expandedIssues.includes(issueId)) {
        this.expandedIssues = this.expandedIssues.filter((id) => id !== issueId)
      } else {
        this.expandedIssues.push(issueId)
      }
    },
    handleSubmit() {
      if (!this.selectedIssue) {
        alert('Please select an issue type before submitting the form.')
        return
      }
      const newIssue = {
        id: this.submittedIssues.length + 1,
        subject: this.form.subject,
        status: 'Submitted',
        description: this.form.description,
        date: new Date().toISOString().split('T')[0],
      }
      this.submittedIssues.unshift(newIssue)
      this.form.subject = ''
      this.form.course = ''
      this.form.description = ''
      this.selectedIssue = null
      alert('Issue submitted!')
    },
  },
}
</script>

<style>
.cursor-pointer {
  cursor: pointer;
}

/* Custom card hover effect */
.card.cursor-pointer:hover {
  border-color: var(--bs-primary);
  background-color: var(--bs-light);
}

/* Remove default focus outline from accordion buttons */
.accordion-button:focus {
  box-shadow: none;
}

/* Custom accordion styling */
.accordion-button::after {
  margin-left: 0.5rem;
}

/* Spacing for accordion header in collapsed state */
.accordion-button.collapsed {
  border-bottom: 1px solid var(--bs-border-color);
}
.container {
  padding-top: 70px;
}
</style>
