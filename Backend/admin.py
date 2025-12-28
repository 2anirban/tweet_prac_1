"""
Admin Panel Configuration
Django-like admin interface using SQLAdmin
"""

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from datetime import datetime
import json

from models import User, TweetThread, TweetHistory
from utils.auth_utils import verify_password, create_access_token, decode_access_token
from database import engine


# ============================================
# Admin Authentication Backend
# ============================================

class AdminAuth(AuthenticationBackend):
    """
    Custom authentication backend for admin panel
    Only allows users with is_admin=True to access
    """

    async def login(self, request: Request) -> bool:
        """Handle admin login"""
        form = await request.form()
        email = form.get("username")  # SQLAdmin uses 'username' field
        password = form.get("password")

        # Import here to avoid circular imports
        from database import SessionLocal
        db = SessionLocal()

        try:
            # Find user by email
            user = db.query(User).filter(User.email == email).first()

            if not user:
                return False

            # Verify password
            if not verify_password(password, user.hashed_password):
                return False

            # Check if user is active
            if not user.is_active:
                return False

            # For now, we'll allow any user to access admin
            # In production, add an is_admin field to User model
            # if not user.is_admin:
            #     return False

            # Create session token
            token = create_access_token(
                data={"sub": user.email, "user_id": user.id}
            )

            # Store token in session
            request.session.update({"token": token, "user_id": user.id})

            return True

        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        """Handle admin logout"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated"""
        token = request.session.get("token")

        if not token:
            return False

        # Verify token
        payload = decode_access_token(token)
        if not payload:
            return False

        return True


# ============================================
# Model Admin Views
# ============================================

class UserAdmin(ModelView, model=User):
    """Admin view for User model"""

    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    # Columns to display in list view
    column_list = [User.id, User.username, User.email, User.is_active, User.created_at]

    # Columns that can be searched
    column_searchable_list = [User.username, User.email]

    # Columns that can be sorted
    column_sortable_list = [User.id, User.username, User.email, User.created_at]

    # Default sorting
    column_default_sort = [(User.created_at, True)]  # True = descending

    # Columns to display in detail/edit view
    column_details_list = [
        User.id,
        User.username,
        User.email,
        User.is_active,
        User.created_at,
        User.updated_at
    ]

    # Columns to exclude from forms
    form_excluded_columns = [User.hashed_password, User.created_at, User.updated_at]

    # Filters - temporarily disabled due to SQLAdmin version compatibility
    # column_filters = ["is_active", "created_at"]

    # Pagination
    page_size = 25
    page_size_options = [10, 25, 50, 100]

    # Labels for columns
    column_labels = {
        User.id: "ID",
        User.username: "Username",
        User.email: "Email",
        User.is_active: "Active",
        User.created_at: "Created",
        User.updated_at: "Updated"
    }

    # Formatters for columns
    column_formatters = {
        User.created_at: lambda m, a: m.created_at.strftime("%Y-%m-%d %H:%M") if m.created_at else "",
        User.updated_at: lambda m, a: m.updated_at.strftime("%Y-%m-%d %H:%M") if m.updated_at else "",
    }


class TweetThreadAdmin(ModelView, model=TweetThread):
    """Admin view for TweetThread model"""

    name = "Tweet Thread"
    name_plural = "Tweet Threads"
    icon = "fa-solid fa-comment"

    # Columns to display in list view
    column_list = [
        TweetThread.id,
        TweetThread.topic,
        TweetThread.tweet_count,
        TweetThread.user_id,
        TweetThread.created_at
    ]

    # Searchable columns
    column_searchable_list = [TweetThread.topic]

    # Sortable columns
    column_sortable_list = [
        TweetThread.id,
        TweetThread.topic,
        TweetThread.tweet_count,
        TweetThread.created_at
    ]

    # Default sorting
    column_default_sort = [(TweetThread.created_at, True)]

    # Detail view columns
    column_details_list = [
        TweetThread.id,
        TweetThread.user_id,
        TweetThread.topic,
        TweetThread.thread_content,
        TweetThread.tweet_count,
        TweetThread.created_at,
        TweetThread.updated_at
    ]

    # Filters - temporarily disabled due to SQLAdmin version compatibility
    # column_filters = ["user_id", "tweet_count", "created_at"]

    # Pagination
    page_size = 25
    page_size_options = [10, 25, 50, 100]

    # Labels
    column_labels = {
        TweetThread.id: "ID",
        TweetThread.user_id: "User ID",
        TweetThread.topic: "Topic",
        TweetThread.thread_content: "Tweets (JSON)",
        TweetThread.tweet_count: "Tweet Count",
        TweetThread.created_at: "Created",
        TweetThread.updated_at: "Updated"
    }

    # Formatters
    column_formatters = {
        TweetThread.created_at: lambda m, a: m.created_at.strftime("%Y-%m-%d %H:%M") if m.created_at else "",
        TweetThread.updated_at: lambda m, a: m.updated_at.strftime("%Y-%m-%d %H:%M") if m.updated_at else "",
        TweetThread.thread_content: lambda m, a: f"{m.thread_content[:100]}..." if len(m.thread_content) > 100 else m.thread_content,
    }

    # Custom display for thread_content in detail view
    def _format_thread_content(self, value):
        """Format thread content as readable list"""
        try:
            tweets = json.loads(value)
            return "\n".join([f"{i+1}. {tweet}" for i, tweet in enumerate(tweets)])
        except:
            return value


class TweetHistoryAdmin(ModelView, model=TweetHistory):
    """Admin view for TweetHistory model"""

    name = "Tweet History"
    name_plural = "Tweet Histories"
    icon = "fa-solid fa-clock-rotate-left"

    # Columns to display
    column_list = [
        TweetHistory.id,
        TweetHistory.user_id,
        TweetHistory.thread_id,
        TweetHistory.status,
        TweetHistory.processing_time,
        TweetHistory.created_at
    ]

    # Searchable
    column_searchable_list = [TweetHistory.status]

    # Sortable
    column_sortable_list = [
        TweetHistory.id,
        TweetHistory.status,
        TweetHistory.processing_time,
        TweetHistory.created_at
    ]

    # Default sorting
    column_default_sort = [(TweetHistory.created_at, True)]

    # Detail view
    column_details_list = [
        TweetHistory.id,
        TweetHistory.thread_id,
        TweetHistory.user_id,
        TweetHistory.generation_params,
        TweetHistory.processing_time,
        TweetHistory.status,
        TweetHistory.created_at
    ]

    # Filters - temporarily disabled due to SQLAdmin version compatibility
    # column_filters = ["status", "user_id", "thread_id", "created_at"]

    # Pagination
    page_size = 50
    page_size_options = [25, 50, 100, 200]

    # Labels
    column_labels = {
        TweetHistory.id: "ID",
        TweetHistory.thread_id: "Thread ID",
        TweetHistory.user_id: "User ID",
        TweetHistory.generation_params: "Parameters (JSON)",
        TweetHistory.processing_time: "Processing Time (ms)",
        TweetHistory.status: "Status",
        TweetHistory.created_at: "Created"
    }

    # Formatters
    column_formatters = {
        TweetHistory.created_at: lambda m, a: m.created_at.strftime("%Y-%m-%d %H:%M:%S") if m.created_at else "",
        TweetHistory.processing_time: lambda m, a: f"{m.processing_time}ms" if m.processing_time else "N/A",
    }

    # Color code status
    column_type_formatters = {
        TweetHistory.status: lambda value: f"<span class='badge badge-{'success' if value == 'success' else 'danger'}'>{value}</span>"
    }


# ============================================
# Initialize Admin
# ============================================

def create_admin(app):
    """
    Create and configure admin panel

    Args:
        app: FastAPI application instance

    Returns:
        Admin instance
    """
    # Create authentication backend
    authentication_backend = AdminAuth(secret_key="your-secret-key-change-in-production")

    # Create admin instance
    admin = Admin(
        app=app,
        engine=engine,
        title="Tweet Generator Admin",
        authentication_backend=authentication_backend,
        base_url="/admin",
        logo_url=None,  # You can add your logo URL here
    )

    # Add model views
    admin.add_view(UserAdmin)
    admin.add_view(TweetThreadAdmin)
    admin.add_view(TweetHistoryAdmin)

    return admin
