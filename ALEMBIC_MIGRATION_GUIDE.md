# Alembic Migration Guide

Complete guide for adding database migrations to the Tweet Generator application.

---
Great question! Here's a clear guide on when to use Alembic commands:
When You Need Alembic Migrations
✅ Schema Changes (Database Structure)
When: You modify models.py - adding/removing/changing columns or tables Examples:
Add new field to User
Remove a column
Change column type
Add new table
Modify relationships
Commands:

cd Backend

# 1. Create migration (auto-detects changes)
python -m alembic revision --autogenerate -m "Description of change"

# 2. Apply migration
python -m alembic upgrade head

# 3. Restart server
# (Ctrl+C and run python main.py again)
Example Workflow:

# 1. Edit models.py
class User(Base):
    # ... existing fields ...
    is_admin = Column(Boolean, default=False)  # NEW FIELD

# 2. Run Alembic commands
cd Backend
python -m alembic revision --autogenerate -m "Add is_admin to users"
python -m alembic upgrade head

# 3. Done! New column is in database
When You DON'T Need Alembic
❌ Code-Only Changes (No Database Structure Change)
When: You modify Python code but NOT the database structure Examples:
Admin Panel Changes (admin.py)
Change column_list
Change labels
Change pagination settings
Enable/disable filters
API Routes (routers/auth.py, routers/tweets.py)
Add new endpoints
Modify route logic
Change responses
Configuration (config.py, .env)
Change settings
Update environment variables
Utilities (utils/auth_utils.py)
Change helper functions
Update business logic
What to do:

# Just restart the server
# Press Ctrl+C, then:
python main.py
❌ Data Changes (Adding Records)
When: Adding/updating/deleting data (not structure) Examples:
Register new user
Create tweet thread
Update user profile
Delete records
What to do:
Nothing! Just use your API or admin panel
No Alembic needed
Complete Decision Tree

Did you change models.py?
│
├─ YES → Did you add/remove/modify columns/tables?
│         │
│         ├─ YES → Use Alembic migration
│         │        1. alembic revision --autogenerate -m "msg"
│         │        2. alembic upgrade head
│         │        3. Restart server
│         │
│         └─ NO → Just restart server
│
└─ NO → Did you change other Python files (admin.py, routes, etc.)?
          │
          └─ YES → Just restart server
                   (or uvicorn auto-reloads if in dev mode)
Quick Reference
Change Type	Example	Alembic?	Command
Add column	is_admin = Column(Boolean)	✅ Yes	revision --autogenerate + upgrade head
Remove column	Delete field from model	✅ Yes	revision --autogenerate + upgrade head
Change column type	String → Text	✅ Yes	revision --autogenerate + upgrade head
Add new model	New class Product(Base)	✅ Yes	revision --autogenerate + upgrade head
Admin panel config	Change column_list	❌ No	Just restart server
Add API route	New @router.post()	❌ No	Just restart server
Change .env	Update OPENAI_API_KEY	❌ No	Just restart server
Add user data	Register new user	❌ No	Nothing (just use API)
Admin Panel Specific Changes
If you want to show phone_number in admin panel:
File: admin.py

class UserAdmin(ModelView, model=User):
    # Add phone_number to the list
    column_list = [
        User.id, 
        User.username, 
        User.email,
        User.phone_number,  # ← ADD THIS
        User.is_active, 
        User.created_at
    ]
    
    # Make it searchable (optional)
    column_searchable_list = [User.username, User.email, User.phone_number]
    
    # Add label (optional)
    column_labels = {
        User.id: "ID",
        User.username: "Username",
        User.email: "Email",
        User.phone_number: "Phone",  # ← ADD THIS
        User.is_active: "Active",
        User.created_at: "Created",
    }
Do you need Alembic? ❌ No - just restart server!
Best Practice Workflow

# 1. Make changes to models.py
# (add phone_number field)

# 2. Create & apply migration
cd Backend
python -m alembic revision --autogenerate -m "Add phone_number to users"
python -m alembic upgrade head

# 3. Update admin.py to show new field
# (edit column_list, etc.)

# 4. Restart server
python main.py

# 5. Check admin panel at http://localhost:8000/admin
Summary
Use Alembic when:
✅ You change models.py structure (add/remove/modify columns/tables)
Don't use Alembic when:
❌ You change admin panel configuration
❌ You add/modify API routes
❌ You update settings or .env
❌ You add/edit data records
Always remember:

# After ANY code change (with or without migration):










## What is Alembic?

**Alembic** is a lightweight database migration tool for SQLAlchemy. It allows you to:

- ✅ Track database schema changes over time
- ✅ Version control your database structure
- ✅ Safely upgrade/downgrade database schemas
- ✅ Collaborate with team on database changes
- ✅ Deploy schema changes to production

Think of it like **Git for your database schema**.

---

## Why Use Alembic?

### Without Alembic

When you change your models:

```python
# Add new field to User model
class User(Base):
    # ... existing fields ...
    phone_number = Column(String, nullable=True)  # NEW FIELD
```

You need to:
1. Drop the entire database
2. Recreate tables with `Base.metadata.create_all()`
3. **LOSE ALL DATA** 💥

### With Alembic

1. Change your model
2. Create migration: `alembic revision --autogenerate -m "Add phone_number to users"`
3. Apply migration: `alembic upgrade head`
4. **Data preserved** ✅

---

## Installation

Alembic is already in your `requirements.txt`:

```txt
alembic==1.13.1
```

If you haven't installed it yet:

```bash
pip install alembic==1.13.1
```

---

## Setup Steps

### Step 1: Initialize Alembic

Navigate to your Backend directory:

```bash
cd Backend
alembic init alembic
```

This creates:

```
Backend/
├── alembic/
│   ├── versions/          # Migration scripts go here
│   ├── env.py            # Alembic environment config
│   ├── script.py.mako    # Template for migrations
│   └── README
├── alembic.ini           # Alembic configuration file
├── main.py
├── models.py
└── ...
```

---

### Step 2: Configure alembic.ini

**File:** `Backend/alembic.ini`

**Find this line (around line 63):**

```ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```

**Change to:**

```ini
# Comment out the hardcoded URL - we'll use env.py instead
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

**Why?** We want to use the same database URL from your `.env` file, not hardcode it here.

---

### Step 3: Configure env.py

**File:** `Backend/alembic/env.py`

**Replace the entire file with this:**

```python
"""Alembic environment configuration"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
from os.path import abspath, dirname

# Add parent directory to path so we can import our modules
sys.path.insert(0, dirname(dirname(abspath(__file__))))

# Import your Base and models
from database import Base, engine
from models import User, TweetThread, TweetHistory  # Import all models
from config import settings

# this is the Alembic Config object
config = context.config

# Set the database URL from your .env file
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the metadata from your Base
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Use the existing engine from database.py
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**Key Changes Made:**

1. **Line 9-10:** Added parent directory to Python path
2. **Line 12-14:** Import your `Base`, `engine`, and all models
3. **Line 15:** Import settings
4. **Line 21:** Set database URL from `.env` file
5. **Line 27:** Set `target_metadata = Base.metadata`
6. **Line 61:** Use existing engine instead of creating new one

---

### Step 4: Create Initial Migration

Now create your first migration to capture the current database state:

```bash
cd Backend
python -m alembic revision --autogenerate -m "Initial migration"
```

This creates a file in `alembic/versions/` like:

```
alembic/versions/xxxxxxxxxxxx_initial_migration.py
```

**What it contains:**

```python
def upgrade() -> None:
    # Creates all your tables
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        # ... all columns ...
    )
    # ... creates tweet_threads, tweet_histories ...

def downgrade() -> None:
    # Drops all tables
    op.drop_table('tweet_histories')
    op.drop_table('tweet_threads')
    op.drop_table('users')
```

---

### Step 5: Apply Migration

```bash
alembic upgrade head
```

**Output:**

```
INFO  [alembic.runtime.migration] Running upgrade  -> xxxxxxxxxxxx, Initial migration
```

Your database is now under version control! 🎉

---

## Common Migration Commands

### Check Current Migration Version

```bash
alembic current
```

Output:

```
xxxxxxxxxxxx (head)
```

### View Migration History

```bash
alembic history
```

Output:

```
<base> -> xxxxxxxxxxxx (head), Initial migration
```

### Create New Migration (Auto-detect changes)

```bash
alembic revision --autogenerate -m "Add phone_number to users"
```

**Example:** After adding `phone_number` to User model:

```python
class User(Base):
    # ... existing fields ...
    phone_number = Column(String, nullable=True)
```

Run the command above, and Alembic will detect the change and create a migration.

### Create Empty Migration (Manual)

```bash
alembic revision -m "Add custom data transformation"
```

Use this when you need to write custom SQL or data transformations.

### Upgrade to Latest Version

```bash
alembic upgrade head
```

### Upgrade One Step

```bash
alembic upgrade +1
```

### Downgrade One Step

```bash
alembic downgrade -1
```

### Downgrade to Specific Version

```bash
alembic downgrade <revision_id>
```

### Downgrade All (Back to Empty Database)

```bash
alembic downgrade base
```

**⚠️ Warning:** This drops all tables!

---

## Workflow: Making Database Changes

### Example: Add `is_admin` field to User

**Step 1: Modify Model**

Edit `Backend/models.py`:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # NEW FIELD
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ... relationships ...
```

**Step 2: Create Migration**

```bash
cd Backend
alembic revision --autogenerate -m "Add is_admin to users"
```

Alembic creates: `alembic/versions/yyyyyyyyyyyy_add_is_admin_to_users.py`

**Step 3: Review Migration**

Open the generated file and check:

```python
def upgrade() -> None:
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'is_admin')
```

**Step 4: Apply Migration**

```bash
alembic upgrade head
```

**Step 5: Verify**

```bash
alembic current
```

Done! ✅

---

## Code Changes Summary

### 1. alembic.ini

**Change:**

```ini
# Line 63 - Comment out hardcoded URL
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

### 2. alembic/env.py

**Replace entire file** with the code from Step 3 above.

**Key imports:**

```python
from database import Base, engine
from models import User, TweetThread, TweetHistory
from config import settings
```

**Key settings:**

```python
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
target_metadata = Base.metadata
connectable = engine  # Use existing engine
```

### 3. main.py (Optional - Remove Auto-Create Tables)

**Current code:**

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Tweet Generator API...")
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)  # ← Remove this when using Alembic
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    # ...
```

**After adopting Alembic:**

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Tweet Generator API...")

    # Remove Base.metadata.create_all() - use Alembic migrations instead
    # Tables should be created via: alembic upgrade head

    logger.info("Tweet Generator API started successfully")
    # ...
```

**Why?** Alembic manages table creation/updates, not `create_all()`.

---

## Migration File Structure

Each migration file looks like:

```python
"""Add is_admin to users

Revision ID: abc123def456
Revises: previous_revision
Create Date: 2024-01-20 10:30:00.123456
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123def456'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Apply changes"""
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))

def downgrade() -> None:
    """Revert changes"""
    op.drop_column('users', 'is_admin')
```

- **upgrade():** Apply changes (forward migration)
- **downgrade():** Revert changes (rollback)

---

## Best Practices

### 1. Always Review Auto-Generated Migrations

```bash
alembic revision --autogenerate -m "description"
```

Then **open the file** and verify:
- Alembic correctly detected your changes
- No unwanted changes included
- Downgrade logic is correct

### 2. Test Migrations

```bash
# Apply migration
alembic upgrade head

# Test your app
python main.py

# Rollback to test downgrade
alembic downgrade -1

# Re-apply
alembic upgrade head
```

### 3. Use Descriptive Messages

✅ Good:
```bash
alembic revision --autogenerate -m "Add is_admin field to users table"
```

❌ Bad:
```bash
alembic revision --autogenerate -m "update"
```

### 4. One Logical Change Per Migration

✅ Good:
- Migration 1: "Add is_admin to users"
- Migration 2: "Add phone_number to users"

❌ Bad:
- Migration 1: "Add is_admin, phone_number, and rename email"

### 5. Never Edit Applied Migrations

Once a migration is applied and committed to version control:
- **DO NOT** edit it
- **DO** create a new migration to fix issues

### 6. Backup Before Major Migrations

```bash
# SQLite backup
cp tweet_generator.db tweet_generator.db.backup

# Then run migration
alembic upgrade head
```

### 7. Add to .gitignore

Add this to your `.gitignore`:

```
# Database
*.db
*.db-journal

# But keep migrations
!alembic/versions/*.py
```

**Keep in version control:**
- ✅ `alembic.ini`
- ✅ `alembic/env.py`
- ✅ `alembic/versions/*.py` (all migration files)

**Don't commit:**
- ❌ `tweet_generator.db`
- ❌ `__pycache__`

---

## Troubleshooting

### Issue 1: "Can't locate revision identified by 'xxxx'"

**Problem:** Migration file missing or database out of sync

**Solution:**

```bash
# Check current version
alembic current

# Check history
alembic history

# If needed, stamp to specific version
alembic stamp head
```

### Issue 2: "Target database is not up to date"

**Problem:** Someone else added migrations

**Solution:**

```bash
# Pull latest migrations from git
git pull

# Apply new migrations
alembic upgrade head
```

### Issue 3: "Multiple heads" error

**Problem:** Two branches of migrations created

**Solution:**

```bash
# View branches
alembic branches

# Merge branches
alembic merge heads -m "Merge migration branches"

# Apply merged migration
alembic upgrade head
```

### Issue 4: "No module named 'models'"

**Problem:** Import path issue in `env.py`

**Solution:** Check `env.py` has:

```python
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))
```

### Issue 5: Alembic doesn't detect model changes

**Problem:** Model not imported in `env.py`

**Solution:** Make sure all models are imported:

```python
from models import User, TweetThread, TweetHistory  # Import ALL models
```

---

## Data Migrations

Sometimes you need to transform data, not just schema:

```python
"""Set all users to is_admin=False by default

Revision ID: abc123
"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Add column
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))

    # Set default values for existing users
    op.execute("UPDATE users SET is_admin = 0 WHERE is_admin IS NULL")

    # Make column non-nullable
    op.alter_column('users', 'is_admin', nullable=False)

def downgrade() -> None:
    op.drop_column('users', 'is_admin')
```

---

## Production Deployment

### Step 1: Commit Migrations

```bash
git add alembic/versions/*.py
git commit -m "Add migration: Add is_admin to users"
git push
```

### Step 2: On Production Server

```bash
# Pull latest code
git pull

# Apply migrations
alembic upgrade head

# Restart application
systemctl restart tweet-generator
```

### Step 3: Verify

```bash
alembic current
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `alembic init alembic` | Initialize Alembic |
| `alembic revision --autogenerate -m "msg"` | Create migration (auto-detect) |
| `alembic revision -m "msg"` | Create empty migration |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic upgrade +1` | Apply next migration |
| `alembic downgrade -1` | Rollback one migration |
| `alembic downgrade base` | Rollback all migrations |
| `alembic current` | Show current version |
| `alembic history` | Show migration history |
| `alembic stamp head` | Mark database as current |

---

## Complete Setup Checklist

- [ ] Install Alembic: `pip install alembic==1.13.1`
- [ ] Initialize: `alembic init alembic`
- [ ] Configure `alembic.ini` (comment out sqlalchemy.url)
- [ ] Configure `alembic/env.py` (import models, use existing engine)
- [ ] Create initial migration: `alembic revision --autogenerate -m "Initial migration"`
- [ ] Apply migration: `alembic upgrade head`
- [ ] Remove `Base.metadata.create_all()` from `main.py`
- [ ] Test: Make a model change, create migration, apply it
- [ ] Commit to git: `git add alembic/ alembic.ini`

---

## Summary

You now have:

✅ **Version-controlled database schema**
✅ **Safe migration workflow**
✅ **Production-ready deployment process**
✅ **Rollback capability**
✅ **Team collaboration on database changes**

**Key Files Modified:**

1. `alembic.ini` - Commented out hardcoded URL
2. `alembic/env.py` - Configured to use your models and settings
3. `main.py` - Remove `Base.metadata.create_all()` (optional)

**Start using Alembic:**

```bash
cd Backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

**You're all set! 🚀**
