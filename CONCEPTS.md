# Middleware & CORS — Concepts

## What is Middleware?

Middleware is a layer that sits **between the client request and the route handler**. Every request passes through middleware before reaching your endpoint, and every response passes through it on the way back.

```
Client → [Middleware 1] → [Middleware 2] → Route Handler → [Middleware 2] → [Middleware 1] → Client
```

### Common Use Cases

- Logging every request (method, path, time taken)
- Adding security headers (`X-Frame-Options`, `X-Content-Type-Options`)
- Rate limiting
- Request validation / body parsing
- Authentication checks (before route handler)
- CORS headers
- Compression (gzip)

### How We Implemented It

We created a `ProcessTimeMiddleware` in `backend_app/core/middleware.py`:

```python
class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{elapsed:.4f}s"
        print(f"[{request.method}] {request.url.path} → {response.status_code} ({elapsed:.3f}s)")
        return response
```

**What it does:**
1. Records the start time **before** the request reaches the route
2. Calls `call_next(request)` — passes the request through the chain
3. After the response is generated, calculates how long it took
4. Adds `X-Process-Time` header to the response
5. Logs the method, path, status code, and time to console

**Registered in `main.py`:**
```python
app.add_middleware(ProcessTimeMiddleware)
```

### Try it

```bash
curl -s -D - http://localhost:8006/api/v1/me \
  -H "Authorization: Bearer $TOKEN" | head -20
```

Look for `x-process-time: 0.0023s` in the response headers.

---

## What is CORS?

**CORS** = **Cross-Origin Resource Sharing**

### The Problem

Browsers enforce a **Same-Origin Policy**: a web page from `http://example.com` cannot make requests to `http://api.com` unless the server explicitly allows it.

```
Browser (localhost:3000) → ❌ BLOCKED → API (localhost:8006)
```

This protects users from malicious sites making unauthorized API calls with their cookies.

### How CORS Fixes It

The server sends special HTTP headers telling the browser which origins are allowed.

### The Headers

| Header | What it does |
|--------|-------------|
| `Access-Control-Allow-Origin` | Which origins are allowed (`*` = all) |
| `Access-Control-Allow-Methods` | Which HTTP methods are allowed (`GET, POST, PUT, DELETE`) |
| `Access-Control-Allow-Headers` | Which request headers are allowed (`Content-Type, Authorization`) |
| `Access-Control-Allow-Credentials` | Whether cookies/auth can be sent |

### Preflight Requests (OPTIONS)

For non-simple requests (e.g., `POST` with JSON, custom headers like `Authorization`), the browser first sends an **OPTIONS** request to check permissions before the actual request.

```
Browser → OPTIONS /api/v1/items → Server
                                    ↓
Browser ←  204 No Content  ← (CORS headers in response)
                                    ↓
Browser → POST /api/v1/items → Server (allowed!)
```

### How We Implemented It

In `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow any frontend domain
    allow_credentials=True,
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers (Authorization, Content-Type, etc.)
)
```

**`allow_origins=["*"]`** — allows any origin (okay for development). In production, restrict it:

```python
allow_origins=[
    "https://myapp.com",
    "https://admin.myapp.com",
]
```

### Why Our /docs Was Breaking

Before adding CORS, Swagger UI (served at `http://localhost:8006/docs`) was making `fetch()` calls to `http://localhost:8006/api/v1/login`. Even though it's the same server, the browser treated the docs page origin differently, causing **"Failed to fetch"** errors.

---

## Middleware vs CORS — How They Differ

| | Middleware | CORS |
|---|---|---|
| **Purpose** | Process/manipulate requests and responses | Allow/restrict cross-origin browser access |
| **Layer** | Application logic layer | Security layer (browser-side) |
| **Headers** | Any custom headers (`X-Process-Time`) | Specific CORS headers (`Access-Control-*`) |
| **Applies to** | All clients (browser, mobile, curl) | Browsers only (curl ignores CORS) |

## Middleware Order Matters

In FastAPI, middleware runs in the **order they are added** (first added = outermost):

```python
app.add_middleware(CORSMiddleware, ...)    # 1st — handles CORS first
app.add_middleware(ProcessTimeMiddleware)  # 2nd — logs timing
```

```
Client → CORSMiddleware → ProcessTimeMiddleware → Route → ProcessTimeMiddleware → CORSMiddleware → Client
```

CORS must come first so preflight `OPTIONS` requests are handled before any other middleware interacts with them.
