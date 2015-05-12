##功能
git_export.bash+ftp_copy.py：导出某次git提交最新版，打包成一个文件夹，并从服务器ftp上下载备份文件  
git_backup.bash:复制出某次提交所有更改的文件，并备份上一个版本的这些文件到backup_文件夹
##使用
1.安装python3.4  
2.添加环境变量C:\Python34;C:\Python34\Scripts;  
3.脚本放置在上传代码的目录,编辑export.bash 设置reop_path路径,编辑ftp_copy.py 设置ftp参数  
4.打开git bash,运行./git_xx.bash,按提示输入commit版本哈希值即可
