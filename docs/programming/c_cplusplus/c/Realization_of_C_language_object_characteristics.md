# C语言对象特性的实现

# 1 概述

# 2 Python3对象特性的实现

**version**：3.8.6

## 2.1 PyObject：Python对象机制的核心

在 Python 的世界中，一切都是对象，一个整数是一个对象，一个字符串也是一个对象，更为奇妙的是，类型也是一个对象，整数类型是一个对象，字符串类型也是一个对象。

Python是由C语言开发的，C语言不是面向对象的语言，那么是如果通过C实现的Python的面向对象机制呢？

在 Python 中，一个对象一旦被创建，它在内存中的大小就是不变的了。这就意味着那些需要容纳可变长度数据的对象只能在对象内维护一个指向一个可变大小的内存区域的指针。为什么要设定这样一条特殊的规则呢，因为遵循这样的规则可以使通过指针维护对象的工作变得非常的简单。

在 Python 中，所有的东西都是对象，而所有的对象都拥有一些相同的内容，这些内容在 PyObject 中定义，PyObject 是整个 Python 对象机制的核心。

文件：`Include/object.h`

```c
typedef struct _object
{
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    struct _typeobject *ob_type;//就是对象的__class__将返回的信息，也就是metaclass。
} PyObject;
```

参见：

- [宏_PyObject_HEAD_EXTRA](# 2.1.1 宏`_PyObject_HEAD_EXTRA`)

实际上，PyObject 是 Python 中不包含可变长度数据的对象的基石，而对于包含可变长度数据的对象，它的基石是 PyVarObject：

```c
typedef struct
{
    PyObject ob_base;
    Py_ssize_t ob_size; /* Number of items in variable part */
} PyVarObject;
```

注：

- **ob_size**：此变量实际上就是指明了该 对象中一共包含了多少个元素。
  - 注意，ob_size 指明的是元素的个数，而不是字节的数目。

可以看出PyObject中定义了每一个 Python 对象都必须有的内容，这些内容将出现在每一个 Python 对象所占有的内存的最开始的字节中，这就是说，在 Python 中，每一个对象都拥有相同的对象头部。这就使得在 Python 中，对对象的引用变得非常的统一，我们只需要用一个 PyObject *就可以引用任意的一个对象（因为C语言中的指针代表的目标内存的首地址），而不论该对象实际是一个什么对象。

### 2.1.1 宏`_PyObject_HEAD_EXTRA`

结构体`_object`中的宏`_PyObject_HEAD_EXTRA`的作用是，如果定义了宏`Py_TRACE_REFS`则在`struct _object`里边定义两个`struct _object`类型的指针以支持所有活动堆对象的双向链接列表。

```c
#ifdef Py_TRACE_REFS
/* Define pointers to support a doubly-linked list of all live heap objects. */
#define _PyObject_HEAD_EXTRA  \
    struct _object *_ob_next; \
    struct _object *_ob_prev;

#define _PyObject_EXTRA_INIT 0, 0,

#else
#define _PyObject_HEAD_EXTRA
#define _PyObject_EXTRA_INIT
#endif
```

注：宏`Py_TRACE_REFS`是在文件`configure`文件中写入到`confdefs.h`头文件的：

```shell
if test "$with_trace_refs" = "yes"
then

$as_echo "#define Py_TRACE_REFS 1" >>confdefs.h

fi
```

## 2.2 类型对象PyTypeObject

类型对象PyTypeObject是一个可变长度的对象，因为其开始位置使用宏定义`PyObject_VAR_HEAD`引入了PyVarObject ob_base定义。

```c
// >>>Python-3.8.6\Include\cpython\object.h
typedef struct _typeobject {
    PyObject_VAR_HEAD//宏定义：#define PyObject_VAR_HEAD PyVarObject ob_base;
    const char *tp_name; /* For printing, in format "<module>.<name>" */
    Py_ssize_t tp_basicsize, tp_itemsize; /* For allocation */

    /* Methods to implement standard operations */

    destructor tp_dealloc;
    Py_ssize_t tp_vectorcall_offset;
    getattrfunc tp_getattr;
    setattrfunc tp_setattr;
    PyAsyncMethods *tp_as_async; /* formerly known as tp_compare (Python 2)
                                    or tp_reserved (Python 3) */
    reprfunc tp_repr;

    /* Method suites for standard classes */

    PyNumberMethods *tp_as_number;
    PySequenceMethods *tp_as_sequence;
    PyMappingMethods *tp_as_mapping;

    /* More standard operations (here for binary compatibility) */

    hashfunc tp_hash;
    ternaryfunc tp_call;
    reprfunc tp_str;
    getattrofunc tp_getattro;
    setattrofunc tp_setattro;

    /* Functions to access object as input/output buffer */
    PyBufferProcs *tp_as_buffer;

    /* Flags to define presence of optional/expanded features */
    unsigned long tp_flags;

    const char *tp_doc; /* Documentation string */

    /* Assigned meaning in release 2.0 */
    /* call function for all accessible objects */
    traverseproc tp_traverse;

    /* delete references to contained objects */
    inquiry tp_clear;

    /* Assigned meaning in release 2.1 */
    /* rich comparisons */
    richcmpfunc tp_richcompare;

    /* weak reference enabler */
    Py_ssize_t tp_weaklistoffset;

    /* Iterators */
    getiterfunc tp_iter;
    iternextfunc tp_iternext;

    /* Attribute descriptor and subclassing stuff */
    struct PyMethodDef *tp_methods;
    struct PyMemberDef *tp_members;
    struct PyGetSetDef *tp_getset;
    struct _typeobject *tp_base;
    PyObject *tp_dict;//这个对象再python2.1.3中是不存在的，再Python2.2.3中才开始出现，
    descrgetfunc tp_descr_get;
    descrsetfunc tp_descr_set;
    Py_ssize_t tp_dictoffset;
    initproc tp_init;
    allocfunc tp_alloc;
    newfunc tp_new;
    freefunc tp_free; /* Low-level free-memory routine */
    inquiry tp_is_gc; /* For PyObject_IS_GC */
    PyObject *tp_bases;
    PyObject *tp_mro; /* method resolution order */
    PyObject *tp_cache;
    PyObject *tp_subclasses;
    PyObject *tp_weaklist;
    destructor tp_del;

    /* Type attribute cache version tag. Added in version 2.6 */
    unsigned int tp_version_tag;

    destructor tp_finalize;
    vectorcallfunc tp_vectorcall;

    /* bpo-37250: kept for backwards compatibility in CPython 3.8 only */
    Py_DEPRECATED(3.8) int (*tp_print)(PyObject *, FILE *, int);

#ifdef COUNT_ALLOCS
    /* these must be last and never explicitly initialized */
    Py_ssize_t tp_allocs;
    Py_ssize_t tp_frees;
    Py_ssize_t tp_maxalloc;
    struct _typeobject *tp_prev;
    struct _typeobject *tp_next;
#endif
} PyTypeObject;
```

在`_typeobject`的定义中包含了许多的信息，主要可以分为四类：

1. 类型名：tp_name，主要是 Python 内部以及调试的时候使用。

2. 创建该类型对象是分配内存空间的大小的信息，即 tp_basicsize 和
   tp_itemsize；

3. 与该类型对象相关联的操作信息：

   - 实现标准操作的方法：

     - `destructor tp_dealloc;`：

       - 函数指针的声明：`typedef void (*destructor)(PyObject *);`

     - `Py_ssize_t tp_vectorcall_offset;`：

       ```c
       // >>>Python-3.8.6\Include\pyport.h
       /* Py_ssize_t is a signed integral type such that sizeof(Py_ssize_t) ==
        * sizeof(size_t).  C99 doesn't define such a thing directly (size_t is an
        * unsigned integral type).  See PEP 353 for details.
        */
       #ifdef HAVE_SSIZE_T
       typedef ssize_t         Py_ssize_t;
       #elif SIZEOF_VOID_P == SIZEOF_SIZE_T
       typedef Py_intptr_t     Py_ssize_t;
       #else
       #   error "Python needs a typedef for Py_ssize_t in pyport.h."
       #endif
       
       // >>>Python-3.8.6\PC\pyconfig.h
       /* Define like size_t, omitting the "unsigned" */
       #ifdef MS_WIN64
       typedef __int64 ssize_t;
       #else
       typedef _W64 int ssize_t;
       #endif
       #define HAVE_SSIZE_T 1
       ```

     - `getattrfunc tp_getattr;`：

       ```c
       # >>>Python-3.8.6\Include\object.h
       typedef PyObject *(*getattrfunc)(PyObject *, char *);
       ```

       

     - `setattrfunc tp_setattr;`：

       ```c
       # >>>Python-3.8.6\Include\object.h
       typedef int (*setattrfunc)(PyObject *, char *, PyObject *);
       ```

       

     - `PyAsyncMethods *tp_as_async;`：

       ```c
       // >>>Python-3.8.6\Include\cpython\object.h
       typedef struct {
           unaryfunc am_await;
           unaryfunc am_aiter;
           unaryfunc am_anext;
       } PyAsyncMethods;
       
       # >>>Python-3.8.6\Include\object.h
       typedef PyObject *(*unaryfunc)(PyObject *);
       ```

       

     - `reprfunc tp_repr;`：

       ```c
       // >>>Python-3.8.6\Include\object.h
       typedef PyObject *(*reprfunc)(PyObject *);
       ```

       

   - 标准类的方法套件：

     - `PyNumberMethods *tp_as_number;`：

       ```c
       // >>>Python-3.8.6\Include\cpython\object.h
       typedef struct {
           /* Number implementations must check *both*
              arguments for proper type and implement the necessary conversions
              in the slot functions themselves. */
           /*数字实现方法必须检查两个参数的类型是否正确，并在插槽函数本身中实现必要的转换。*/
       
           binaryfunc nb_add;//python中档a+b发生时，会调用int对象中的int.__add__,会通过PyTypeObject中的 PyObject *tp_dict 查看对应关系（对应于此方法），然后调用调用次方法完成加法操作。
           binaryfunc nb_subtract;//减法，int.__rsub__
           binaryfunc nb_multiply;//乘法，int.__mul__
           binaryfunc nb_remainder;//
           binaryfunc nb_divmod;
           ternaryfunc nb_power;
           unaryfunc nb_negative;
           unaryfunc nb_positive;
           unaryfunc nb_absolute;
           inquiry nb_bool;
           unaryfunc nb_invert;
           binaryfunc nb_lshift;
           binaryfunc nb_rshift;
           binaryfunc nb_and;
           binaryfunc nb_xor;
           binaryfunc nb_or;
           unaryfunc nb_int;
           void *nb_reserved;  /* the slot formerly known as nb_long */
           unaryfunc nb_float;
       
           binaryfunc nb_inplace_add;
           binaryfunc nb_inplace_subtract;
           binaryfunc nb_inplace_multiply;
           binaryfunc nb_inplace_remainder;
           ternaryfunc nb_inplace_power;
           binaryfunc nb_inplace_lshift;
           binaryfunc nb_inplace_rshift;
           binaryfunc nb_inplace_and;
           binaryfunc nb_inplace_xor;
           binaryfunc nb_inplace_or;
       
           binaryfunc nb_floor_divide;
           binaryfunc nb_true_divide;
           binaryfunc nb_inplace_floor_divide;
           binaryfunc nb_inplace_true_divide;
       
           unaryfunc nb_index;
       
           binaryfunc nb_matrix_multiply;
           binaryfunc nb_inplace_matrix_multiply;
       } PyNumberMethods;
       
       # >>>Python-3.8.6\Include\object.h
       typedef PyObject *(*unaryfunc)(PyObject *);
       typedef PyObject *(*binaryfunc)(PyObject *, PyObject *);//双元函数
       typedef PyObject *(*ternaryfunc)(PyObject *, PyObject *, PyObject *);
       typedef int (*inquiry)(PyObject *);
       ```

     - `PySequenceMethods *tp_as_sequence;`：

     - ``：

     - ``：

     - ``：

     - `PyMappingMethods *tp_as_mapping;`：

     - ``：

     - ``：

     - ``：

     - ``：

     - ``：

     - ``：

     - ``：

     - ``：

     - ``：

     - ``：

   - 更多的标准操作（为了二进制兼容性）：

     - `hashfunc tp_hash;`：

     - ``：

     - ``：

     - `ternaryfunc tp_call;`：对应于class对象的`__call__`

       ```c
       // >>>Python-3.8.6\Include\object.h
       typedef PyObject *(*ternaryfunc)(PyObject *, PyObject *, PyObject *);
       ```

       - python中的可调用性（callable）：只要一个对象的class中实现了`__call__`操作（更确切地说，再Python内部的PyTypeObject中，`tp_call`不为空），那么这个对象就是一个可调用的对象。换句话说，再Python中，所谓的“调用”就是执行对象的type所对应的class对象的`tp_call`操作。下边代码展示了一个可调用对象：

         ```python
         class A:
             def __call__(self, *args, **kwargs):
                 print("Hello Python")
         
         if __name__=="__main__":
             a = A()
             a()
         // 输出：Hello Python
         ```

       - 

     - ``：

     - `reprfunc tp_str;`：

     - ``：

     - `getattrofunc tp_getattro;`：

     - `setattrofunc tp_setattro;`：

   - 访问对象作为输入/输出缓冲区的函数：

   - 定义可选/扩展功能的标志：

   - 文档字符串：

   - 所有可访问对象的调用函数：

     - `traverseproc tp_traverse;`

   - 删除对包含对象的引用：

     - `inquiry tp_clear;`:

   - rich comparisons

     - `richcmpfunc tp_richcompare;`:

   - 弱引用支持：

     - `Py_ssize_t tp_weaklistoffset;`:

   - 迭代器：

     - `getiterfunc tp_iter;`:
     - `iternextfunc tp_iternext;`:

   - 属性描述符和子类化的东西：

     - `struct PyMethodDef *tp_methods;`：
     - `struct PyMemberDef *tp_members;`：
     - `struct PyGetSetDef *tp_getset;`：
     - `struct _typeobject *tp_base;`：
     - `PyObject *tp_dict;`：完成内置类型从type对象到class对象的关键
     - `descrgetfunc tp_descr_get;`：
     - `descrsetfunc tp_descr_set;`：
     - `Py_ssize_t tp_dictoffset;`：
     - `initproc tp_init;`：
     - `allocfunc tp_alloc;`：
     - `newfunc tp_new;`：
     - `freefunc tp_free;`：
     - `inquiry tp_is_gc;`：
     - `PyObject *tp_bases;`：
     - `PyObject *tp_mro;`：
     - `PyObject *tp_cache;`：
     - `PyObject *tp_subclasses;`：
     - `PyObject *tp_weaklist;`：
     - `destructor tp_del;`：

   - ``:

   - ``:

   - ``:

   - ``:

   - ``:

   - ``:

   - ``: