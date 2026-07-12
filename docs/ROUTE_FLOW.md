# Route Flow Directory

This file documents the routing flow between public channels and authenticated Warborn dashboard workspaces.

## Public Landing Page Routing
* `/warborn`: Product introduction and feature display.
* `/warborn/preview`: Interactive agent sandbox running restricted preview.
* `/request-access`: Intake form for requesting developer access credentials.
* `/auth/login`: Clean router redirect pointing users directly to `/login`.

## Authenticated Application Routing
* `/login`: Standard developer OS credential authentication interface.
* `/warborn/app`: Protected terminal chat console with full agent capabilities.
* `/dashboard`: Mission Control personal OS overview page.
