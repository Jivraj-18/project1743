<template>
  <div id="sidebar" :class="{ collapsed: isCollapsed }">
    <!-- Toggle Button (outside scrollable area) -->
    <button
      @click="toggleSidebar"
      class="toggle-btn btn btn-sm btn-outline-secondary"
      title="Toggle sidebar"
    >
      <i :class="toggleIcon"></i>
    </button>

    <!-- Fixed Heading (outside scrollable area) -->
    <div class="sidebar-header" v-show="!isCollapsed">
      <h5 class="text-center">{{ courseData.title }}</h5>
    </div>

    <!-- Scrollable Wrapper -->
    <div class="sidebar-wrapper">
      <!-- The rest of the sidebar content scrolls -->
      <div class="sidebar-content" v-show="!isCollapsed">
        <div class="accordion" id="weeksAccordion">
          <div v-for="(week, index) in courseData.weeks" :key="index" class="accordion-item">
            <h2 class="accordion-header">
              <button
                class="accordion-button"
                :class="{ collapsed: activeItem !== `week-${index}` }"
                @click="toggleItem(`week-${index}`)"
              >
                {{ week.title }}
              </button>
            </h2>
            <div
              class="accordion-collapse collapse"
              :class="{ show: activeItem === `week-${index}` }"
            >
              <ul class="list-group list-group-flush">
                <!-- Lectures -->
                <li
                  v-for="lecture in week.lectures"
                  :key="lecture.lec_id"
                  class="list-group-item"
                  :class="{ active: activeLesson === `lecture-${lecture.lec_id}` }"
                  @click="navigateToLesson(lecture, 'lecture', week)"
                >
                  {{ lecture.title }}
                </li>
                <!-- Practice Assignments -->
                <li
                  v-for="assignment in week.p_assignments"
                  :key="assignment.pa_id"
                  class="list-group-item"
                  :class="{ active: activeLesson === `practice_assignments-${assignment.pa_id}` }"
                  @click="navigateToLesson(assignment, 'practice_assignments', week)"
                >
                  {{ assignment.title }}
                </li>
                <!-- Practice Programming Assignments -->
                <li
                  v-for="assignment in week.pp_assignments || []"
                  :key="assignment.ppa_id"
                  class="list-group-item"
                  :class="{ active: activeLesson === `practice_programming-${assignment.ppa_id}` }"
                  @click="navigateToLesson(assignment, 'practice_programming', week)"
                >
                  {{ assignment.title }}
                </li>
                <!-- Graded Assignments -->
                <li
                  v-for="assignment in week.g_assignments"
                  :key="assignment.ga_id"
                  class="list-group-item"
                  :class="{ active: activeLesson === `graded_assignments-${assignment.ga_id}` }"
                  @click="navigateToLesson(assignment, 'graded_assignments', week)"
                >
                  {{ assignment.title }}
                </li>
                <!-- Graded Programming Assignments -->
                <li
                  v-for="assignment in week.grp_assignments || []"
                  :key="assignment.grpa_id"
                  class="list-group-item"
                  :class="{ active: activeLesson === `graded_programming-${assignment.grpa_id}` }"
                  @click="navigateToLesson(assignment, 'graded_programming', week)"
                >
                  {{ assignment.title }}
                </li>
                <!-- Concept Summary -->
                <li
                  v-if="week.concept_summary"
                  :key="week.concept_summary.cs_id"
                  class="list-group-item"
                  :class="{
                    active: activeLesson === `concept_summary-${week.concept_summary.cs_id}`,
                  }"
                  @click="navigateToLesson(week.concept_summary, 'concept_summary', week)"
                >
                  {{ week.concept_summary.title }}
                </li>
              </ul>
            </div>
          </div>
          <div
            v-if="!this.$route.path.includes('/ta/course/')"
            class="accordion-item no-toggle"
            id="createWithAI"
          >
            <h2 class="accordion-header">
              <!-- Use a static accordion button that never toggles -->
              <button class="accordion-button text-dark static" @click="navigateToAssignment">
                Practice with AI
              </button>
            </h2>
          </div>

          <div class="accordion-item" id="weeksAccordion">
            <button
              class="accordion-button"
              :class="{ collapsed: activeItem !== `week-${index}` }"
              @click="toggleItem(`week-${index}`)"
            >
              Supplementary contents
            </button>
            <div
              class="accordion-collapse collapse"
              :class="{ show: activeItem === `week-${index}` }"
            >
              <ul class="list-group list-group-flush">
                <li class="list-group-item" @click="fetch_contents">Extra Contents</li>
              </ul>
            </div>
          </div>
          <div
            v-if="!this.$route.path.includes('/ta/course/')"
            class="accordion-item no-toggle"
            id="createWithAI"
          >
            <h2 class="accordion-header">
              <!-- Use a static accordion button that never toggles -->
              <button class="accordion-button text-dark static" @click="showBookmarkQuestions">
                Bookmarked Questions
              </button>
            </h2>
          </div>
        </div>
      </div>
      <!-- end .sidebar-content -->
    </div>
    <!-- end .sidebar-wrapper -->
  </div>
  <!-- end #sidebar -->
</template>

<script>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  setup() {
    const route = useRoute()
    const router = useRouter()
    const courseId = computed(() => route.params.id)
    return { courseId, router, route }
  },
  data() {
    return {
      isCollapsed: false,
      activeItem: null,
      activeLesson: null,
      courses: [
        {
          id: '1',
          title: 'Python',
          weeks: [
            {
              id: '1',
              title: 'Week 1',
              lectures: [
                { lec_id: 'lecture-1', title: 'L1.1 - Introduction', type: 'lecture' },
                { lec_id: 'lecture-2', title: 'L1.2 - Basics', type: 'lecture' },
              ],
              g_assignments: [
                { ga_id: '1', title: 'Graded Assignment 1', type: 'graded-assignment' },
              ],
              grp_assignments: [
                {
                  grpa_id: '1',
                  title: 'Graded Programming Assignment 1',
                  type: 'graded-programming-assignment',
                },
              ],
              p_assignments: [
                { pa_id: '1', title: 'Practice Assignment 1', type: 'practice-assignment' },
              ],
              pp_assignments: [
                {
                  ppa_id: '1',
                  title: 'Practice Programming Assignment 1',
                  type: 'practice-programming-assignment',
                },
                {
                  ppa_id: '2',
                  title: 'Practice Programming Assignment 2',
                  type: 'practice-programming-assignment',
                },
              ],
              concept_summary: {
                cs_id: 'cs1',
                title: 'Concept Summary 1',
                type: 'concept-summary',
              },
            },
            {
              id: '2',
              title: 'Week 2',
              lectures: [
                { lec_id: 'lecture-3', title: 'L2.1 - Advanced Concepts', type: 'lecture' },
                { lec_id: 'lecture-4', title: 'L2.2 - Hands-on', type: 'lecture' },
              ],
              g_assignments: [
                { ga_id: '2', title: 'Graded Assignment 2', type: 'graded-assignment' },
              ],
              grp_assignments: [
                {
                  grpa_id: '3',
                  title: 'Graded Programming Assignment 3',
                  type: 'graded-programming-assignment',
                },
              ],
              p_assignments: [
                { pa_id: '2', title: 'Practice Assignment 2', type: 'practice-assignment' },
              ],
              pp_assignments: [
                {
                  ppa_id: '4',
                  title: 'Practice Programming Assignment 4',
                  type: 'practice-programming-assignment',
                },
              ],
              concept_summary: {
                cs_id: 'cs2',
                title: 'Concept Summary 2',
                type: 'concept-summary',
              },
            },
          ],
        },
        {
          id: '2',
          title: 'Maths-1',
          weeks: [
            {
              id: '1',
              title: 'Week 1: Algebra',
              lectures: [
                { lec_id: 'lecture-1', title: 'L1.1 - Linear Equations', type: 'lecture' },
                { lec_id: 'lecture-2', title: 'L1.2 - Quadratic Equations', type: 'lecture' },
              ],
              g_assignments: [
                { ga_id: '1', title: 'Graded Assignment 1', type: 'graded-assignment' },
              ],
              p_assignments: [
                { pa_id: '1', title: 'Practice Assignment 1', type: 'practice-assignment' },
              ],
              concept_summary: {
                cs_id: 'cs1',
                title: 'Concept Summary 1',
                type: 'concept-summary',
              },
            },
            {
              id: '2',
              title: 'Week 2: Calculus',
              lectures: [
                { lec_id: 'lecture-3', title: 'L2.1 - Limits', type: 'lecture' },
                { lec_id: 'lecture-4', title: 'L2.2 - Derivatives', type: 'lecture' },
              ],
              g_assignments: [
                { ga_id: '2', title: 'Graded Assignment 2', type: 'graded-assignment' },
              ],
              p_assignments: [
                { pa_id: '2', title: 'Practice Assignment 2', type: 'practice-assignment' },
              ],
              concept_summary: {
                cs_id: 'cs2',
                title: 'Concept Summary 2',
                type: 'concept-summary',
              },
            },
          ],
        },
      ],
    }
  },
  computed: {
    toggleIcon() {
      return this.isCollapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left'
    },
    courseData() {
      return (
        this.courses.find((course) => course.id === this.courseId) || {
          title: 'Unknown Course',
          weeks: [],
        }
      )
    },
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed
      this.$emit('sidebar-toggled', this.isCollapsed)
    },
    toggleItem(item) {
      this.activeItem = this.activeItem === item ? null : item
    },
    navigateToLesson(item, type, week) {
      // Update activeLesson and navigate to the proper route.
      this.activeLesson = `${type}-${item.lec_id || item.ga_id || item.pa_id || item.cs_id}`

      // Determine the base route based on the current route
      const base = this.$route.path.includes('/ta/course/')
        ? `/ta/course/${this.courseId}`
        : `/student/course/${this.courseId}`

      // Navigate to the new route
      this.$router.push(
        `${base}/week/${week.id}/${type}/${item.lec_id || item.ga_id || item.pa_id || item.cs_id || item.ppa_id || item.grpa_id}`,
      )
    },
    navigateToAssignment() {
      // Update activeLesson and navigate to the proper route.
      this.$router.push(`/student/course/${this.courseId}/practice_with_ai`)
    },
    fetch_contents() {
      alert('Will be uploaded later')
    },
    showBookmarkQuestions(){
      this.$router.push(`/student/course/${this.courseId}/bookmarked_questions`)
    }
  },
  watch: {
    $route: {
      immediate: true,
      handler(newRoute) {
        if (newRoute.params.week_id) {
          const weekIndex = this.courseData.weeks.findIndex((w) => w.id === newRoute.params.week_id)
          this.activeItem = weekIndex !== -1 ? `week-${weekIndex}` : null
        } else {
          this.activeItem = null
        }
        let type = ''
        let id = ''
        if (newRoute.path.includes('/lecture/')) {
          type = 'lecture'
          id = newRoute.params.lecture_id
        } else if (newRoute.path.includes('/practice_assignments/')) {
          type = 'practice_assignments'
          id = newRoute.params.assignment_id
        } else if (newRoute.path.includes('/practice_programming/')) {
          type = 'practice_programming'
          id = newRoute.params.programming_assignment_id
        } else if (newRoute.path.includes('/graded_assignments/')) {
          type = 'graded_assignments'
          id = newRoute.params.assignment_id
        } else if (newRoute.path.includes('/graded_programming/')) {
          type = 'graded_programming'
          id = newRoute.params.programming_assignment_id
        } else if (newRoute.path.includes('/concept_summary/')) {
          type = 'concept_summary'
          id = newRoute.params.cs_id
        }
        this.activeLesson = type && id ? `${type}-${id}` : null
      },
    },
  },
}
</script>

<style scoped>
/* The main sidebar container */
#sidebar {
  /* Increased width from 250px to 280px */
  width: 280px;
  transition: width 0.3s ease-in-out;
  position: fixed;
  top: 60px; /* Below the navbar */
  left: 0;
  height: calc(100vh - 60px);
  background-color: #f8f9fa;
  box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* We don't want the main container to scroll */
}

#sidebar.collapsed {
  width: 60px; /* Slightly bigger when collapsed to give more room */
}

/* The fixed heading at the top of the sidebar */
.sidebar-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: auto;
  padding: 15px 0;
  background-color: #f8f9fa;
  text-align: center;
  z-index: 999;
  box-sizing: border-box;
  border-bottom: 1px solid #ddd;
}

/* The scrollable wrapper (below the heading) */
.sidebar-wrapper {
  position: absolute;
  top: 60px; /* space for heading (15px top + heading size ~45px = ~60px total) */
  left: 0;
  width: 100%;
  height: calc(100% - 60px);
  overflow-y: auto;
  padding-right: 10px;
  /* Add a bit of left padding so items aren't glued to the edge */
  padding-left: 10px;
}

/* Hide content when collapsed */
#sidebar.collapsed .sidebar-content,
#sidebar.collapsed .sidebar-header {
  display: none;
}

/* Toggle button styling */
.toggle-btn {
  position: absolute;
  top: 10px;
  right: -35px; /* shift the button to the right so it doesn't overlap the scrollbar */
  transform: translateX(-100%);
  transition: right 0.3s ease-in-out;
  z-index: 1000; /* So it stays on top */
}

#sidebar.collapsed .toggle-btn {
  right: -35px;
  transform: translateX(-100%);
}

/* Accordion & active item styling */
.accordion-button {
  cursor: pointer;
  font-size: 1rem;
  /* Add some left padding to separate text from the edge */
  padding-left: 1.5rem !important;
}

.list-group-item {
  /* Slight left padding for list items */
  padding-left: 1.5rem !important;
}

.list-group-item.active {
  background-color: #d6d6d6 !important;
  color: black !important;
  font-weight: bold;
  border: 1px solid #d6d6d6 !important;
}

/* Custom scrollbar styling */
.sidebar-wrapper::-webkit-scrollbar {
  width: 8px;
}

.sidebar-wrapper::-webkit-scrollbar-track {
  background-color: #f1f1f1;
}

.sidebar-wrapper::-webkit-scrollbar-thumb {
  background-color: #c1c1c1;
  border-radius: 4px;
  border: 1px solid #f1f1f1;
}

/* For Firefox (scrollbar styling) */
.sidebar-wrapper {
  scrollbar-width: thin; /* "auto" or "thin" */
  scrollbar-color: #c1c1c1 #f1f1f1; /* thumb and track color */
}
.no-toggle .accordion-button::after {
  display: none; /* Hide the arrow */
}

.accordion-button.static {
  background-color: inherit; /* Keep same background as siblings */
  /* Optionally override active styles if needed */
  box-shadow: none;
}
</style>
