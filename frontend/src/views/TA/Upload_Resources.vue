<template>
  <div>
    <!-- Simplified Header -->
    <NavBar />

    <!-- Page Title -->
    <div class="page-title"></div>

    <!-- Main Content -->
    <div class="upload-container">
      <!-- Form Row -->
      <div class="row">
        <div class="col-md-6">
          <!-- Course Selection -->
          <select class="week-select mb-3" v-model="selectedCourse" @change="fetchResources">
            <option disabled value="">Select Course</option>
            <option value="python">Python</option>
            <option value="maths-1">Maths-1</option>
          </select>

          <!-- Week Selection -->
          <select class="week-select" v-model="selectedWeek" @change="fetchResources">
            <option disabled value="">Select Week</option>
            <option value="1">WEEK 1</option>
            <option value="2">WEEK 2</option>
          </select>

          <!-- Resource Title Input -->
          <input
            type="text"
            class="form-control"
            placeholder="Resource Title"
            v-model="resourceTitle"
          />

          <!-- Description Input -->
          <textarea
            class="form-control"
            rows="6"
            placeholder="Description..."
            v-model="resourceDescription"
          ></textarea>

          <!-- Selected File Display -->
          <div v-if="selectedFile" class="mb-2">
            <small>Selected file: <strong>{{ selectedFile.name }}</strong></small>
          </div>

          <!-- Upload Button Area -->
          <div class="mt-3">
            <button class="btn btn-primary w-100" @click="uploadResource" :disabled="!formValid">
              Upload Resource
            </button>
          </div>
        </div>

        <div class="col-md-6">
          <!-- Upload Area -->
          <div
            class="upload-area"
            @click="triggerFileInput"
            @dragover.prevent="handleDragOver"
            @dragleave.prevent="handleDragLeave"
            @drop.prevent="handleDrop"
          >
            <div class="upload-icon">
              <i class="bi bi-cloud-upload fs-4"></i>
            </div>
            <div class="upload-text">
              <span class="fw-bold">Click to upload</span> or drag and drop
            </div>
            <div class="text-muted mb-3">OR</div>
            <button class="browse-button" @click="triggerFileInput">Browse Files</button>
            <input ref="fileInput" type="file" class="d-none" @change="handleFileChange" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/TA/NavBar.vue'
export default {
  name: 'TAUploadResources',
  data() {
    return {
      // Form selections
      selectedCourse: '',
      selectedWeek: '',
      resourceTitle: '',
      resourceDescription: '',
      // Reactive property for file upload
      selectedFile: null,
      // List of resources (dummy data in this example)
      resourcesList: [],
      // For editing a resource
      editForm: {
        id: null,
        title: '',
        description: '',
        // Stored file name of the original upload
        fileName: '',
        newFile: null,
        newFileName: '',
      },
    }
  },
  components: { NavBar },
  computed: {
    // Form is valid only if course, week, title, description and file are provided
    formValid() {
      return (
        this.selectedCourse &&
        this.selectedWeek &&
        this.resourceTitle.trim() &&
        this.resourceDescription.trim() &&
        this.selectedFile
      )
    },
    // Generate formatted file name: course_week_originalfilename
    formattedFileName() {
      if (!this.selectedCourse || !this.selectedWeek || !this.selectedFile) return ''
      return `${this.selectedCourse}_${this.selectedWeek}_${this.selectedFile.name}`
    },
  },
  methods: {
    async fetchResources() {
      if (!this.selectedCourse || !this.selectedWeek) {
        this.resourcesList = []
        return
      }
      try {
        // Construct file path assuming the resource file list is stored as a text file (with JSON data)
        const filePath = `/src/assets/uploaded_resources/${this.selectedCourse}_week${this.selectedWeek}.txt`
        const response = await fetch(filePath)
        if (!response.ok) {
          throw new Error('File not found')
        }
        const data = await response.json()
        this.resourcesList = data.resources || []
      } catch (error) {
        console.error(error)
        // Fallback dummy data
        this.resourcesList = [
          {
            id: 'dummy1',
            title: 'Dummy Resource 1',
            description: 'This is a dummy resource for testing.',
            fileName: `${this.selectedCourse}_${this.selectedWeek}_dummy1.txt`,
          },
          {
            id: 'dummy2',
            title: 'Dummy Resource 2',
            description: 'Another dummy resource for testing.',
            fileName: `${this.selectedCourse}_${this.selectedWeek}_dummy2.txt`,
          },
        ]
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    handleDragOver(e) {
      e.currentTarget.style.borderColor = '#6c757d'
    },
    handleDragLeave(e) {
      e.currentTarget.style.borderColor = '#dee2e6'
    },
    handleDrop(e) {
      e.currentTarget.style.borderColor = '#dee2e6'
      const files = e.dataTransfer.files
      if (files && files.length > 0) {
        this.selectedFile = files[0]
      }
    },
    handleFileChange(e) {
      const file = e.target.files[0]
      if (file) {
        this.selectedFile = file
      }
    },
    uploadResource() {
      if (!this.formValid) {
        alert('Please fill in all required fields and select a file.')
        return
      }
      // Generate file name based on the naming convention
      const fileName = this.formattedFileName
      // In a real app, you would upload the file and persist resource data via an API call.
      const newResource = {
        id: 'r' + (this.resourcesList.length + 1),
        title: this.resourceTitle,
        description: this.resourceDescription,
        fileName: fileName,
      }
      this.resourcesList.push(newResource)
      this.resourceTitle = ''
      this.resourceDescription = ''
      this.selectedFile = null
      this.$refs.fileInput.value = ''
      alert('Resource uploaded successfully! File saved as: ' + fileName)
    },
    openEditModal(resource) {
      // Populate the edit form with resource data
      this.editForm.id = resource.id
      this.editForm.title = resource.title
      this.editForm.description = resource.description
      this.editForm.fileName = resource.fileName
      this.editForm.newFile = null
      this.editForm.newFileName = ''
      const modal = new bootstrap.Modal(document.getElementById('editResourceModal'))
      modal.show()
    },
    handleEditFileChange(e) {
      const file = e.target.files[0]
      if (file) {
        this.editForm.newFile = file
        this.editForm.newFileName = file.name
      }
    },
    saveEdit() {
      const index = this.resourcesList.findIndex((res) => res.id === this.editForm.id)
      if (index !== -1) {
        this.resourcesList[index].title = this.editForm.title
        this.resourcesList[index].description = this.editForm.description
        if (this.editForm.newFile) {
          // Update file name following the convention
          const newFileName = `${this.selectedCourse}_${this.selectedWeek}_${this.editForm.newFile.name}`
          this.resourcesList[index].fileName = newFileName
          console.log('New file selected for update:', this.editForm.newFile)
        }
        alert('Resource updated successfully!')
      }
      this.closeEditModal()
    },
    deleteResource(resourceId) {
      this.resourcesList = this.resourcesList.filter((res) => res.id !== resourceId)
      alert('Resource deleted successfully!')
      this.closeEditModal()
    },
    closeEditModal() {
      const modal = bootstrap.Modal.getInstance(document.getElementById('editResourceModal'))
      modal.hide()
    },
    viewFile(fileName) {
      // In a real app, you would generate a proper URL to the file. For now, we assume the file is in the assets folder.
      const fileUrl = `/src/assets/uploaded_resources/${fileName}`
      window.open(fileUrl, '_blank')
    },
  },
}
</script>

<style scoped>
body {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.navbar {
  border-bottom: 1px solid #dee2e6;
  background-color: white !important;
}

.nav-link {
  color: #6c757d !important;
  font-size: 1.1rem;
  padding: 1rem 1.5rem !important;
}

.nav-link.active {
  color: #212529 !important;
  font-weight: 500;
}

.page-title {
  text-align: center;
  padding: 1rem;
  background-color: white;
  margin-bottom: 2rem;
  padding-top: 70px;
}

.upload-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.week-select {
  background-color: #dee2e6;
  border: none;
  padding: 0.75rem;
  border-radius: 4px;
  width: 100%;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  cursor: pointer;
}

.form-control {
  border: 1px solid #dee2e6;
  padding: 0.75rem;
  margin-bottom: 1.5rem;
}

.form-control::placeholder {
  color: #adb5bd;
}

.upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  padding: 3rem;
  text-align: center;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.upload-area:hover {
  border-color: #adb5bd;
}

.upload-icon {
  width: 48px;
  height: 48px;
  background-color: #f8f9fa;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.upload-text {
  margin-bottom: 0.5rem;
}

.browse-button {
  background-color: #212529;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.browse-button:hover {
  background-color: #343a40;
}

.card {
  border: 1px solid #dee2e6;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .upload-container {
    padding: 0 1rem;
  }
}
</style>
