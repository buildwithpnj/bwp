# Learnings Log

### 1. Next.js App Router Static Compilations
- **Issue**: Next.js static prerender bails out or fails compile when `useSearchParams()` is invoked at the page root level without a wrapping component.
- **Solution**: Wrap any component evaluating URL search queries in a `<Suspense>` boundary block.

### 2. Google OAuth Scope Accumulations
- **Issue**: Connecting Google Drive initially does not grant calendar permissions unless explicitly requested.
- **Solution**: Request scopes incrementally or bundle `"https://www.googleapis.com/auth/drive"` and `"https://www.googleapis.com/auth/calendar"` together during authorization URLs creation.

### 3. Fernet Encryption Conversions
- **Issue**: Fernet encryption requires byte parameters, whereas SQL columns require strings.
- **Solution**: Decode ciphertext blocks back to standard UTF-8 strings before commit triggers, and re-encode to bytes before decryption cycles.
