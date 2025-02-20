<template>
  <div class="main-wrapper">
    <Navbar />
    <Kai />
    <div class="main-container">
      <Sidebar @sidebar-toggled="handleSidebarToggle" />
      <div class="content-area" :class="{ expanded: isSidebarCollapsed }">
        <router-view :isSidebarCollapsed="isSidebarCollapsed" />
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/instructor/NavBar.vue'
import Sidebar from '@/components/instructor/Sidebar.vue'
import Kai from '@/components/Kai.vue'

export default {
  components: {
    Navbar,
    Sidebar,
    Kai,
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
