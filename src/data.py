from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Create database engine (SQLite)
engine = create_engine("sqlite:///test.db", echo=True)

# Base class
Base = declarative_base()

# Define a table
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# Create the table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data
student1 = Student(name="John", age=20)
student2 = Student(name="Emma", age=22)

session.add(student1)
session.add(student2)
session.commit()

# Query data
students = session.query(Student).all()
for student in students:
    print(student.id, student.name, student.age)
