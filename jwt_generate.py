from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"

payload = {
    "sub": "user123",
    "name": "John Doe",
    "role": "admin",
}

token = jwt.encode(
    {**payload, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
    SECRET_KEY,
    algorithm=ALGORITHM,
)

print("Generated JWT Token:")
print(token)

decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print("\nDecoded Payload:")
print(decoded)
