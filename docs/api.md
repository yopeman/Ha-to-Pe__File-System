# Ha-to-Pe File System — API Reference

Unified API contract for all Ha-to-Pe clients (web, mobile, desktop, CLI). The backend implements this spec with **FastAPI (REST)** and **Ariadne (GraphQL)**.

**Related docs:** [requirement.md](./requirement.md), [db_schema.md](./db_schema.md), [backend_implementation_plan.md](./backend_implementation_plan.md)

**Canonical schema file (implementation):** `backend/app/api/graphql/schema.graphql`

---

## 1. Overview

### 1.1 Base URLs

| Environment | REST | GraphQL | WebSocket |
|-------------|------|---------|-----------|
| Local dev | `http://localhost:8000` | `http://localhost:8000/graphql` | `ws://localhost:8000/graphql` |
| Production | `https://api.example.com` | `https://api.example.com/graphql` | `wss://api.example.com/graphql` |

### 1.2 Protocol Responsibilities

| Protocol | Use for |
|----------|---------|
| **GraphQL** | User profile, tree metadata, mutations (mkdir, move, trash, share, search), subscriptions |
| **REST** | Auth token exchange, file upload/download streams, OAuth redirects, admin report export |
| **WebSocket** | GraphQL subscriptions (`directoryChanged`, `directoryPresence`) |

### 1.3 Versioning

- REST: prefix optional `/v1` in production (v1 omits prefix in dev).
- GraphQL: schema evolves additively; breaking changes require a new endpoint or deprecation period.
- This document version: **0.1** (matches backend Phase 0–5 target).

### 1.4 Delivery Phases

Operations are tagged by backend implementation phase. Clients should not call operations before the matching backend phase ships.

| Phase | Scope |
|-------|-------|
| 0 | Auth, `me` |
| 1 | Private file system, upload/download, trash, search |
| 2 | Sharing, permissions, public links |
| 3 | Real-time subscriptions |
| 4 | Path resolution, zip/unzip |
| 5 | Admin, billing |

---

## 2. Authentication

### 2.1 Token Model

| Token | Lifetime | Storage (client guidance) |
|-------|----------|---------------------------|
| Access token (JWT) | 30 minutes (configurable) | Memory |
| Refresh token | 7 days (configurable) | HttpOnly cookie (web) or secure storage (mobile/desktop/CLI) |

### 2.2 REST Auth Endpoints

#### `POST /auth/register` — Phase 0

Create account with email and password.

**Request**

```json
{
  "email": "user@example.com",
  "password": "secret",
  "display_name": "Jane Doe"
}
```

**Response `201`**

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Errors:** `409` email exists, `422` validation.

---

#### `POST /auth/login` — Phase 0

**Request**

```json
{
  "email": "user@example.com",
  "password": "secret"
}
```

**Response `200`**

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Errors:** `401` invalid credentials.

---

#### `POST /auth/refresh` — Phase 0

**Request**

```json
{
  "refresh_token": "eyJ..."
}
```

**Response `200`**

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

Rotates refresh token on each use.

---

#### `POST /auth/logout` — Phase 0

Revokes refresh token.

**Headers:** `Authorization: Bearer <access_token>`

**Request**

```json
{
  "refresh_token": "eyJ..."
}
```

**Response `204`**

---

#### `GET /auth/google` — Phase 0

Starts OAuth 2.0 authorization code flow. Redirects to Google.

**Query params**

| Param | Description |
|-------|-------------|
| `redirect_uri` | Client callback (web) |
| `desktop` | `1` — loopback callback for Electron |
| `mobile` | `1` — deep link callback for Expo |

---

#### `GET /auth/github` — Phase 0

Same pattern as Google for GitHub OAuth.

---

#### `GET /auth/google/callback` / `GET /auth/github/callback` — Phase 0

OAuth provider callback. Exchanges code for tokens; redirects to client with tokens or sets session.

---

### 2.3 Authenticated Requests

**GraphQL**

```http
POST /graphql
Authorization: Bearer <access_token>
Content-Type: application/json
```

**REST (protected)**

```http
Authorization: Bearer <access_token>
```

**Public access (Phase 2)**

- Public directory REST: `GET /public/{token}/...` — no auth header.
- GraphQL public browse: optional `publicToken` argument (see §5.2).

---

## 3. Errors

### 3.1 REST Error Body

```json
{
  "error": {
    "code": "QUOTA_EXCEEDED",
    "message": "Storage quota exceeded",
    "details": {
      "required_bytes": 52428800,
      "available_bytes": 12582912
    }
  }
}
```

### 3.2 GraphQL Errors

Standard GraphQL `errors` array with extensions:

```json
{
  "errors": [
    {
      "message": "Permission denied",
      "extensions": {
        "code": "FORBIDDEN"
      }
    }
  ]
}
```

### 3.3 Error Code Catalog

| Code | HTTP | Meaning | Client action |
|------|------|---------|---------------|
| `UNAUTHORIZED` | 401 | Missing or invalid token | Refresh or re-login |
| `FORBIDDEN` | 403 | No permission on resource | Hide action / show message |
| `NOT_FOUND` | 404 | Node or route not found | Refresh listing |
| `CONFLICT` | 409 | Version mismatch or name collision | Refetch and retry |
| `QUOTA_EXCEEDED` | 413 | Storage full | Show upgrade / free space |
| `BAD_USER_INPUT` | 422 | Validation failed | Fix input |
| `RATE_LIMITED` | 429 | Too many requests | Back off |
| `INTERNAL_ERROR` | 500 | Server error | Retry later |

**Security (NFR-06):** `FORBIDDEN` and `NOT_FOUND` responses must not reveal existence of inaccessible nodes to unauthorized users. Use generic messages for cross-tenant probes.

---

## 4. Permissions

Permissions are enforced **server-side only**. Clients may query effective actions for UI gating.

### 4.1 Action Strings

**File actions:** `create`, `write`, `read`, `delete`, `copy`, `move`, `zip`, `download`, `upload`

**Directory actions:** `create`, `read`, `delete`, `copy`, `move`, `zip`, `download`, `dir_contents`

**Zip actions:** `unzip`, `copy`, `move`, `delete`, `download`

`dir_contents` on a directory grant with `inherit: true` applies all file actions to descendants.

### 4.2 GraphQL — Effective Permissions — Phase 2

```graphql
query NodePermissions($nodeId: ID!) {
  nodePermissions(nodeId: $nodeId) {
    actions
    sourceDirectoryId
  }
}
```

---

## 5. GraphQL Schema

Full target schema. Implement incrementally per phase (see §10).

```graphql
# Scalars
scalar BigInt
scalar DateTime

# --- Enums ---

enum NodeType {
  DIRECTORY
  FILE
  ZIP
}

enum Visibility {
  PRIVATE
  SHARED
  PUBLIC
}

enum SearchScope {
  CURRENT_DIRECTORY
  GLOBAL
}

enum DirectoryChangeType {
  NODE_CREATED
  NODE_RENAMED
  NODE_MOVED
  NODE_TRASHED
  NODE_RESTORED
  NODE_PERMANENTLY_DELETED
}

enum InvitationStatus {
  PENDING
  ACCEPTED
  REJECTED
  REVOKED
  EXPIRED
}

# --- Core types ---

interface Node {
  id: ID!
  name: String!
  nodeType: NodeType!
  parent: Directory
  owner: User!
  sizeBytes: BigInt!
  createdAt: DateTime!
  updatedAt: DateTime!
  version: Int!
  path: String!                    # Phase 4 — logical path e.g. /root/docs/file.txt
}

type User {
  id: ID!
  email: String!
  displayName: String!
  quotaBytes: BigInt!
  storageUsedBytes: BigInt!
  isAdmin: Boolean!
  root: Directory!
}

type Directory implements Node {
  visibility: Visibility!          # Phase 2
  children: [Node!]!
  grants: [PermissionGrant!]!      # Phase 2 — owner/admin only
}

type File implements Node {
  mimeType: String
}

type ZipArchive implements Node {
  entryCount: Int
  uncompressedBytes: BigInt
}

type PermissionGrant {
  id: ID!
  grantee: User!
  actions: [String!]!
  inherit: Boolean!
  grantedBy: User!
  createdAt: DateTime!
}

type ShareInvitation {
  id: ID!
  directory: Directory!
  inviter: User!
  inviteeEmail: String!
  actions: [String!]!
  inherit: Boolean!
  status: InvitationStatus!
  expiresAt: DateTime!
  createdAt: DateTime!
}

type PublicLink {
  id: ID!
  directory: Directory!
  token: String!
  url: String!
  allowWrite: Boolean!
  expiresAt: DateTime
}

type StorageTier {
  id: ID!
  name: String!
  capacityBytes: BigInt!
  priceCents: Int!
  currency: String!
}

type StorageUpgrade {
  id: ID!
  tier: StorageTier!
  status: String!
  quotaDeltaBytes: BigInt!
  createdAt: DateTime!
}

type AdminStats {
  totalUsers: Int!
  totalStorageUsedBytes: BigInt!
  totalSharedDirectories: Int!
  uploadsLast30Days: Int!
}

type NodePermissions {
  actions: [String!]!
  sourceDirectoryId: ID
}

type DirectoryChangeEvent {
  type: DirectoryChangeType!
  directoryId: ID!
  nodeId: ID
  actor: User
  timestamp: DateTime!
}

type PresenceEntry {
  user: User!
  clientType: String!
  lastSeenAt: DateTime!
}

# --- Queries ---

type Query {
  # Phase 0
  me: User

  # Phase 1
  node(id: ID!): Node
  directory(id: ID!): Directory
  trash: [Node!]!
  search(
    query: String!
    scope: SearchScope!
    directoryId: ID
  ): [Node!]!

  # Phase 2
  nodePermissions(nodeId: ID!): NodePermissions!
  sharedWithMe: [Directory!]!
  invitations: [ShareInvitation!]!
  publicDirectory(token: String!): Directory

  # Phase 4
  resolvePath(cwdId: ID!, path: String!): Node
  nodePath(nodeId: ID!): String!

  # Phase 5
  adminStats: AdminStats!
  storageTiers: [StorageTier!]!
}

# --- Mutations ---

type Mutation {
  # Phase 1 — file system
  mkdir(parentId: ID!, name: String!): Directory!
  createFile(parentId: ID!, name: String!): File!
  rename(
    nodeId: ID!
    name: String!
    expectedVersion: Int!
  ): Node!
  move(
    nodeId: ID!
    targetParentId: ID!
    expectedVersion: Int
  ): Node!
  copy(nodeId: ID!, targetParentId: ID!): Node!
  moveToTrash(nodeId: ID!): Node!
  restoreFromTrash(nodeId: ID!): Node!
  permanentDelete(nodeId: ID!): Boolean!
  emptyTrash: Int!

  # Phase 2 — sharing
  setVisibility(
    directoryId: ID!
    visibility: Visibility!
  ): Directory!
  inviteCollaborator(
    directoryId: ID!
    email: String!
    actions: [String!]!
    inherit: Boolean = true
  ): ShareInvitation!
  acceptInvitation(token: String!): PermissionGrant!
  declineInvitation(token: String!): Boolean!
  updateGrant(
    grantId: ID!
    actions: [String!]!
    inherit: Boolean!
  ): PermissionGrant!
  revokeGrant(grantId: ID!): Boolean!
  createPublicLink(
    directoryId: ID!
    allowWrite: Boolean = false
  ): PublicLink!
  revokePublicLink(directoryId: ID!): Boolean!

  # Phase 3 — presence heartbeat (optional mutation alternative to subscription)
  heartbeatPresence(
    directoryId: ID!
    clientType: String!
  ): Boolean!

  # Phase 4 — archives
  createZip(
    sourceIds: [ID!]!
    targetParentId: ID!
    name: String!
  ): ZipArchive!
  unzip(
    zipId: ID!
    targetParentId: ID!
  ): Directory!

  # Phase 5 — admin & billing
  setDefaultQuota(bytes: BigInt!): Boolean!
  purchaseStorageUpgrade(tierId: ID!): StorageUpgrade!
}

# --- Subscriptions — Phase 3 ---

type Subscription {
  directoryChanged(directoryId: ID!): DirectoryChangeEvent!
  directoryPresence(directoryId: ID!): [PresenceEntry!]!
}
```

---

## 6. REST API (Non-GraphQL)

### 6.1 Upload — Phase 1

Three-step upload for streaming large files.

#### Step 1: Create session

`POST /upload/sessions`

**Headers:** `Authorization: Bearer <access_token>`

**Request**

```json
{
  "target_directory_id": "42",
  "file_name": "report.pdf",
  "expected_size_bytes": 1048576,
  "mime_type": "application/pdf"
}
```

**Response `201`**

```json
{
  "session_id": "7f3a...",
  "upload_url": "/upload/sessions/7f3a...",
  "expires_at": "2026-06-08T13:00:00Z"
}
```

**Errors:** `403` forbidden, `413` quota exceeded, `404` directory not found.

---

#### Step 2: Upload bytes

`PUT /upload/sessions/{session_id}`

**Headers**

```http
Authorization: Bearer <access_token>
Content-Type: application/octet-stream
Content-Length: 1048576
```

**Body:** raw file bytes (streamed).

**Response `204`**

---

#### Step 3: Complete

`POST /upload/sessions/{session_id}/complete`

**Response `200`**

```json
{
  "node": {
    "id": "99",
    "name": "report.pdf",
    "node_type": "file",
    "size_bytes": 1048576,
    "mime_type": "application/pdf"
  }
}
```

---

### 6.2 Download File — Phase 1

`GET /download/{node_id}`

**Headers:** `Authorization: Bearer <access_token>`

**Response `200`**

```http
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="report.pdf"
Content-Length: 1048576
```

Body: streamed file bytes.

**Errors:** `403`, `404`.

---

### 6.3 Download Directory as Zip — Phase 4

`GET /download/directory/{directory_id}/zip`

**Headers:** `Authorization: Bearer <access_token>`

**Response `200`**

```http
Content-Type: application/zip
Content-Disposition: attachment; filename="archive.zip"
```

Streamed zip archive of directory subtree.

---

### 6.4 Public Browse — Phase 2

`GET /public/{token}/nodes`

List public directory children (read-only grant).

**Query:** `parent_id` (optional, default public root)

**Response `200`**

```json
{
  "nodes": [
    {
      "id": "10",
      "name": "readme.txt",
      "node_type": "file",
      "size_bytes": 1024
    }
  ]
}
```

`GET /public/{token}/download/{node_id}` — download file from public tree.

---

### 6.5 Admin Report Export — Phase 5

`GET /admin/reports/{type}`

**Headers:** `Authorization: Bearer <access_token>` (admin only)

**Query**

| Param | Description |
|-------|-------------|
| `format` | `json`, `csv` |
| `from` | ISO date |
| `to` | ISO date |

**Response `200`:** file download or JSON body.

**Errors:** `403` non-admin.

---

### 6.6 Health — Phase 0

`GET /health`

**Response `200`**

```json
{
  "status": "ok",
  "database": "ok"
}
```

---

## 7. Path Resolution — Phase 4

Logical paths used by CLI and clients. **Not** host filesystem paths.

### 7.1 Rules

| Pattern | Meaning |
|---------|---------|
| `/root/docs` | Absolute from user root |
| `docs/report.pdf` | Relative to current working directory |
| `../shared` | Parent directory then `shared` |
| `.` | Current directory |

### 7.2 GraphQL

```graphql
query ResolvePath($cwdId: ID!, $path: String!) {
  resolvePath(cwdId: $cwdId, path: $path) {
    id
    name
    nodeType
    path
  }
}
```

**Errors:** `NOT_FOUND` invalid path, `FORBIDDEN` no access.

---

## 8. Subscriptions — Phase 3

### 8.1 Transport

- WebSocket at `/graphql` with `graphql-transport-ws` or `graphql-ws` subprotocol.
- Connection init payload includes `Authorization: Bearer <access_token>`.

### 8.2 `directoryChanged`

Emitted when a child of `directoryId` is created, renamed, moved, or trashed by any user.

```graphql
subscription DirectoryChanged($directoryId: ID!) {
  directoryChanged(directoryId: $directoryId) {
    type
    directoryId
    nodeId
    actor { id displayName }
    timestamp
  }
}
```

Clients should refetch `directory(id).children` or patch cache on event.

### 8.3 `directoryPresence`

```graphql
subscription DirectoryPresence($directoryId: ID!) {
  directoryPresence(directoryId: $directoryId) {
    user { id displayName }
    clientType
    lastSeenAt
  }
}
```

Send `heartbeatPresence` mutation every 30s while viewing a shared directory (or include heartbeat in subscription keep-alive).

---

## 9. Example Flows

### 9.1 Register, browse root, create folder — Phase 0–1

```graphql
# 1. After POST /auth/register
query Me {
  me {
    id
    email
    root { id name }
    storageUsedBytes
    quotaBytes
  }
}

# 2. List root children
query RootListing {
  directory(id: "ROOT_ID") {
    id
    name
    children { id name nodeType sizeBytes updatedAt }
  }
}

# 3. Create folder
mutation {
  mkdir(parentId: "ROOT_ID", name: "documents") {
    id name
  }
}
```

---

### 9.2 Upload file — Phase 1

```bash
# 1. Create session
curl -X POST http://localhost:8000/upload/sessions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target_directory_id":"42","file_name":"photo.jpg","expected_size_bytes":204800,"mime_type":"image/jpeg"}'

# 2. Upload bytes
curl -X PUT "http://localhost:8000/upload/sessions/SESSION_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @photo.jpg

# 3. Complete
curl -X POST "http://localhost:8000/upload/sessions/SESSION_ID/complete" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 9.3 Share directory — Phase 2

```graphql
mutation {
  setVisibility(directoryId: "42", visibility: SHARED) {
    id visibility
  }
}

mutation {
  inviteCollaborator(
    directoryId: "42"
    email: "collab@example.com"
    actions: ["read", "upload", "create"]
    inherit: true
  ) {
    id status inviteeEmail
  }
}

# Invitee:
mutation {
  acceptInvitation(token: "INVITE_TOKEN") {
    id actions grantee { email }
  }
}
```

---

### 9.4 Rename with optimistic locking — Phase 1–3

```graphql
mutation {
  rename(
    nodeId: "99"
    name: "final-report.pdf"
    expectedVersion: 3
  ) {
    id name version
  }
}
```

On `CONFLICT`, client refetches node and prompts user to retry.

---

### 9.5 CLI path resolve — Phase 4

```graphql
query {
  resolvePath(cwdId: "42", path: "../shared/project") {
    id name nodeType path
  }
}
```

---

## 10. Operation Index by Phase

### Phase 0

| Type | Name |
|------|------|
| REST | `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout` |
| REST | `GET /auth/google`, `GET /auth/github`, callbacks |
| REST | `GET /health` |
| Query | `me` |

### Phase 1

| Type | Name |
|------|------|
| Query | `node`, `directory`, `trash`, `search` |
| Mutation | `mkdir`, `createFile`, `rename`, `move`, `copy`, `moveToTrash`, `restoreFromTrash`, `permanentDelete`, `emptyTrash` |
| REST | `POST/PUT/POST /upload/sessions/*`, `GET /download/{id}` |

### Phase 2

| Type | Name |
|------|------|
| Query | `nodePermissions`, `sharedWithMe`, `invitations`, `publicDirectory` |
| Mutation | `setVisibility`, `inviteCollaborator`, `acceptInvitation`, `declineInvitation`, `updateGrant`, `revokeGrant`, `createPublicLink`, `revokePublicLink` |
| REST | `GET /public/{token}/*` |

### Phase 3

| Type | Name |
|------|------|
| Subscription | `directoryChanged`, `directoryPresence` |
| Mutation | `heartbeatPresence` |

### Phase 4

| Type | Name |
|------|------|
| Query | `resolvePath`, `nodePath` |
| Mutation | `createZip`, `unzip` |
| REST | `GET /download/directory/{id}/zip` |

### Phase 5

| Type | Name |
|------|------|
| Query | `adminStats`, `storageTiers` |
| Mutation | `setDefaultQuota`, `purchaseStorageUpgrade` |
| REST | `GET /admin/reports/{type}` |

---

## 11. Client Integration Notes

| Client | Auth | Upload | Real-time |
|--------|------|--------|-------------|
| Web | JWT in memory + refresh cookie optional | `fetch` / XHR PUT | Apollo `GraphQLWsLink` |
| Mobile | SecureStore refresh token | `FileSystem.uploadAsync` | Apollo WebSocket |
| Desktop | `safeStorage` + IPC | Main process stream PUT | Apollo WebSocket |
| CLI | `~/.config/hatope/credentials.json` | httpx stream PUT | Out of scope v1 |

### 11.1 Code Generation

Point GraphQL Code Generator at `http://localhost:8000/graphql` (introspection) or copy `backend/app/api/graphql/schema.graphql`.

```bash
# web / mobile / desktop
npm run codegen

# after schema changes in CI
graphql-codegen --check
```

---

## 12. OpenAPI

FastAPI auto-generates OpenAPI for REST at:

```
GET /docs      # Swagger UI
GET /redoc     # ReDoc
GET /openapi.json
```

GraphQL operations are not in OpenAPI; use this document and the GraphQL schema file.

---

## 13. Document History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-06-08 | Initial unified API reference |
