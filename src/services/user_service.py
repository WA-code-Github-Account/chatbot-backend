from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from src.models.user import User
from src.models.session import Session
from passlib.context import CryptContext
from typing import Optional
from uuid import UUID
import uuid
from jose import jwt
from datetime import datetime, timedelta
from config.settings import settings
import logging


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Generate a hash for the given password"""
        return self.pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password"""
        try:
            # Find user by username
            stmt = select(User).where(User.username == username)
            result = await self.db_session.execute(stmt)
            user = result.scalar_one_or_none()

            if not user or not self.verify_password(password, user.hashed_password):
                return None

            return user
        except Exception as e:
            logger.error(f"Error authenticating user {username}: {str(e)}")
            return None

    async def create_user(self, username: str, email: str, password: str, role: str = "user") -> Optional[User]:
        """Create a new user with the given credentials"""
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_username(username)
            if existing_user:
                raise ValueError(f"User with username {username} already exists")

            existing_email = await self.get_user_by_email(email)
            if existing_email:
                raise ValueError(f"User with email {email} already exists")

            # Hash the password
            hashed_password = self.get_password_hash(password)

            # Create user instance
            user = User(
                id=uuid.uuid4(),
                username=username,
                email=email,
                hashed_password=hashed_password,
                role=role
            )

            # Add to session and commit
            self.db_session.add(user)
            await self.db_session.commit()
            await self.db_session.refresh(user)

            logger.info(f"User created with ID: {user.id}")
            return user
        except Exception as e:
            logger.error(f"Error creating user {username}: {str(e)}")
            await self.db_session.rollback()
            raise

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by their ID"""
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.db_session.execute(stmt)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            return None

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by their username"""
        try:
            stmt = select(User).where(User.username == username)
            result = await self.db_session.execute(stmt)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger.error(f"Error retrieving user {username}: {str(e)}")
            return None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email"""
        try:
            stmt = select(User).where(User.email == email)
            result = await self.db_session.execute(stmt)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger.error(f"Error retrieving user with email {email}: {str(e)}")
            return None

    async def create_session(self, user_id: UUID, ip_address: str = None, user_agent: str = None) -> Optional[Session]:
        """Create a new session for the user"""
        try:
            from datetime import datetime, timedelta

            # Create a unique session token
            import secrets
            session_token = secrets.token_urlsafe(32)

            # Session expires in 30 minutes (configurable)
            expires_at = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

            # Create session instance
            session = Session(
                id=uuid.uuid4(),
                user_id=user_id,
                session_token=session_token,
                expires_at=expires_at,
                ip_address=ip_address,
                user_agent=user_agent
            )

            # Add to session and commit
            self.db_session.add(session)
            await self.db_session.commit()
            await self.db_session.refresh(session)

            logger.info(f"Session created for user {user_id}")
            return session
        except Exception as e:
            logger.error(f"Error creating session for user {user_id}: {str(e)}")
            await self.db_session.rollback()
            raise

    async def validate_session(self, session_token: str) -> Optional[User]:
        """Validate a session token and return the associated user if valid"""
        try:
            # Find the session by token
            stmt = select(Session).where(
                Session.session_token == session_token,
                Session.active == True,
                Session.expires_at > datetime.utcnow()
            )
            result = await self.db_session.execute(stmt)
            session = result.scalar_one_or_none()

            if not session:
                return None

            # Get the associated user
            user = await self.get_user_by_id(session.user_id)
            return user
        except Exception as e:
            logger.error(f"Error validating session: {str(e)}")
            return None

    async def deactivate_session(self, session_token: str) -> bool:
        """Deactivate a specific session"""
        try:
            stmt = update(Session).where(
                Session.session_token == session_token
            ).values(active=False)

            result = await self.db_session.execute(stmt)
            await self.db_session.commit()

            if result.rowcount > 0:
                logger.info(f"Session {session_token} deactivated")
                return True
            else:
                logger.warning(f"No session found for token {session_token}")
                return False
        except Exception as e:
            logger.error(f"Error deactivating session {session_token}: {str(e)}")
            await self.db_session.rollback()
            return False