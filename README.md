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