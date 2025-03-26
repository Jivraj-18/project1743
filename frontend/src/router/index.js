import { createRouter, createWebHistory } from 'vue-router'
import Courses from '../views/Instructor/Courses.vue'
import Updates from '../views/Instructor/Updates.vue'
import Student_Courses from '../views/Student/Courses.vue'
import ReportIssues from '../views/Student/reportIssues.vue'
import course from '../views/Instructor/Course.vue'
import ToDo from '@/views/Student/ToDo.vue'
import Login from '@/views/Login.vue'
import Announcements from '@/views/Student/Announcements.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', // done
      redirect: '/login',
    },
    {
      path: '/login', //done
      name: 'login',
      component: Login,
    },
    {
      path: '/student/announcements', // done
      name: 'announcements',
      component: () => import('@/views/Student/Announcements.vue'),
    },
    {
      path: '/student/profile', //done
      name: 'student_profile',
      component: () => import('@/views/Student/Profile.vue'),
    },
    {
      path: '/ta/profile', //done
      name: 'ta_profile',
      component: () => import('@/views/TA/Profile.vue'),
    },
    {
      path: '/instructor/courses', // done
      name: 'instructor-courses',
      component: Courses,
    },
    {
      path: '/instructor/updates', // there is no backend for this
      name: 'instructor-updates',
      component: Updates,
      props: true,
    },
    {
      path: '/student/courses', // done
      name: 'student-courses',
      component: Student_Courses,
      props: true,
    },
    {
      path: '/student/report-issues', // done 
      name: 'report-issues',
      component: ReportIssues,
      props: true,
    },
    {
      path: '/student/to_do', // there is no backend for this
      name: 'to_do',
      component: ToDo,
      props: true,
    },
    {
      path: '/instructor/course/:id', 
      name: 'instructor_course',
      component: course,
      props: true,
      children: [
        {
          path: '',
          name: 'instructor_course_about', //done
          component: () => import('@/components/instructor/About.vue'), // Default component
        },
        {
          path: 'create_assignment', // siddant will do 
          name: 'instructor_create_assignment',
          component: () => import('@/components/instructor/Create_with_AI.vue'),
        },
        {
          path: 'week/:week_id',
          name: 'week',
          // component: week,
          children: [
            {
              path: 'lecture/:lecture_id', //done
              name: 'lecture',
              component: () => import('@/components/Lecture.vue'),
            },
            {
              path: 'graded_assignments/:assignment_id', // done
              component: () => import('@/components/instructor/InstructorAssignment.vue'),
            },
            {
              path: 'practice_assignments/:assignment_id', //done
              component: () => import('@/components/instructor/InstructorAssignment.vue'),
            },
            {
              path: 'concept_summary/:cs_id', // siddhant will do this 
              component: () => import('@/components/ConceptsSummary.vue'),
            },
            {
              path: 'practice_programming/:programming_assignment_id', // done
              name: 'instructor_practice_programming_assignment',
              component: () =>
                import('@/components/instructor/InstructorProgrammingAssignment.vue'),
            },
            {
              path: 'graded_programming/:programming_assignment_id', // done
              name: 'instructor_graded_programming_assignment',
              component: () =>
                import('@/components/instructor/InstructorProgrammingAssignment.vue'),
            },
          ],
        },
      ],
    },
    {
      path: '/student/course/:id',
      name: 'student_course',
      component: () => import('@/views/Student/Course.vue'),
      props: true,
      children: [
        {
          path: '',
          name: 'student_course_about',
          component: () => import('@/components/student/About.vue'), // done
        },
        {
          path: 'practice_with_ai', // siddhant will do this
          name: 'practice_with_ai',
          component: () => import('@/components/student/Practice_with_AI.vue'),
        },
        {
          path: 'bookmarked_questions',
          name: 'bookmarked_questions',
          component: () => import('@/components/student/Bookmark_Questions.vue'), // pendings
        },
        {
          path: 'week/:week_id',
          name: 'student_week',
          children: [
            {
              path: 'lecture/:lecture_id', // done
              name: 'student_lecture',
              component: () => import('@/components/Lecture.vue'),
            },
            {
              path: 'graded_assignments/:assignment_id', // done
              name: 'student_graded_assignment',
              component: () => import('@/components/student/StudentAssignment.vue'),
            },
            {
              path: 'practice_assignments/:assignment_id', // done
              name: 'student_practice_assignment',
              component: () => import('@/components/student/StudentAssignment.vue'),
            },
            {
              path: 'concept_summary/:cs_id', // siddhant will do this
              name: 'student_concept_summary',
              component: () => import('@/components/ConceptsSummary.vue'),
            },
            {
              path: 'practice_programming/:programming_assignment_id', // done
              name: 'student_practice_programming_assignment',
              component: () => import('@/components/student/StudentProgrammingAssignment.vue'),
            },
            {
              path: 'graded_programming/:programming_assignment_id', // done
              name: 'student_graded_programming_assignment',
              component: () => import('@/components/student/StudentProgrammingAssignment.vue'),
            },
          ],
        },
      ],
    },
    {
      path: '/instructor/upload_resources',
      name: 'instructor_upload_resources',
      component: () => import('@/views/Instructor/Upload_Resources.vue'),
      props: true,
    },
    {
      path: '/ta/upload_resources',
      name: 'upload_resources',
      component: () => import('@/views/TA/Upload_Resources.vue'),
      props: true,
    },
    {
      path: '/ta/courses',
      name: 'ta-courses',
      component: Student_Courses,
      props: true,
    },
    {
      path: '/ta/course/:id',
      name: 'ta_course',
      component: () => import('@/views/Student/Course.vue'),
      props: true,
      children: [
        {
          path: '',
          name: 'ta_course_about',
          component: () => import('@/components/student/About.vue'), // Default component
        },
        {
          path: 'week/:week_id',
          name: 'ta_week',
          children: [
            {
              path: 'lecture/:lecture_id',
              name: 'ta_lecture',
              component: () => import('@/components/Lecture.vue'),
            },
            {
              path: 'graded_assignments/:assignment_id',
              name: 'ta_graded_assignment',
              component: () => import('@/components/student/StudentAssignment.vue'),
            },
            {
              path: 'practice_assignments/:assignment_id',
              name: 'ta_practice_assignment',
              component: () => import('@/components/student/StudentAssignment.vue'),
            },
            {
              path: 'concept_summary/:cs_id', // siddhant will do this
              name: 'ta_concept_summary',
              component: () => import('@/components/ConceptsSummary.vue'),
            },
            {
              path: 'practice_programming/:programming_assignment_id',
              name: 'ta_practice_programming_assignment',
              component: () => import('@/components/student/StudentProgrammingAssignment.vue'),
            },
            {
              path: 'graded_programming/:programming_assignment_id',
              name: 'ta_graded_programming_assignment',
              component: () => import('@/components/student/StudentProgrammingAssignment.vue'),
            },
          ],
        },
      ],
    },
    {
      path: '/ta/to_do',
      name: 'ta-to_do',
      component: () => import('@/views/TA/To_do.vue'),
      props: true,
    },
    {
      path: '/ta/view_issues',
      name: 'ta-view_issues',
      component: () => import('@/views/TA/View_Issues.vue'),
      props: true,
    },
  ],
})

export default router
