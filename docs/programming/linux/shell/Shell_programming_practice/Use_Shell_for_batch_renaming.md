# 批量重命名——Shell编程实践

此案例解决需要批量重命名的场景。

# 1 版本V1

## 1.1 V1.0

此版本是解决一个目录下有多个文件和文件夹（包括子文件）需要去除名称尾部固定内容的场景。

使用系统：Linux

使用此版本需要把此版本的脚本文件放到需要压缩的文件夹及文件夹的顶级目录下。

脚本内容：

```shell
#!/bin/sh
del_str=$1
echo "删除的字符串：$del_str"
function rename() {
	if [[ `contain $1` -eq 1 ]]
	then
		if test -d "$2$1"
		then
			file=`expr $1 : "\(.*\)$del_str"`
			#echo "文件夹目标文件：`$2$file`"#需要注释掉行，避免mv错误返回错误的路径
			mv "$2$1" "$2$file"
			echo "$2$file"#如果是文件夹，重命名后路径变化，需要返回新的路径一般迭代操作
		else
			suffix=`expr $1 : ".*$del_str\(\..*\)"`
			fileName=`expr $1 : "\(.*\)$del_str\..*"`
			#echo "文件目标文件：`$2$fileName$suffix`"
			mv "$2$1" "$2$fileName$suffix"
		fi
	else
		echo "$2$1"
	fi
}

function batch() {
	for file in `ls "$1"`# $1加引号为解决路径中有空格的问题
	do
		if test -d "$1/$file"
		then
			file=`rename $file "$1/"`
			batch "$file"
		else
			rename $file "$1/"
		fi
	done
}

function contain() {
	result=$(echo $1 | grep "${del_str}")
	if [[ "$result" != "" ]]
	then
		echo 1;
	else
		echo 0;
	fi
}

for file in `ls`
do
	rename $file "`pwd`/"
	if test -d $file
	then
		batch "`pwd`/$file"
	fi
done
```

