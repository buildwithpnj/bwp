# Security Spec & Hardening Matrix (11_SECURITY_GUIDE.md)

This document maps the security configurations, content validation pipelines, and credentials management patterns designed to protect the **BuildWithPNJ** platform.

---

## 1. HTTP Security Headers

Next.js is configured with strict security headers inside `next.config.js` for all incoming requests:

- **Content Security Policy (CSP)**: Restricts scripts and style sources to prevent malicious code execution:
  ```
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https://github.com;
  connect-src 'self' https://api.github.com;
  ```
- **Strict-Transport-Security (HSTS)**: Forces connections over HTTPS.
- **X-Frame-Options**: Set to `DENY` to prevent clickjacking attacks in iframe wrappers.
- **X-Content-Type-Options**: Set to `nosniff` to enforce MIME type verification.

---

## 2. API Rate Limiting

To safeguard FastAPI backend endpoints against denial-of-service (DoS) attempts and brute-forcing:
- **Redis Token Bucket**: Expose a rate-limiting middleware using Redis.
- **Limits Matrix**:
  - `POST /auth/login`: Maximum of **5 requests per minute** per IP.
  - `/api/v1/telemetry`: Maximum of **60 requests per minute** per IP.

---

## 3. Input Sanitization & XSS Mitigation

- **Pydantic Validation**: All FastAPI request parameters are strictly validated using Pydantic schemas (e.g. email checks, character limit controls).
- **HTML Sanitization**: When rendering user inputs or parsed markdown descriptions, HTML tags are parsed and cleaned using sanitization libraries to remove scripts.

---

## 4. Secrets & Credentials Management

- **Zero Hardcoded Secrets**: Access tokens, Postgres URIs, and GitHub client secrets must only be loaded via Environment Variables (`.env` files in development, secure Vercel environment storage in production).
- **Environment Schema Verification**: Build scripts verify the presence of required variables before starting compiles to prevent runtime failures:
  ```typescript
  const requiredEnv = ['DATABASE_URL', 'JWT_SECRET', 'GITHUB_TOKEN'];
  requiredEnv.forEach(env => {
    if (!process.env[env]) throw new Error(`Missing environment variable: ${env}`);
  });
  ```
- **Service Tokens**: Supabase service-role keys must only be accessed inside isolated backend code paths and never exposed to the client bundle.
