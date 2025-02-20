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
          <!-- Router link to instructor/course/id -->
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
      courses: this.getDummyData(),
    }
  },
  methods: {
    // This method returns dummy summary data for the courses.
    getDummyData() {
      return [
        {
          id: 1,
          header: 'Python',
          summaries: [
            { label: 'Week 1 Assignment Score', value: '85%' },
            { label: 'Week 2 Assignment Score', value: '82%' },
            { label: 'Week 3 Assignment Score', value: '95%' },
            { label: 'Quiz 1 Score', value: '90%' },
          ],
        },
        {
          id: 2,
          header: 'Maths-1',
          summaries: [
            { label: 'Week 1 Assignment Score', value: '75%' },
            { label: 'Week 2 Assignment Score', value: '85%' },
            { label: 'Week 3 Assignment Score', value: '91%' },
            { label: 'Quiz 1 Score', value: '80%' },
          ],
        },
      ]
    },
  },
  computed: {
    navbarComponent() {
      return this.$route.path.includes('/ta') ? 'TA_NavBar' : 'NavBar'
    },
  },
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1100px;
  margin: 2rem auto;
  display: flex;
  gap: 1.5rem;
  justify-content: center; /* Center cards horizontally */
  flex-wrap: nowrap; /* Prevent cards from wrapping to the next line */
  padding-top: 70px;
}

.course-card {
  background-color: #e9ecef;
  border-radius: 8px;
  overflow: hidden;
  flex: 0 0 calc(50% - 0.75rem); /* Two cards side by side */
  padding-bottom: 1rem;
  box-sizing: border-box; /* Include padding in the width */
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
