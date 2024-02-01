数据库 
```
smartbugsVulnDetector
```
账户
webAppUser
```
db.createUser({
  user: "webAppUser",
  pwd: "webAppPassword",
  roles: ["readWrite"]
})
```

集合 
```
用户信息 user_info
{
  "_id": ObjectId("user_id"),
  "username": "user123",
  "password": "hashed_password",
  "email": "user@example.com"
}
文件信息 file_info
{
  "_id": ObjectId("file_id"),
  "filename": "example.txt",
  "userId": ObjectId("user_id"),
  "uploadTime": ISODate("upload_time"),
  "content": "file_content"
}
处理记录信息 record_info
{
  "_id": ObjectId("record_id"),
  "fileId": ObjectId("file_id"),
  "result": "processing_result",
  "timestamp": ISODate("processing_time")
}
```