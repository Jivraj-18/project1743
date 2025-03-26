from .models import Instructor, Student, Course, User, user_roles, Issue, CourseStudent, Content, Question, AssignmentStudent, Assignment, Event, UserTask, StarredQuestion
from .extensions import db

from .fs import FileManager
aisum = FileManager('aisum')

def makeS (s, t):
    s = s
    b = "Do it yourself"

    if t == "gen":

        isweek = s.get("week", False)
        sumup = ""
        i = 0

        if isweek:

            results = db.session.query(Content).filter(Content.content_type == isweek).all()
            
            for row in results:
                result_tuple = tuple(row.__dict__.values())
                sumup += aisum.file_to_text(row.ai_summary.split("/")[1]) + "\n"

        b = f"""
            Scope: { sumup } 
            Number of Questions: { s.get('N', 3)}
        """

    elif t == "sumup":

        

        isweek = s.get("week", False)
        islec = s.get("lecture", False)
        sumup = ""
        
        if islec:
            results = db.session.query(Content).filter(Content.content_name == islec).first()
            sumup += aisum.file_to_text(results.ai_summary.split("/")[1]) + "\n"
        
        elif isweek:
            
            results = db.session.query(Content).filter(Content.content_type == isweek).all()
            for row in results:
                result_tuple = tuple(row.__dict__.values())
                sumup += aisum.file_to_text(row.ai_summary.split("/")[1]) + "\n"

        else:
            sumup = "Do it Accoding to Query"

        b = sumup

    elif t == "chat":
        b = "This is the conversation which is going between you and the USER. Can you continue it?\n\n"

        for speaker, message in s.get("conversation", []):
            b += f"{speaker}: {message}\n"

        b += "\nCan you continue the conversation from here?"

        print(b)

    else:
        b = "Do what ever you think is appropraite"

    print("MAKES => ",t, b)

    return b


