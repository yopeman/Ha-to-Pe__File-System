# Ha-to-Pe File System

## Database Schema:

### Users
1. id (PK) NOT NULL
2. username NOT NULL
3. email NOT NULL
4. password_hash NOT NULL
5. role [user, admin] NOT NULL (default 'user')
6. created_at NOT NULL
7. updated_at NOT NULL
8. deleted_at (nullable)

**Unique constraints:** `(username)`, `(email)`

### OAuthAccounts
1. id (PK) NOT NULL
2. user_id (FK) NOT NULL
3. provider NOT NULL
4. provider_user_id NOT NULL
5. created_at NOT NULL
6. updated_at NOT NULL

**Unique constraints:** `(user_id, provider)`, `(provider, provider_user_id)`

### Nodes
1. id (PK) NOT NULL
2. parent_id (FK) (nullable – root nodes)
3. owner_id (FK) NOT NULL
4. name NOT NULL
5. type [DIRECTORY, FILE, ZIP] NOT NULL (ENUM)
6. visibility [PRIVATE, SHARED, PUBLIC] NOT NULL (default 'PRIVATE')
7. is_hidden NOT NULL (default false)
8. created_at NOT NULL
9. updated_at NOT NULL
10. trashed_at (nullable)
11. deleted_at (nullable)

**Unique constraints:** `(parent_id, name)` with application-level soft-delete handling

### FileVersions
1. id (PK) NOT NULL
2. node_id (FK) NOT NULL
3. version_number NOT NULL
4. storage_path NOT NULL
5. size NOT NULL
6. created_by (FK) NOT NULL
7. created_at NOT NULL
8. deleted_at (nullable)

**Unique constraints:** `(node_id, version_number)`

### Groups
1. id (PK) NOT NULL
2. name NOT NULL
3. created_by (FK) NOT NULL
4. created_at NOT NULL
5. updated_at NOT NULL
6. deleted_at (nullable)

**Unique constraints:** `(name)` if global; or `(created_by, name)` for per-user groups

### Permissions
1. id (PK) NOT NULL
2. group_id (FK) NOT NULL
3. list NOT NULL (default false)
4. read_metadata NOT NULL (default false)
5. create_file NOT NULL (default false)
6. create_directory NOT NULL (default false)
7. rename NOT NULL (default false)
8. move NOT NULL (default false)
9. copy NOT NULL (default false)
10. delete NOT NULL (default false)
11. restore NOT NULL (default false)
12. purge NOT NULL (default false)
13. download NOT NULL (default false)
14. zip NOT NULL (default false)
15. share NOT NULL (default false)
16. change_visibility NOT NULL (default false)
17. manage_permissions NOT NULL (default false)
18. change_owner NOT NULL (default false)
19. created_at NOT NULL
20. updated_at NOT NULL

**Unique constraints:** `(group_id)` – one permission set per group

### Invitations
1. id (PK) NOT NULL
2. node_id (FK) NOT NULL
3. invited_by (FK) NOT NULL
4. invited_user (FK) NOT NULL
5. status [PENDING, ACCEPTED, DECLINED, EXPIRED] NOT NULL (default 'PENDING')
6. created_at NOT NULL
7. updated_at NOT NULL
8. expires_at NOT NULL
9. accepted_at (nullable)

**Unique constraints:** `(node_id, invited_user, status)` with `status = 'PENDING'` (partial unique index)

### Shares
1. id (PK) NOT NULL
2. user_id (FK) (nullable – either user_id or group_id must be set)
3. node_id (FK) NOT NULL
4. group_id (FK) (nullable)
5. created_at NOT NULL
6. updated_at NOT NULL
7. deleted_at (nullable)

**Unique constraints:** Application logic ensures no duplicate active shares; optional partial index `(node_id, user_id)` where `user_id IS NOT NULL AND deleted_at IS NULL`

### ActivityLogs
1. id (PK) NOT NULL
2. user_id (FK) (nullable – system actions)
3. node_id (FK) (nullable – actions not tied to a node)
4. action NOT NULL
5. metadata (JSON, nullable)
6. created_at NOT NULL

**Unique constraints:** None

### UserStorage
1. id (PK) NOT NULL
2. user_id (FK) NOT NULL
3. used_bytes NOT NULL (default 0)
4. quota_bytes NOT NULL (default – from settings)
5. created_at NOT NULL
6. updated_at NOT NULL

**Unique constraints:** `(user_id)` – one storage record per user

### Payments
1. id (PK) NOT NULL
2. user_id (FK) NOT NULL
3. amount NOT NULL
4. currency NOT NULL (default 'USD')
5. status [pending, completed, canceled, failed] NOT NULL (default 'pending')
6. transaction_id (nullable – before external confirmation)
7. created_at NOT NULL
8. updated_at NOT NULL
9. paid_at (nullable)

**Unique constraints:** `(transaction_id)` when not null

### Settings
1. free_storage_gb NOT NULL
2. price_per_gb NOT NULL
3. trash_retention_days NOT NULL
4. created_at NOT NULL
5. updated_at NOT NULL

**Unique constraints:** None (single-row table)
