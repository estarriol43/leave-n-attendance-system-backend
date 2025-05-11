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
## POST /api/leave-requests
- We change the basic unit of leave from half day to the whole day, so I remove the `start_half_day` and `end_half_day` field in the request
### request
```json
{
  "leave_type_id": 1,
  "start_date": "2023-12-24",
  "end_date": "2023-12-31",
  "reason": "Year-end holiday",
  "proxy_user_id": 3
}
```

## GET /api/leave-requests
- ADD two query parameter `page` and `per_page` to support pagination
### query parameters
- status (optional): Filter by status (Pending, Approved, Rejected)
- startDate (optional): Filter by start date
- endDate (optional): Filter by end date
- page: Which page you want to get
- per_page: How many entries per page