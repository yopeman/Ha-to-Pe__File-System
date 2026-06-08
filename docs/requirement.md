# Ha-to-Pe File System — Requirements

## 1. Overview

Ha-to-Pe is a multi-user, permission-aware virtual file system. Users manage files and directories through a web GUI, mobile app, desktop app, and/or a terminal shell. The system supports sharing, real-time collaboration, trash management, compression, and storage quotas with admin-controlled limits and billing.

### 1.1 Goals

- Provide a secure, hierarchical file system with fine-grained access control.
- Support multiple client surfaces (web, mobile, desktop, shell) against a single backend API.
- Enable collaboration through shared directories with real-time updates.
- Offer storage quotas with admin-configurable defaults and upgrade paths.

### 1.2 Out of Scope (Initial Release)

- Concurrent binary editing of the same file (e.g., operational transforms).
- Full-text search inside file contents (name-based search only in v1).
- Third-party cloud storage backends (local/object storage adapter only in v1).

---

## 2. User Accounts

| ID | Requirement | Priority |
|----|-------------|----------|
| ACC-01 | Users can create an account. | Must |
| ACC-02 | Users can sign in and sign out. | Must |
| ACC-03 | Authentication uses OAuth 2.0 with Google and/or GitHub. | Must |
| ACC-04 | Each user has a private root directory created at registration. | Must |
| ACC-05 | Each user has an assigned storage quota (see §10). | Must |

---

## 3. File System Nodes

The system recognizes three node types. All nodes live in a logical tree (parent/child), not on the host OS filesystem.

| Type | Description |
|------|-------------|
| **File** | A binary blob with metadata (name, size, mime type, timestamps). |
| **Directory** | A container for child files and subdirectories. |
| **Zip** | A compressed archive treated as a first-class node; supports unzip into a target directory. |

### 3.1 General Node Rules

| ID | Requirement | Priority |
|----|-------------|----------|
| FS-01 | Users can create files and directories within directories they have permission to write. | Must |
| FS-02 | Users can rename, copy, and move files and directories. | Must |
| FS-03 | Node names must be unique among siblings under the same parent directory. | Must |
| FS-04 | Paths are resolved logically (absolute from root, relative from current working directory). | Must |
| FS-05 | The system must not expose raw host filesystem paths to clients. | Must |

---

## 4. Upload and Download

| ID | Requirement | Priority |
|----|-------------|----------|
| UDL-01 | Users can upload one or more files into a target directory. | Must |
| UDL-02 | Users can download individual files. | Must |
| UDL-03 | Users can download directory contents (as zip archive). | Must |
| UDL-04 | Upload and download must respect the user's effective permissions on the target node. | Must |
| UDL-05 | Upload must enforce storage quota before accepting the file. | Must |
| UDL-06 | Large files must be streamed; the server must not load entire files into memory. | Must |

---

## 5. Zip and Unzip

| ID | Requirement | Priority |
|----|-------------|----------|
| ZIP-01 | Users can create a zip archive from selected files and/or directories. | Must |
| ZIP-02 | Zip archives are stored as nodes of type `zip`. | Must |
| ZIP-03 | Users can unzip a zip archive into a target directory. | Must |
| ZIP-04 | Unzip must validate archive size and entry count to mitigate zip bombs. | Must |
| ZIP-05 | Zip operations require the appropriate permissions on source and target nodes. | Must |

---

## 6. Trash

| ID | Requirement | Priority |
|----|-------------|----------|
| TRH-01 | Users can move files and directories to trash (soft delete). | Must |
| TRH-02 | Users can restore items from trash to their original location (or a fallback if the parent no longer exists). | Must |
| TRH-03 | Users can permanently delete individual items from trash. | Must |
| TRH-04 | Users can empty the entire trash (permanent delete of all trashed items). | Must |
| TRH-05 | Trashed items do not count toward active storage listing but remain in quota until permanently deleted. | Should |
| TRH-06 | Trash is scoped per user (or per shared-root owner for shared content). | Must |

---

## 7. Client Interfaces

Users interact with the file system through one or more clients. All clients use the same backend API and permission model.

### 7.1 Graphical User Interface (GUI)

| ID | Requirement | Priority |
|----|-------------|----------|
| GUI-01 | Web client built with React and Vite. | Must |
| GUI-02 | Mobile client built with React Native, Expo, and EAS. | Should |
| GUI-03 | Desktop client built with Electron. | Should |
| GUI-04 | GUI supports tree navigation, upload, download, trash, search, and sharing flows. | Must |

### 7.2 Terminal / Shell

| ID | Requirement | Priority |
|----|-------------|----------|
| SHL-01 | Users can operate on files via a terminal/shell interface. | Must |
| SHL-02 | Shell supports absolute paths (e.g., `/home/docs`) and relative paths (e.g., `../project`). | Must |
| SHL-03 | Shell maintains a current working directory per session. | Must |
| SHL-04 | Shell commands enforce the same permissions as the GUI. | Must |
| SHL-05 | Core commands: `cd`, `ls`, `mkdir`, `rm`, `mv`, `cp`, `upload`, `download`, `zip`, `unzip`, `trash`, `restore`, `search`. | Must |

---

## 8. Search

| ID | Requirement | Priority |
|----|-------------|----------|
| SRC-01 | Users can search nodes by name. | Must |
| SRC-02 | Search scope: current directory (descendants of current dir). | Must |
| SRC-03 | Search scope: global (all nodes the user has read access to). | Must |
| SRC-04 | Search results respect read permissions; users must not see nodes they cannot access. | Must |

---

## 9. Directory Visibility and Sharing

### 9.1 Visibility Types

| Visibility | Description |
|------------|-------------|
| **Private** | Visible only to the owner and users explicitly granted access. |
| **Shared** | Accessible via invitation; collaborators receive permission grants. |
| **Public** | Readable (and optionally writable) via a public link or anonymous grant. |

| ID | Requirement | Priority |
|----|-------------|----------|
| VIS-01 | Directories have a visibility setting: private, shared, or public. | Must |
| VIS-02 | Owners can invite users to shared directories. | Must |
| VIS-03 | Invitations can specify permission grants (see §10). | Must |
| VIS-04 | Public directories expose read access without authentication (configurable). | Should |

### 9.2 Real-Time Collaboration

| ID | Requirement | Priority |
|----|-------------|----------|
| RTC-01 | Multiple users with access to a shared directory can collaborate in real time. | Must |
| RTC-02 | Clients receive live updates when directory contents change (create, move, delete, rename). | Must |
| RTC-03 | Clients can display presence (who is viewing a shared directory). | Should |
| RTC-04 | Write conflicts are detected via versioning; conflicting writes return an error and require refresh. | Must |
| RTC-05 | Real-time features are limited to shared (and optionally public) directories. | Must |

---

## 10. Permissions

Permissions are enforced at the service layer on every operation. Directory grants propagate to all nested files and subdirectories unless explicitly overridden.

### 10.1 File Permissions

| Action | Description |
|--------|-------------|
| `create` | Create a new file in a directory. |
| `write` | Modify file content or metadata. |
| `read` | View file metadata and download content. |
| `delete` | Move file to trash or permanently delete. |
| `copy` | Duplicate the file. |
| `move` | Relocate the file to another directory. |
| `zip` | Include the file in a zip archive. |
| `download` | Download file bytes. |
| `upload` | Upload/replace file content. |

### 10.2 Directory Permissions

| Action | Description |
|--------|-------------|
| `create` | Create child files or subdirectories. |
| `read` | List directory contents and view metadata. |
| `delete` | Move directory to trash or permanently delete. |
| `copy` | Duplicate the directory and its subtree. |
| `move` | Relocate the directory. |
| `zip` | Archive the directory. |
| `download` | Download directory as zip. |
| `dir_contents` | Full set of file permissions on all descendants (inherited). |

Directory `dir_contents` implies the file permission set is applied recursively to every nested file and subdirectory.

### 10.3 Zip Permissions

| Action | Description |
|--------|-------------|
| `unzip` | Extract archive into a target directory. |
| `copy` | Duplicate the zip node. |
| `move` | Relocate the zip node. |
| `delete` | Move zip to trash or permanently delete. |
| `download` | Download the zip archive. |

### 10.4 Permission Rules

| ID | Requirement | Priority |
|----|-------------|----------|
| PRM-01 | The directory owner has full permissions by default. | Must |
| PRM-02 | Permission grants are stored per user (or role) per directory. | Must |
| PRM-03 | Grants with `inherit=true` apply to all nested nodes. | Must |
| PRM-04 | The system resolves effective permissions by walking up the directory tree. | Must |
| PRM-05 | Operations without the required permission are rejected with an authorization error. | Must |

---

## 11. Storage and Quotas

| ID | Requirement | Priority |
|----|-------------|----------|
| STO-01 | Each user receives a default free storage allocation (e.g., 512 GB). | Must |
| STO-02 | Users can upgrade storage capacity (integration details TBD). | Should |
| STO-03 | The system tracks `storage_used_bytes` per user. | Must |
| STO-04 | Upload is rejected if `used + new_file_size > quota`. | Must |
| STO-05 | Permanent delete frees storage; trash retention policy is configurable. | Must |

---

## 12. Admin

| ID | Requirement | Priority |
|----|-------------|----------|
| ADM-01 | Admins can set the default free storage limit for new users. | Must |
| ADM-02 | Admins can set the price (or tier configuration) for storage upgrades. | Should |
| ADM-03 | Admins can view analytics summaries (total users, storage used, uploads, shared dirs, etc.). | Must |
| ADM-04 | Admins can generate exportable analytics reports. | Should |
| ADM-05 | Admin actions require an elevated role separate from regular users. | Must |

---

## 13. Technology Stack

### 13.1 Backend

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| Framework | FastAPI |
| GraphQL | Ariadne (schema-first) |
| API style | GraphQL + RESTful |
| Authentication | OAuth 2.0 (Google, GitHub) |
| ORM | SQLAlchemy |
| Database | MySQL (production), SQLite (development) |
| Testing | pytest |
| Architecture | OOP-first, layered (domain → services → API) |
| Package manager | UV |
| Formatting | isort, black |

### 13.2 Frontend

| Client | Technology |
|--------|------------|
| Web | React + Vite |
| Mobile | React Native + Expo + EAS |
| Desktop | Electron |

### 13.3 API Responsibilities

| Protocol | Use for |
|----------|---------|
| **REST** | File upload/download, OAuth callbacks, binary streaming (zip download) |
| **GraphQL** | Tree navigation, metadata, permissions, sharing, search, subscriptions |

---

## 14. Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-01 | All user input (paths, file names) must be validated and sanitized. | Must |
| NFR-02 | The system must prevent path traversal attacks. | Must |
| NFR-03 | Secrets (OAuth keys, DB credentials) must not be committed to source control. | Must |
| NFR-04 | Core business logic must be covered by unit tests (services, permissions). | Must |
| NFR-05 | Integration tests must cover upload, trash, and permission inheritance flows. | Must |
| NFR-06 | API responses for authorization failures must not leak existence of inaccessible nodes. | Should |
| NFR-07 | The codebase must be formatted with black and isort. | Must |

---

## 15. Delivery Phases

Development is organized in phases. Each phase delivers a usable, testable increment.

### Phase 0 — Foundation
- Project scaffolding (UV, FastAPI, SQLAlchemy, pytest).
- User model, authentication (email/password or OAuth).
- Core domain models: `Node`, `Directory`, `File`, `ZipArchive`.
- Database schema and migrations.

### Phase 1 — Private File System
- Directory tree CRUD for a single user.
- File upload/download with quota enforcement.
- Trash: move, restore, permanent delete, empty trash.
- Name search (current dir and global).
- Web GUI: tree view and basic operations.

### Phase 2 — Sharing and Permissions
- Directory visibility (private, shared, public).
- Invitations and permission grants with inheritance.
- Permission checks on all operations.

### Phase 3 — Real-Time Collaboration
- WebSocket / GraphQL subscriptions for directory changes.
- Presence in shared directories.
- Optimistic locking and conflict detection.

### Phase 4 — Extended Clients
- Terminal/shell client.
- Zip/unzip operations.
- Mobile (React Native) and desktop (Electron) clients.

### Phase 5 — Admin and Billing
- Admin dashboard for quota and pricing configuration.
- Analytics and reporting.
- Storage upgrade flow.

---

## 16. Glossary

| Term | Definition |
|------|------------|
| **Node** | Any item in the file system tree (file, directory, or zip). |
| **Grant** | A permission assignment from a directory to a user or role. |
| **Effective permission** | The resolved set of actions a user may perform on a node. |
| **Soft delete** | Moving a node to trash without removing its data. |
| **Quota** | Maximum storage bytes a user may consume. |

---

## 17. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-06-08 | — | Initial requirements draft |
