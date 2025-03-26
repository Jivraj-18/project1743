<template>
  <div>
    <h2>Programming Assignment</h2>

    <div class="question-box">
      <p>{{ questionText }}</p>

      <div v-if="showHint" class="hint-box">
        <p><strong>Hint:</strong> {{ currentQuestion?.hints }}</p>
      </div>
      <button @click="toggleHint" class="hint-btn">{{ showHint ? 'Hide Hint' : 'Show Hint' }}</button>
    </div>

    <div id="onecompiler-embed">
      <iframe id="oc-editor" :src="editorUrl" width="100%" height="450px" frameborder="0" style="border-radius: 4px"
        @load="onIframeLoad"></iframe>
    </div>

    <div class="test-cases-section">
      <h3>Test Cases</h3>
      <div v-for="(testCase, index) in testCases" :key="index" class="test-case">
        <div><strong>Input:</strong> {{ testCase.input }}</div>
        <div><strong>Expected Output:</strong> {{ testCase.expected_output }}</div>
      </div>
    </div>

    <button @click="sendCode" class="btn">Reset Code</button>
    <button @click="runCode" class="btn primary">Run Code</button>
    <button @click="submitCode" class="btn success">Submit Solution</button>

    <!-- Execution Output Section -->
    <div class="execution-output" v-if="currentOutput">
      <h3>Execution Output</h3>
      <pre>{{ currentOutput }}</pre>
    </div>

    <div v-if="testResults.length" class="test-results">
      <h3>Test Results</h3>
      <ul>
        <li v-for="(result, index) in testResults" :key="index" :class="{ pass: result.passed, fail: !result.passed }">
          <strong>Input:</strong> {{ result.input }} |
          <strong>Expected:</strong> {{ result.expected }} |
          <strong>Actual:</strong> {{ result.actual }} |
          <strong>Status:</strong> {{ result.passed ? '✅ Pass' : '❌ Fail' }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      editorUrl: "https://onecompiler.com/embed/javascript?listenToEvents=true&codeChangeEvent=true",
      questionText: "Loading question...",
      defaultCode: "",
      studentCode: null,
      iframeLoaded: false,
      currentQuestion: null,
      testCases: [],
      showHint: false,
      testResults: [],
      currentTestIndex: -1,  // Track which test case is currently running
      isTestRunning: false,  // Flag to indicate if a test is running
      currentOutput: null,   // Store the current execution output
      waitingForCodeResponse: false, // Track if we're waiting for a response from OneCompiler
    };
  },
  mounted() {
    this.fetchAssignmentData();
    window.addEventListener('message', this.handleIframeMessage);
  },
  beforeUnmount() {
    window.removeEventListener('message', this.handleIframeMessage);
  },
  methods: {
    fetchAssignmentData() {
      const assignmentId = this.$route.params.programming_assignment_id;
      
      // Get student ID from localStorage
      const userData = JSON.parse(localStorage.getItem('userdata'));
      const studentId = userData.student_id;

      fetch(`http://localhost:5000/api/assignments/${assignmentId}/${studentId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.questions?.length > 0) {
            this.currentQuestion = data.questions.find(q => q.question_type === 'Programming');
            if (this.currentQuestion) {
              this.questionText = this.currentQuestion.question;
              this.defaultCode = this.currentQuestion.question;
              
              try {
                this.testCases = JSON.parse(this.currentQuestion.correct_options);
              } catch (e) {
                console.error("Error parsing test cases:", e);
              }
              
              // Check if there's a submission with code
              if (data.submission && data.submission.code) {
                this.studentCode = data.submission.code;
                console.log("Found student's submitted code:", this.studentCode);
              }
              
              // If iframe is loaded, populate with student code if available, otherwise use default code
              if (this.iframeLoaded) {
                this.sendCode();
              }
            }
          }
        }).catch(error => {
          console.error("Error fetching assignment data:", error);
        });
    },
    onIframeLoad() {
      this.iframeLoaded = true;
      if (this.studentCode || this.defaultCode) {
        this.sendCode();
      }
    },
    sendCode() {
      const iFrame = document.getElementById("oc-editor");
      if (iFrame?.contentWindow) {
        // Use student's code if available, otherwise use default code
        const codeToSend = this.studentCode || this.defaultCode;
        
        iFrame.contentWindow.postMessage({
          eventType: "populateCode",
          language: "javascript",
          files: [{ name: "solution.js", content: codeToSend }]
        }, "*");
      }
    },
    runCode() {
      this.testResults = [];
      this.currentTestIndex = 0;
      
      if (this.testCases.length > 0) {
        this.runNextTestCase();
      }
    },
    runNextTestCase() {
      if (this.currentTestIndex >= this.testCases.length) {
        // All tests completed
        this.isTestRunning = false;
        this.currentTestIndex = -1;
        return;
      }
      
      const testCase = this.testCases[this.currentTestIndex];
      this.isTestRunning = true;
      
      const iFrame = document.getElementById("oc-editor");
      if (iFrame?.contentWindow) {
        // Send the test input to the editor
        iFrame.contentWindow.postMessage({
          eventType: "populateStdin",
          stdin: testCase.input.toString()
        }, "*");
        
        // Wait a moment to ensure input is set, then trigger the run
        setTimeout(() => {
          iFrame.contentWindow.postMessage({ eventType: "triggerRun" }, "*");
        }, 100);
      }
    },
    handleIframeMessage(event) {
      // Handle run complete event
      if (event.data?.action === 'runComplete') {
        if (this.isTestRunning && this.currentTestIndex >= 0) {
          // Get output from the new data structure
          const output = event.data.result?.output;
          this.currentOutput = output; // Store the raw execution output
          
          // Process the test case result
          this.processTestResult(output);
        }
      }
      
      // Handle get code response event
      if (event.data?.action === 'getCodeResponse') {
        this.waitingForCodeResponse = false;
        const code = event.data.files?.[0]?.content;
        if (code) {
          console.log("Received code from OneCompiler, submitting solution");
          this.submitSolution(code);
        } else {
          console.error("Received getCodeResponse but no code content");
          this.submitCodeAlternative();
        }
      }
    },
    processTestResult(output) {
      if (this.currentTestIndex >= 0 && this.currentTestIndex < this.testCases.length) {
        const testCase = this.testCases[this.currentTestIndex];
        const actualOutput = output ? output.trim() : '';
        const expected = testCase.expected_output.trim();
        const passed = actualOutput === expected;
        
        // Store the result
        this.testResults.push({
          input: testCase.input,
          expected: expected,
          actual: actualOutput || '(no output)',
          passed
        });
        
        // Move to next test case after a short delay
        this.currentTestIndex++;
        setTimeout(() => {
          this.runNextTestCase();
        }, 500);
      }
    },
    toggleHint() {
      this.showHint = !this.showHint;
    },
    submitCode() {
      // First try to get the code from OneCompiler using their API
      const iFrame = document.getElementById("oc-editor");
      
      // Add a safety check to make sure we'll get a response
      this.waitingForCodeResponse = true;
      
      if (iFrame?.contentWindow) {
        try {
          // Request code from OneCompiler
          iFrame.contentWindow.postMessage({ eventType: "getCode" }, "*");
          console.log("Requested code from OneCompiler");
          
          // Set a timeout in case we don't get a response
          setTimeout(() => {
            if (this.waitingForCodeResponse) {
              // If we're still waiting after 2 seconds, try the alternative approach
              console.log("No response from OneCompiler, trying alternative method");
              this.submitCodeAlternative();
              this.waitingForCodeResponse = false;
            }
          }, 2000);
        } catch (error) {
          console.error("Error requesting code from OneCompiler:", error);
          this.submitCodeAlternative();
        }
      } else {
        console.error("Cannot access OneCompiler iframe");
        this.submitCodeAlternative();
      }
    },
    submitCodeAlternative() {
      // In case we can't get the code from OneCompiler event handling,
      // use the most recent code we have
      const code = this.studentCode || this.defaultCode;
      if (code) {
        this.submitSolution(code);
      } else {
        alert("Unable to retrieve your code. Please try again or copy your code manually.");
      }
    },
    submitSolution(code) {
      const assignmentId = this.$route.params.programming_assignment_id;
      const userData = JSON.parse(localStorage.getItem('userdata'));
      const studentId = userData.student_id;
      
      // Create a placeholder answer for the API format
      const questionId = this.currentQuestion.question_id;
      const studentAnswers = {};
      studentAnswers[questionId] = "submission"; // Placeholder value
      
      // Add debugging to see what we're sending
      console.log("Submitting solution with data:", {
        student_id: studentId,
        assignment_id: assignmentId,
        student_answers: studentAnswers,
        code: code.substring(0, 50) + "..." // Log just part of code for brevity
      });
      
      // Submit the code to the backend
      fetch('http://localhost:5000/api/assignments', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          student_id: studentId,
          assignment_id: assignmentId,
          student_answers: studentAnswers,
          code: code
        })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        alert("Solution submitted successfully!");
        console.log("Submission response:", data);
        
        // Store the submitted code locally to reflect the changes
        this.studentCode = code;
        
        // Run tests to show results visually
        this.runCode();
      })
      .catch(error => {
        alert(`Error submitting solution: ${error.message}`);
        console.error("Error:", error);
      });
    }
  }
};
</script>

<style scoped>
.test-results {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.test-results ul {
  list-style: none;
  padding: 0;
}

.test-results li {
  padding: 5px;
  margin-bottom: 5px;
  border-radius: 3px;
}

.pass {
  background: #d4edda;
  color: #155724;
}

.fail {
  background: #f8d7da;
  color: #721c24;
}

/* Added styles for execution output display */
.execution-output {
  margin-top: 20px;
  padding: 10px;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 5px;
}

.execution-output pre {
  white-space: pre-wrap;
  font-family: monospace;
  margin: 0;
  padding: 10px;
  background: #f1f1f1;
  border-radius: 3px;
  max-height: 200px;
  overflow-y: auto;
}

.question-box {
  border: 1px solid #4a90e2;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 5px;
  background-color: #f5f9ff;
  position: relative;
}

.hint-box {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 10px;
  margin-top: 15px;
}

.hint-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.test-cases-section {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 5px;
}

.test-case {
  padding: 8px;
  margin-bottom: 5px;
  background-color: white;
  border: 1px solid #e9ecef;
  border-radius: 4px;
}

.btn {
  margin-right: 10px;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn.primary {
  background-color: #007bff;
  color: white;
}

.btn.success {
  background-color: #28a745;
  color: white;
}
</style>