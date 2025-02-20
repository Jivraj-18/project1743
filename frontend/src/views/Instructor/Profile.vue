<template>
  <div class="d-flex flex-column vh-100">
    <NavBar />
    <!-- Content -->
    <div id="mainContent" class="flex-grow-1 overflow-auto">
      <div class="container py-4">
        <!-- Page Header -->
        <div class="card mb-3">
          <div class="card-body">
            <h4 class="mb-0">Public Profile</h4>
          </div>
        </div>

        <!-- Student Profile Card -->
        <div class="card mb-4">
          <div class="card-body">
            <div class="row">
              <!-- Left Column: Dummy space for potential profile photo removal -->
              <div class="col-md-3 d-flex align-items-center justify-content-center">
                <!-- Removed image -->
                <i class="bi bi-person-circle display-1 text-secondary"></i>
              </div>
              <!-- Right Column: Student details -->
              <div class="col-md-9">
                <h5 class="fw-bold">
                  {{ student.name }}
                  <i class="bi bi-patch-check-fill text-primary"></i>
                </h5>
                <p class="mb-1"><strong>Program:</strong> {{ student.program }}</p>
                <p class="mb-1">
                  <strong>Level:</strong> {{ student.level }}
                  <i class="bi bi-patch-check-fill text-primary"></i>
                </p>
                <p class="mb-3">
                  <strong>Date of Birth:</strong> {{ student.dob }}
                  <i class="bi bi-patch-check-fill text-primary"></i>
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Badges Section -->
        <div class="mb-4">
          <h5 class="fw-bold">Badges <i class="bi bi-patch-check-fill text-primary"></i></h5>
          <div class="d-flex flex-wrap gap-3 mt-3">
            <div
              v-for="(badge, index) in student.badges"
              :key="index"
              class="badge-item bg-secondary text-white p-2 rounded text-center"
            >
              <span class="badge-title">{{ badge }}</span>
            </div>
          </div>
          <a href="#" class="text-secondary small d-block mt-2">click here to view more badges</a>
        </div>

        <!-- Contact Details -->
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="fw-bold">
              Contact Details <i class="bi bi-patch-check-fill text-primary"></i>
            </h5>
            <p class="mb-1"><strong>Phone number:</strong> {{ student.phone }}</p>
            <p class="mb-1"><strong>Email address:</strong> {{ student.email }}</p>
            <p class="mb-0"><strong>Address for Communication:</strong></p>
            <p class="ms-3 mb-0">
              {{ student.address }}
            </p>
          </div>
        </div>

        <!-- Education, Work, Projects -->
        <div class="row">
          <div class="col-md-4">
            <div class="card mb-3">
              <div class="card-header">Education</div>
              <div class="card-body">
                <p class="mb-0">{{ student.education }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card mb-3">
              <div class="card-header">Work</div>
              <div class="card-body">
                <p class="mb-0">{{ student.work }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card mb-3">
              <div class="card-header">Projects</div>
              <div class="card-body">
                <p class="mb-0">{{ student.projects }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/instructor/NavBar.vue'
export default {
  name: 'PublicProfile',
  data() {
    return {
      isSidebarCollapsed: false,
      weeks: [
        {
          name: 'Week-1',
          items: [
            'L1.1 - Lorem Ipsum',
            'L1.2 - Lorem Ipsum',
            'Graded Assignment',
            'Revise with AI',
          ],
        },
        {
          name: 'Week-2',
          items: [
            'L2.1 - Lorem Ipsum',
            'L2.2 - Lorem Ipsum',
            'Graded Assignment',
            'Revise with AI',
          ],
        },
        {
          name: 'Week-3',
          items: [
            'L3.1 - Lorem Ipsum',
            'L3.2 - Lorem Ipsum',
            'Graded Assignment',
            'Revise with AI',
          ],
        },
      ],
      student: {
        name: 'RAJAT GOEL',
        program: 'BS Degree in Data Science and Applications',
        level: 'DEGREE',
        dob: '29 July 1985',
        badges: ['TOPPER', 'Most Assessment Completed', 'All Assessment Completed', 'FINISHER'],
        phone: '+91 9876543210',
        email: 'random123@ds.study.iitm.ac.in',
        address: '221B Some Random Road, MyColony, MyCity, India - 567890',
        education: '[Add your education details here]',
        work: '[Add your work details here]',
        projects: '[Add your projects here]',
      },
    }
  },
  components: { NavBar },
  mounted() {
    this.fetchStudentData()
  },
  methods: {
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed
    },
    // This function will later fetch student data from the backend.
    // For now, it uses dummy data.
    fetchStudentData() {
      // dummy data already loaded in data()
      // Future: make an API call and update student object.
    },
  },
}
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
}
#mainContainer {
  flex: 1;
  display: flex;
  overflow: hidden;
}
#sidebar {
  width: 240px;
  transition: width 0.3s ease;
}
#sidebar.collapsed {
  width: 40px;
}
#mainContent {
  padding-top: 70px; /* Adjust based on NavBar height */
}
.sidebar-content {
  padding: 1rem;
}
.card {
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.badge-item {
  min-width: 100px;
  padding: 0.75rem;
}
</style>
