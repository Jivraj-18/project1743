<template>
  <div class="main-wrapper">
    <component :is="navbarComponent" />
    <div class="main-container">
      <Sidebar @sidebar-toggled="handleSidebarToggle" />
      <div class="content-area" :class="{ expanded: isSidebarCollapsed }">
        <router-view :isSidebarCollapsed="isSidebarCollapsed" />
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/student/NavBar.vue'
import Sidebar from '@/components/student/Sidebar.vue'
import TA_NavBar from '@/components/TA/NavBar.vue'

export default {
  components: {
    Navbar,
    Sidebar,
    TA_NavBar,
  },
  data() {
    return {
      isSidebarCollapsed: false, // Track sidebar state
    }
  },
  methods: {
    handleSidebarToggle(isCollapsed) {
      this.isSidebarCollapsed = isCollapsed
    },
  },
  computed: {
    navbarComponent() {
      return this.$route.path.includes('/ta') ? 'TA_NavBar' : 'Navbar'
    },
  },
}
</script>

<style scoped>
.main-container {
  display: flex;
  padding-top: 70px;
}

.content-area {
  flex-grow: 1;
  padding: 20px;
  transition: margin-left 0.3s ease-in-out;
}

.content-area.expanded {
  margin-left: 50px; /* Adjust when sidebar is collapsed */
}
</style>
