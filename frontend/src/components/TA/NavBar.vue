<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-3 fixed-top">
    <div class="container-fluid">
      <!-- Navbar Toggler Button -->
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

      <div class="collapse navbar-collapse" id="navbarContent">
        <!-- Left-side menu items -->
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link
              class="nav-link"
              :class="{ active: $route.path === '/ta/view_issues' }"
              to="/ta/view_issues"
              >Issues
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              :class="{ active: $route.path === '/ta/to_do' }"
              to="/ta/to_do"
              >To Do
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              :class="{ active: $route.path === '/ta/upload_resources' }"
              to="/ta/upload_resources"
              >Upload Resources
            </router-link>
          </li>
          <li class="nav-item dropdown dropdown-hover">
            <router-link
              class="nav-link"
              :class="{
                active:
                  $route.path.startsWith('/ta/courses') || $route.path.startsWith('/ta/course'),
              }"
              to="/ta/courses"
              id="coursesDropdown"
              role="button"
            >
              Courses
              <i class="bi bi-chevron-down"></i>
            </router-link>

            <ul class="dropdown-menu" aria-labelledby="coursesDropdown">
              <li>
                <router-link
                  class="dropdown-item"
                  :class="{ active: $route.path.startsWith('/ta/course/1') }"
                  to="/ta/course/1"
                  >Python</router-link
                >
              </li>
              <li>
                <router-link
                  class="dropdown-item"
                  :class="{ active: $route.path.startsWith('/ta/course/2') }"
                  to="/ta/course/2"
                  >Maths 1</router-link
                >
              </li>
            </ul>
          </li>
        </ul>

        <!-- Right-side menu items -->
        <ul class="navbar-nav ms-auto gap-3 d-none d-lg-flex">
          <li class="nav-item">
            <router-link class="nav-link" to="/ta/profile">
              <i class="fa-solid fa-circle-user fs-4"></i>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">
              <i class="fa-solid fa-right-from-bracket fs-4"></i>
            </router-link>
          </li>
        </ul>

        <!-- Responsive menu items -->
        <ul class="navbar-nav d-lg-none w-100">
          <li class="nav-item">
            <router-link class="nav-link" to="/ta/profile"> Profile </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login"> Logout </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavbarComponent',
}
</script>

<style scoped>
/* Custom hover effect */
.dropdown-hover:hover .dropdown-menu {
  display: block;
}

/* Ensure the dropdown remains clickable */
.dropdown-menu {
  margin-top: 0;
}

/* Fixed navbar styles */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1030;
  background-color: #ffffff;
}

/* Add padding to prevent content from being hidden under the navbar */
.main-wrapper {
  padding-top: 70px; /* Adjust this value based on navbar height */
}

.navbar-nav .nav-link {
  color: #000;
  font-weight: 500;
}

.navbar-nav .nav-link.active {
  color: #007bff;
  font-weight: bold;
}

.navbar-nav.gap-3 {
  gap: 1rem;
}
</style>
