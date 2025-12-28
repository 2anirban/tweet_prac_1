# Database Models Complete Guide

**Complete reference for understanding SQLAlchemy models, relationships, and database concepts in the Tweet Generator project.**

---

## Table of Contents

1. [Database Setup (database.py)](#1-database-setup-databasepy)
2. [Understanding Models (models.py)](#2-understanding-models-modelspy)
3. [Understanding Attributes](#3-understanding-attributes)
4. [SQLAlchemy Relationships Explained](#4-sqlalchemy-relationships-explained)
5. [Relationship Types Guide](#5-relationship-types-guide)
6. [Project Relationships Analysis](#6-project-relationships-analysis)
7. [Practical Examples](#7-practical-examples)

---

## 1. Database Setup (database.py)

### Overview
This file sets up the database connection and session management for the FastAPI application using SQLAlchemy ORM (Object-Relational Mapping).

### Code Breakdown

#### Imports
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
```

**What they do:**
- **`create_engine`**: Creates a connection to the database
- **`declarative_base`**: Factory function that creates a base class for your ORM models
- **`sessionmaker`**: Factory for creating database session objects
- **`settings`**: Import configuration from config.py

#### Database URL
```python
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
```

- Loads the database connection string from environment configuration
- Currently using SQLite: `"sqlite:///./test.db"`
- For production, use PostgreSQL/MySQL:
  - PostgreSQL: `"postgresql://user:password@localhost/dbname"`
  - MySQL: `"mysql://user:password@localhost/dbname"`

#### Database Engine
```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only for SQLite
)
```

**What it does:**
- Creates the core interface to the database
- **`connect_args={"check_same_thread": False}`**:
  - SQLite-specific parameter
  - Allows FastAPI (multi-threaded) to work with SQLite
  - ⚠️ **Remove this parameter** when using PostgreSQL/MySQL

#### Base Class
```python
Base = declarative_base()
```

- Creates a base class that all database models inherit from
- Your models in models.py will look like:
  ```python
  class User(Base):
      __tablename__ = "users"
      # ... columns here
  ```

#### Session Factory
```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Parameters:**
- **`autocommit=False`**: Changes aren't automatically committed (you control when to commit)
- **`autoflush=False`**: Changes aren't automatically flushed to DB before queries
- **`bind=engine`**: Binds this session to the engine we created

#### Database Dependency
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Purpose:**
- Dependency function used in FastAPI endpoints
- Creates a new database session for each request
- **`yield db`**: Provides the session to the endpoint
- **`finally: db.close()`**: Ensures the session is closed after the request
- Prevents memory leaks and ensures proper cleanup

**Usage in FastAPI:**
```python
from fastapi import Depends
from database import get_db

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

---

## 2. Understanding Models (models.py)

### What are Models?

**Models** are Python classes that represent database tables. Each model class defines:
- Table name
- Column definitions
- Data types
- Relationships with other tables

### Model Classes vs Model Instances

#### Model Class (Blueprint)
```python
class User(Base):          # ← Model CLASS (blueprint for table)
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
```

**What it is:**
- A class definition that describes the table structure
- The blueprint for creating user objects
- Defines what columns exist and their types

#### Model Instance (Actual Object)
```python
# Creating an INSTANCE of the User model
user = User(
    email="john@example.com",
    username="john",
    hashed_password="hashed123"
)
```

**What it is:**
- An actual object with real data
- Represents a single row in the database
- Can be saved, queried, updated, or deleted

### Comparison

| Term | Type | Example |
|------|------|---------|
| **Model Class** | Class definition | `User`, `TweetThread`, `TweetHistory` |
| **Model Instance** | Object with data | `user = User(email="...")` |
| **Database Table** | SQL table | `users`, `tweet_threads`, `tweet_histories` |
| **Table Row** | Database record | One row in the users table |

---

## 3. Understanding Attributes

### What is an Attribute?

An **attribute** is a **variable that belongs to an object** (or class). Think of it as a **property** or **characteristic** of an object.

### Simple Analogy: Car Object

```python
class Car:
    def __init__(self, color, brand):
        self.color = color      # ← attribute
        self.brand = brand      # ← attribute
        self.speed = 0          # ← attribute

# Create a car instance
my_car = Car(color="red", brand="Toyota")

# Access attributes using dot notation
print(my_car.color)   # "red"
print(my_car.brand)   # "Toyota"
print(my_car.speed)   # 0
```

**Attributes** = Variables that belong to an object
**Accessing attributes** = `object.attribute_name`

### Attributes in Database Models

In your models, you have TWO types of attributes:

#### 1. Column Attributes (Data Storage)

```python
class User(Base):
    id = Column(Integer, primary_key=True)           # ← attribute
    email = Column(String, unique=True)              # ← attribute
    username = Column(String, unique=True)           # ← attribute
    hashed_password = Column(String, nullable=False) # ← attribute
    is_active = Column(Boolean, default=True)        # ← attribute
    created_at = Column(DateTime, default=datetime.utcnow) # ← attribute
```

**What they do:**
- Store actual data from the database
- Each attribute corresponds to a table column

**Usage:**
```python
user = db.query(User).first()
print(user.email)           # "john@example.com"
print(user.username)        # "john"
print(user.is_active)       # True
```

#### 2. Relationship Attributes (Navigation Properties)

```python
class User(Base):
    # Relationship attributes
    tweet_threads = relationship("TweetThread", ...)   # ← attribute
    tweet_histories = relationship("TweetHistory", ...) # ← attribute
```

**What they do:**
- Allow navigation to related objects
- NOT stored in database (created by SQLAlchemy)
- Fetch related data when accessed

**Usage:**
```python
user = db.query(User).first()
print(user.tweet_threads)    # [<TweetThread>, <TweetThread>, ...]
print(user.tweet_histories)  # [<TweetHistory>, <TweetHistory>, ...]
```

### Dot Notation (`.`) = Attribute Access

```python
object.attribute_name
  ↑         ↑
  |         └─── Attribute (variable belonging to the object)
  └──────────── Object (instance)
```

**Examples:**
```python
thread.topic                      # accessing 'topic' attribute
thread.user                       # accessing 'user' attribute
thread.user.username              # accessing 'username' of User
thread.tweet_histories            # accessing 'tweet_histories' attribute
thread.tweet_histories[0].status  # accessing 'status' of first TweetHistory
```

---

## 4. SQLAlchemy Relationships Explained

### What are Relationships?

**Relationships** define how database tables are connected to each other. They allow you to navigate from one object to related objects.

### Components of a Relationship

#### 1. ForeignKey (Database Level)

```python
class TweetThread(Base):
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    #                        ↑
    #                        └── Links to users.id column
```

**Purpose:**
- Creates database constraint
- Enforces referential integrity
- Prevents orphaned records
- Enables efficient joins

#### 2. relationship() (ORM Level)

```python
class TweetThread(Base):
    user = relationship("User", back_populates="tweet_threads")
    #                    ↑                ↑
    #                    |                └── Links to User.tweet_threads
    #                    └── Target model class
```

**Purpose:**
- Creates Python attribute for navigation
- Allows accessing related objects
- Handles lazy/eager loading
- Manages cascade behavior

#### 3. back_populates

```python
# In TweetThread
user = relationship("User", back_populates="tweet_threads")

# In User
tweet_threads = relationship("TweetThread", back_populates="user")
```

**Purpose:**
- Links both sides of the relationship
- Creates bidirectional navigation
- Keeps both sides in sync

### How Relationships Work

#### Before Querying (Class Definition)
```python
class TweetThread(Base):
    user = relationship("User", ...)  # Just a definition, no data yet
```

#### After Querying (Instance with Data)
```python
thread = db.query(TweetThread).first()  # Get instance from database

# Now relationship attributes have values
print(thread.user)           # <User object> - SQLAlchemy fetched this
print(thread.user.username)  # "alice" - Access User's attributes
```

SQLAlchemy automatically:
1. Sees you defined a `user` relationship attribute
2. Looks up the related User from the database (using `user_id`)
3. Stores that User instance in the `user` attribute
4. You access it with `thread.user`

### Cascade Behavior

```python
tweet_threads = relationship("TweetThread", cascade="all, delete-orphan")
```

**What it does:**
- **"all"**: All operations (save, update, delete) cascade to children
- **"delete-orphan"**: If a child is removed from the collection, it's deleted

**Example:**
```python
user = db.query(User).first()
db.delete(user)
db.commit()

# This also deletes:
# - All TweetThread records created by this user (cascade)
# - All TweetHistory records associated with those threads (cascade)
```

---

## 5. Relationship Types Guide

### How to Identify Relationship Types

The relationship type is determined by:
1. **Where the ForeignKey is located**
2. **Whether the relationship returns ONE object or MANY objects**

### Key Rules

| Relationship Type | ForeignKey Location | Returns | uselist | Example |
|------------------|---------------------|---------|---------|---------|
| **One-to-Many** | On "many" side | List on "one" side, single on "many" | Default (True) | User → TweetThreads |
| **Many-to-One** | On "many" side | Single on "many" side | Default (True) | TweetThread → User |
| **One-to-One** | On one side | Single on both sides | False | User → Profile |
| **Many-to-Many** | Association table | List on both sides | Default (True) | Students ↔ Courses |

### 1️⃣ One-to-Many

**Definition:** One parent can have many children, but each child has only one parent.

**Identifiers:**
- ✅ ForeignKey on the "many" side
- ✅ Relationship returns a **list** on the "one" side
- ✅ Relationship returns a **single object** on the "many" side

**Example:**
```python
# ONE User can have MANY TweetThreads

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    # No ForeignKey here (this is the "one" side)
    tweet_threads = relationship("TweetThread", back_populates="user")
    #                                           ↑ Returns LIST


class TweetThread(Base):
    __tablename__ = "tweet_threads"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # ForeignKey HERE
    #                        ↑ Marks the "many" side
    user = relationship("User", back_populates="tweet_threads")
    #                           ↑ Returns SINGLE object
```

**Visual:**
```
User (1) ────────────┐
                     │
                     ├───→ TweetThread (Many)
                     ├───→ TweetThread
                     └───→ TweetThread
```

**Usage:**
```python
user = db.query(User).first()
print(user.tweet_threads)  # [<TweetThread>, <TweetThread>]  ← LIST

thread = db.query(TweetThread).first()
print(thread.user)  # <User>  ← SINGLE object
```

### 2️⃣ Many-to-One

**Definition:** Many children belong to one parent.

**Note:** This is the **same as One-to-Many**, just viewed from the opposite direction.

**Example:**
```python
# MANY TweetThreads belong to ONE User

class TweetThread(Base):
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tweet_threads")
    #                           ↑ Returns SINGLE User
```

**Perspective:**
- **One-to-Many**: One User → Many TweetThreads (from User's perspective)
- **Many-to-One**: Many TweetThreads → One User (from TweetThread's perspective)

### 3️⃣ One-to-One

**Definition:** One record in Table A relates to exactly one record in Table B.

**Identifiers:**
- ✅ ForeignKey on one side
- ✅ **`uselist=False`** parameter in relationship
- ✅ Both sides return a **SINGLE object** (not a list)
- ✅ Often `unique=True` on ForeignKey

**Example:**
```python
# ONE User has ONE Profile (and vice versa)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    profile = relationship("Profile", uselist=False, back_populates="user")
    #                                 ↑ Makes it one-to-one


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    #                                                  ↑ Enforces one-to-one at DB level
    user = relationship("User", back_populates="profile")
```

**Visual:**
```
User (1) ←──────────→ Profile (1)
```

**Usage:**
```python
user = db.query(User).first()
print(user.profile)  # <Profile>  ← SINGLE object, NOT a list

profile = db.query(Profile).first()
print(profile.user)  # <User>  ← SINGLE object
```

### 4️⃣ Many-to-Many

**Definition:** Multiple records in Table A can relate to multiple records in Table B.

**Identifiers:**
- ✅ Requires an **association table** (junction table)
- ✅ **TWO ForeignKeys** in the association table
- ✅ Both sides return **lists**
- ✅ Uses `secondary` parameter in relationship

**Example:**
```python
from sqlalchemy import Table

# Association Table (junction table)
student_course = Table('student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    courses = relationship("Course", secondary=student_course, back_populates="students")
    #                                ↑ Points to association table


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    students = relationship("Student", secondary=student_course, back_populates="courses")
```

**Visual:**
```
Student (Many) ←────→ [student_course] ←────→ Course (Many)
                      (association table)
```

**Usage:**
```python
student = db.query(Student).first()
print(student.courses)  # [<Course>, <Course>]  ← LIST

course = db.query(Course).first()
print(course.students)  # [<Student>, <Student>]  ← LIST
```

### Quick Identification Checklist

To identify a relationship, ask these questions:

#### Question 1: Where is the ForeignKey?
- **On Table A** → A is the "many" side
- **On Table B** → B is the "many" side
- **On both (via association table)** → Many-to-Many

#### Question 2: What does the relationship return?
- **Returns a list** → That side has "many"
- **Returns a single object** → That side has "one"
- **Has `uselist=False`** → One-to-One

#### Question 3: How many ForeignKeys?
- **One ForeignKey** → One-to-Many or One-to-One
- **Two ForeignKeys in association table** → Many-to-Many

---

## 6. Project Relationships Analysis

### Your Database Models

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tweet_threads = relationship("TweetThread", back_populates="user", cascade="all, delete-orphan")
    tweet_histories = relationship("TweetHistory", back_populates="user", cascade="all, delete-orphan")


class TweetThread(Base):
    __tablename__ = "tweet_threads"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    topic = Column(String, nullable=False)
    thread_content = Column(Text, nullable=False)
    tweet_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="tweet_threads")
    tweet_histories = relationship("TweetHistory", back_populates="tweet_thread", cascade="all, delete-orphan")


class TweetHistory(Base):
    __tablename__ = "tweet_histories"
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey('tweet_threads.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    generation_params = Column(Text, nullable=True)
    processing_time = Column(Integer, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="tweet_histories")
    tweet_thread = relationship("TweetThread", back_populates="tweet_histories")
```

### Relationship Breakdown

#### Relationship 1: User ↔ TweetThread

**Type:** **One-to-Many** (User → TweetThread)

**Analysis:**
- ✅ ForeignKey in `TweetThread.user_id` → TweetThread is "many" side
- ✅ `user.tweet_threads` returns list → User is "one" side
- ✅ `thread.user` returns single object → TweetThread is "many" side

**What it means:**
- One user can create many tweet threads
- Each tweet thread belongs to exactly one user

**ForeignKey:**
```python
user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
```

**Relationships:**
```python
# In User
tweet_threads = relationship("TweetThread", ...)  # Returns LIST

# In TweetThread
user = relationship("User", ...)  # Returns SINGLE User object
```

#### Relationship 2: TweetThread ↔ TweetHistory

**Type:** **One-to-Many** (TweetThread → TweetHistory)

**Analysis:**
- ✅ ForeignKey in `TweetHistory.thread_id` → TweetHistory is "many" side
- ✅ `thread.tweet_histories` returns list → TweetThread is "one" side
- ✅ `history.tweet_thread` returns single object → TweetHistory is "many" side

**What it means:**
- One tweet thread can have many history records
- Each history record belongs to exactly one tweet thread

**ForeignKey:**
```python
thread_id = Column(Integer, ForeignKey('tweet_threads.id'), nullable=False)
```

**Relationships:**
```python
# In TweetThread
tweet_histories = relationship("TweetHistory", ...)  # Returns LIST

# In TweetHistory
tweet_thread = relationship("TweetThread", ...)  # Returns SINGLE TweetThread
```

#### Relationship 3: User ↔ TweetHistory

**Type:** **One-to-Many** (User → TweetHistory)

**Analysis:**
- ✅ ForeignKey in `TweetHistory.user_id` → TweetHistory is "many" side
- ✅ `user.tweet_histories` returns list → User is "one" side
- ✅ `history.user` returns single object → TweetHistory is "many" side

**What it means:**
- One user can have many history records
- Each history record belongs to exactly one user

**ForeignKey:**
```python
user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
```

**Relationships:**
```python
# In User
tweet_histories = relationship("TweetHistory", ...)  # Returns LIST

# In TweetHistory
user = relationship("User", ...)  # Returns SINGLE User object
```

### Summary Table

| From | To | Type | ForeignKey Location | Returns |
|------|----|----|---------------------|---------|
| User | TweetThread | One-to-Many | `TweetThread.user_id` | List of TweetThreads |
| TweetThread | User | Many-to-One | `TweetThread.user_id` | Single User |
| TweetThread | TweetHistory | One-to-Many | `TweetHistory.thread_id` | List of TweetHistories |
| TweetHistory | TweetThread | Many-to-One | `TweetHistory.thread_id` | Single TweetThread |
| User | TweetHistory | One-to-Many | `TweetHistory.user_id` | List of TweetHistories |
| TweetHistory | User | Many-to-One | `TweetHistory.user_id` | Single User |

### Visual Database Structure

```
┌─────────────────┐
│      User       │
│   (1 record)    │
└────────┬────────┘
         │
         │ One-to-Many
         │
         ├─────────────────────────────────────┐
         │                                     │
         ▼                                     ▼
┌─────────────────┐                  ┌─────────────────┐
│  TweetThread    │                  │  TweetHistory   │
│  (Many records) │                  │  (Many records) │
└────────┬────────┘                  └─────────────────┘
         │                                     ▲
         │ One-to-Many                         │
         │                                     │
         └─────────────────────────────────────┘
```

**All relationships in this project are One-to-Many!**

---

## 7. Practical Examples

### Example 1: Creating Related Objects

```python
from sqlalchemy.orm import Session
from models import User, TweetThread, TweetHistory
from database import get_db

# Get database session
db = next(get_db())

# Step 1: Create a User
user = User(
    email="alice@example.com",
    username="alice",
    hashed_password="hashed_password_here"
)
db.add(user)
db.commit()
db.refresh(user)  # Get the auto-generated ID

print(f"Created user: {user.username} (ID: {user.id})")

# Step 2: Create a TweetThread for this user
thread = TweetThread(
    user_id=user.id,
    topic="AI and the Future",
    thread_content='["Tweet 1 about AI", "Tweet 2 about ML", "Tweet 3 about future"]',
    tweet_count=3
)
db.add(thread)
db.commit()
db.refresh(thread)

print(f"Created thread: {thread.topic} (ID: {thread.id})")

# Step 3: Create a TweetHistory record
history = TweetHistory(
    thread_id=thread.id,
    user_id=user.id,
    generation_params='{"model": "gpt-4", "temperature": 0.7}',
    processing_time=1500,  # milliseconds
    status="success"
)
db.add(history)
db.commit()

print(f"Created history record (ID: {history.id})")
```

### Example 2: Navigating Relationships

```python
# Query a user
user = db.query(User).filter(User.username == "alice").first()

# Navigate from User to TweetThreads (One-to-Many)
print(f"\n{user.username} has {len(user.tweet_threads)} tweet threads:")
for thread in user.tweet_threads:
    print(f"  - {thread.topic} ({thread.tweet_count} tweets)")

# Navigate from User to TweetHistories (One-to-Many)
print(f"\n{user.username} has {len(user.tweet_histories)} history records:")
for history in user.tweet_histories:
    print(f"  - Status: {history.status}, Time: {history.processing_time}ms")

# Query a thread
thread = db.query(TweetThread).first()

# Navigate from TweetThread to User (Many-to-One)
print(f"\nThread '{thread.topic}' was created by: {thread.user.username}")

# Navigate from TweetThread to TweetHistories (One-to-Many)
print(f"Thread has {len(thread.tweet_histories)} history records:")
for history in thread.tweet_histories:
    print(f"  - {history.status} ({history.processing_time}ms)")

# Query a history record
history = db.query(TweetHistory).first()

# Navigate from TweetHistory to User (Many-to-One)
print(f"\nHistory record belongs to user: {history.user.username}")

# Navigate from TweetHistory to TweetThread (Many-to-One)
print(f"History record is for thread: {history.tweet_thread.topic}")
```

### Example 3: Cascade Delete in Action

```python
# Create a user with threads and histories
user = User(email="bob@example.com", username="bob", hashed_password="hash")
db.add(user)
db.commit()

# Create 2 threads
for i in range(2):
    thread = TweetThread(
        user_id=user.id,
        topic=f"Topic {i+1}",
        thread_content=f'["Tweet {i+1}"]',
        tweet_count=1
    )
    db.add(thread)
db.commit()

# Create history for each thread
for thread in user.tweet_threads:
    history = TweetHistory(
        thread_id=thread.id,
        user_id=user.id,
        status="success",
        processing_time=1000
    )
    db.add(history)
db.commit()

print(f"User {user.username} has:")
print(f"  - {len(user.tweet_threads)} threads")
print(f"  - {len(user.tweet_histories)} histories")

# Now delete the user
db.delete(user)
db.commit()

# Thanks to cascade="all, delete-orphan", this also deleted:
# - All 2 TweetThread records
# - All 2 TweetHistory records

# Verify
remaining_threads = db.query(TweetThread).filter(TweetThread.user_id == user.id).count()
remaining_histories = db.query(TweetHistory).filter(TweetHistory.user_id == user.id).count()

print(f"\nAfter deleting user:")
print(f"  - Remaining threads: {remaining_threads}")  # 0
print(f"  - Remaining histories: {remaining_histories}")  # 0
```

### Example 4: Querying with Joins

```python
from sqlalchemy import select

# Get all threads with user information (explicit join)
stmt = (
    select(TweetThread, User)
    .join(User, TweetThread.user_id == User.id)
    .where(User.username == "alice")
)
results = db.execute(stmt).all()

for thread, user in results:
    print(f"{user.username} created: {thread.topic}")

# More efficient: Use relationship loading
user = db.query(User).filter(User.username == "alice").first()
for thread in user.tweet_threads:  # SQLAlchemy handles the join automatically
    print(f"{user.username} created: {thread.topic}")
```

### Example 5: Updating Related Objects

```python
# Get a user
user = db.query(User).filter(User.username == "alice").first()

# Update user directly
user.email = "newemail@example.com"
db.commit()

# Create a new thread for this user
new_thread = TweetThread(
    user_id=user.id,
    topic="New Topic",
    thread_content='["New tweet"]',
    tweet_count=1
)
user.tweet_threads.append(new_thread)  # Add to relationship
db.commit()

# Update an existing thread
first_thread = user.tweet_threads[0]
first_thread.topic = "Updated Topic"
db.commit()

# Delete a thread (also deletes its histories due to cascade)
thread_to_delete = user.tweet_threads[0]
db.delete(thread_to_delete)
db.commit()
```

---

## Key Takeaways

### 1. Models
- **Models** are classes that represent database tables
- **Instances** are objects with actual data (rows)
- Use `Base` as parent class for all models

### 2. Attributes
- **Column attributes** store database data
- **Relationship attributes** provide navigation to related objects
- Access using dot notation: `object.attribute`

### 3. Relationships
- **ForeignKey** creates database constraint
- **relationship()** creates Python navigation
- **back_populates** links both sides

### 4. Relationship Types
- **One-to-Many**: Most common, ForeignKey on "many" side
- **Many-to-One**: Same as one-to-many, opposite perspective
- **One-to-One**: Add `uselist=False` and `unique=True`
- **Many-to-Many**: Requires association table with `secondary`

### 5. Your Project
- All relationships are **One-to-Many**
- User → TweetThread → TweetHistory
- Cascade deletes configured properly
- ForeignKeys enforce data integrity

---

## Additional Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [SQLAlchemy Relationships Guide](https://docs.sqlalchemy.org/en/14/orm/relationships.html)
- [FastAPI with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Database Design Best Practices](https://www.databasestar.com/database-design/)

---

**Created for:** Tweet Generator Project
**Last Updated:** 2024
**Reference:** [models.py](Backend/models.py), [database.py](Backend/database.py)










schemas.py


from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# ============================================
# User Schemas
# ============================================

class UserCreate(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for safe user data (never expose password!)"""
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Enables ORM mode for SQLAlchemy


# ============================================
# Authentication Schemas
# ============================================

class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for JWT token payload (decoded token)"""
    email: Optional[str] = None
    user_id: Optional[int] = None


# ============================================
# Tweet Generation Schemas
# ============================================

class TweetGenerationRequest(BaseModel):
    """Schema for tweet generation request"""
    topic: str = Field(..., min_length=10, max_length=500, description="Topic description (10-500 characters)")
    # Optional parameters for customization (future enhancements)
    tone: Optional[str] = Field(None, description="Tone: professional, casual, humorous, etc.")
    max_tweets: Optional[int] = Field(5, ge=1, le=20, description="Maximum number of tweets in thread")


class TweetGenerationResponse(BaseModel):
    """Schema for generated tweet thread (immediate response)"""
    tweets: List[str] = Field(..., description="List of tweets in the thread")
    tweet_count: int = Field(..., description="Number of tweets generated")
    topic: str = Field(..., description="Original topic")


# ============================================
# Tweet Thread Schemas (Database Records)
# ============================================

class TweetThreadBase(BaseModel):
    """Base schema for TweetThread"""
    topic: str
    tweet_count: int


class TweetThreadCreate(TweetThreadBase):
    """Schema for creating a tweet thread in database"""
    thread_content: str  # JSON string of tweets
    user_id: int


class TweetThreadResponse(BaseModel):
    """Schema for tweet thread response (from database)"""
    id: int
    user_id: int
    topic: str
    tweets: List[str] = Field(..., description="Parsed tweets from thread_content")
    tweet_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_with_parsed_tweets(cls, db_thread):
        """Custom constructor to parse thread_content JSON"""
        import json
        tweets = json.loads(db_thread.thread_content) if db_thread.thread_content else []
        return cls(
            id=db_thread.id,
            user_id=db_thread.user_id,
            topic=db_thread.topic,
            tweets=tweets,
            tweet_count=db_thread.tweet_count,
            created_at=db_thread.created_at,
            updated_at=db_thread.updated_at
        )


# ============================================
# Tweet History Schemas
# ============================================

class TweetHistoryResponse(BaseModel):
    """Schema for individual tweet history record"""
    id: int
    thread_id: int
    user_id: int
    status: str
    processing_time: Optional[int] = None
    generation_params: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserTweetHistoryResponse(BaseModel):
    """Schema for user's complete tweet history"""
    threads: List[TweetThreadResponse]
    total_count: int
    page: int = 1
    page_size: int = 10
    













How to Use These Schemas
Example 1: User Registration

@app.post("/auth/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # UserCreate validates input
    hashed_pw = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # UserResponse formats output (no password!)
    return UserResponse.model_validate(user)
Example 2: Generate Tweets

@app.post("/tweets/generate", response_model=TweetGenerationResponse)
def generate_tweets(request: TweetGenerationRequest, current_user: User = Depends(get_current_user)):
    # TweetGenerationRequest validates input
    tweets = generate_tweet_thread(request.topic, request.max_tweets)
    
    # Save to database
    import json
    thread_content = json.dumps(tweets)
    db_thread = TweetThread(
        user_id=current_user.id,
        topic=request.topic,
        thread_content=thread_content,
        tweet_count=len(tweets)
    )
    db.add(db_thread)
    db.commit()
    
    # TweetGenerationResponse formats output
    return TweetGenerationResponse(
        tweets=tweets,
        tweet_count=len(tweets),
        topic=request.topic
    )
Example 3: Get Thread History

@app.get("/tweets/history", response_model=UserTweetHistoryResponse)
def get_history(
    page: int = 1,
    page_size: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    threads = db.query(TweetThread)\
        .filter(TweetThread.user_id == current_user.id)\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    total = db.query(TweetThread).filter(TweetThread.user_id == current_user.id).count()
    
    # Parse threads
    parsed_threads = [
        TweetThreadResponse.from_orm_with_parsed_tweets(t) for t in threads
    ]
    
    return UserTweetHistoryResponse(
        threads=parsed_threads,
        total_count=total,
        page=page,
        page_size=page_size
    )