
- 找软件的 BundleId，通过查看软件的 "显示包内容 > Info.plist" 就可以找到了


```
添加屏幕录制权限：
sudo /usr/bin/sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT or REPLACE INTO access VALUES('kTCCServiceScreenCapture','com.techsmith.camtasia2019',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,1585206926);"

添加麦克风权限：
sudo /usr/bin/sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT or REPLACE INTO access VALUES('kTCCServiceMicrophone','com.techsmith.camtasia2019',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,1585206926);"

添加摄像头权限：
sudo /usr/bin/sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT or REPLACE INTO access VALUES('kTCCServiceCamera','com.techsmith.camtasia2019',0,1,1,NULL,NULL,NULL,'UNUSED',NULL,0,1585206926);"
```

