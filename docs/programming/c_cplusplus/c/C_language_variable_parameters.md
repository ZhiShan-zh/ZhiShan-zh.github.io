# C语言可变参数

# 效果示例

```c
#include <stdarg.h>
#include <stdio.h>

void fun(int len, ...){
    va_list vargs;
    va_start(vargs, len);
    if(len < 0){
        va_end(vargs);
    }else{
        for(int i=0; i<len; i++){
            printf("%d=%d\n", i+1, va_arg(vargs, int));
        }
    }
    va_end(vargs);
}

int
main(){
    fun(5, 6, 7, 8, 9, 10);
    return 0;
}
```

输出：

```
1=6
2=7
3=8
4=9                                                           
5=10
```

# 可变参数的使用方法

- 定义一个函数，最后一个参数为省略号，省略号前面可以设置自定义参数。
- 在函数定义中创建一个 **va_list** 类型变量，该类型是在 stdarg.h 头文件中定义的。
- 使用 **int** 参数和 **va_start** 宏来初始化 **va_list** 变量为一个参数列表。宏 va_start 是在 stdarg.h 头文件中定义的。
- 使用 **va_arg** 宏和 **va_list** 变量来访问参数列表中的每个项。
- 使用宏 **va_end** 来清理赋予 **va_list** 变量的内存。