class Session:
    def __init__(self, user):
        self.user = user

    def login(self):
        print(f'{self.user} logged in.')

    def action_log(self):
        print(f'Action log for {self.user}.')

    def logout(self):
        print(f'{self.user} logged out.')

class Role:
    def check_role(self, user):
        if isinstance(user, Student):
            return 'Student role verified'
        elif isinstance(user, TA):
            return 'TA role verified'
        elif isinstance(user, Instructor):
            return 'Instructor role verified'
        else:
            return 'Role verification failed'

class TA:
    def __init__(self, name):
        self.name = name

    def upload_resources(self):
        print(f'{self.name} uploaded resources.')

    def todo(self):
        print(f'{self.name} is managing to-do.')

    def view_issues(self):
        print(f'{self.name} is viewing issues.')


class Student:
    def __init__(self, name):
        self.name = name
        self.course = None

    def view_profile(self):
        print(f'{self.name} is viewing profile.')

    def view_announcements(self):
        print(f'{self.name} is viewing announcements.')

    def todo(self):
        print(f'{self.name} is managing to-do.')

    def mycourses(self):
        print("")

    def view_content(self):
        print(f'{self.name} is viewing course content.')

    def view_assignment(self):
        print(f'{self.name} is viewing assignments.')

    def submit_assignment(self):
        print(f'{self.name} is submitting assignments.')

    def view_marks(self):
        print(f'{self.name} is viewing marks.')


    def chat_with_ai(self):
        print(f'{self.name} is chatting with AI.')

    def summarize_with_ai(self):
        print(f'{self.name} is summarizing content with AI.')

    def revise_week_with_ai(self):
        print(f'{self.name} is revising week content with AI.')

    def solve_with_ai(self):
        print(f'{self.name} is solving assignments with AI.')

    def bookmark_Ques(self):
        print(f'{self.name} saved bookmarked questions.')

    def analyze_with_ai(self):
        print(f'{self.name} is analyzing mistakes.')

    def report_issues(self):
        print(f'{self.name} is reporting issues.')



class Instructor:
    def __init__(self, name):
        self.name = name

    def upload_resources(self):
        print(f'{self.name} uploaded resources.')

    def modify_resources(self):
        print(f'{self.name} edited resources.')

    def todo(self):
        print(f'{self.name} is managing to-do.')

    def view_stats(self):
        print(f'{self.name} is viewing statistics.')

    def manage_issues(self):
        print(f'{self.name} is managing issues.')

    def add_event(self):
        print(f'{self.name} added an event.')

    def assign_tasks(self):
        print()

    def generate_questions(self):
        print(f'{self.name} generated questions.')

    def modify_questions(self):
        print(f'{self.name} modified questions.')



class GenAI:
    def __init__(self, s: str):
        self.s = s
        self.b = []

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

        response = self.scrab("what")
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
                "content": f"Topic: {s['topic']}\nScope: {s['scope']}\nNumber of Questions: {s['N']}"
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
                            "question": {
                            "type": "string",
                            "description": "The text of the multiple-choice question."
                            },
                            "options": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "A possible answer option for the question."
                            },
                            "minItems": 4,
                            "maxItems": 4,
                            "description": "A list of four answer options."
                            },
                            "answer": {
                            "type": "string",
                            "description": "The correct answer to the question."
                            }
                        },
                        "required": ["question", "options", "answer"],
                        "description": "An individual multiple-choice question with its options and correct answer."
                        },
                        "minItems": 3,
                        "maxItems": 10,
                        "description": "A list of multiple-choice questions."
                    }
                    },
                    "required": ["questions"],
                    "description": "A structured response containing a list of multiple-choice questions."
                }
                }
            }
        }

        ques = json.loads(self.scrab(ptp)['choices'][0]['message']['content'])['questions']

        c = 0
        dd = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for i in ques:
            c += 1
            d = 0
            print(f"Q{c}. {i['question']}")
            for j in i['options']:
                if j == i['answer']:
                    print(f"\033[32m {dd[d]}. {i['answer']}\033[0m")
                else:
                    print(f" {dd[d]}. {j}")
                d += 1
            print("")

        return b

    def chat(self, data):
        s = data
        b = {}

        self.b.append( "Append History" )

        return b


class RAG:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.stages = {}

    def make_stage(self, name, data):
        """
        Takes a name for the stage and a dictionary with keys as labels and values as documents.
        Creates a stage with corresponding TF-IDF matrix and labels.
        """
        labels = list(data.keys())
        documents = [doc.lower() for doc in data.values()]
        X = self.vectorizer.fit_transform(documents)

        self.stages[name] = {
            'labels': labels,
            'data': X
        }

    def selector(self, user_query, stage):
        """
        Takes a user query and the name of a stage,
        returns a dictionary of labels with corresponding similarity scores.
        """
        user_query = user_query.lower()

        # Check if the stage exists
        if stage not in self.stages:
            print(f"No such stage: {stage}")
            return {}

        stage_data = self.stages[stage]
        labels = stage_data['labels']
        X = stage_data['data']

        # Convert user query into TF-IDF features
        query_vector = self.vectorizer.transform([user_query])

        # Calculate cosine similarity between the user query and all documents
        cosine_similarities = cosine_similarity(query_vector, X)
        probabilities = cosine_similarities.flatten()

        # Return labels with corresponding similarity scores
        result = {label: prob for label, prob in zip(labels, probabilities)}
        return result


class FileManager:
    def __init__(self, directory_name):
        self.directory_name = directory_name

    def create_directory(self):
        try:
            os.makedirs(self.directory_name, exist_ok=True)
            print(f"Directory '{self.directory_name}' created successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def files_in_dir(self):
        try:
            filenames = [f for f in os.listdir(self.directory_name) if os.path.isfile(os.path.join(self.directory_name, f))]
            return filenames
        except Exception as e:
            print(f"Error: {e}")
            return []

    def text_to_file(self, file_name, text):
        with open(f"{self.directory_name}/{file_name}", 'w') as file:
            file.write(text)
        print(f"Text has been written to {file_name}")

    def file_to_text(self, file_name):
        try:
            with open(f"{self.directory_name}/{file_name}", 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"The file {file_name} does not exist.")
            return None



class Course:
    def __init__(self, name):
        self.name = name
        self.assignments = []
        self.contents = []
        self.students = []
        self.instructor = None
        self.ta = None

    def modify_assignment(self, assignment):
        self.assignments.append(assignment)
        print(f'Assignment {assignment.details} added to {self.name}.')

    def modify_content(self, content):
        self.contents.append(content)
        print(f'Content {content.material} added to {self.name}.')

    def assign_instructor(self, instructor):
        self.instructor = instructor
        print(f'Instructor {instructor.name} assigned to {self.name}.')

    def assign_ta(self, ta):
        self.ta = ta
        print(f'TA {ta.name} assigned to {self.name}.')

    def enroll_student(self, student):
        self.students.append(student)
        student.enroll_in_course(self)
        print(f'{student.name} enrolled in {self.name}.')

