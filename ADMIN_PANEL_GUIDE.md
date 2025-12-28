# Admin Panel Guide

Django-like admin interface for managing your Tweet Generator application.

---

## Overview

The admin panel provides a **Django-style interface** for managing:
- 👥 **Users** - View, edit, and manage user accounts
- 🐦 **Tweet Threads** - Browse and manage generated tweet threads
- 📊 **Tweet History** - Monitor generation history and analytics

Built with **SQLAdmin**, it offers:
- ✅ Full CRUD operations
- ✅ Search and filters
- ✅ Pagination
- ✅ Sorting
- ✅ Authentication
- ✅ Beautiful UI

---

## Installation

### Install Dependencies

```bash
pip install sqladmin==0.16.1 itsdangerous==2.1.2
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

---

## Accessing the Admin Panel

### 1. Start the Server

```bash
cd Backend
python main.py
```

### 2. Open Admin Panel

Visit: **`http://localhost:8000/admin`**

### 3. Login

Use any registered user credentials:
- **Username**: Your email (e.g., `admin@example.com`)
- **Password**: Your password

Currently, any active user can access the admin panel.

---

## Features

### 1. Users Management

**Path:** `/admin/user`

**Features:**
- View all registered users
- Search by username or email
- Filter by active status
- Sort by any column
- View user details
- Edit user information
- Activate/deactivate accounts

**Columns Displayed:**
- ID
- Username
- Email
- Active Status
- Created Date

**Actions:**
- ✏️ Edit user details
- 🔍 View full details
- 🗑️ Delete users

---

### 2. Tweet Threads Management

**Path:** `/admin/tweetthread`

**Features:**
- Browse all generated tweet threads
- Search by topic
- Filter by user, tweet count, or date
- View thread content (JSON)
- Edit thread details
- Delete threads

**Columns Displayed:**
- ID
- Topic
- Tweet Count
- User ID
- Created Date

**Details View:**
- Full tweet content
- Thread metadata
- Creation/update timestamps

---

### 3. Tweet History Management

**Path:** `/admin/tweethistory`

**Features:**
- Monitor all generation attempts
- Track success/failure rates
- View processing times
- Filter by status, user, or thread
- Analyze generation parameters

**Columns Displayed:**
- ID
- User ID
- Thread ID
- Status (Success/Failed)
- Processing Time
- Created Date

**Analytics:**
- See which generations succeeded
- Identify slow generations
- Track user activity

---

## User Interface

### Dashboard

When you log in, you'll see:

```
┌─────────────────────────────────────────┐
│     Tweet Generator Admin Panel         │
├─────────────────────────────────────────┤
│  📊 Dashboard                           │
│  👥 Users (15)                          │
│  🐦 Tweet Threads (127)                 │
│  📈 Tweet Histories (134)               │
└─────────────────────────────────────────┘
```

### List View

Each model has a list view with:
- **Search bar** at the top
- **Filters** on the right sidebar
- **Pagination** at the bottom
- **Action buttons** for each record

Example - Users List:

```
┌─────────────────────────────────────────────────────────────┐
│ Search: [________]                    [+ Create New User]   │
├─────┬──────────┬───────────────────┬────────┬──────────────┤
│ ID  │ Username │ Email             │ Active │ Created      │
├─────┼──────────┼───────────────────┼────────┼──────────────┤
│ 1   │ admin    │ admin@example.com │ ✓      │ 2024-01-15   │
│ 2   │ john     │ john@example.com  │ ✓      │ 2024-01-16   │
│ 3   │ jane     │ jane@example.com  │ ✗      │ 2024-01-17   │
└─────┴──────────┴───────────────────┴────────┴──────────────┘
  < 1 2 3 >  Showing 1-25 of 67 records
```

### Detail View

Click on any record to see full details:

```
┌─────────────────────────────────────────┐
│  User Details                           │
├─────────────────────────────────────────┤
│  ID: 1                                  │
│  Username: admin                        │
│  Email: admin@example.com               │
│  Active: Yes                            │
│  Created: 2024-01-15 10:30:00          │
│  Updated: 2024-01-20 14:25:00          │
│                                         │
│  [Edit] [Delete] [Back to List]        │
└─────────────────────────────────────────┘
```

### Edit View

Edit any record with a form:

```
┌─────────────────────────────────────────┐
│  Edit User                              │
├─────────────────────────────────────────┤
│  Username: [admin____________]          │
│  Email: [admin@example.com___]          │
│  Active: [✓] Is Active                  │
│                                         │
│  [Save Changes] [Cancel]                │
└─────────────────────────────────────────┘
```

---

## Common Tasks

### 1. View All Users

1. Click **"Users"** in the sidebar
2. Browse the list
3. Use search to find specific users
4. Filter by active status if needed

### 2. Edit a User

1. Go to Users list
2. Click on the user's row
3. Click **"Edit"**
4. Modify fields
5. Click **"Save Changes"**

### 3. View Tweet Threads

1. Click **"Tweet Threads"** in the sidebar
2. Search by topic
3. Click on a thread to see full content
4. View all tweets in the thread

### 4. Monitor Generation History

1. Click **"Tweet Histories"** in the sidebar
2. Filter by status (success/failed)
3. Sort by processing time to find slow generations
4. Check parameters used for each generation

### 5. Delete Records

1. Navigate to the record
2. Click **"Delete"**
3. Confirm deletion
4. Record and related data will be deleted

---

## Search & Filters

### Search

Available on all models:

**Users:**
- Search by username
- Search by email

**Tweet Threads:**
- Search by topic

**Tweet Histories:**
- Search by status

### Filters

**Users:**
- Filter by: Active status, Created date

**Tweet Threads:**
- Filter by: User ID, Tweet count, Created date

**Tweet Histories:**
- Filter by: Status, User ID, Thread ID, Created date

### Example: Find All Failed Generations

1. Go to **Tweet Histories**
2. In the right sidebar, find **"Status"** filter
3. Select **"failed"**
4. View all failed generations
5. Check error details in the parameters field

---

## Pagination

All lists support pagination:

- **Default**: 25 records per page (Users, Tweet Threads)
- **Default**: 50 records per page (Tweet Histories)

**Options:**
- 10 records per page
- 25 records per page
- 50 records per page
- 100 records per page
- 200 records per page (History only)

Change page size in the dropdown at the bottom.

---

## Security

### Current Setup

- **Authentication**: Required - uses your app's login system
- **Authorization**: Any active user can access admin (for development)

### Production Setup

For production, you should:

1. **Add admin flag to User model:**

```python
# In models.py
class User(Base):
    # ... existing fields ...
    is_admin = Column(Boolean, default=False)
```

2. **Update admin authentication:**

Uncomment lines in `admin.py`:

```python
# In admin.py, AdminAuth.login()
if not user.is_admin:  # Uncomment this
    return False       # And this
```

3. **Create admin user manually:**

```python
from database import SessionLocal
from models import User
from utils.auth_utils import hash_password

db = SessionLocal()
admin_user = User(
    username="admin",
    email="admin@example.com",
    hashed_password=hash_password("secure_admin_password"),
    is_active=True,
    is_admin=True  # Admin flag
)
db.add(admin_user)
db.commit()
```

---

## Customization

### Change Admin URL

In `admin.py`:

```python
admin = Admin(
    # ... other settings ...
    base_url="/custom-admin",  # Change from /admin
)
```

### Add Logo

```python
admin = Admin(
    # ... other settings ...
    logo_url="https://yoursite.com/logo.png",
)
```

### Customize Columns

In any Admin class (e.g., `UserAdmin`):

```python
# Show different columns
column_list = [User.id, User.email, User.created_at]

# Add more searchable columns
column_searchable_list = [User.username, User.email, User.id]

# Change labels
column_labels = {
    User.created_at: "Registration Date",
    User.is_active: "Account Active"
}
```

### Add Custom Actions

```python
class UserAdmin(ModelView, model=User):
    # ... existing code ...

    async def on_model_change(self, data, model, is_created, request):
        """Called when a model is created or updated"""
        if is_created:
            logger.info(f"New user created: {model.username}")
```

---

## Troubleshooting

### Issue 1: Can't Access /admin

**Problem:** 404 error when visiting `/admin`

**Solution:**
1. Make sure admin is initialized in `main.py`
2. Restart the server
3. Check logs for errors

### Issue 2: Login Fails

**Problem:** Can't log in to admin panel

**Solution:**
1. Verify you're using a registered user
2. Use **email** as username (not username)
3. Check password is correct
4. Ensure user is active

### Issue 3: Import Errors

**Problem:** `ModuleNotFoundError: No module named 'sqladmin'`

**Solution:**
```bash
pip install sqladmin itsdangerous
```

### Issue 4: Session Errors

**Problem:** Session-related errors

**Solution:**
Add session middleware if missing:
```python
from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
```

---

## Best Practices

### 1. Regular Monitoring

- Check Tweet Histories daily for failures
- Monitor processing times
- Review user activity

### 2. Data Cleanup

- Periodically delete old test data
- Archive old tweet threads
- Clean up failed generation records

### 3. Security

- Use strong admin passwords
- Limit admin access to trusted users
- Enable HTTPS in production
- Add IP restrictions if needed

### 4. Performance

- Use filters instead of scrolling through all records
- Archive old data to separate tables
- Monitor database size

---

## Keyboard Shortcuts

- `Ctrl + F` - Focus search box
- `Escape` - Close modals
- `Enter` - Submit forms
- `Backspace` - Go back (in some browsers)

---

## API Endpoints (Admin Backend)

The admin panel creates these endpoints:

- `GET /admin` - Admin dashboard
- `GET /admin/user` - Users list
- `GET /admin/tweetthread` - Tweet threads list
- `GET /admin/tweethistory` - History list
- `POST /admin/login` - Admin login
- `POST /admin/logout` - Admin logout

All admin endpoints are protected by authentication.

---

## Comparison with Django Admin

### Similarities

✅ Automatic CRUD interface
✅ Search and filters
✅ Pagination
✅ Model relationships
✅ Custom admin classes
✅ Authentication

### Differences

| Feature | Django Admin | SQLAdmin |
|---------|-------------|----------|
| Framework | Django | FastAPI |
| ORM | Django ORM | SQLAlchemy |
| Templates | Django templates | Jinja2 |
| Async Support | Limited | Full support |
| Setup | Automatic | Manual configuration |

---

## Future Enhancements

Potential improvements:

- [ ] Bulk actions (delete multiple records)
- [ ] Export to CSV
- [ ] Advanced analytics dashboard
- [ ] User activity logs
- [ ] Email notifications
- [ ] Custom widgets
- [ ] Rich text editor for content
- [ ] Image upload support

---

## Summary

You now have a fully functional admin panel with:

✅ **User Management** - Full CRUD for users
✅ **Tweet Thread Management** - Browse and manage threads
✅ **History Monitoring** - Track all generations
✅ **Search & Filters** - Find records quickly
✅ **Pagination** - Handle large datasets
✅ **Authentication** - Secure access
✅ **Beautiful UI** - Professional interface

**Access it at:** `http://localhost:8000/admin`

---

## Additional Resources

- [SQLAdmin Documentation](https://aminalaee.dev/sqladmin/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [Starlette Middleware](https://www.starlette.io/middleware/)

---

**Enjoy your Django-like admin panel! 🎉**
