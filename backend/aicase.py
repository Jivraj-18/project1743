import pytest
import requests
import json


cases = [
    ["", False, 400],
    ["suifdghb", False, 400],
    [{}, False, 400],
    [{"type": "gen"}, True, 200],
    [{"type": "sumup"}, True, 200],
    [{"type": "chat"}, True, 200],
    [{"type": "sdfgib"}, False, 400],
    [{
        "type": "gen",
        "background" : "Some random stuff Goes here from Mr. BOB"
    }, False, 400],
    [{
        "type": "gen",
        "background" : {}
    }, True, 200],
    [{
        "type": "gen",
        "background" : {
            "Some" : "value",
            "N" : 3
        }
    }, True, 200],
    [{
        "type": "gen",
        "prompt": "",
        "background": {
            "week": "Week 1"
        }
    }, True, 200],
    [{
        "type": "gen",
        "prompt": "",
        "background": {
            "week": "Week 1",
            "N" : 4
        }
    }, True, 200],

    [{
        "type": "sumup",
        "prompt": "",
        "background": {
            "week" : "Week 1"
        }
    }, True, 200],

    [{
            "type": "sumup",
            "prompt": "",
            "background": {}
    }, True, 200],

    [{
        "type": "sumup",
        "prompt": "",
        "background": {
            "week" : "Week 100"
        }
    }, True, 200],

    [{
        "type": "sumup",
        "prompt": "In terms of a childs dream",
        "background": {
            "week" : "Week 1"
        }
    }, True, 200],

    [{
        "type": "sumup",     
        "prompt": "",
        "background": {
        "week": "Week 1",
        "lecture": "Lecture 1.1 Random Lec"
    }
  }, False, 500],
    [{
        "type": "sumup",
        "prompt": "",
        "background": {
        "week": "Week 1",
        "lecture": "L2.8: Introduction to the if statement"
    }
  }, True, 200],

  [{
    "type": "chat",
    "prompt": "What is python used for ?",
  }, True, 200],

  [{
    "type": "chat",     
    "prompt": "Okay so Can you tell me little bit more about it and next concepts",
    "background": {
        "conversation" : [] 
    }
  }, True, 200],
  [{
    "type": "chat",     
    "prompt": "Okay so Can you tell me little bit more about it and next concepts",
    "background": {
        "conversation" : [
            ["User", "Hi"],
            ["AI", "Hi, How can I help you"],
            ["User", "Can you tell me what Python exactly is"],
            ["AI", "Okay, so Python is a high-level, interpreted programming language known for its easy-to-read syntax. Its used for various applications, including web development, data analysis, artificial intelligence, machine learning, automation, and more. Python is versatile and has a large community and vast library support."],
            ["User", "Okay, so how many data types are in Python"],
            ["AI", "Python has several built-in data types. The basic ones include:\n1. **int** (integer) - For whole numbers\n2. **float** (floating point) - For decimal numbers\n3. **str** (string) - For text\n4. **bool** (boolean) - For True or False values\n5. **list** - An ordered collection of items\n6. **tuple** - An ordered, immutable collection of items\n7. **set** - An unordered collection of unique items\n8. **dict** (dictionary) - A collection of key-value pairs\n\nAdditionally, Python allows the creation of custom data types using classes."]
        ] 
    }
  }, True, 200],


]


# API endpoint
API_URL = "http://localhost:5000/api/ai"  # Change this to your API endpoint


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