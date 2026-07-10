# Troubleshooting Guide — Warborn OS

Common errors and debugging strategies for Google Drive integration.

## 1. Missing Refresh Token in Callback
* **Symptom**: Callback route returns `OAuth connection failed: Google did not return a refresh token.`
* **Cause**: Google only returns `refresh_token` on the **first** consent screen authorize. If the user previously authorized the app, Google skips returning the refresh token on re-authorization.
* **Solution**: The user must go to Google account settings -> Security -> Third-party apps with account access, remove access for 'Warborn OS', and then retry connecting. This forces Google to display the full consent prompt containing the refresh token.

## 2. Invalid Encryption Key Error
* **Symptom**: `InvalidToken` raised during download or upload.
* **Cause**: The `ENCRYPTION_KEY` has been changed between restarts. The database contains tokens encrypted with the old key, which cannot be decrypted.
* **Solution**: Check if your `ENCRYPTION_KEY` was rotated. If rotated, the old providers must be disconnected and re-authorized.

## 3. Quota Exceeded (90% capacity)
* **Symptom**: Logs display warning that preferred provider capacity is exceeded.
* **Cause**: The active Google Drive account has used over 90% of its available space.
* **Solution**: The manager will automatically route uploads to the next active provider. Clean up space in the Google Drive account or link another account.
