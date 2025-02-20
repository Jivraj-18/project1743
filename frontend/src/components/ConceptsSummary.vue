<template>
  <div>
    <!-- MAIN CONTENT -->
    <div :class="['content', { 'content-expanded': isSidebarCollapsed }]">
      <div class="content-inner">
        <!-- Page Header -->
        <div class="page-header">
          <h2 class="mb-0">{{ summaryData.header }}</h2>
        </div>

        <!-- Subheading -->
        <h4 class="mb-3">{{ summaryData.subheading }}</h4>

        <!-- Accordion for Concepts -->
        <div class="accordion" id="conceptsAccordion">
          <div class="accordion-item" v-for="(concept, idx) in summaryData.concepts" :key="idx">
            <h2 class="accordion-header">
              <button
                class="accordion-button"
                :class="{ collapsed: !concept.open }"
                type="button"
                @click="toggleConcept(idx)"
              >
                {{ concept.title }}
              </button>
            </h2>
            <div
              :id="'concept' + idx + 'Collapse'"
              class="accordion-collapse collapse"
              :class="{ show: concept.open }"
            >
              <div class="accordion-body">
                {{ concept.body }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isSidebarCollapsed: Boolean,
  },
  data() {
    return {
      summaryData: {
        header: '',
        subheading: '',
        concepts: [],
      },
    }
  },
  methods: {
    /**
     * Returns dummy summary data based on courseId and weekId.
     * Later, replace this with an API call.
     */
    getDummySummary(courseId, weekId) {
      const week = parseInt(weekId)
      const course = parseInt(courseId)

      if (course === 1) {
        switch (week) {
          case 1:
            return {
              header: 'Python - Week 1 Summary',
              subheading: 'Introduction & Basics',
              concepts: [
                { title: 'What is Python?', body: 'Overview of Python programming.', open: false },
                { title: 'Environment Setup', body: 'Installing Python.', open: false },
                { title: 'First Program', body: 'Writing your first script.', open: false },
              ],
            }
          case 2:
            return {
              header: 'Python - Week 2 Summary',
              subheading: 'Data Structures & Control Flow',
              concepts: [
                { title: 'Lists and Tuples', body: 'Working with lists & tuples.', open: false },
                { title: 'Dictionaries', body: 'Using key-value pairs.', open: false },
                {
                  title: 'Conditionals & Loops',
                  body: 'If-else statements and loops.',
                  open: false,
                },
              ],
            }
          default:
            return { header: 'Python Summary Not Found', subheading: 'No data.', concepts: [] }
        }
      } else if (course === 2) {
        switch (week) {
          case 1:
            return {
              header: 'Maths-1 - Week 1 Summary',
              subheading: 'Algebra & Arithmetic',
              concepts: [
                { title: 'Basic Algebra', body: 'Introduction to algebra.', open: false },
                { title: 'Arithmetic Review', body: 'Review of number theory.', open: false },
                { title: 'Problem Solving', body: 'Techniques for solving problems.', open: false },
              ],
            }
          case 2:
            return {
              header: 'Maths-1 - Week 2 Summary',
              subheading: 'Linear Equations & Graphs',
              concepts: [
                { title: 'Solving Equations', body: 'Solving linear equations.', open: false },
                { title: 'Graphing', body: 'Plotting and interpreting graphs.', open: false },
                { title: 'Applications', body: 'Real-world uses.', open: false },
              ],
            }
          default:
            return { header: 'Maths-1 Summary Not Found', subheading: 'No data.', concepts: [] }
        }
      } else {
        return { header: 'Course Summary Not Found', subheading: 'Invalid course.', concepts: [] }
      }
    },
    /**
     * Fetches summary data based on route parameters.
     */
    fetchSummaryData() {
      const courseId = this.$route.params.id
      const weekId = this.$route.params.week_id
      this.summaryData = this.getDummySummary(courseId, weekId)
      // const courseId = 1
      // const weekId = 1
      // this.summaryData = this.getDummySummary(courseId, weekId)
    },
    /**
     * Toggles the concept dropdown state.
     */
    toggleConcept(index) {
      this.summaryData.concepts[index].open = !this.summaryData.concepts[index].open
    },
  },
  created() {
    this.fetchSummaryData()
  },
  watch: {
    '$route.params.course_id'() {
      this.fetchSummaryData()
    },
    '$route.params.week_id'() {
      this.fetchSummaryData()
    },
  },
}
</script>

<style scoped>
/* Ensure the component fills the viewport */
.content {
  flex: 1;
  overflow-y: auto;
  transition: margin-left 0.3s ease-in-out;
  margin-left: 250px;
}

.content-expanded {
  margin-left: 50px;
}

.sidebar.collapsed + #content {
  margin-left: 50px;
}

.content-inner {
  padding: 1rem;
}

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

/* Content styling */
#content {
  flex: 1;
  overflow-y: auto;
}

.content-inner {
  padding: 1rem;
}

/* Page header styling */
.page-header {
  background-color: #d1d5db;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

/* Responsive accordion button */
.accordion-button {
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.3s ease-in-out;
}

.accordion-button:focus {
  outline: none;
  box-shadow: none;
}
</style>
