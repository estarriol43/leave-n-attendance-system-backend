# API modify note
## POST /api/auth/login
### Modify reason
- Modify request format to comply with `OAuth2PasswordRequestForm`
    - Modify the field name from "email" to "username", but the content that you need to fill in is still user's email.
- Modify response format to let fastAPI Swagger UI automatically get token and  speedup backen testing
### request
```json
{
  "username": "user@example.com",
  "password": "securepassword"
}
```

### response
```json
{
    "access_token": "jwt_token",
    "token_type": "bearer"
}
```