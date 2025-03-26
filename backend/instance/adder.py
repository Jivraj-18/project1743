from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Table
from sqlalchemy.orm import relationship, declarative_base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, declarative_base

import re

Base = declarative_base()

class Course(Base):
    __tablename__ = 'Course'
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String, nullable=False)
    description = Column(String)

class Content(Base):
    __tablename__ = 'Content'
    content_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(ForeignKey('Course.course_id'), nullable=False)
    content_type = Column(String, nullable=False)
    content_name = Column(String)
    url = Column(String)
    transcript_url = Column(String)
    ai_summary = Column(String)

    course = relationship('Course')


# Set up the database connection
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Content.__table__.drop(engine)
# Content.__table__.create(engine)

def extract_video_id(url):
    match = re.search(r'v=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None



dat = [
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.1: Introduction",
		"url": "https://www.youtube.com/watch?v=8ndsDXohLMQ"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.2: Introduction to Replit",
		"url": "https://www.youtube.com/watch?v=NgZZ0HIUqbs"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.3: More on Replit, print and Common Mistakes",
		"url": "https://www.youtube.com/watch?v=As7_aq6XGfI"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.4: A Quick Introduction to Variables",
		"url": "https://www.youtube.com/watch?v=Yg6xzi2ie5s"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.5: Variables and Input Statement",
		"url": "https://www.youtube.com/watch?v=ruQb8jzkGyQ"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.6: Variables and Literals",
		"url": "https://www.youtube.com/watch?v=tDaXdoKfX0k"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.7: Data Types 1",
		"url": "https://www.youtube.com/watch?v=8n4MBjuDBu4"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.8: Data Types 2",
		"url": "https://www.youtube.com/watch?v=xQXxufhEJHw"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.9: Operators and Expressions 1",
		"url": "https://www.youtube.com/watch?v=8pu73HKzNOE"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.10: Operators and Expressions 2",
		"url": "https://www.youtube.com/watch?v=Y53K9FFu97Q"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.11: Introduction to Strings",
		"url": "https://www.youtube.com/watch?v=sS89tiDuqoM"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.12: More on Strings",
		"url": "https://www.youtube.com/watch?v=e45MVXwya7A"
	},
	{
		"course_id": 2,
		"content_type": "Week 1",
		"content_name": "L1.13: Conclusion: FAQs",
		"url": "https://www.youtube.com/watch?v=_Ccezy5hlc8"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.1: Introduction",
		"url": "https://www.youtube.com/watch?v=aEPFZSzZ6VQ"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.2: Variables : A Programmer's Perspective",
		"url": "https://www.youtube.com/watch?v=XZSnqseRbZY"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.3: Variables Revisited: Dynamic Typing",
		"url": "https://www.youtube.com/watch?v=2OFZY77eOjw"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.4: More on Variables, Operators and Expressions",
		"url": "https://www.youtube.com/watch?v=-f833WH_cVo"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.5: Escape characters and types of quotes",
		"url": "https://www.youtube.com/watch?v=4vWM2oTGEio"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.6: String Methods",
		"url": "https://www.youtube.com/watch?v=bRAo6TJJjCU"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.7: An Interesting Cipher: More on Strings",
		"url": "https://www.youtube.com/watch?v=oxFYdHVNpg8"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.8: Introduction to the if statement",
		"url": "https://www.youtube.com/watch?v=FTX5wF_3J9Q"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.9: Tutorial on if, else and else-if (elif) conditions",
		"url": "https://www.youtube.com/watch?v=-dBqiRCHbNw"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.10: Introduction to 'import library'",
		"url": "https://www.youtube.com/watch?v=OdjXL5U95eI"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.11: Different ways to import a library",
		"url": "https://www.youtube.com/watch?v=eW58_ky7oc8"
	},
	{
		"course_id": 2,
		"content_type": "Week 2",
		"content_name": "L2.12: Conclusion",
		"url": "https://www.youtube.com/watch?v=DK16M8EvOLE"
	}
]

# dat = [{
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.1: Natural Numbers and their operations",
# 	"url": "https://www.youtube.com/watch?v=WEC6jPWvoj8"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.2: Rational Numbers",
# 	"url": "https://www.youtube.com/watch?v=jHBIJ50DhJQ"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.3: Real and Complex Numbers",
# 	"url": "https://www.youtube.com/watch?v=hz7cuJj17wU"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.4: Set Theory",
# 	"url": "https://www.youtube.com/watch?v=8z04uTycZpE"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.5: Construction of Subsets and set operations",
# 	"url": "https://www.youtube.com/watch?v=Ue3y-OE_2lE"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.6: Sets: Examples",
# 	"url": "https://www.youtube.com/watch?v=bW5O7a1VX4w"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.7: Examples of Set Operations and Counting Problems",
# 	"url": "https://www.youtube.com/watch?v=NwYHojyw3SU"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.8: Relations",
# 	"url": "https://www.youtube.com/watch?v=_bNfC5yW6bk"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.9: Functions",
# 	"url": "https://www.youtube.com/watch?v=M-nlI2fgaWI"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.10: Relations: examples",
# 	"url": "https://www.youtube.com/watch?v=6CyagSq3fWA"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 1",
# 	"content_name": "L1.11:Function: examples",
# 	"url": "https://www.youtube.com/watch?v=6YrUx0bAnuQ"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.1: Rectangular Coordinate system",
# 	"url": "https://www.youtube.com/watch?v=RfG2NLXqGE8"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.2: Distance formula",
# 	"url": "https://www.youtube.com/watch?v=aDhyAkXiDOY"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.3: Section formula",
# 	"url": "https://www.youtube.com/watch?v=B5yv8zPrkek"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.4: Area of triangle",
# 	"url": "https://www.youtube.com/watch?v=x62fodF7ezk"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.5: Slope of a line",
# 	"url": "https://www.youtube.com/watch?v=V-b3BL8DAvU"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.6: Parallel and perpendicular lines",
# 	"url": "https://www.youtube.com/watch?v=CXhBGVfmtBg"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.7: Representation of a Line-1",
# 	"url": "https://www.youtube.com/watch?v=fKUK8xeuWNo"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.8: Representation of a Line-2",
# 	"url": "https://www.youtube.com/watch?v=zM0q4y-y4so"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.9: General equation of line",
# 	"url": "https://www.youtube.com/watch?v=_3Iidm8NnbM"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.10: Equation of parallel and perpendicular lines in general form",
# 	"url": "https://www.youtube.com/watch?v=gJuJtTYmbSs"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.11: Equation of a perpendicular line passing through a point",
# 	"url": "https://www.youtube.com/watch?v=CjeHgCXhi4k"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.12: Distance of a line from a given point",
# 	"url": "https://www.youtube.com/watch?v=tYSZ4L0X3kY"
# },
# {
# 	"course_id": 1,
# 	"content_type": "Week 2",
# 	"content_name": "L2.13: Straight line fit",
# 	"url": "https://www.youtube.com/watch?v=xdZHsFuyBZM"
# }
# ]


course_name="Python"

# First, create the Course instance if it doesn't exist
course = session.query(Course).filter(Course.course_name == course_name).first()
if not course:
    course = Course(course_name=course_name, description=f"This is an {course_name} course")
    session.add(course)
    session.commit()



for i in dat:


    vid = extract_video_id(i["url"])

    new_content = Content(
        course_id = course.course_id,
        content_type = i["content_type"],
        content_name= i["content_name"],
        url= i["url"],
        transcript_url= f"sub/{vid}.txt",
        ai_summary= f"aisum/{vid}.txt"
    )

    session.add(new_content)
    session.commit()

    print(f"Added : {i["content_name"]}")