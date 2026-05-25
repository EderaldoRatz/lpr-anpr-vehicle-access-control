"""
Authentication API endpoints.
Handles user login, registration, and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import logging
from app.database import get_db
from app.security import TokenManager
from app.models.user import User, UserRole
from app.schemas import UserCreate, UserResponse, TokenResponse
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system.
    
    - **username**: Unique username (3-50 chars)
    - **email**: Valid email address
    - **full_name**: User's full name
    - **password**: Password (minimum 8 chars)
    """
    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            logger.warning(f"Registration attempt with existing username: {user_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            logger.warning(f"Registration attempt with existing email: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            password_hash=hash_password(user_data.password),
            role=UserRole.VIEWER
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"✅ New user registered: {user_data.username}")
        return new_user
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(username: str, password: str, db: Session = Depends(get_db)):
    """
    Login user and get JWT tokens.
    
    - **username**: User's username or email
    - **password**: User's password
    
    Returns access_token and refresh_token
    """
    try:
        # Find user by username or email
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            logger.warning(f"Login attempt with invalid username: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not verify_password(password, user.password_hash):
            logger.warning(f"Login attempt with wrong password for: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login attempt with inactive user: {username}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Generate tokens
        access_token = TokenManager.create_access_token(
            data={"sub": user.id, "username": user.username, "role": user.role}
        )
        refresh_token = TokenManager.create_refresh_token(
            data={"sub": user.id}
        )
        
        logger.info(f"✅ User logged in: {username}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token from login
    """
    try:
        payload = TokenManager.verify_token(refresh_token)
        
        # Create new access token
        access_token = TokenManager.create_access_token(
            data={"sub": payload["sub"]}
        )
        
        logger.info(f"✅ Token refreshed for user: {payload['sub']}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    except Exception as e:
        logger.error(f"❌ Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: dict = Depends(TokenManager.verify_token), db: Session = Depends(get_db)):
    """
    Get current logged-in user information.
    """
    try:
        user = db.query(User).filter(User.id == current_user["sub"]).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except Exception as e:
        logger.error(f"❌ Error fetching user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user"
        )
