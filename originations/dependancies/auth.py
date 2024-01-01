## Initial Basic Auth
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from originations.config.config import settings

from originations.services.authentication.api_authentication import authenticate
from originations.services.secretsmanager.secrets import access_secret_version


security = HTTPBasic()


## Authentication code
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    # correct_username = secrets.compare_digest(credentials.username, "user")
    # correct_password = authenticate(credentials.password, settings.password)
    # if not (correct_username and correct_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Basic"},
    #     )
    return credentials.username
