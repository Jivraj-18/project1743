// const SINELAB = "https://vigilant-computing-machine-x449gvr5qp7h6vqp-5000.app.github.dev/api/ai"
const SINELAB = "http://localhost:5000/api/ai"


async function scrab(s) {
    
    s = s
    
    var b = new Promise((f,r) => {
        fetch(SINELAB, {
            method: "POST",
            headers: {
              "Content-Type": "application/json" 
            },
            body: JSON.stringify(s)
        })
        .then(a => a.json())
        .then(a => f(a))
        .catch(e => {
            alert("Error in AI Part")
            f(false)
        })
    })

    return b

}


async function chat(s) {

    s = s

    var res = await scrab({
        type: "chat",
        prompt: s.prompt,
        background: {
            "week": "Week 1",
            "lecture": "Lecture 1.1",
            "conversation" : s.conversation 
        }
    })
    
    console.log("AI Res : ", JSON.parse(res.res).response, s)

    var b = new Promise((f,r) => {
        f(JSON.parse(res.res).response)
    })

    return b

}


async function gen(s) {
    

    // JSON.stringify({
    //         type: "gen",     
    //         prompt: "",
    //         background: {
    //             "week" : "Week 1",
    //             "lecture" : "Lecture 1.1"
    //         }
    //     })
    // })



    var res = await scrab({
        type: "gen",
        prompt: "",
        background: s
    })


    console.log("Gen Ques : ", JSON.parse(res.res))


    s = s
    var b = new Promise((f,r) => {
        f(JSON.parse(res.res))
    })

    return b

}


async function sumup(s) {

    var b = {
        type: "sumup",     
        prompt: s.prompt ? s.prompt : "",
        background: {
            // "week" : "Week 1",
            "lecture" : s.lecture,
            "pre" : s.pre ? true : false
        }
    }

    return new Promise((f,r) => {
        fetch(SINELAB, {
            method: "POST",
            headers: {
                "Content-Type": "application/json" 
            },
            body: JSON.stringify(b)
        })
        .then(response => response.json())  // Parse JSON response
        .then(data => {
            console.log('Success:', data);
            f(JSON.parse(data.res))
        })
        .catch(error => {
            console.error('Error:', error);
        });
    })

}


const sb = { gen, sumup, chat}
export {sb}