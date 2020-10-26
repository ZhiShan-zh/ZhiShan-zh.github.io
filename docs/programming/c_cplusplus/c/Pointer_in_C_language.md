# C语言中的指针

对于内存首部相同的不同对象的指针可以用同一个顶层指针来接收:

```c
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

typedef struct{
    char * name;
} Name;

typedef struct{
    Name name;
} Type;

typedef struct{
    Name name;
    char * str;
} TypeChar;

int main(){
    TypeChar *typeChar;
    typeChar->name.name = "char";
    typeChar->str = "testChar";
    Type * type = typeChar;
    //输出
    printf("Type->Name.name:%s\n", type->name.name);
    //把type强转成TypeChar，并输出其内容：
    printf("typeChar->name.name=%s, typeChar->str=%s\n", ((TypeChar *)type)->name.name, typeChar->str);
    return 0;
}
```

输出：

```
Type->Name.name:char
typeChar->name.name=char, typeChar->str=testChar
```

