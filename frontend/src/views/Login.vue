<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Decorative Header -->
      <div class="login-header mb-4">
        <h3>Welcome Back</h3>
        <p>Please sign in to continue</p>
      </div>

      <!-- Email field -->
      <div class="mb-3">
        <input
          v-model="email"
          type="email"
          class="form-control"
          placeholder="Email"
          aria-label="Email"
        />
      </div>

      <!-- Password field with toggle -->
      <div class="input-group mb-3">
        <input
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          class="form-control"
          placeholder="Password"
          aria-label="Password"
          id="passwordInput"
        />
        <button class="btn btn-outline-secondary" type="button" @click="togglePassword">
          <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
        </button>
      </div>

      <!-- Error Message -->
      <p v-if="errorMessage" class="text-danger mb-3">{{ errorMessage }}</p>

      <!-- Sign In Button -->
      <button class="btn btn-dark w-100 mb-3" @click="login">Sign In</button>

      <!-- Divider -->
      <div class="divider"></div>

      <!-- Google Sign In Button -->
      <button class="btn btn-dark w-100 google-btn" @click="googleSignIn">
        <i class="bi bi-google me-2"></i> Sign in with Google
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const email = ref('')
    const password = ref('')
    const showPassword = ref(false)
    const errorMessage = ref('')
    const router = useRouter()

    // Dummy user data
    

    // Toggle password visibility
    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }

    // Login function using dummy data
    const login = () => {
      // use fetch to send a post request with email alone in the body, it should get a json response back with token as one key store in browsers local storage 
      // and redirect to the dashboard
      // use this url : http://localhost:5000/api/login
      fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email.value, password: password.value }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok')
          }
          return response.json()
        })
        .then((data) => {
          // load course from localhost:5000/api/mycourses/student_id, get student_id from data.student_id and store in localstorage allcourses  
          
          localStorage.setItem('userdata', JSON.stringify(data))
          localStorage.setItem('token', data.token)
          // in the response data there is a key roles which is an array of strings, get the first element and check if it's a student or ta or instructore based on that redirect to appropriate dashboard following urls 
          //'/ta/profile','/instructor/profile','/student/profile'
          const role = data.roles[0]
          if (role === 'student') {
            router.push('/student/profile')
          } else if (role === 'ta') {
            router.push('/ta/profile')
          } else if (role === 'instructor') {
            router.push('/instructor/updates')
          } else {
            errorMessage.value = 'Invalid role'
          }


          
        })
        .catch((error) => {
          errorMessage.value = 'Login failed. Please try again.'
          console.error('Error:', error)
        })
      
    }

    // Google sign in alert
    const googleSignIn = () => {
      alert('Not available now')
    }

    return {
      email,
      password,
      showPassword,
      errorMessage,
      togglePassword,
      login,
      googleSignIn,
    }
  },
}
</script>

<style scoped>
/* Background color from previous design */
.login-container {
  background-color: #eceff1;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

/* Increased card size with soft shadows and rounded corners */
.login-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 2rem;
  width: 400px; /* Increased width for a bigger card */
  text-align: center;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.5s ease-in-out;
}

/* Decorative header styling */
.login-header h3 {
  margin: 0;
  font-weight: 700;
  color: #2d3436;
}

.login-header p {
  margin: 0;
  font-size: 0.9rem;
  color: #636e72;
}

/* Divider styling */
.divider {
  margin: 1.5rem 0;
  border-bottom: 1px solid #b2bec3;
}

/* Hover effect for buttons */
.btn {
  transition:
    background-color 0.3s ease,
    transform 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
}

/* Google button additional styling */
.google-btn {
  background-color: #fff;
  color: #333;
  border: 1px solid #ccc;
}

.google-btn:hover {
  background-color: #f1f1f1;
}

/* Fade in animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
