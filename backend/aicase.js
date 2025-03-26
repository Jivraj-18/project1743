cases = [
    ["", false],
    ["suifdghb", false],
    [{}, false],
    [{"type": "gen"}, true],
    [{"type": "sumup"}, true],
    [{"type": "chat"}, true],
    [{"type": "sdfgib"}, false],
    [{
        "type": "gen",
        "background" : "Some random stuff Goes here from Mr. BOB"
    }, false],
    [{
        "type": "gen",
        "background" : {}
    }, true],
    [{
        "type": "gen",
        "background" : {
            "Some" : "value",
            "N" : 3
        }
    }, true],
    [{
        "type": "gen",
        "prompt": "",
        "background": {
            "week": "Week 1"
        }
    }, true],
    [{
        "type": "gen",
        "prompt": "",
        "background": {
            "week": "Week 1",
            "N" : 4
        }
    }, true],

    [{
        "type": "sumup",     
        "prompt": "",
        "background": {
            "week" : "Week 1"
        }
    }, true],

    [{
            "type": "sumup",
            "prompt": "",
            "background": {
                "week" : "Week 100"
            }
    }, true],

    [{
        "type": "sumup",
        "prompt": "",
        "background": {
            // "week" : "Week 100"
        }
    }, true],

    [{
        "type": "sumup",
        "prompt": "In terms of a childs dream",
        "background": {
            "week" : "Week 1"
        }
    }, true],

    [{
        "type": "sumup",     
        "prompt": "",
        "background": {
        "week": "Week 1",
        "lecture": "Lecture 1.1 Random Lec"
    }
  }, false],
    [{
        "type": "sumup",
        "prompt": "",
        "background": {
        "week": "Week 1",
        "lecture": "L2.8: Introduction to the if statement"
    }
  }, true],

  [{
    "type": "chat",
    "prompt": "What is python used for ?",
  }, true],

  [{
    "type": "chat",     
    "prompt": "Okay so Can you tell me little bit more about it and next concepts",
    "background": {
        "conversation" : [] 
    }
  }, true],
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
  }, true],


]



for (var i = 0; i < cases.length; i++){
    await fetch("/api/ai", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: JSON.stringify(cases[i][0])
    })
    .then(a => a.json())
    .then(a => console.log(i, cases[i][1] == (a.error ? false : true) ? "PASS" : "FAIL",a))
}

