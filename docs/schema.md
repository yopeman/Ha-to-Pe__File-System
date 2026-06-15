# Ha-to-Pe File System Project Database Schema: 

## Users 
1. id
2. username
3. email (unique)
4. password 
5. role: admin, user
6. is deleted
7. created at
8. updated at
9. deleted at

## Auth Accounts
1. id
2. user id
3. provider 
4. provider user id 
5. created at
6. updated at
7. unique (provider name, provider user id)

## Nodes
1. id
2. parent id
3. owner id
4. name
5. type: file, dir, zip
6. visibility: private, shared, public
7. size
8. storage path
9. is hidden
10. is trashed
11. is deleted
12. created at
13. updated at
14. trashed at
15. deleted at

## Collaborators 
1. id
2. user id
3. node id
4. status: pending, accepted, declined, expired
5. is deleted 
6. created at
7. updated at
8. accepted at
9. deleted at

## Permission Grants
1. id
2. node id
3. collab id
4. for: public, collab
5. created at
6. updated at
7. unique (dir, collab id)

## Permissions 
1. id
2. grant id (unique)
3. create file
4. create dir
5. read
6. write 
7. delete
8. copy 
9. move 
10. upload 
11. download 
12. zip
13. unzip 
14. list
15. recover
16. subdir permissions: inherited, full access, creator permissions 
17. created at
18. updated at

## Histories 
1. id
2. user id 
3. node id
4. changes 
5. created at
6. updated

## Settings 
1. id
2. default free storage 
3. storage fee per GB
4. discount rate 
5. trash retention timeout
6. created at
7. updated at

## Payments
1. id
2. user id
3. amount
4. currency
5. method
6. status: pending, completed, canceled, failed
7. paid_at
8. transaction_id
9. checkout_url
10. receipt_url
11. created at
12. updated at

## Quota
1. id
2. user id
3. payment id
4. storage size in GB
5. type: default, paid
6. created at
7. updated at