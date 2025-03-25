<template>
  <div>
    <Navbar />
    <div class="container my-2">
      <!-- Page header bar -->
      <div v-for="announcement in announcements" :key="announcement.event_id" class="mb-5">
        <h5 class="fw-bold">{{ new Date(announcement.date).toLocaleDateString() }}</h5>
        <h6 class="fw-bold">{{ announcement.title }}</h6>
        <p>{{ announcement.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/student/NavBar.vue';
export default {
  components: { Navbar },
  data() {
    return {
      announcements: [],
    };
  },
  mounted() {
    fetch('http://localhost:5000/api/events')
      .then((response) => response.json())
      .then((data) => {
        this.announcements = data;
      })
      .catch((error) => {
        console.error('Error fetching announcements:', error);
      });
  },
};
</script>

<style scoped>
/* Page header styling */
.page-header {
  background-color: #d1d5db;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}
</style>