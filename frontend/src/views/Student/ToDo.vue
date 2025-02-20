<template>
  <div class="container mt-4">
    <NavBar />
    <div class="d-flex justify-content-between align-items-center mb-3">
      <button class="btn btn-primary" @click="showModal = true">Add Task</button>
    </div>

    <!-- Current Deadlines Section -->
    <div class="task-section">
      <h5>Current Deadlines (This Week)</h5>
      <div v-if="currentDeadlines.length">
        <div
          v-for="(task, index) in currentDeadlines"
          :key="index"
          class="task-item"
          :class="{ completed: task.completed }"
        >
          <input type="checkbox" v-model="task.completed" class="form-check-input" />
          <span class="task-name">{{ task.name }}</span>
          <span class="task-category">{{ task.category }}</span>
          <span class="task-date">{{ formatDate(task.dueDate) }}</span>
          <button class="btn btn-danger btn-sm" @click="deleteTask(task)">&times;</button>
        </div>
      </div>
      <p v-else>No current deadlines.</p>
    </div>

    <!-- Upcoming Deadlines Section -->
    <div class="task-section">
      <h5>Upcoming Deadlines (Next Week & Beyond)</h5>
      <div v-if="upcomingDeadlines.length">
        <div
          v-for="(task, index) in upcomingDeadlines"
          :key="index"
          class="task-item"
          :class="{ completed: task.completed }"
        >
          <input type="checkbox" v-model="task.completed" class="form-check-input" />
          <span class="task-name">{{ task.name }}</span>
          <span class="task-category">{{ task.category }}</span>
          <span class="task-date">{{ formatDate(task.dueDate) }}</span>
          <button class="btn btn-danger btn-sm" @click="deleteTask(task)">&times;</button>
        </div>
      </div>
      <p v-else>No upcoming deadlines.</p>
    </div>

    <!-- Add Task Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h5>Add Task</h5>
        <input
          type="text"
          v-model="newTask.name"
          placeholder="Task Name"
          class="form-control mb-2"
        />
        <input
          type="text"
          v-model="newTask.category"
          placeholder="Category"
          class="form-control mb-2"
        />
        <input type="date" v-model="newTask.dueDate" class="form-control mb-2" />
        <button class="btn btn-success me-2" @click="addTask">Add</button>
        <button class="btn btn-secondary" @click="showModal = false">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/student/NavBar.vue'
export default {
  data() {
    return {
      tasks: [],
      showModal: false,
      newTask: { name: '', category: '', dueDate: '', completed: false },
    }
  },
  components: { NavBar },
  computed: {
    currentDeadlines() {
      const today = new Date()
      const endOfWeek = new Date()
      endOfWeek.setDate(today.getDate() + (7 - today.getDay())) // End of current week
      return this.tasks.filter((task) => new Date(task.dueDate) <= endOfWeek)
    },
    upcomingDeadlines() {
      const today = new Date()
      const endOfWeek = new Date()
      endOfWeek.setDate(today.getDate() + (7 - today.getDay())) // End of current week
      return this.tasks.filter((task) => new Date(task.dueDate) > endOfWeek)
    },
  },
  methods: {
    fetchTasks() {
      // Dummy tasks
      this.tasks = [
        {
          name: 'Python Graded Assignment 1',
          category: 'DL',
          dueDate: '2025-02-21',
          completed: false,
        },
        { name: 'Project Milestone 1', category: 'SWT', dueDate: '2025-02-22', completed: false },
        { name: 'Java Coding Assignment', category: 'DL', dueDate: '2025-02-19', completed: false },
        {
          name: 'Research Paper Submission',
          category: 'SWT',
          dueDate: '2025-02-20',
          completed: false,
        },
        { name: 'Machine Learning Quiz', category: 'DL', dueDate: '2025-02-25', completed: false },
        { name: 'Web App Sprint Review', category: 'SWT', dueDate: '2025-02-26', completed: false },
        { name: 'Database Final Report', category: 'DL', dueDate: '2025-03-01', completed: false },
        {
          name: 'AI Capstone Presentation',
          category: 'SWT',
          dueDate: '2025-03-02',
          completed: false,
        },
      ]
    },
    addTask() {
      if (this.newTask.name && this.newTask.dueDate) {
        this.tasks.push({ ...this.newTask })
        this.tasks.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate)) // Sort by due date
        this.newTask = { name: '', category: '', dueDate: '', completed: false }
        this.showModal = false
      }
    },
    deleteTask(task) {
      this.tasks = this.tasks.filter((t) => t !== task)
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
  },
  mounted() {
    this.fetchTasks()
  },
}
</script>

<style scoped>
/* General Styles */
.task-section {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

/* Task List */
.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #ccc;
}

.task-item.completed span {
  text-decoration: line-through;
  color: #6c757d;
}

/* Task Name */
.task-name {
  flex: 2;
}

/* Task Category */
.task-category {
  flex: 1;
  text-align: center;
}

/* Task Due Date */
.task-date {
  flex: 1;
  text-align: center;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  width: 400px; /* Adjust width */
  padding: 15px; /* Reduce padding */
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.task-item input[type='checkbox'] {
  margin-right: 10px;
}

.container {
  margin-top: 70px; /* Adjust the value as needed */
}
.modal-dialog {
  margin: 1.75rem auto; /* default margin */
}
</style>
