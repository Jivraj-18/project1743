<template>
  <div class="min-vh-100 py-4">
    <NavBar />
    <div class="container-expanded">
      <div class="row">
        <!-- Issues Summary -->
        <div class="col-lg-6 mb-3">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-white">
              <h2 class="h5 mb-0">Issues Summary</h2>
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
                    <small class="text-muted">Submitted on: {{ issue.date }}</small>
                  </div>
                  <hr class="my-3 text-muted" />
                  <div class="d-flex justify-content-end">
                    <button class="btn btn-primary btn-md" @click="openModal(issue)">
                      Resolve
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Latest Updates & To-Do -->
        <div class="col-lg-6">
          <div class="card shadow-sm mb-3">
            <div class="card-header bg-white">
              <h2 class="h5 mb-0">Latest Updates</h2>
            </div>
            <div class="card-body">
              <ul>
                <li v-for="update in updates" :key="update.id">{{ update.text }}</li>
              </ul>
            </div>
          </div>

          <!-- To-Do List -->
          <div class="card shadow-sm">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h2 class="h5 mb-0">To-Do</h2>
              <button class="btn btn-outline-primary btn-sm" @click="openTaskModal">
                <i class="bi bi-plus-lg"></i>
              </button>
            </div>
            <div class="card-body">
              <div class="todo-container">
                <div
                  v-for="task in sortedTodoList"
                  :key="task.id"
                  class="d-flex justify-content-between align-items-center py-3 border-bottom"
                >
                  <span>
                    {{ task.task }}
                    <small class="text-muted"> (Due: {{ task.dueDate }})</small>
                  </span>
                  <div class="d-flex align-items-center">
                    <input type="checkbox" v-model="task.completed" class="me-2" />
                    <button class="btn btn-sm btn-danger" @click="deleteTask(task.id)">
                      &times;
                    </button>
                  </div>
                </div>
              </div>
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

      <!-- Add Task Modal -->
      <div class="modal fade" id="addTaskModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add New Task</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Task Description</label>
                <input type="text" v-model="newTaskText" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label">Due Date</label>
                <input type="date" v-model="newTaskDueDate" class="form-control" />
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-primary" @click="addTask">Add Task</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/instructor/NavBar.vue'
export default {
  data() {
    return {
      issues: [],
      updates: [
        { id: 1, text: 'New assignment uploaded for Data Science 101' },
        { id: 2, text: 'Live session on Machine Learning scheduled for Feb 25' },
      ],
      todoList: [
        { id: 1, task: 'Upload Week 4 Content', dueDate: '2025-02-25', completed: false },
        { id: 2, task: 'Review student submissions', dueDate: '2025-02-22', completed: false },
      ],
      selectedIssue: {},
      solutionText: '',
      newTaskText: '',
      newTaskDueDate: '',
    }
  },
  components: { NavBar },
  computed: {
    sortedTodoList() {
      return [...this.todoList].sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate))
    },
  },
  methods: {
    async fetchIssues() {
  try {
    const response = await fetch('http://localhost:5000/api/view_reports', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch issues');
    }
    
    const data = await response.json();
    this.issues = data.map(issue => ({
      id: issue.issue_id,
      studentName: issue.user_email,
      subject: issue.subject,
      courseId: issue.course_name,
      description: issue.description,
      date: new Date(issue.issue_date).toLocaleDateString(),
      issueType: issue.issue_type
    }));
  } catch (error) {
    console.error('Error fetching issues:', error);
    // Fallback to dummy data if API request fails
    this.issues = [
      {
        id: 1,
        studentName: 'John Doe',
        subject: 'Login not working',
        courseId: 'CS101',
        description: 'I cannot login to my account even after resetting my password.',
        date: '2025-02-19',
      },
      {
        id: 2,
        studentName: 'Jane Smith',
        subject: 'Video not loading',
        courseId: 'DS102',
        description: 'The video in module 3 keeps buffering and does not load.',
        date: '2025-02-18',
      },
    ];
  }
},
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
      this.issues = this.issues.filter((i) => i.id !== this.selectedIssue.id)
      alert('Issue resolved successfully!')
      bootstrap.Modal.getInstance(document.getElementById('resolveIssueModal')).hide()
    },
    openTaskModal() {
      new bootstrap.Modal(document.getElementById('addTaskModal')).show()
    },
    addTask() {
      if (!this.newTaskText || !this.newTaskDueDate) {
        alert('Please enter both task description and due date.')
        return
      }
      this.todoList.push({
        id: Date.now(),
        task: this.newTaskText,
        dueDate: this.newTaskDueDate,
        completed: false,
      })
      bootstrap.Modal.getInstance(document.getElementById('addTaskModal')).hide()
    },
    deleteTask(id) {
      this.todoList = this.todoList.filter((task) => task.id !== id)
    },
  },
  mounted() {
    this.fetchIssues()
  },
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 2rem auto;
  font-size: 1.2rem;
}
.todo-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.dashboard-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  max-width: 500px;
}
.container-expanded {
  max-width: 95vw; /* Slightly reduced width from 100% */
  margin: 0 auto; /* Centered */
  padding-left: 1rem;
  padding-right: 1rem;
  padding-top: 50px;
}
</style>
