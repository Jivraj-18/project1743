<template>
  <div :class="['content', { 'content-expanded': isSidebarCollapsed }]">
    <div class="content-inner">
      <!-- Show course description from localstroage courseData variable description fileld also name from course_name field-->
      <h1>{{ courseData.course_name }}</h1>
      <p>{{ courseData.description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    courseId() {
      return this.$route.params.id // Extracts course ID from the route
    },
  },
  data() {
    return {
      courseData: {}, // Initialize courseData to an empty object
    }
  },
  mounted() {
    // Fetch course data from local storage when the component is mounted
    const courseData = localStorage.getItem('courseData')
    if (courseData) {
      this.courseData = JSON.parse(courseData)
    }
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

.sidebar.collapsed + #content {
  margin-left: 50px;
}

.content-inner {
  padding: 1rem;
}
</style>
