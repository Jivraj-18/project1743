<template>
  <div>
    <Create_with_AI />
    <main class="container mt-4">
      <Kai />
      <!-- <ConceptsSummary />
      <Lecture /> -->
      <!-- <h1>Welcome to the Home Page</h1>
      <p>This is the main content of the home page.</p> -->
    </main>
  </div>
</template>

<script>
import ConceptsSummary from '@/components/ConceptsSummary.vue'
import Lecture from '@/components/Lecture.vue'
import ProgrammingAssignment from '@/components/student/StudentProgrammingAssignment.vue'
import Kai from '@/components/Kai.vue'
// import Lecture from '@/components/Lecture.vue'

export default {
  components: {
    ConceptsSummary,
    Lecture,
    ProgrammingAssignment,
    Kai,
  },
}
</script>

<style scoped>
/* main {
  text-align: center;
} */
</style>
