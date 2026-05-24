---
name: flareauth-restish
description: Operate FlareAuth Management APIs with Restish OAuth PKCE login
user-invocable: false
allowed-tools:
  - Bash
---

# FlareAuth Restish - Operational Procedures

Use this skill when an agent needs safe terminal access to a deployed FlareAuth Management API. The default path uses Restish OAuth authorization code with PKCE through the built-in public `flareauth-cli` client. Do not ask for client secrets, API keys, or copied bearer tokens.

## Prerequisites

- `restish` is installed and available on `PATH`.
- `FLAREAUTH` is the deployed FlareAuth base URL, for example `https://auth.example.com`.
- The first login can open a browser on the same machine, or the operator can complete the browser login flow.
- The user who authorizes Restish has admin or management permission in that FlareAuth deployment.
- The deployment includes the built-in public native client:
  - client id: `flareauth-cli`
  - no client secret
  - PKCE required
  - redirect URIs include `http://127.0.0.1:8484/callback` and `http://localhost:8484/callback`
  - scopes include `openid offline_access management:read management:write`

## Session Setup

Set these variables at the start of every session:

```bash
export FLAREAUTH="https://auth.example.com"
export FA_API="flareauth"
export FA_MGMT="$FLAREAUTH/api/management"
```

Confirm the target before any mutation:

```bash
printf 'Target FlareAuth: %s\nManagement API: %s\n' "$FLAREAUTH" "$FA_MGMT"
```

## First Run

1. Confirm the OpenAPI document is reachable. The Management OpenAPI operation is `getManagementOpenApi`.

```bash
restish get "$FA_MGMT/openapi.json" -o json >/dev/null
```

2. Configure a named Restish API. Use the FlareAuth base URL or the Management OpenAPI URL when prompted. Select OAuth2 authorization code when Restish asks for auth, use client id `flareauth-cli`, leave client secret empty, use redirect URL `http://127.0.0.1:8484/callback`, and request scopes `openid offline_access management:read management:write`.

```bash
restish api configure "$FA_API"
restish api sync "$FA_API"
```

3. Trigger the OAuth PKCE login with a harmless read. Restish starts a local callback listener on port `8484`, opens a browser, exchanges the authorization code, and caches tokens for later commands.

```bash
restish get "$FA_MGMT/readiness" -o json
```

Authorize as an admin or management-capable user. Later commands reuse the cached Restish token and refresh it when possible.

## Guardrails

- Print and inspect `$FLAREAUTH` and `$FA_MGMT` before any `post`, `put`, `patch`, or `delete`.
- Never print raw secrets, bearer tokens, `restish auth-header` output, or Restish token cache contents.
- After every write, run the matching `get` or `list` command and verify the returned state.
- Respect `401` and `403`. Do not bypass authorization, use another user's session, or inject copied tokens.
- Prefer narrow `patch` bodies over broad rewrites.
- Treat `flareauth-cli` and any other `systemManaged` application as protected. Do not update or delete system-managed clients.
- Avoid broad destructive commands. Delete only explicitly named test or operator-approved resources.

## Readiness

Operations: `getReadiness`, `getManagementOpenApi`.

```bash
restish get "$FA_MGMT/readiness" -o json
restish get "$FA_MGMT/openapi.json" -o json >/dev/null
```

## Applications

Operations: `listApplications`, `getApplication`, `createApplication`, `updateApplication`, `deleteApplication`, `listRedirectUris`, `replaceRedirectUris`.

```bash
# List applications.
restish get "$FA_MGMT/applications" -o json

# Get one application.
APP_ID="app_123"
restish get "$FA_MGMT/applications/$APP_ID" -o json

# Create an application. Keep scopes ordinary; management scopes are reserved for flareauth-cli.
restish post "$FA_MGMT/applications" \
  name:"Example Web App" \
  type:web \
  redirectUris:'["https://app.example.com/callback"]' \
  grantTypes:'["authorization_code","refresh_token"]' \
  scopes:'["openid","profile","email"]' \
  -o json

# Update one field at a time when possible, then verify.
restish patch "$FA_MGMT/applications/$APP_ID" name:"Example Web App - Production" -o json
restish get "$FA_MGMT/applications/$APP_ID" -o json

# Replace redirect URIs as a deliberate whole-list operation, then verify.
restish put "$FA_MGMT/applications/$APP_ID/redirect-uris" \
  redirectUris:'["https://app.example.com/callback","https://app.example.com/oauth/callback"]' \
  -o json
restish get "$FA_MGMT/applications/$APP_ID/redirect-uris" -o json

# Delete only a confirmed non-system-managed application, then verify it is gone.
restish delete "$FA_MGMT/applications/$APP_ID"
restish get "$FA_MGMT/applications/$APP_ID" --rsh-ignore-status-code -o json
```

Before deleting, inspect the application and stop if `id`, `clientId`, or `slug` is `flareauth-cli`, or if `systemManaged` is true.

## Connectors

Operations: `listConnectors`, `getConnector`, `listConnectorReadiness`, `listConnectorTemplates`, `createConnector`, `updateConnector`, `deleteConnector`.

```bash
# List connectors and provider templates.
restish get "$FA_MGMT/connectors" -o json
restish get "$FA_MGMT/connectors/templates" -o json

# Inspect readiness for one connector.
CONNECTOR_ID="conn_123"
restish get "$FA_MGMT/connectors/$CONNECTOR_ID/readiness" -o json

# Patch a connector narrowly, then verify the connector and readiness.
restish patch "$FA_MGMT/connectors/$CONNECTOR_ID" enabled:true -o json
restish get "$FA_MGMT/connectors/$CONNECTOR_ID" -o json
restish get "$FA_MGMT/connectors/$CONNECTOR_ID/readiness" -o json
```

Connector secret material may be write-only or masked by the API. Do not print configured secrets or use verbose output around secret-bearing connector updates.

## Sign-In Settings

Operations: `getSignInSettings`, `updateSignInSettings`.

```bash
restish get "$FA_MGMT/sign-in-settings" -o json

# Example narrow patch. Use fields from the current OpenAPI/schema for the deployed version.
restish patch "$FA_MGMT/sign-in-settings" allowEmailPassword:true -o json
restish get "$FA_MGMT/sign-in-settings" -o json
```

## Branding Settings

Operations: `getBrandingSettings`, `updateBrandingSettings`, `uploadBrandingLogo`, `uploadBrandingFavicon`.

```bash
restish get "$FA_MGMT/branding-settings" -o json

# Example narrow patch.
restish patch "$FA_MGMT/branding-settings" appName:"Example Auth" primaryColor:"#2563eb" -o json
restish get "$FA_MGMT/branding-settings" -o json
```

For logo or favicon uploads, inspect the OpenAPI for the deployed version first and avoid echoing binary data or asset contents into logs.

## Account Center Settings

Operations: `getAccountCenterSettings`, `updateAccountCenterSettings`.

```bash
restish get "$FA_MGMT/account-center-settings" -o json

# Example narrow patch.
restish patch "$FA_MGMT/account-center-settings" enabled:true -o json
restish get "$FA_MGMT/account-center-settings" -o json
```

## Users

Operations: `listUsers`, `getUser`, `updateUser`, `deleteUser`, `banUser`, `unbanUser`, `createUserPasswordResetRequest`, `listUserSessions`, `deleteUserSessions`.

Prefer read-only user operations unless the task explicitly requires user mutation.

```bash
# List users. Add query params only when supported by the deployed OpenAPI.
restish get "$FA_MGMT/users" -o json

# Get one user.
USER_ID="user_123"
restish get "$FA_MGMT/users/$USER_ID" -o json

# Read user sessions and linked accounts where appropriate.
restish get "$FA_MGMT/users/$USER_ID/sessions" -o json
restish get "$FA_MGMT/users/$USER_ID/linked-accounts" -o json

# Request a password reset without exposing tokens or secrets, then verify user state if needed.
restish post "$FA_MGMT/users/$USER_ID/password-reset-requests" redirectTo:"https://app.example.com/reset" -o json
restish get "$FA_MGMT/users/$USER_ID" -o json
```

## Troubleshooting

### Restish is missing

```bash
command -v restish
```

Install Restish with the operator-approved package manager for the environment, then restart the shell and rerun `restish --help`.

### OpenAPI discovery is missing

Check the public Management OpenAPI endpoint directly:

```bash
restish get "$FA_MGMT/openapi.json" --rsh-ignore-status-code -o json
```

If it is not available, the deployment may not include the Restish-ready Management OpenAPI changes. Stop and report the missing `/api/management/openapi.json`; do not fall back to undocumented endpoints for mutations.

### Non-admin login

A successful browser login can still return `403` on Management API requests if the user lacks admin or management permission. Stop and ask the operator to authorize with a management-capable user. Do not try alternate clients or copied tokens.

### Expired or bad cached token

Clear the Restish auth cache for the named API and rerun a harmless read to trigger PKCE login again:

```bash
restish api clear-auth-cache "$FA_API"
restish get "$FA_MGMT/readiness" -o json
```

Do not inspect or print the token cache.

### Missing built-in CLI client

If Restish configuration or token exchange reports an unknown client for `flareauth-cli`, the deployment has not bootstrapped the built-in public native client. Stop and report that `flareauth-cli` is missing or misconfigured. Do not create a replacement client with management scopes unless the task explicitly asks for bootstrap repair and the operator confirms the target deployment.

### Generated operation commands are unavailable

Restish can expose generated API commands when discovery succeeds. Generic verb commands in this skill remain valid as long as the named API auth profile matches the same base URL. Run `restish api sync "$FA_API"` and inspect `restish --help` for generated commands before assuming an operation command is missing.
