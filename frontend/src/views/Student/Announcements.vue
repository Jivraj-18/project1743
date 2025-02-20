<template>
  <div>
    <Navbar />
    <div class="container my-2">
      <!-- Page header bar -->
      <!-- ANNOUNCEMENT #1 -->
      <div class="mb-5">
        <h5 class="fw-bold">10 January</h5>
        <h6 class="fw-bold">
          Course Cards For January 2025 Term Added To Your Dashboard
          <br />
          <small class="text-muted">ONLY FOR JAN 2025 REGISTERED</small>
        </h6>
        <p>Dear Students,</p>
        <p>
          <strong>THIS ANNOUNCEMENT IS ONLY FOR JAN 2025 REGISTERED</strong>
        </p>
        <p>
          We are pleased to inform you that the course cards for your registered courses for the
          January 2025 term have been added to your student dashboard under the Current Courses
          section.
        </p>
        <p><strong>Please Take the Following Actions:</strong></p>
        <ol>
          <li>
            <strong>Check Course Cards:</strong> Verify that the courses you have registered for are
            visible on your dashboard.
          </li>
          <li>
            <strong>Seek Portal Access:</strong> Clicking on a course card will direct you to the
            Seek portal. However, please note that lecture videos and content access will only be
            available starting from the official course launch date.
          </li>
        </ol>
      </div>
      <hr />

      <!-- ANNOUNCEMENT #2 -->
      <div class="mb-5">
        <h5 class="fw-bold">10 February</h5>
        <h6 class="fw-bold">Important: Last Chance To Edit Exam City Preference For Quiz 2</h6>
        <p>Dear Learners,</p>
        <p>
          The option to edit the exam city preference for the Quiz 2 is available in your dashboard
          under Hall ticket and Exam cities.
          <br />
          Last date to edit the exam city is Sunday (16/02/2025) at 5 PM IST.
        </p>
        <p>
          Students who wish to change their exam city from India to Outside India, or vice versa,
          must email
          <a href="mailto:support@study.iitm.ac.in">support@study.iitm.ac.in</a>
          to receive a G-form.
        </p>
        <p>
          We request students to select the exam city considering all your situation. No more
          changes will be entertained in the city after the deadline.
        </p>
        <p><strong>Note :</strong></p>
        <ul>
          <li>
            The Quiz 1 exam city shown on the dashboard is final. The given edit option is only for
            quiz 2.
          </li>
          <li>
            This is not applicable for the students registered for Repeat Oppe only / Repeat end
            term only / Registered only for projects.
          </li>
        </ul>
        <p>Regards,<br />IITM BS TEAM</p>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/student/NavBar.vue'
export default {
  components: { Navbar },
}
</script>

<style scoped>
/* Page header styling */
.page-header {
  background-color: #d1d5db;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

/* If you want the same “card-custom” style as your assignments,
     you can replicate that here. Otherwise, standard Bootstrap classes suffice. */
</style>
