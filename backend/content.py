from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Base class for the ORM models
Base = declarative_base()


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

class Course(Base):
    __tablename__ = 'Course'
    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String, nullable=False)
    description = Column(String)

# Database URL for SQLite database
DATABASE_URL = 'sqlite:///./database.db'

# Set up the engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

# Array of data you want to insert
data = [
    {"course_id": 1, "content_type": "video", "content_name": "Intro Video", "url": "http://example.com/video1", "transcript_url": "http://example.com/transcript1", "ai_summary": "This is a video about intro."},
    {"course_id": 2, "content_type": "article", "content_name": "Python Basics", "url": "http://example.com/article1", "transcript_url": "http://example.com/transcript2", "ai_summary": "This article covers Python basics."},
    # Add more rows as needed
]

# Insert data into the content table
def insert_data():
    # Create a new session to interact with the database
    session = SessionLocal()

    try:
        for item in data:
            content = Content(
                course_id=item['course_id'],
                content_type=item['content_type'],
                content_name=item['content_name'],
                url=item['url'],
                transcript_url=item['transcript_url'],
                ai_summary=item['ai_summary']
            )
            session.add(content)  # Add the content to the session

        session.commit()  # Commit the transaction to the database
        print("Data inserted successfully!")

    except Exception as e:
        session.rollback()  # Rollback in case of an error
        print(f"Error inserting data: {e}")

    finally:
        session.close()  # Close the session

# Call the insert function
insert_data()
