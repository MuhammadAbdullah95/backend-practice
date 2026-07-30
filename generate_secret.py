import secrets

secret_key = secrets.token_urlsafe(64)

print("Generated SECRET_KEY:")
print(secret_key)
