<template>
  <div>
    <component :is="navbarComponent" />

    <div class="dashboard-container">
      <div class="course-card" v-for="(course, index) in courses" :key="index">
        <div class="course-header">{{ course.header }}</div>
        <div class="course-content">
          <div class="course-item" v-for="(summary, idx) in course.summaries" :key="idx">
            {{ summary.label }}: <strong>{{ summary.value }}</strong>
          </div>
        </div>
        <div class="course-footer">
          <router-link
            :to="`${$route.path.includes('/ta') ? '/ta' : '/student'}/course/${course.id}`"
          >
            <i class="bi bi-chevron-right"></i>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/student/NavBar.vue'
import TA_NavBar from '@/components/TA/NavBar.vue'

export default {
  components: {
    NavBar,
    TA_NavBar,
  },
  data() {
    return {
      courses: [],
      studentId: this.$route.query.student_id,
    }
  },

  computed: {
    navbarComponent() {
      return this.$route.path.includes('/ta') ? 'TA_NavBar' : 'NavBar'
    },
  },
  methods: {
    async fetchCourses() {
      try {
        console.log(this.studentId)
        const response = await fetch(`http://localhost:5000/api/mycourses/${this.studentId}`)
        const data = await response.json()
        this.processCourseData(data)
      } catch (error) {
        console.error('Error fetching courses:', error)
      }
    },
    processCourseData(data) {
      this.courses = Object.keys(data).map((courseName, index) => ({
        id: index + 1, // Temporary ID, update based on actual course ID
        header: courseName,
        summaries: data[courseName].map((assignment, idx) => ({
          label: `Assignment ${assignment.assignment_id} Score`,
          value: `${assignment.percentage}%`,
        })),
      }))
    },
  },
  created() {
    this.fetchCourses()
  },
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1100px;
  margin: 2rem auto;
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
  padding-top: 70px;
}

.course-card {
  background-color: #e9ecef;
  border-radius: 8px;
  overflow: hidden;
  flex: 0 0 calc(50% - 0.75rem);
  padding-bottom: 1rem;
  box-sizing: border-box;
}

.course-header {
  background-color: #d6d8db;
  padding: 2rem;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.course-content {
  padding: 1rem 1.5rem;
}

.course-item {
  font-size: 1rem;
  padding: 0.5rem 0;
}

.course-footer {
  text-align: right;
  padding-right: 1.5rem;
}
</style>
