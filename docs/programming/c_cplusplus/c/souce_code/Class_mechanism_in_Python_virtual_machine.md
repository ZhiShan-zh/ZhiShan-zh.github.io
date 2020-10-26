# Python虚拟机中的类机制

# 1 Python中的对象模型

在Python2.2之前，Python中存在着一个巨大的裂缝，就是Python的内置type（比如int、dict）于Python程序员定义的class并不完成等同。比如，程序员自定义的class A可以被继承，作为另一个class B的基类，但是Python的内置类型却不能被继承。

在面向对象的理论中，有两个核心的概念：类和对象。Python中也实现了这两个概念，但是在Python中所有的东西都是对象，所以类也是一种对象。

在Python2.2之前，Python中存在三类对象：

- type对象：表示Python内置的类型；
- class对象：表示Python程序员自定义的类型；
- instance对象（实例对象）：表示由class对象创建的实例。

在Python2.2之后，type和class已经统一，我们用class对象来统一表示之前的type对象和class对象。

## 1.1 对象间的关系

Python对象之前存在着两种关系：

- `is-kind-of`关系：这种关系对应于面向对象中的基类和子类之间的关系；
- `is-instance-of`关系：这种关系对应于面向对象中的类和实例之间的关系。

```python
class A(object):
    pass

a = A()
```

- 其中存在三个对象：
  - object（class对象）
  - A（class对象）
  - a（instance对象）
- `is-kind-of`关系：object和A之间，A是object的子类；
- `is-instance-of`关系：
  - a和A之间，a是A的一个实例；
  - a和object之间，a也是object的一个实例。



Python提供了一些方法用来探测这些关系：

- 通过对象的`__class__`属性或Python内置的type方法可以探测一个对象和哪个对象存在`is-instance-of`关系；

- 通过对象的`__bases__`属性可以探测一个对象和哪个对象存在`is-kind-of`关系。

- Python还提供两个内置方法：

  - `issubclass(class, classinfo)`：判断class是否是classinfo的子类

    ```python
    class A:
        pass
    class B(A):
        pass
    print(issubclass(B, A))  #输出：True
    ```

  - `isinstance(object, classinfo)`：判断object是否是classinfo的实例

    ```python
    class A:
        pass
     
    class B(A):
        pass
    isinstance(A(), A)    # return True
    type(A()) == A        # return True
    isinstance(B(), A)    # return True
    type(B()) == A        # return False
    ```

## 1.2 `<class 'type'>`和`<class 'object'>`

`<class 'type'>`属于Python中的一种特殊的class对象，这种特殊的class对象能够成为其他class对象的type。这种特殊的class对象我们称之为metaclass对象。创建一个class对象的关键之处在于metaclass对象。

```c
// >>>Python-3.8.6/Objects/typeobject.c
PyTypeObject PyBaseObject_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "object",                                   /* tp_name */
    sizeof(PyObject),                           /* tp_basicsize */
    0,                                          /* tp_itemsize */
    object_dealloc,                             /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    object_repr,                                /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    (hashfunc)_Py_HashPointer,                  /* tp_hash */
    0,                                          /* tp_call */
    object_str,                                 /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    PyObject_GenericSetAttr,                    /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   /* tp_flags */
    object_doc,                                 /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    object_richcompare,                         /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    object_methods,                             /* tp_methods */
    0,                                          /* tp_members */
    object_getsets,                             /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    object_init,                                /* tp_init */
    PyType_GenericAlloc,                        /* tp_alloc */
    object_new,                                 /* tp_new */
    PyObject_Del,                               /* tp_free */
};


PyTypeObject PyType_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "type",                                     /* tp_name */
    sizeof(PyHeapTypeObject),                   /* tp_basicsize */
    sizeof(PyMemberDef),                        /* tp_itemsize */
    (destructor)type_dealloc,                   /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    (reprfunc)type_repr,                        /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    (ternaryfunc)type_call,                     /* tp_call */
    0,                                          /* tp_str */
    (getattrofunc)type_getattro,                /* tp_getattro */
    (setattrofunc)type_setattro,                /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE | Py_TPFLAGS_TYPE_SUBCLASS,         /* tp_flags */
    type_doc,                                   /* tp_doc */
    (traverseproc)type_traverse,                /* tp_traverse */
    (inquiry)type_clear,                        /* tp_clear */
    0,                                          /* tp_richcompare */
    offsetof(PyTypeObject, tp_weaklist),        /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    type_methods,                               /* tp_methods */
    type_members,                               /* tp_members */
    type_getsets,                               /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    offsetof(PyTypeObject, tp_dict),            /* tp_dictoffset */
    type_init,                                  /* tp_init */
    0,                                          /* tp_alloc */
    type_new,                                   /* tp_new */
    PyObject_GC_Del,                            /* tp_free */
    (inquiry)type_is_gc,                        /* tp_is_gc */
};

// >>>Python-3.8.6/Objects/listobject.c
PyTypeObject PyList_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "list",
    sizeof(PyListObject),
    0,
    (destructor)list_dealloc,                   /* tp_dealloc */
    0,                                          /* tp_vectorcall_offset */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    (reprfunc)list_repr,                        /* tp_repr */
    0,                                          /* tp_as_number */
    &list_as_sequence,                          /* tp_as_sequence */
    &list_as_mapping,                           /* tp_as_mapping */
    PyObject_HashNotImplemented,                /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE | Py_TPFLAGS_LIST_SUBCLASS, /* tp_flags */
    list___init____doc__,                       /* tp_doc */
    (traverseproc)list_traverse,                /* tp_traverse */
    (inquiry)_list_clear,                       /* tp_clear */
    list_richcompare,                           /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    list_iter,                                  /* tp_iter */
    0,                                          /* tp_iternext */
    list_methods,                               /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)list___init__,                    /* tp_init */
    PyType_GenericAlloc,                        /* tp_alloc */
    PyType_GenericNew,                          /* tp_new */
    PyObject_GC_Del,                            /* tp_free */
};

```



Python中还有一个特殊的class对象——`<class 'object'>`，在Python中，任何一个class都必须直接或间接继承自object，这个object可以视之为万物之母。

```shell
>>> type.__class__
<class 'type'>
>>> type.__bases__
(<class 'object'>,)
>>> object.__class__
<class 'type'>
>>> object.__bases__
()
>>> int.__class__
<class 'type'>
>>> int.__bases__
(<class 'object'>,)
>>> dict.__class__
<class 'type'>
>>> dict.__bases__
(<class 'object'>,)
```

![image-20201006165049958](https://zhishan-zh.github.io/media/python_source_code_20201006165301.png)

如上图所示，中间一列的class对象有一种类似于“波粒二相性”的特殊性质，我们说Python中的对象分为class对象和instance对象，但中间这一列的对象即是class对象，又是instance对象。说它是class对象，因为它可以通过实例化的动作创建新的instance对象；说它是instance对象，因为它确实是metaclass对象经过实例化得到的。

- 在Python中，任何一个对象都有一个type，可以通过对象的`__class__`属性获得。任何一个instance对象的type都是一个class对象，而任何一个class对象的type都是metaclass对象。在大多数情况下这个metaclass都是`<type 'type'>`，而在Python内部，它实际上对应的就是PyType_Type。
- 在Python中，任何一个class对象都直接或间接与`<class 'object'>`对象之间存在`is-kind-of`关系，包括`<class 'type'>`。在Python内部，`<class 'object'>`对应的是PyBaseObject_Type。

# 2 从type对象到class对象

在Python中，实现“类”这个概念的是class对象，在Python内部，class对象其实就是一个PyObject结构体。

```c
class MyInt(int):
    def __add__(self, other):
        return int.__add__(self, other) + 10;

a = MyInt(1)
b = MyInt(2)
print(a+b)
```

当`a+b`发生时，会调用`MyInt.__add__`，在这里调用了`int.__add__`。当虚拟机需要调用`int.__add__`时，它可以到符号“int”对应的class对象——PyLong_Type——的tp_dict指向的dict对象中查找符号`__add__`对应的操作，并调用该操作，从而完成`int.__add__`的调用。

在Python中，不仅只有函数可以被调用，一切对象都有可能被调用。

在Python中有一个可调用性（calllable）的概念，只要一对象对应的class对象中实现了`__call__`操作（更确切地说，在Python内部的PyTypeObject中，tp_call不为空）那么这个对象就是一个可调用的对象，换句话说，在Python中，所谓”调用“，就是执行对象的type锁对应的class对象的tp_call操作。

## 2.1 处理基类和type信息

```c
// >>>Python-3.8.6/Objects/typeobject.c
int
PyType_Ready(PyTypeObject *type)
{
    PyObject *dict, *bases;
    PyTypeObject *base;
    Py_ssize_t i, n;
	//此后省略N行代码
    
    //类型名称不能为空
    if (type->tp_name == NULL) {
        PyErr_Format(PyExc_SystemError,
                     "Type does not define the tp_name field.");
        goto error;
    }

    /* 初始化tp_base（基类），如果tp_base为空并且type(当前类型)不是PyBaseObject_Type则设置其基类为PyBaseObject_Type*/
    base = type->tp_base;
    if (base == NULL && type != &PyBaseObject_Type) {
        base = type->tp_base = &PyBaseObject_Type;
        Py_INCREF(base);
    }

    /* 现在只有当type（当前类型）为PyBaseObject_Type时，其基类才为空
     */

    /* 如果基类没有初始化，则先初始化基类，参见下一节：处理基类列表 */
    if (base != NULL && base->tp_dict == NULL) {
        if (PyType_Ready(base) < 0)
            goto error;
    }

    /*
    如果当前type的类型不为空，且其基类不为空，则设置其类型为基类的类型
    */
    if (Py_TYPE(type) == NULL && base != NULL)
        Py_TYPE(type) = Py_TYPE(base);
	//此后省略N行代码
}

// >>>Python-3.8.6/Include/object.h
static inline void _Py_INCREF(PyObject *op)
{
    _Py_INC_REFTOTAL;
    op->ob_refcnt++;
}
#define Py_INCREF(op) _Py_INCREF(_PyObject_CAST(op))
#define Py_TYPE(ob) (_PyObject_CAST(ob)->ob_type)
```

## 2.2 处理基类列表

接下来，Python虚拟机将处理类型的基类列表，因为Python支持多重继承，所以每一个Python的class对象都会是一个基类列表。

```c
// >>>Python-3.8.6/Objects/typeobject.c
int
PyType_Ready(PyTypeObject *type)//PyBaseObject_Type
{
    PyObject *dict, *bases;
    PyTypeObject *base;
    Py_ssize_t i, n;
	//此后省略N行代码
    
    /*
    如果当前type的类型不为空，且其基类不为空，则设置其类型为基类的类型
    */
    if (Py_TYPE(type) == NULL && base != NULL)
        Py_TYPE(type) = Py_TYPE(base);
    
    //处理bases：基类列表
    bases = type->tp_bases;
    //如果bases为空，则会根据base的情况设置bases
    if (bases == NULL) {
        if (base == NULL)//type为PyBaseObject_Type的情况
            bases = PyTuple_New(0);
        else
            bases = PyTuple_Pack(1, base);
        if (bases == NULL)
            goto error;
        type->tp_bases = bases;
    }
	//此后省略N行代码
}
```

对于我们现在考虑的PyBaseObject_Type来说，其tp_bases为空，而其base也为NULL，所以它的基类列表就是一个空的tuple对象。

而对于PyType_Type和其他类型而言，虽然tp_bases为空，然是base不为NULL，而是&PyBaseObject_Type，所以它们的基类列表不为空，都包含一个PyBaseObject_Type。

## 2.3 填充tp_dict

```c
// >>>Python-3.8.6/Objects/typeobject.c
int
PyType_Ready(PyTypeObject *type)//PyBaseObject_Type
{
    PyObject *dict, *bases;
    PyTypeObject *base;
    Py_ssize_t i, n;
	//此后省略N行代码
    
	/* 初始化tp_dict */
    dict = type->tp_dict;
    if (dict == NULL) {
        dict = PyDict_New();
        if (dict == NULL)
            goto error;
        type->tp_dict = dict;
    }

    /* Add type-specific descriptors to tp_dict */
    if (add_operators(type) < 0)
        goto error;
    if (type->tp_methods != NULL) {
        if (add_methods(type, type->tp_methods) < 0)
            goto error;
    }
    if (type->tp_members != NULL) {
        if (add_members(type, type->tp_members) < 0)
            goto error;
    }
    if (type->tp_getset != NULL) {
        if (add_getset(type, type->tp_getset) < 0)
            goto error;
    }
	//此后省略N行代码
}
```

