<template>
  <div>
    <!-- Main Content -->
    <div :class="['content', { 'content-expanded': isSidebarCollapsed }]">
      <div class="content-inner">
        <!-- Page title -->
        <h4 class="mb-3">{{ videoData.title }}</h4>

        <div class="row">
          <!-- Video Section (left) -->
          <div class="col-md-8 mb-3">
            <!-- Example HTML5 video with controls -->
            <video class="w-100" controls :poster="videoData.poster">
              <source :src="videoData.videoUrl" type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>

          <!-- Scrollable text (right) -->
          <div class="col-md-4 mb-3" style="max-height: 400px; overflow-y: auto">
            <p>{{ videoData.description }}</p>
          </div>
        </div>

        <!-- AI SUMMARY -->
        <div class="ai-summary-box">
          <h5 class="mb-2">AI SUMMARY</h5>
          <p>{{ videoData.aiSummary }}</p>
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
      videoData: {
        title: '',
        poster: '',
        videoUrl: '',
        description: '',
        aiSummary: '',
      },
    }
  },
  methods: {
    /**
     * Fetches dummy video data based on courseId, weekId, and videoId.
     * Later, this function can be replaced with an API call.
     */
    getDummyVideoData(courseId, weekId, videoId) {
      const course = parseInt(courseId)
      const week = parseInt(weekId)
      const video = videoId

      if (course === 1) {
        if (week === 1) {
          if (video === 'lecture-1') {
            return {
              title: 'L1.1 Introduction to Python',
              poster: '', // Add a poster image if available
              videoUrl:
                'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
              description:
                'Introduction to Python programming, its applications, and why it is widely used.',
              aiSummary:
                'This lesson introduces Python, its features, and its applications in modern programming.',
            }
          } else if (video === 'lecture-2') {
            return {
              title: 'L1.2 Python Installation',
              poster: '',
              videoUrl:
                'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
              description:
                'Step-by-step guide on installing Python and setting up a development environment.',
              aiSummary:
                'Covers Python installation, setting up an IDE, and writing a simple Python script.',
            }
          }
        } else if (week === 2) {
          if (video === 'lecture-3') {
            return {
              title: 'L2.1 Lists and Tuples',
              poster: '',
              videoUrl:
                'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
              description:
                'Understanding Python lists and tuples, their differences, and use cases.',
              aiSummary:
                'Explains Python lists and tuples, their syntax, and when to use each data structure.',
            }
          }
          if (video === 'lecture-4') {
            return {
              title: 'L2.2 Dictionaries',
              poster: '',
              videoUrl:
                'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
              description:
                'Introduction to algebra, including variables, expressions, and basic equations.',
              aiSummary:
                'Explains algebra fundamentals, including expressions, operations, and simple equations.',
            }
          }
        }
      } else if (course === 2) {
        if (week === 1) {
          if (video === 'lecture-1') {
            return {
              title: 'L1.1 Introduction to Linear Equations',
              poster: '', // Add a poster image if available
              videoUrl:
                'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
              description:
                'Introduction to Python programming, its applications, and why it is widely used.',
              aiSummary:
                'This lesson introduces Python, its features, and its applications in modern programming.',
            }
          } else if (video === 'lecture-2') {
            return {
              title: 'L1.2 Quadratic Equations',
              poster: '',
              videoUrl:
                'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
              description:
                'Step-by-step guide on installing Python and setting up a development environment.',
              aiSummary:
                'Covers Python installation, setting up an IDE, and writing a simple Python script.',
            }
          }
        } else if (week === 2) {
          if (video === 'lecture-3') {
            return {
              title: 'L2.1 Limits',
              poster: '',
              videoUrl:
                'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
              description:
                'Understanding Python lists and tuples, their differences, and use cases.',
              aiSummary:
                'Explains Python lists and tuples, their syntax, and when to use each data structure.',
            }
          }
          if (video === 'lecture-4') {
            return {
              title: 'L2.2 Derivatives',
              poster: '',
              videoUrl:
                'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
              description:
                'Introduction to algebra, including variables, expressions, and basic equations.',
              aiSummary:
                'Explains algebra fundamentals, including expressions, operations, and simple equations.',
            }
          }
        }
      }
      return {
        title: 'Video Not Found',
        poster: '',
        videoUrl: '',
        description: 'No content available for this course, week, or video.',
        aiSummary: 'No summary available.',
      }
    },

    /**
     * Fetches video data based on route parameters.
     */
    fetchVideoData() {
      const courseId = this.$route.params.id
      console.log(courseId)
      const weekId = this.$route.params.week_id
      console.log(weekId)
      const videoId = this.$route.params.lecture_id
      console.log(videoId)
      this.videoData = this.getDummyVideoData(courseId, weekId, videoId)
      // const courseId = 1
      // const weekId = 1
      // const videoId = 2
      // this.videoData = this.getDummyVideoData(courseId, weekId, videoId)
      
    },
  },
  created() {
    this.fetchVideoData()
  },
  watch: {
    // Corrected watchers to match actual route param names
    '$route.params.id'() {
      // Was 'course_id'
      this.fetchVideoData()
    },
    '$route.params.week_id'() {
      this.fetchVideoData()
    },
    '$route.params.lecture_id'() {
      // Was 'video_id'
      this.fetchVideoData()
    },
  },
}
</script>

<style scoped>
/* Main container: content */
#content {
  padding: 1rem;
}

/* AI Summary box styling */
.ai-summary-box {
  background-color: #d1d5db;
  border-radius: 4px;
  padding: 1rem;
  margin-top: 1rem;
}

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
</style>
