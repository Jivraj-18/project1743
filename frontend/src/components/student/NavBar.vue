<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <!-- Navbar toggler for mobile -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarContent"
        aria-controls="navbarContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <!-- Collapsible content -->
      <div class="collapse navbar-collapse" id="navbarContent">
        <!-- Left-aligned navigation links -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link
              class="nav-link"
              :class="{ active: $route.path === '/student/announcements' }"
              to="/student/announcements"
            >
              Announcements
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              :class="{ active: $route.path === '/student/to_do' }"
              to="/student/to_do"
            >
              To-do
            </router-link>
          </li>
          <!-- My Courses: link navigates on click and shows dropdown on hover -->
          <li class="nav-item dropdown dropdown-hover">
            <router-link
              class="nav-link"
              :class="{ active: $route.path.startsWith('/student/course') }"
              to="/student/courses"
              id="myCoursesDropdown"
              role="button"
            >
              My Courses
              <i class="bi bi-chevron-down"></i>
            </router-link>
            <!-- Dropdown menu populated with courses -->
            <ul class="dropdown-menu" aria-labelledby="myCoursesDropdown">
              <li v-for="course in courses" :key="course.id">
                <router-link
                  class="dropdown-item"
                  :class="{ active: $route.path.startsWith('/student/course/' + course.id) }"
                  :to="'/student/course/' + course.id"
                  >{{ course.name }}</router-link
                >
              </li>

              
            </ul>
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              :class="{ active: $route.path === '/student/report-issues' }"
              to="/student/report-issues"
            >
              Report Issues
            </router-link>
          </li>
        </ul>
        
        <!-- Right-aligned links for larger screens: icons for Profile & Logout -->
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0 d-none d-lg-flex gap-3">
          <li class="nav-item">
            <router-link class="nav-link" to="/student/profile">
              <i class="fa-solid fa-circle-user fs-4"></i>
            </router-link>
          </li>
          <li class="nav-item">
            <!--run logout method when cliced on icon instead of redirecting to login page-->
            <a class="nav-link" href="#" @click.prevent="logout">
              <i class="fa-solid fa-right-from-bracket fs-4"></i>
            </a>
            <!-- <router-link class="nav-link" to="/login">
              <i class="fa-solid fa-right-from-bracket fs-4"></i>
            </router-link> -->
          </li>
        </ul>
        <!-- Right-aligned links for small screens: text links for Profile & Logout -->
        <ul class="navbar-nav d-lg-none">
          <li class="nav-item">
            <router-link class="nav-link" to="/student/profile">Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Logout</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavbarComponent',
  data() {
    return {
      courses: [],
    };
  },
  methods: {
    logout() {
      fetch('http://localhost:5000/api/logout', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      })
        .then((response) => {
          if (response.ok) {
            localStorage.removeItem('token');
            this.$router.push('/login');
          } else {
            console.error('Logout failed');
          }
        })
        .catch((error) => {
          console.error('Error during logout:', error);
        });
    },
    fetchCourses(studentId) {
  fetch(`http://localhost:5000/api/mycourses/${studentId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (Array.isArray(data)) {  // Ensure the response is an array
        this.courses = data.map(course => ({
          id: course.course_id, // Extract course_id
          name: course.course_name // Extract course_name
        }));
      } else {
        console.error('Unexpected API response format:', data);
        this.courses = [];
      }
    })
    .catch((error) => {
      console.error('Error fetching courses:', error);
    });
}
,
  },
  mounted() {
    const userData = JSON.parse(localStorage.getItem('userdata') || '{}');
    const studentId = userData.student_id;

    console.log('Student ID:', studentId);
    if (studentId) {
      this.fetchCourses(studentId);
    }
    
  },
};


</script>

<style scoped>
/* Show dropdown menu on hover */
.dropdown-hover:hover .dropdown-menu {
  display: block;
}
.dropdown-menu {
  margin-top: 0;
}

/* Optional: Style active links */
.nav-link.active {
  font-weight: bold;
  color: #0d6efd !important; /* Use Bootstrap primary color */
}
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1030;
  background-color: #ffffff;
}
</style>
