# smartbugsVulnDetector

安装mogoDB
```
"https://blog.csdn.net/majiayu000/article/details/126491116"
"http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/"

官方  
"https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/"
```

创建数据库目录
```
sudo mkdir -p /var/lib/mongo
sudo mkdir -p /var/log/mongodb
sudo chown `whoami` /var/lib/mongo     # 设置权限
sudo chown `whoami` /var/log/mongodb   # 设置权限
```

启动数据库后台
```
mongod --dbpath /var/lib/mongo --logpath /var/log/mongodb/mongod.log --fork
```

关闭服务
```
mongod --dbpath /var/lib/mongo --logpath /var/log/mongodb/mongod.log --shutdown
```

数据库操作
```
show dbs 查看全部数据库
use DATABASE_NAME 使用/新建数据库

```
```
集合操作
db.createCollection("NAME") 新建集合
```
用户操作
```
show users 查看全部角色

```