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

### 4. FastAPI Event Loop Thread Pollution
- **Issue**: Invoking `asyncio.run()` inside background operations closes the default thread loop, causing subsequent uvicorn requests to crash with `RuntimeError: Event loop is closed`.
- **Solution**: Run sub-processes on standard threads or use `asyncio.to_thread()` to safely delegate blocking operations to isolated threads.

### 5. High-Framerate Animation DOM Bypasses
- **Issue**: Running real-time coordinates state updates in React loops (e.g. 60 FPS particle tracers) causes adjacent text inputs (like the notes editor) to blink and lose cursor focus due to continuous re-renders.
- **Solution**: Manipulate DOM nodes directly via `el.style.transform = ...` inside canvas loops, bypassing the React virtual DOM.

### 6. Hook Reference Stability
- **Issue**: Declaring arrays (e.g. phrases lists) or calculation helpers inside rendering scope triggers infinite loops when referenced in `useEffect` dependency lists.
- **Solution**: Hoist constant arrays outside the component blocks and wrap rendering calculators in stable `useCallback` hooks.

