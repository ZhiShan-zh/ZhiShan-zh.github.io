# 批量重命名——Shell编程实践

此案例解决需要批量重命名的场景。

# 1 版本V1

## 1.1 V1.0

此版本是解决一个目录下有多个文件和文件夹（包括子文件）需要去除名称尾部固定内容的场景。

路径和文件名可以包含空格。

使用系统：Linux

使用此版本需要把此版本的脚本文件放到需要压缩的文件及文件夹的顶级目录下，并需要携带一个参数，此参数为需要去除的字符串

脚本内容：

```shell
#!/bin/sh
del_str="$1"
echo "删除的字符串：$del_str"
function rename() {
  if [[ `contain "$1"` -eq 1 ]]
  then
    if test -d "$2$1"
    then
      file=`expr "$1" : "\(.*\)$del_str"`
      #需要注释掉行，避免mv错误返回错误的路径
      #echo "文件夹目标文件：`$2$file`"
      mv "$2$1" "$2$file"
      #如果是文件夹，重命名后路径变化，需要返回新的路径一般迭代操作
      echo "$2$file"
    else
      suffix=`expr "$1" : ".*$del_str\(\..*\)"`
      # 解决有些文件没有后缀的问题
      if test $suffix; then
        fileName=`expr "$1" : "\(.*\)$del_str\..*"`
        echo "文件目标文件：`$2$fileName$suffix`"
        mv "$2$1" "$2$fileName$suffix"
      else
        file=`expr "$1" : "\(.*\)$del_str"`
        mv "$2$1" "$2$file"
      fi
    fi
  else
    echo "$2$1"
  fi
}

function batch() {
  # $1加引号为解决路径中有空格的问题，使用tr解决ls中遍历的文件名出现空格而分成多个项
  for file in `ls "$1" | tr ' ' '\?'`
  do
    # 因为file文件名中的空格已经被？替换，所以到真正用到的时候需要把？替换成空格
    file=`tr '\?' ' ' <<< $file`
    if test -d "$1/$file" 
    then
      file=`rename "$file" "$1/"`
      batch "$file"
    else
      rename "$file" "$1/"
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
# 使用tr解决ls中遍历的文件名出现空格而分成多个项
for file in `ls | tr ' ' '\?'` 
do
  # 因为file文件名中的空格已经被？替换，所以到真正用到的时候需要把？替换成空格
  file=`tr '\?' ' ' <<<$file`
  rename "$file" "`pwd`/"
  if test -d "$file"
  then
    batch "`pwd`/$file"
  fi
done
```

