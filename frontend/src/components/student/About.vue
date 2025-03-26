<template>
  <div :class="['content', { 'content-expanded': isSidebarCollapsed }]">
    <div class="content-inner">
      <h1 v-if="courseId === '2'">Welcome to Python Course</h1>
      <h1 v-else-if="courseId === '1'">Welcome to Math-1 Course</h1>
      <h1 v-else>Welcome to the Course</h1>

      <p v-if="courseId === '1'">
        This Python course covers fundamental to advanced programming concepts, including data
        structures, OOP, and frameworks.
      </p>
      <p v-else-if="courseId === '2'">
        This Math-1 course focuses on calculus, linear algebra, and foundational mathematical
        principles essential for further studies.
      </p>
      <p v-else>This is the main content of the about page.</p>
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
