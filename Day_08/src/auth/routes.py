from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from sqlalchemy.ext.asyncio.session import AsyncSession

# Configuration and Database
from src.config import config
from src.db.main import get_session
from src.celery_task import send_email
from src.db.redis import add_jti_to_blocklist # Uncommented if Redis is used

# Email/Messaging
from src.mail import create_message, mail

# Schemas and Exceptions
from src.exception import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken
from .schemas import UserCreation, UserModel, UserLoginModel, UserBooksModel, EmailModel, PasswordRequestModel,PasswordResetConfirmModel

# Core Logic
from .service import UserService
from .utils import create_access_token, decode_token, verify_passwd, create_url_safe_token, decode_url_safe_token, generate_passwd_hash
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses
    html = "<h1>Welcome to the App</h1>"
    subject = "Welcome to out app"
    
    send_email.delay(emails, subject, html)
    
    return {"message":"Email sent successfully"}
    

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data : UserCreation, bg_tasks: BackgroundTasks,
                              session : AsyncSession  = Depends(get_session)):
    email = user_data.email
    
    user_exists = await user_service.user_exists(email, session)
    
    if user_exists:
        raise UserAlreadyExists()
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with {email} already exists.")
    
    new_user = await user_service.create_user(user_data, session)
    
    token = create_url_safe_token({"email": email})
    print(token)
    
    link = f"http://{config.DOMAIN}/api/v1/auth/verify/{token}"
    
    html_message = f"""
                    <h1>Verify your Email</h1>
                    <p>Please click this <a href="{link}">verification link</a> to verify your email</p>
                    """
                    
    email = [email]
    subject = "Verify your email"
    
    send_email.delay(email, subject, html_message)
    
    return {"message":"Account created! Check email to verify your account",
            "user":new_user}



@auth_router.get('/verify/{token}')
async def verfiy_user_account(token:str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    print(token_data)
    
    user_email = token_data.get('email')
    
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)        
        if not user:
            raise UserNotFound()
        
        await user_service.update_user(user, {'is_verified':True}, session)
        
        return JSONResponse(content={"message":"Account verified successfully"},
                            status_code=status.HTTP_200_OK)
        
    return JSONResponse(content={"message":"Error occured during verification"},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@auth_router.post('/login')
async def login_users(login_data : UserLoginModel,
                      session : AsyncSession  = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    
    user = await user_service.get_user_by_email(email, session)
    
    if user is not None:
        password_valid = verify_passwd(password, user.password_hash)
        
        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid),
                    'role' : user.role
                }
            )
            
            refresh_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            
            return JSONResponse(
                content={
                    "message":"Login successful!",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid)
                    }
                }
            )
            
    raise InvalidCredentials()
    # raise HTTPException(
    #     status_code=status.HTTP_403_FORBIDDEN,
    #     detail="Imvalid Email or Password")
    
    

@auth_router.get('/refresh_token')
async def get_new_access_token(token_details : dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])
        return JSONResponse(content={"access_token":new_access_token})
    
    raise InvalidToken()
    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                     detail="Invalid or expired token")
    


@auth_router.get('/me', response_model=UserBooksModel)
async def get_current_user(user = Depends(get_current_user), _: bool = Depends(role_checker)):
    return user

    
@auth_router.get("/logout")
async def revoke_token(token_details : dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    
    await add_jti_to_blocklist(jti)
    
    return JSONResponse(
        content={"message":"Logged out successfully"},
        status_code=status.HTTP_200_OK
    )


"""
    1. Provide the email -> password reset request
    2. send password reset link
    3. reset password -> password reset confirm
"""

@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordRequestModel):
    email = email_data.email

    # MUST use URL SAFE TOKEN, not JWT !!!
    token = create_url_safe_token({"email": email})
    print("PASSWORD RESET TOKEN:", token)


    link = f"http://{config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
        <h1>Reset your password</h1>
        <p>Please click this <a href="{link}">link</a> to reset your password</p>
    """

    message = create_message(
        recipients=[email],
        subject="Reset your password",
        body=html_message
    )

    await mail.send_message(message)

    return {"message": "Password reset email sent"}


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session)
):
    # decode using URLSafeTimedSerializer
    token_data = decode_url_safe_token(token)
    print("PASSWORD RESET Account TOKEN:", token_data)


    if not token_data:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password reset token"
        )

    user_email = token_data.get("email")
    if not user_email:
        raise HTTPException(status_code=400, detail="Invalid token payload")

    if passwords.new_password != passwords.confirm_new_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    user = await user_service.get_user_by_email(user_email, session)
    if not user:
        raise UserNotFound()

    password_hash = generate_passwd_hash(passwords.new_password)

    await user_service.update_user(
        user,
        {"password_hash": password_hash},
        session
    )

    return JSONResponse(
        content={"message": "Password reset successfully"},
        status_code=200
    )
