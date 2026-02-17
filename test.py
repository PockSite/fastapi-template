from app.core.security import verify_access_token

token = ""
payload = verify_access_token(token)
print(payload)