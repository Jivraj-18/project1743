<template>
  <div id="app">
    <!-- Render Kai only if not on the login page -->
    <Kai v-if="!isLoginPage" />
    <router-view />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Kai from '@/components/Kai.vue'

export default {
  name: 'App',
  components: {
    Kai,
  },
  setup() {
    const route = useRoute()
    // Change this logic if you use a different path or route name for login
    const isLoginPage = computed(() => route.path === '/login')
    return { isLoginPage }
  },
}
</script>
