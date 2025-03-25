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
      iframeLoaded: false,
      currentQuestion: null,
      testCases: [],
      showHint: false,
      testResults: [],
      currentTestIndex: -1,  // Track which test case is currently running
      isTestRunning: false,  // Flag to indicate if a test is running
      currentOutput: null,   // Store the current execution output
    };
  },
  mounted() {
    this.fetchAssignmentQuestions();
    window.addEventListener('message', this.handleIframeMessage);
  },
  beforeUnmount() {
    window.removeEventListener('message', this.handleIframeMessage);
  },
  methods: {
    fetchAssignmentQuestions() {
      fetch(`http://localhost:5000/api/questions_for_assignment/${this.$route.params.programming_assignment_id}`, {
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
              this.questionText = `${data.questions[0].question}`;
              this.defaultCode = this.currentQuestion.question;
              try {
                this.testCases = JSON.parse(this.currentQuestion.correct_options);
              } catch (e) {
                console.error("Error parsing test cases:", e);
              }
              if (this.iframeLoaded) this.sendCode();
            }
          }
        }).catch(error => {
          console.error("Error fetching questions:", error);
        });
    },
    onIframeLoad() {
      this.iframeLoaded = true;
      if (this.defaultCode) this.sendCode();
    },
    sendCode() {
      const iFrame = document.getElementById("oc-editor");
      if (iFrame?.contentWindow) {
        iFrame.contentWindow.postMessage({
          eventType: "populateCode",
          language: "javascript",
          files: [{ name: "solution.js", content: this.defaultCode }]
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
      // Handle the new format of event.data
      if (event.data?.action === 'runComplete') {
        if (this.isTestRunning && this.currentTestIndex >= 0) {
          // Get output from the new data structure
          const output = event.data.result?.output;
          this.currentOutput = output; // Store the raw execution output
          
          // Process the test case result
          this.processTestResult(output);
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
      alert("Solution submitted for evaluation!");
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