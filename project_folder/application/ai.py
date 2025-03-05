import base64
import requests
import json

from .rag import query_selector

chatChecker = """

The AI response should adapt to the type of user query according to the following categories:

Asking for a Solution:
The AI should never provide a direct solution to the user's problem.
Instead, the AI should guide the user step-by-step, offering hints, encouragement, and strategies that help them explore the solution on their own.
Encourage critical thinking by breaking down the problem and asking questions that prompt the user to think through the process themselves.
Maintain a supportive and patient tone. If the user is stuck, provide additional clues or suggestions to keep them moving forward.
Example: If a user asks for a solution to a coding problem, avoid writing the code directly but suggest the next logical steps in the problem-solving process.
Asking for an Explanation:
The AI should not give a direct, overly simplified answer but instead provide a thorough and clear explanation in a way that deepens the user's understanding.
Make sure the explanation is tailored to the user's current level of understanding and ask guiding questions if needed to ensure clarity.
Break down complex ideas into digestible pieces and use analogies or examples to help illustrate points.
Example: If the user asks how a concept works, the AI should explain it in depth and provide real-world applications or examples.
Motivation:
The AI should respond with encouraging, positive, and uplifting messages that help the user feel confident and motivated.
Avoid sounding generic or condescending. Personalize the response when possible to the user's current situation and context.
Example: If a user feels overwhelmed, remind them of past successes, how challenges are opportunities for growth, and that they are capable of overcoming difficulties.
Asking to Analyze:
The AI should help the user analyze the situation or problem carefully by posing thoughtful questions and encouraging them to think critically.
Instead of simply offering conclusions, the AI should suggest ways to break down the problem and point out areas for deeper investigation or reflection.
Ensure that the analysis helps the user think about multiple perspectives and encourages them to reach their own conclusions.
Example: If the user asks for an analysis of a situation, guide them by asking them to consider different aspects and viewpoints to form their own conclusions.
General Chat:
For casual or off-topic conversations, the AI can respond naturally, keeping the tone friendly, light, and engaging.
This type of conversation should flow like a normal chat, maintaining a balance between being informative and conversational.
Example: If the user asks a general question like “What's your favorite color?”, feel free to engage without overcomplicating the answer.

"""


class INK:
    def __init__(self, s: str):
        self.s = s

    def scrab(self, data):
        s = data
        b = {}


        url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.s}"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            b = response.json()
        else:
            b = {"error": f"Request failed with status code {response.status_code} with proxy hub"}

        return b

    def summarize(self, data):
        s = data
        b = {}

        ptp = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a expert content summarizer. Your task is to simplify the given content so that a student can understand it easily."
                },
                {
                    "role": "user",
                    "content": f"Query: {s['prompt']}"
                },
                {
                    "role": "user",
                    "content": f"Content: {s['content']}"
                }
            ],
            "temperature": 0.7,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                "name": "sumup",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"}
                    },
                    "required": ["summary"],
                    "additionalProperties": False,
                },
            },
            }
        }

        b = json.loads(self.scrab(ptp)['choices'][0]['message']['content'])
        
        return b

    def generate_questions(self, data):
        s = data
        b = {}

        ptp = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                "role": "system",
                "content": "You are a question generation assistant. Your task is to produce exactly N questions based on the topic and detailed scope provided by the user. Each question must be concise and stay within the subject boundaries defined. Do not output any extra text—only a JSON object as specified in the schema."
                },
                {
                    "role": "user",
                    "content": f"Query: {s['prompt']}"
                },
                {
                    "role": "user",
                    "content": f"Content: {s['content']}"
                }
            ],
            "temperature": 0.7,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                "name": "MCQSchema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "questions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "questionId" : {"type": "integer"},
                                    "question": {"type": "string"},
                                    "options": {
                                        "type": "object",
                                        "properties" : {
                                            "A" : {"type": "string"},
                                            "B" : {"type": "string"},
                                            "C" : {"type": "string"},
                                            "D" : {"type": "string"},
                                        },
                                        "required": ["A", "B", "C", "D"], 
                                    },
                                    "answer": {"type": "string"}
                                },
                                "required": ["questionId", "question", "options", "answer"]
                            },
                        }
                    },
                    "required": ["questions"]
                    
                }
                }
            }
        }

        dat = json.loads(self.scrab(ptp)['choices'][0]['message']['content'])
        ques = dat['questions']


        ptp = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                "role": "system",
                "content": "You are a question solving assistant. Your task is to check the question and its answer and tell me is that answer mentioned is correct answer of the question or not with a reason"
                },
                {
                    "role": "user",
                    "content": f"Questions: {ques}"
                },
            ],
            "temperature": 0.3,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                "name": "MCQSchema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "questions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "questionId": {"type": "integer"},
                                    "iscorrect" : {"type" : "boolean"},
                                    "reason": {"type": "string"}
                                },
                                "required": ["questionId", "iscorrect", "reason"]
                            },
                        }
                    },
                    "required": ["questions"]
                    
                }
                }
            }
        }


        dat = json.loads(self.scrab(ptp)['choices'][0]['message']['content'])
        checked = dat['questions']

        for question in ques:
            matching_item = next((item for item in checked if item['questionId'] == question['questionId']), None)
            if matching_item:
                question['iscorrect'] = matching_item['iscorrect']
                question['reason'] = matching_item['reason']

        print(ques)


        for question_data in ques:
            print(f"Question: {question_data['question']}\n")
            
            for option, answer in question_data['options'].items():
                if option == question_data['answer']:
                    print(f"\033[32m{option}. {answer}\033[0m")  # Correct answer in green
                else:
                    print(f"{option}. {answer}")  # Other options in default color
            
            print()

        b = ques
        return b

    def chat(self, data):
        s = data
        b = {}

        # We Need to Use RAG here to check the Documents Involved.

        ptp = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": f"{chatChecker}"
                },
                {
                    "role": "user",
                    "content": f"{s['content']}"
                },
                {
                    "role": "user",
                    "content": f"Query: {s['prompt']}"
                }
            ],
            "temperature": 0.7,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                "name": "response",
                    "schema": {
                        "$schema": "http://json-schema.org/draft-04/schema#",
                        "title": "Model",
                        "type": "object",
                        "properties": {
                            "response" : {"type": "string"}
                        }
                    }
                }
            }
        }

        dat = json.loads(self.scrab(ptp)['choices'][0]['message']['content'])
        b = dat
        
        b = dat
        return b

    def surprise_features(self, data):
        b = {}
        return b

ink = INK("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDA2MDVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.3Obdi1LKmdOki-kPPdF_QtPlcNA-5opr6Txsv5Vccho")
