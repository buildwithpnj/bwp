# Environment Configuration — Warborn OS

This document explains the environment variables required for the storage subsystem.

## Required Environment Variables

All variables should be added to the `.env` file in the root directory.

| Variable | Description |
|---|---|
| `GOOGLE_CLIENT_ID` | OAuth 2.0 Web Client ID generated in Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | OAuth 2.0 Web Client Secret generated in Google Cloud Console |
| `GOOGLE_REDIRECT_URI` | Callback endpoint of the app (default: `http://localhost:3000/storage/callback`) |
| `ENCRYPTION_KEY` | Custom encryption key string used to encrypt refresh tokens |

## Dynamic Storage Seeding Variables (Optional)

Configure these keys to automatically register Drive A, Drive B, and Drive C inside the database on first boot:

```env
# Drive A Config
GOOGLE_DRIVE_A_REFRESH_TOKEN=1//...
GOOGLE_DRIVE_A_FOLDER_ID=root
GOOGLE_DRIVE_A_EMAIL=drivea@example.com

# Drive B Config
GOOGLE_DRIVE_B_REFRESH_TOKEN=1//...
GOOGLE_DRIVE_B_FOLDER_ID=root
GOOGLE_DRIVE_B_EMAIL=driveb@example.com

# Drive C Config
GOOGLE_DRIVE_C_REFRESH_TOKEN=1//...
GOOGLE_DRIVE_C_FOLDER_ID=root
GOOGLE_DRIVE_C_EMAIL=drivec@example.com
```
