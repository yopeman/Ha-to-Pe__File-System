# Ha-to-Pe File System

## Database Schema: 

### Users
1. id
2. username
3. email
4. password_hash
5. role
6. created_at
7. updated_at
8. deleted_at

### OAuthAccounts
1. id
2. user_id
3. provider
4. provider_user_id
5. created_at

### Nodes
1. id
2. parent_id
3. owner_id
4. name
5. type:
   1. DIRECTORY
   2. FILE
   3. ZIP
6. visibility:
   1. PRIVATE
   2. SHARED
   3. PUBLIC
7. size
8. is_hidden
9. is_trashed
10. is_deleted
11. created_at
12. updated_at
13. trashed_at
14. deleted_at

### FileVersions
1. id
2. node_id
3. version_number
4. storage_path
5. size
6. created_by
7. created_at

### DirectoryGroups
1. id
2. creator_id
3. group_name
4. permissions (lists):
   1. list
   2. read_metadata
   3. create_file
   4. create_directory
   5. rename
   6. move
   7. copy
   8. delete
   9. restore
   10. purge
   11. download
   12. zip
   13. share
   14. change_visibility
   15. manage_permissions
   16. change_owner

### Shares
1. id
2. user_id
3. node_id
4. group_id
5. created_at
6. updated_at

### Publics
1. id
2. node_id
3. group_id
4. created_at
5. updated_at

### Invitations
1. id
2. node_id
3. invited_by
4. invited_user
5. status:
   1. PENDING
   2. ACCEPTED
   3. DECLINED
   4. EXPIRED
6. created_at
7. accepted_at

### ActivityLogs
1. id
2. user_id
3. node_id
4. action
5. metadata
6. created_at

### UserStorage
1. id
2. user_id
3. used_bytes
4. quota_bytes
5. updated_at

### Payments
1. id
2. user_id
3. amount
4. currency
5. status
6. transaction_id
7. created_at
8. paid_at

### Settings
1. free_storage_gb
2. price_per_gb
3. trash_retention_days
4. created_at
5. updated_at

## Project organization
```
app/
├── api/
│   ├── rest/
│   └── graphql/
│
├── models/
├── schemas/
├── repositories/
├── services/
├── permissions/
├── storage/
├── websocket/
├── auth/
└── tests/
```