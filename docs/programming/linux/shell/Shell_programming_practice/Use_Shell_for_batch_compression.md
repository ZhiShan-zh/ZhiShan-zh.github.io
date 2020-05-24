# Shell编程实践

此案例解决需要批量压缩的场景。

# 1 版本V1

## 1.1 V1.0

此版本是最初的批量压缩版本，解决一个目录下有多个需要压缩的文件夹的应用场景。

使用系统：Linux

使用此版本需要把此版本的脚本文件放到需要压缩的文件夹的同级目录下，然后执行此脚本可以把当前目录下每个文件夹分别压缩成一个此文件夹名称的zip压缩文件，并保留当前文件夹。

脚本内容：

```shell
#!/bin/sh
PWD=`pwd`
for var in `ls`
do
	if test -d $var
	then
		echo "压缩\"$PWD/$var\"..."
		zip -q -r $var.zip $var
	fi
done
```

