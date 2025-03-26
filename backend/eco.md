# API Test Cases Documentation

## Overview
This document outlines all the test cases used to validate the AI API (`/api/ai`) which uses `POST` method. Each test case includes its description, request details, expected outcomes, and justification for its importance.

**Test Code:**
```python
API_URL = "http://localhost:5000/api/ai"  #API Endpoint
```

```python
cases = [[..], [..], .... , [..]]
# Every case in cases in in format [ Request Body, Is Success?, Response Status Code ]
```

```python
@pytest.mark.parametrize("reqBody, isok, statusCode", cases)
def test_api(reqBody, isok, statusCode):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Send POST request
    response = requests.post(API_URL, headers=headers, data=json.dumps(reqBody))
    
    # Check for JSON response
    try:
        result = response.json()
    except ValueError:
        pytest.fail("Invalid JSON response")

    # Check if the status code
    assert response.status_code == statusCode, f"Expected status code {statusCode}, but got {response.status_code}"

    # Determine if the response indicates success or error
    success = False if "error" in result else True

    # Assert that the result matches the expected outcome
    assert success == isok, f"Test failed for input: {reqBody}. Got: {result}"
```


## Test Cases

### **Test Case 1**
- **Test ID:** TC01
- **Test Description:**  
If the request body is an empty string (""), the system should return an error message stating that the input is invalid. This test ensures the system doesn't attempt to process an empty or non-informative request.
- **Request Body:**
    ```json
    ""
    ```
- **Expected Response:**
    ```json
    {
        "res": "Invalid input",
        "error": true
    }
    ```
- **Status Code:** `400` BAD REQUEST
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with an invalid or malformed request body.
2. Verify that the response status code is 400 BAD Request.
3. Ensure that the response body contains an "error" field.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the system can handle empty string inputs appropriately. An empty string is not a valid request, and the system should respond with an error message indicating that the input is invalid.

---

### **Test Case 2**
- **Test ID:** TC02
- **Test Description:**  
If the request body contains a string that doesn't conform to the expected format (in this case, a random string like "suifdghb"), the system should detect this as invalid input and return a meaningful error message.
- **Request Body:**
    ```json
    "suifdghb"
    ```
- **Expected Response:**
    ```json
    {
        "res": "Invalid input",
        "error": true
    }
    ```
- **Status Code:** `400` BAD REQUEST
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with an invalid or malformed request body.
2. Verify that the response status code is 400 BAD Request.
3. Ensure that the response body contains an "error" field.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the system can properly handle requests with invalid or unrecognized input formats. When the request body contains an invalid value, such as a random string instead of a properly structured JSON object, the system should respond with an error indicating that the input is invalid.

---

### **Test Case 3**
- **Test ID:** TC03
- **Test Description:**  
If the request body is empty, the system should return an error message stating that the request is invalid due to the absence of a specified type. This test checks the system's robustness in handling incomplete or malformed requests.
- **Request Body:**
    ```json
    {}
    ```
- **Expected Response:**
    ```json
    {
        "res": "Oops, Invalid Type",
        "error": true
    }
    ```
- **Status Code:** `400` BAD REQUEST
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with an invalid or malformed request body.
2. Verify that the response status code is 400 BAD Request.
3. Ensure that the response body contains an "error" field.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the system can handle requests where the input is completely empty. When no type or any other required information is provided, the system should respond with a clear error message indicating that the request is invalid.

---

### **Test Case 4**
- **Test ID:** TC04
- **Test Description:**  
When the request is of type "gen", the system should automatically generate 3 multiple-choice questions (Default = 3) on a variety of topics. Each question should include the question text, multiple answer options, the correct answer, and a brief explanation of why that answer is correct.
- **Request Body:**
    ```json
    {
      "type": "gen"
    }
    ```
- **Example Expected Response:**  
    ```json
    {
        "res": "[{\"questionId\": 1, \"question\": \"What is the capital of France?\", \"options\": {\"A\": \"Berlin\", \"B\": \"Madrid\", \"C\": \"Paris\", \"D\": \"Lisbon\"}, \"answer\": \"C\", \"iscorrect\": true, \"reason\": \"The capital of France is indeed Paris.\"}, {\"questionId\": 2, \"question\": \"Which planet is known as the Red Planet?\", \"options\": {\"A\": \"Earth\", \"B\": \"Mars\", \"C\": \"Jupiter\", \"D\": \"Venus\"}, \"answer\": \"B\", \"iscorrect\": true, \"reason\": \"Mars is commonly known as the Red Planet.\"}, {\"questionId\": 3, \"question\": \"What is the largest mammal in the world?\", \"options\": {\"A\": \"Elephant\", \"B\": \"Blue Whale\", \"C\": \"Great White Shark\", \"D\": \"Giraffe\"}, \"answer\": \"B\", \"iscorrect\": true, \"reason\": \"The Blue Whale is the largest mammal in the world.\"}]"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the system can generate multiple-choice questions when the type is set to "gen" without any specific background information. It checks if the system can create relevant and correct questions based on general knowledge topics such as geography, astronomy, and biology, even when no extra context is provided.

---

### **Test Case 5**
- **Test ID:** TC05
- **Test Description:**  
The system should recognize that the input lacks content for summarization and respond with a message prompting the user to provide the content to be summarized. This ensures that the system gracefully handles incomplete or empty requests by providing clear instructions on what is required.
- **Request Body:**
    ```json
    {
      "type": "sumup"
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "{\"summary\": \"Please provide the specific content you want summarized, as the current content is not available.\"}"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the system can handle a sumup request where no specific content is provided. In this case, the system should ask for the necessary content to summarize, rather than attempting to generate a summary with no context.

---

### **Test Case 6**
- **Test ID:** TC06
- **Test Description:**  
The system should detect that the request is of type chat and respond appropriately with an introductory message asking what the user would like to talk about. This ensures the system can engage with the user in a conversational manner, even if no further details are provided in the request.
- **Request Body:**
    ```json
    {
      "type": "chat"
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "{\"response\": \"Sure! What would you like to ask or talk about? I'm here to help with any questions or topics you have in mind!\"}"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the system can correctly handle a basic chat request when the type is provided without additional context or background. The system should respond with a friendly, open-ended prompt, inviting the user to initiate a conversation.

---

### **Test Case 7**
- **Test ID:** TC07
- **Test Description:**  
The system should detect that "type": "sdfgib" is not a valid request type and respond accordingly with a clear error message. This ensures that the system validates input types and prevents processing of invalid data.
- **Request Body:**
    ```json
    {
      "type": "sdfgib"
    }
    ```
- **Expected Response:**
    ```json
    {
        "res": "Oops, Invalid Type",
        "error": true
    }
    ```
- **Status Code:** `400` BAD REQUEST
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with an invalid or malformed request body.
2. Verify that the response status code is 400 BAD Request.
3. Ensure that the response body contains an "error" field.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test checks if the system can correctly handle requests with an invalid or unrecognized type. When the provided type is not supported or does not match any predefined options, the system should return an error indicating that the request is invalid.

---

### **Test Case 8**
- **Test ID:** TC08
- **Test Description:**  
The system is expected to detect that the background contains arbitrary text that doesn’t align with any structured or expected input format, and it should respond with an error indicating that the request is invalid.
- **Request Body:**
    ```json
    {
      "type": "gen",
      "background": "Some random stuff Goes here from Mr. BOB"
    }
    ```
- **Expected Response:**
    ```json
    {
        "res": "Oops, BAD Request",
        "error": true
    }
    ```
- **Status Code:** `400` BAD REQUEST
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with an invalid or malformed request body.
2. Verify that the response status code is 400 BAD Request.
3. Ensure that the response body contains an "error" field.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test is designed to ensure that the system can handle and respond appropriately to invalid or nonsensical input in the background field. The input "Some random stuff Goes here from Mr. BOB" does not provide structured or meaningful information, so the system should identify it as an issue and return an appropriate error response.

---

### **Test Case 9**
- **Test ID:** TC09
- **Test Description:**  
Given an empty background, the system should still generate 3 multiple-choice questions (Default = 3) on general knowledge topics. The questions should be diverse, with a mix of categories, and the system should provide correct answers with explanations for each.
- **Request Body:**
    ```json
    {
      "type": "gen",
      "background": {}
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "[{\"questionId\": 1, \"question\": \"What is the capital of France?\", \"options\": {\"A\": \"Berlin\", \"B\": \"Madrid\", \"C\": \"Paris\", \"D\": \"Rome\"}, \"answer\": \"C\", \"iscorrect\": true, \"reason\": \"The capital of France is indeed Paris.\"}, {\"questionId\": 2, \"question\": \"Which planet is known as the Red Planet?\", \"options\": {\"A\": \"Earth\", \"B\": \"Mars\", \"C\": \"Jupiter\", \"D\": \"Saturn\"}, \"answer\": \"B\", \"iscorrect\": true, \"reason\": \"Mars is commonly referred to as the Red Planet.\"}, {\"questionId\": 3, \"question\": \"What is the largest mammal in the world?\", \"options\": {\"A\": \"Elephant\", \"B\": \"Blue Whale\", \"C\": \"Great White Shark\", \"D\": \"Giraffe\"}, \"answer\": \"B\", \"iscorrect\": true, \"reason\": \"The Blue Whale is the largest mammal in the world.\"}]"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the AI can generate general knowledge multiple-choice questions when provided with no specific background or context. It checks the system's ability to create valid and relevant questions across various subjects like geography, astronomy, and biology.

---

### **Test Case 10**
- **Test ID:** TC10
- **Test Description:**  
In this case, the system should generate 3 multiple-choice questions (Default = 3) on general knowledge topics, despite the lack of specific background information. The questions should cover various domains like geography, astronomy, and biology. The system should also provide the correct answer with reasoning for each question.
- **Request Body:**
    ```json
    {
      "type": "gen",
      "background": {
        "Some": "value",
        "N": 3
      }
    }
    ```
- **Expected Response:**  
    ```
    {
        "res": "[{\"questionId\": 1, \"question\": \"What is the capital of France?\", \"options\": {\"A\": \"Berlin\", \"B\": \"Madrid\", \"C\": \"Paris\", \"D\": \"Rome\"}, \"answer\": \"C\", \"iscorrect\": true, \"reason\": \"The capital of France is indeed Paris.\"}, {\"questionId\": 2, \"question\": \"Which planet is known as the Red Planet?\", \"options\": {\"A\": \"Earth\", \"B\": \"Mars\", \"C\": \"Jupiter\", \"D\": \"Venus\"}, \"answer\": \"B\", \"iscorrect\": true, \"reason\": \"Mars is commonly referred to as the Red Planet due to its reddish appearance.\"}, {\"questionId\": 3, \"question\": \"What is the largest mammal in the world?\", \"options\": {\"A\": \"Elephant\", \"B\": \"Blue Whale\", \"C\": \"Giraffe\", \"D\": \"Great White Shark\"}, \"answer\": \"B\", \"iscorrect\": true, \"reason\": \"The Blue Whale is the largest mammal in the world.\"}]"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test verifies that the system can generate multiple-choice questions based on arbitrary or incomplete context. Even though the request does not specify a clear topic or content (with "Some": "value"), the system should be capable of generating general knowledge questions that are appropriate and relevant, demonstrating flexibility in handling such inputs.

---

### **Test Case 11**
- **Test ID:** TC11
- **Test Description:**  
The system is expected to generate (Default = 3) 3 multiple-choice questions based on the content typically covered in Week 1 of a Python course, such as displaying text, using data types, and understanding variables. The AI should include the correct answer, options, and a brief explanation for each question.
- **Request Body:**
    ```json
    {
      "type": "gen",
      "prompt": "",
      "background": {
        "week": "Week 1"
      }
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "[{\"questionId\": 1, \"question\": \"What is the basic command used to display text in Python?\", \"options\": {\"A\": \"display\", \"B\": \"show\", \"C\": \"print\", \"D\": \"output\"}, \"answer\": \"C\", \"iscorrect\": true, \"reason\": \"The correct command to display text in Python is 'print', which corresponds to option C.\"}, {\"questionId\": 2, \"question\": \"Which data type is used for decimal numbers in Python?\", \"options\": {\"A\": \"int\", \"B\": \"str\", \"C\": \"float\", \"D\": \"bool\"}, \"answer\": \"C\", \"iscorrect\": true, \"reason\": \"The data type used for decimal numbers in Python is 'float', which corresponds to option C.\"}, {\"questionId\": 3, \"question\": \"What is the purpose of using variables in programming?\", \"options\": {\"A\": \"To store constant values\", \"B\": \"To store changeable values\", \"C\": \"To create errors\", \"D\": \"To display output\"}, \"answer\": \"B\", \"iscorrect\": true, \"reason\": \"Variables are used to store changeable values in programming, which corresponds to option B.\"}]"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the system can generate relevant multiple-choice questions based on the Week 1 programming course content, focusing on Python basics. The questions should assess understanding of key concepts, such as commands, data types, and variables, which are essential for beginners.

---

### **Test Case 12**
- **Test ID:** TC12
- **Test Description:**  
The AI should generate 4 multiple-choice questions that assess the learner's understanding of the basic Python concepts covered in Week 1, such as programming language, commands, data types, and operators. Each question should have options, an answer, and a brief explanation of why the answer is correct.
- **Request Body:**
    ```json
    {
        "type": "gen",
        "prompt": "",
        "background": {
            "week": "Week 1",
            "N": 4
        }
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "[{\"questionId\": 1, \"question\": \"What is the main programming language focused on in the tutorial?\", \"options\": {\"A\": \"Java\", \"B\": \"C++\", \"C\": \"Python\", \"D\": \"Ruby\"}, \"answer\": \"C\", \"iscorrect\": true, \"reason\": \"The main programming language focused on in the tutorial is Python, which corresponds to option C.\"}, {\"questionId\": 2, \"question\": \"What is the basic command used to display text on the screen in Python?\", \"options\": {\"A\": \"output\", \"B\": \"echo\", \"C\": \"print\", \"D\": \"show\"}, \"answer\": \"C\", \"iscorrect\": true, \"reason\": \"The basic command used to display text on the screen in Python is 'print', which corresponds to option C.\"}, {\"questionId\": 3, \"question\": \"Which data type is used for decimal numbers in Python?\", \"options\": {\"A\": \"String\", \"B\": \"Integer\", \"C\": \"Float\", \"D\": \"Boolean\"}, \"answer\": \"C\", \"iscorrect\": true, \"reason\": \"The data type used for decimal numbers in Python is 'Float', which corresponds to option C.\"}, {\"questionId\": 4, \"question\": \"What operator is used for concatenating strings in Python?\", \"options\": {\"A\": \"+\", \"B\": \"*\", \"C\": \"&\", \"D\": \"#\"}, \"answer\": \"A\", \"iscorrect\": true, \"reason\": \"The operator used for concatenating strings in Python is '+', which corresponds to option A.\"}]"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test checks the AI's ability to generate multiple-choice questions based on the course content for Week 1, which is likely focused on Python basics. It ensures the AI can create questions relevant to the topic and validate the correct answers with appropriate reasoning.

---



### **Test Case 13**
- **Test ID:** TC13
- **Test Description:**  
The AI is expected to generate a concise summary that covers the essential topics introduced in Week 1, such as basic Python commands, variables, and data types, while remaining easy to understand for beginners.
- **Request Body:**
    ```json
    {
        "type": "sumup",
        "prompt": "",
        "background": {
            "week": "Week 1"
        }
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "{\"summary\": \"Programming is like learning a new language to communicate with computers, and Python is a great choice because it's popular and easy to learn. In just a few hours, you can start coding. This course will teach you step by step, just like learning to drive a car requires practice. You'll begin by writing simple programs on Replit.com, using the 'print' command to display messages. You can create patterns and learn about commands and common mistakes.\\n\\nYou'll also learn about variables, which are like containers for storing values. You can change what's in a variable and perform math with them. Users can input numbers, which you can use in your programs. We cover data types like integers, floats, and strings, and how to convert between them.\\n\\nYou\\u2019ll understand operators for calculations and comparisons, and how to work with strings, including slicing and replicating them. It's important to remember that errors are part of learning to code, and with practice, you'll get better. Keep coding, ask questions, and enjoy the process!\"}"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test checks the AI's ability to summarize Week 1 of a programming course, ensuring it can convey the basic concepts of Python in a simple, beginner-friendly manner. The summary should focus on key topics like using print, working with variables, and understanding data types.

---

### **Test Case 14**
- **Test ID:** TC14
- **Test Description:**  
In this test, the background includes "week": "Week 100", which is likely outside the valid range of weeks in the system. The AI should not try to generate a summary based on this invalid input. Instead, it should inform the user that the content to summarize cannot be determined due to the unrecognized or invalid week number.

The system should respond by prompting the user to provide valid or specific content to summarize.
- **Request Body:**
    ```json
    {
        "type": "sumup",
        "prompt": "",
        "background": {
            "week": "Week 100"
        }
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "{\"summary\": \"Please provide the content you want summarized.\"}"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the system handles cases where the week provided is invalid or not recognized (in this case, "Week 100"). It is important for the system to gracefully handle such requests by informing the user that the requested content cannot be processed. This test verifies the system's ability to handle invalid or out-of-bounds data and respond with an appropriate message asking the user to provide valid input.

---

### **Test Case 15**
- **Test ID:** TC15
- **Test Description:**  
In this test, the request has an empty "background" field, meaning there is no context for the AI to summarize. The system should recognize that it cannot generate a summary without any provided content and respond with a prompt asking the user to provide specific content to summarize.
- **Request Body:**
    ```json
    {
        "type": "sumup",
        "prompt": "",
        "background": {}
    }
    ```
- **Expected Response:**  
  ```json
    {
        "res": "{\"summary\": \"Please provide the specific content you want summarized.\"}"
    }
  ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the system correctly handles a situation where no background information or context is provided. The AI needs to recognize that without specific content to summarize, it cannot generate a useful summary. This test verifies that the system is capable of gracefully handling empty or incomplete requests by prompting the user for the necessary information.

---

### **Test Case 16**
- **Test ID:** TC16
- **Test Description:**  
The system needs to generate a summary for a programming course, while addressing a prompt that asks for a metaphorical perspective. The content should be relatable and clear for beginners, emphasizing Python and programming basics.
- **Request Body:**
    ```json
    {
        "type": "sumup",
        "prompt": "In terms of a childs dream",
        "background": {
            "week": "Week 1"
        }
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "{\"summary\": \"Programming is like learning a new language to talk to computers, and Python is a popular choice because it's easy to learn. In this course, you'll start coding quickly, learning step by step, just like learning to drive a car requires practice. You'll use a platform called Replit to write your first programs, starting with simple commands like 'print' to display text. You'll also learn how to create patterns, use variables to store values, and perform basic math with them.\\n\\nYou'll explore data types (like integers and strings), how to convert between them, and how to use operators for calculations and comparisons. You'll also learn about strings, including how to manipulate and access parts of them, and how to handle errors. Remember, practice is key in coding, and making mistakes is just part of the learning process. Keep coding, and you'll get better!\"}"
    }
  ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test evaluates the AI's ability to generate a relevant and clear summary based on a metaphorical prompt (Eg. "In terms of a child's dream"). The test ensures that the system can interpret abstract language and still produce an accurate, beginner-friendly summary of the Week 1 content in a programming course, specifically related to Python.

---

### **Test Case 17**
- **Test ID:** TC17
- **Test Description:**  
The test checks the system's behavior when a user requests a summary for a lecture that does not exist in the database or knowledge base. In this scenario, the system is asked to return a summary of "Lecture 1.1 Random Lec," but since this lecture is not found, the system should return an error message indicating it cannot fulfill the request. This helps to ensure that the system doesn't crash or behave unpredictably when faced with missing or invalid data.
- **Request Body:**
    ```json
    {
        "type": "sumup",
        "prompt": "",
        "background": {
            "week": "Week 1",
            "lecture": "Lecture 1.1 Random Lec"
        }
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "Internal Server Error",
        "error": true
    }
    ```
- **Status Code:** `500` INTERNAL SERVER ERROR
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with an invalid or malformed request body.
2. Verify that the response status code is 500 INTERNAL SERVER ERROR.
3. Ensure that the response body contains an "error" field.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**
This test ensures that the system correctly handles requests for non-existent or invalid data. In this case, the user is asking for a summary of a lecture ("Lecture 1.1 Random Lec") that doesn't exist in the system. The goal of this test is to verify that the system appropriately returns an error response (like an Internal Server Error) when it cannot find the requested resource. This is crucial for maintaining robustness in the system, ensuring that invalid queries are gracefully handled, and that users are informed when their requests cannot be processed.

---

### **Test Case 18**
- **Test ID:** TC18
- **Test Description:**  
In this case, the "sumup" request type requires the AI to summarize the core concept of the lecture titled "L2.8: Introduction to the if statement." The model is expected to use the provided background (i.e., the topic of the lecture) and generate a response that explains the concepts from that lecture in a simple, illustrative manner. The response should include an example that demonstrates how the "if statement" works, making the concept clear for someone unfamiliar with it.
- **Request Body:**
    ```json
    {
        "type": "sumup",
        "prompt": "",
        "background": {
            "week": "Week 1",
            "lecture": "L2.8: Introduction to the if statement"
        }
    }
    ```
- **Expected Response:**  
    ```json
    {
        "res": "{\"summary\": \"The 'if statement' in programming helps you make decisions in your code. For example, to check if someone can watch the movie Avengers (which is for ages 13 and older), you can:\\n1. Ask for their birth year.\\n2. Calculate their age by subtracting their birth year from the current year (2021).\\n3. Use an 'if statement' to see if they are under 13:\\n   - If they are under 13, say \\\"You cannot watch this movie.\\\"\\n   - If they are 13 or older, say \\\"You can watch Avengers, enjoy!\\\"\\n4. Finally, say \\\"Have a nice time!\\\" regardless of their age.\\n\\nThis shows how 'if statements' work by checking conditions and choosing different actions based on those conditions.\"}"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test is designed to evaluate the AI’s ability to provide a concise, clear, and accurate summary of a specific topic based on a given lecture or lesson. In this case, the lecture is focused on the "if statement," a core concept in programming. The test assesses whether the AI can distill the information into a digestible summary, highlighting the key points and offering an example to make the concept more relatable and understandable.

---

### **Test Case 19**
- **Test ID:** TC19
- **Test Description:**  
The request contains a simple, straightforward question: "What is Python used for?" The AI needs to identify the major applications of Python and explain them in a clear and engaging way. The model should offer examples, mention relevant libraries or frameworks, and include questions that guide the user towards a specific area of interest for further exploration. This response should provide an introduction to Python’s versatility and serve as a foundation for the conversation to evolve.
- **Request Body:**
    ```json
    {
        "type": "chat",
        "prompt": "What is python used for ?"
    }
    ```
- **Expected Response:**
    ```json
    {
        "res": "{\"response\": \"Python is a versatile programming language that is used for a variety of applications! To help you understand better, let\\u2019s break this down into a few key areas:\\n\\n1. **Web Development**: Python is often used to build server-side web applications. Have you heard of frameworks like Django or Flask? They can make web development easier and more efficient.\\n\\n2. **Data Science and Analysis**: It's popular in data analysis and machine learning because of libraries like Pandas, NumPy, and Scikit-learn. Are you interested in learning how these libraries can help analyze data?\\n\\n3. **Automation and Scripting**: Python is great for writing scripts to automate mundane tasks. Can you think of any repetitive tasks you\\u2019d like to automate?\\n\\n4. **Game Development**: Believe it or not, Python can also be used for game development! Have you ever tried making a simple game using libraries like Pygame?\\n\\n5. **Artificial Intelligence**: Python is heavily used in AI and machine learning projects. What aspects of AI interest you the most?\\n\\nAs you can see, Python has a wide range of applications. Which area are you most curious about?\"}"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test ensures that the AI responds accurately to a direct, open-ended query about the uses of Python. The prompt asks for the general use cases of Python, and the expected response should break down the various areas where Python is applied. By evaluating the response, we can verify that the model can provide a detailed, structured, and engaging answer that covers several key areas, and also encourages further exploration based on the user's interest.

---

### **Test Case 20**
- **Test ID:** TC20
- **Test Description:**  
In this case, the "background" section is empty, which means the system has no prior context to work with. The AI must infer the user's intent from the prompt ("Okay, so can you tell me a little bit more about it and next concepts?") and respond in a way that begins or continues the conversation smoothly. Since the background is absent, the model should provide an introduction or clarification, followed by a general response that could lead to further exploration.
- **Request Body:**
    ```json
    {
        "type": "chat",
        "prompt": "Okay so Can you tell me little bit more about it and next concepts",
        "background": {
            "conversation": []
        }
    }
    ```
- **Expected Response:**
    ```json
    {
        "res": "{\"response\": \"Sure! It sounds like you're looking to dive deeper into a specific topic. What concept are you referring to? Once I know that, I can break it down for you and introduce some related ideas that might build on your understanding. What do you already know about it, and what specific aspects are you curious about?\"}"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test is designed to evaluate the AI's ability to handle an initial query with no prior conversation context. The goal is to assess whether the AI can respond effectively and introduce relevant information when no conversation history is provided. It helps to ensure that the model can initiate and manage a new conversation based on a general prompt, guiding the conversation towards the appropriate direction.

---

### **Test Case 21**
- **Test ID:** TC21
- **Test Description:**  
The test examines how well the system handles a request where the user has an ongoing conversation with the AI. The goal is to ensure that the model can refer to the background (previous exchanges) and produce a relevant and coherent answer in response to a new prompt.

In this specific test, the user is asking for more information about concepts they previously discussed (in this case, Python data types). The system should be able to use the conversation history to understand the context and provide the requested information.
- **Request Body:**
    ```json
    {
        "type": "chat",
        "prompt": "Okay so Can you tell me little bit more about it and next concepts",
        "background": {
            "conversation": [
                [
                    "User",
                    "Hi"
                ],
                [
                    "AI",
                    "Hi, How can I help you"
                ],
                [
                    "User",
                    "Can you tell me what Python exactly is"
                ],
                [
                    "AI",
                    "Okay, so Python is a high-level, interpreted programming language known for its easy-to-read syntax. Its used for various applications, including web development, data analysis, artificial intelligence, machine learning, automation, and more. Python is versatile and has a large community and vast library support."
                ],
                [
                    "User",
                    "Okay, so how many data types are in Python"
                ],
                [
                    "AI",
                    "Python has several built-in data types. The basic ones include:\n1. **int** (integer) - For whole numbers\n2. **float** (floating point) - For decimal numbers\n3. **str** (string) - For text\n4. **bool** (boolean) - For True or False values\n5. **list** - An ordered collection of items\n6. **tuple** - An ordered, immutable collection of items\n7. **set** - An unordered collection of unique items\n8. **dict** (dictionary) - A collection of key-value pairs\n\nAdditionally, Python allows the creation of custom data types using classes."
                ]
            ]
        }
    }
    ```
- **Expected Response:**
    ```json
    {
        "res": "{\"response\": \"AI: Absolutely! Let's delve a bit deeper into each of those data types:\\n\\n1. **int**: Integers can be positive or negative whole numbers. You can perform arithmetic operations like addition, subtraction, multiplication, and division using integers.\\n   - **Example**: `x = 5` or `y = -3`\\n\\n2. **float**: Floats are numbers that have decimal points. They are useful when precision is important, such as in financial calculations.\\n   - **Example**: `price = 19.99` or `temperature = 36.6`\\n\\n3. **str**: Strings are sequences of characters. They're used for storing text and can include letters, numbers, and symbols. You can manipulate strings in various ways, such as concatenating them or finding their length.\\n   - **Example**: `name = \\\"Alice\\\"`\\n\\n4. **bool**: Booleans represent truth values, which can be either `True` or `False`. They're commonly used in conditional statements and loops.\\n   - **Example**: `is_active = True`\\n\\n5. **list**: Lists are ordered collections that can hold items of different data types. You can add, remove, or change items in a list.\\n   - **Example**: `fruits = [\\\"apple\\\", \\\"banana\\\", \\\"cherry\\\"]`\\n\\n6. **tuple**: Tuples are similar to lists but are immutable, meaning their values cannot be changed after they are created. They're useful for fixed collections of items.\\n   - **Example**: `coordinates = (10, 20)`\\n\\n7. **set**: Sets are collections of unique items. They are unordered and do not allow duplicate values, which makes them useful for membership tests.\\n   - **Example**: `unique_numbers = {1, 2, 3}`\\n\\n8. **dict**: Dictionaries store data in key-value pairs. They allow you to quickly access values based on their keys, making them very versatile for representing structured data.\\n   - **Example**: `person = {\\\"name\\\": \\\"John\\\", \\\"age\\\": 30}`\\n\\nNow, if you're interested in what comes next, you might want to explore concepts like:\\n- **Control Structures**: Such as `if` statements, loops (like `for` and `while`), which help you control the flow of your program.\\n- **Functions**: These allow you to encapsulate code into reusable blocks.\\n- **Modules and Libraries**: To organize your code and utilize existing codebases.\\n- **Object-Oriented Programming**: To create custom data types and models using classes.\\n\\nDoes any particular area sound interesting to you, or would you like to dive deeper into one of these concepts?\"}"
    }
    ```
- **Status Code:** `200` OK
- **Test Execution Steps:**
1. Send a POST request to the /api/ai endpoint with a valid request body.
2. Verify that the response status code is 200 OK.
3. Ensure that the response body does not contain any "error" field or message.
- **Test Outcome:** `PASS`
- **Why This Test is Important:**  
This test is designed to assess the ability of AI to understand and respond appropriately based on prior conversation history. By providing a "background" with a series of exchanges between the user and AI, the system needs to recognize the context of the conversation, recall previous topics, and offer relevant, coherent responses to subsequent user queries. It evaluates the model’s capacity to maintain context and continuity in a multi-turn conversation.

---
