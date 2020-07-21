# C程序内存分配管理

# 1 程序的内存空间

## 1.1 C/C++程序存储时结构

### 1.1.1 测试程序代码

名称：`main.c`

```c
#include <stdio.h>
#include <stdlib.h>
int var1 = 1;
char *p1;
int main(void) {
	int var2;
    int var3 = 2;
    static int var4 = 3;
    p1 = new char[10];
    char * p2 = new char[20];
    printf("hello, world!\n");
    exit(0);
}
```

### 1.1.2 查看文件的元数据信息

编译当前c程序：`gcc main.c`

查看文件的元数据信息：

```shell
[zh@zh-inspironn4050 桌面]$ ls -al a.out 
-rwxr-xr-x 1 zh zh 16680  7月 15 15:40 a.out
```

### 1.1.3 使用file命令查看文件的编码格式

识别文件类型和辨别一些文件的编码格式：（通过查看文件的头部信息来获取文件类型）

```shell
[zh@zh-inspironn4050 桌面]$ file a.out 
a.out: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=248363e74201c54f3d22180d8e483e79a76168d3, for GNU/Linux 3.2.0, not stripped
```

### 1.1.4 使用size命令可执行文件（`.out`）存储时结构

size命令：显示一个目标文件或者链接库文件中的目标文件的各个段的大小，当没有输入文件名时，默认为`a.out`。

```shell
[zh@zh-inspironn4050 桌面]$ size a.out 
   text	   data	    bss	    dec	    hex	filename
   1566	    600	     16	   2182	    886	a.out
```

**解释**：

- code segment/text segment：代码段
    - 通常是指用来存放程序执行代码的一块内存区域。
        - 也可以说是存放CPU执行的机器指令（machine instructions）。
    - 通常代码区是可共享的（即另外的执行程序可以调用它），因为对于频繁被执行的程序，只需要在内存中有一份代码即可。
    - 这部分区域的大小在程序运行前就已经确定，并且内存区域通常属于只读，某些架构也允许代码段为可写，即允许修改程序。
    - 在代码段中，也有可能包含一些只读的常数变量，例如字符串常量等。 
    - 代码区还规划了局部变量的相关信息。
- initialized data segment/data segment：全局初始化数据区/静态数据区
    - 该区包含了在程序中明确被初始化的全局变量、静态变量（包括全局静态变量和局部静态变量）。
    - 数据段属于静态内存分配。 
- bss segment：（Block Started by Symbol ）
    - 表示包含静态变量和已经初始化（可执行文件包含了初始化的值）的全局变量的数据段大小。
    - 通常是指用来存放程序中未初始化的全局变量的一块内存区域。
    - 属于静态内存分配。
- dec：十进制总和
- hex：十六进制总和
- filename：文件名

由此可见可执行文件在存储（还没有载入内存）的时候，分为：

- 代码区
- 数据区
- 未初始化数据区

##  1.2 Linux程序运行时内存空间

程序在运行时，由于内存的管理方式是以页为单位的，而且程序使用的地址都是虚拟地址，当程序要使用内存时，操作系统再把虚拟地址映射到真实的物理内存的地址上。所以在程序中，以虚拟地址来看，数据或代码是一块块地存在于内存中的，通常我们称其为一个段。而且代码和数据是分开存放的，即不储存于同于一个段中，而且各种数据也是分开存放在不同的段中的。

### 1.2.1 测试程序代码

文件名：`main.c`

```c
#include <unistd.h>
#include <stdio.h>
 
int main()
{
    printf("程序pid=%d\n", getpid());
    while(1);//进入死循环，以便不退出程序
    return 0;
}
```

说明：

- `unistd.h`：为Linux/Unix系统中内置头文件，包含了许多系统服务的函数原型，例如read函数、write函数和getpid函数等。
    其作用相当于windows操作系统的`windows.h`，是操作系统为用户提供的统一API接口，方便调用系统提供的一些服务。

### 1.2.2 查看程序运行过程中内存空间的情况

编译程序：`gcc main.c`

运行程序：

```shell
[zh@zh-inspironn4050 桌面]$ ./a.out 
程序pid=20652

```

在Linux下有一个目录`/proc/$(pid)`，这个目录保存了进程号为pid的进程运行时的所有信息，其中有一个文件maps，它记录了程序执行过程中的内存空间的情况。

```shell
[zh@zh-inspironn4050 桌面]$ cd
[zh@zh-inspironn4050 ~]$ cd /proc/20652
[zh@zh-inspironn4050 20652]$ ls
arch_status      environ    mem            personality   statm
attr             exe        mountinfo      projid_map    status
autogroup        fd         mounts         root          syscall
auxv             fdinfo     mountstats     sched         task
cgroup           gid_map    net            schedstat     timers
clear_refs       io         ns             sessionid     timerslack_ns
cmdline          latency    numa_maps      setgroups     uid_map
comm             limits     oom_adj        smaps         wchan
coredump_filter  loginuid   oom_score      smaps_rollup
cpuset           map_files  oom_score_adj  stack
cwd              maps       pagemap        stat
```

说明：

- **cmdline**：是一个只读文件，包含进程的完整命令行信息。如果该进程已经被交换出内存或者这个进程是 zombie 进程，则这个文件没有任何内容。该文件以空字符 null 而不是换行符作为结束标志。

    - ```shell
        [zh@zh-inspironn4050 3583]$ cat cmdline 
        ./a.out
        ```

- **exe**：为实际运行程序的符号链接

    - ```shell
        [zh@zh-inspironn4050 3583]$ ls -al exe
        lrwxrwxrwx 1 zh zh 0  7月 16 08:54 exe -> /home/zh/桌面/a.out
        ```

- **comm**：包含进程的命令名。

    - ```shell
        [zh@zh-inspironn4050 3583]$ cat comm
        a.out
        ```

- **cwd**：是进程当前工作目录的符号链接。

    - ```shell
        [zh@zh-inspironn4050 3583]$ ls -al cwd
        lrwxrwxrwx 1 zh zh 0  7月 16 08:56 cwd -> /home/zh/桌面
        ```

- **environ**：显示进程的环境变量。

    - ```shell
        [zh@zh-inspironn4050 3583]$ cat environ 
        SHELL=/bin/bashSESSION_MANAGER=local/zh-inspironn4050:@/tmp/.ICE-unix/1194,unix/zh-inspironn4050:/tmp/.ICE-unix/1194WINDOWID=94371843COLORTERM=truecolorXDG_CONFIG_DIRS=/etc/xdgXDG_SESSION_PATH=/org/freedesktop/DisplayManager/Session0NVM_INC=/home/zh/.nvm/versions/node/v12.16.2/include/nodeXDG_MENU_PREFIX=xfce-GTK_IM_MODULE=ibusLC_ADDRESS=zh_CN.UTF-8LC_NAME=zh_CN.UTF-8SSH_AUTH_SOCK=/tmp/ssh-EoHVjsejX0ts/agent.1307XMODIFIERS=@im=ibusDESKTOP_SESSION=xfceLC_MONETARY=zh_CN.UTF-8SSH_AGENT_PID=1311EDITOR=/usr/bin/nanoGTK_MODULES=canberra-gtk-module:canberra-gtk-moduleXDG_SEAT=seat0PWD=/home/zh/桌面LOGNAME=zhXDG_SESSION_DESKTOP=xfceQT_QPA_PLATFORMTHEME=qt5ctXDG_SESSION_TYPE=x11PANEL_GDK_CORE_DEVICE_EVENTS=0XAUTHORITY=/home/zh/.XauthorityXDG_GREETER_DATA_DIR=/var/lib/lightdm-data/zhGTK2_RC_FILES=/home/zh/.gtkrc-2.0HOME=/home/zhLC_PAPER=zh_CN.UTF-8LANG=zh_CN.utf8LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=01;05;37;41:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.pdf=00;32:*.ps=00;32:*.txt=00;32:*.patch=00;32:*.diff=00;32:*.log=00;32:*.tex=00;32:*.doc=00;32:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.axa=00;36:*.oga=00;36:*.spx=00;36:*.xspf=00;36:XDG_CURRENT_DESKTOP=XFCEVTE_VERSION=6003XDG_SEAT_PATH=/org/freedesktop/DisplayManager/Seat0NVM_DIR=/home/zh/.nvmXDG_SESSION_CLASS=userLC_IDENTIFICATION=zh_CN.UTF-8TERM=xterm-256colorUSER=zhDISPLAY=:0.0SHLVL=1NVM_CD_FLAGS=LC_TELEPHONE=zh_CN.UTF-8QT_IM_MODULE=ibusLC_MEASUREMENT=zh_CN.UTF-8XDG_VTNR=7XDG_SESSION_ID=2MOZ_PLUGIN_PATH=/usr/lib/mozilla/pluginsXDG_RUNTIME_DIR=/run/user/1000LC_TIME=zh_CN.UTF-8QT_AUTO_SCREEN_SCALE_FACTOR=0XDG_DATA_DIRS=/home/zh/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share:/usr/share:/var/lib/snapd/desktop:/usr/sharePATH=/home/zh/.nvm/versions/node/v12.16.2/bin:/home/zh/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/var/lib/snapd/snap/binGDMSESSION=xfceDBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/busHG=/usr/bin/hgNVM_BIN=/home/zh/.nvm/versions/node/v12.16.2/binMAIL=/var/spool/mail/zhLC_NUMERIC=zh_CN.UTF-8_=./a.outOLDPWD=/home/zh
        ```

- **fd**：是一个目录，包含进程打开文件的情况。

    - ```shell
        [zh@zh-inspironn4050 3583]$ ls -al fd
        总用量 0
        dr-x------ 2 zh zh  0  7月 16 08:56 .
        dr-xr-xr-x 9 zh zh  0  7月 16 08:54 ..
        lrwx------ 1 zh zh 64  7月 16 09:03 0 -> /dev/pts/0
        lrwx------ 1 zh zh 64  7月 16 09:03 1 -> /dev/pts/0
        lrwx------ 1 zh zh 64  7月 16 09:03 2 -> /dev/pts/0
        ```

    - 目录中的每一项都是一个符号链接，指向打开的文件，数字则代表文件描述符。

- **latency**：显示哪些代码造成的延时比较大。

    - 如果需要使用这个特性：

        - 切换到管理员：`su`
        - 然后执行：`echo 1 > /proc/sys/kernel/latencytop`

    - ```shell
        [zh-inspironn4050 proc]# cat /proc/1/latency 
        Latency Top version : v0.1
        5 5886 3924 do_epoll_wait __x64_sys_epoll_wait do_syscall_64 entry_SYSCALL_64_after_hwframe
        ```

    - 每一行前三个数字分别是后面代码执行的次数，总共执行延迟时间（单位是微秒）和最长执行延迟时间（单位是微秒），后面则是代码完整的调用栈。

- **limits**：显示当前进程的资源限制。

    - ```shell
        [zh@zh-inspironn4050 3583]$ cat limits 
        Limit                     Soft Limit           Hard Limit           Units     
        Max cpu time              unlimited            unlimited            seconds   
        Max file size             unlimited            unlimited            bytes     
        Max data size             unlimited            unlimited            bytes     
        Max stack size            8388608              unlimited            bytes     
        Max core file size        unlimited            unlimited            bytes     
        Max resident set          unlimited            unlimited            bytes     
        Max processes             23352                23352                processes 
        Max open files            1024                 524288               files     
        Max locked memory         65536                65536                bytes     
        Max address space         unlimited            unlimited            bytes     
        Max file locks            unlimited            unlimited            locks     
        Max pending signals       23352                23352                signals   
        Max msgqueue size         819200               819200               bytes     
        Max nice priority         0                    0                    
        Max realtime priority     0                    0                    
        Max realtime timeout      unlimited            unlimited            us 
        ```

    - Soft Limit：表示kernel设置给资源的值

    - Hard Limit：表示Soft Limit的上限

    - Units：则为计量单元。

- **maps**：显示进程的内存区域映射信息。

    - 记录程序运行的过程中需要哪些库和哪些空间

    - ```shell
        [zh@zh-inspironn4050 20652]$ cat maps
        5618599dd000-5618599de000 r--p 00000000 08:11 810702                     /home/zh/桌面/a.out
        5618599de000-5618599df000 r-xp 00001000 08:11 810702                     /home/zh/桌面/a.out
        5618599df000-5618599e0000 r--p 00002000 08:11 810702                     /home/zh/桌面/a.out
        5618599e0000-5618599e1000 r--p 00002000 08:11 810702                     /home/zh/桌面/a.out
        5618599e1000-5618599e2000 rw-p 00003000 08:11 810702                     /home/zh/桌面/a.out
        561859e43000-561859e64000 rw-p 00000000 00:00 0                          [heap]
        7fe706a1b000-7fe706a40000 r--p 00000000 08:11 402410                     /usr/lib/libc-2.31.so
        7fe706a40000-7fe706b8d000 r-xp 00025000 08:11 402410                     /usr/lib/libc-2.31.so
        7fe706b8d000-7fe706bd7000 r--p 00172000 08:11 402410                     /usr/lib/libc-2.31.so
        7fe706bd7000-7fe706bd8000 ---p 001bc000 08:11 402410                     /usr/lib/libc-2.31.so
        7fe706bd8000-7fe706bdb000 r--p 001bc000 08:11 402410                     /usr/lib/libc-2.31.so
        7fe706bdb000-7fe706bde000 rw-p 001bf000 08:11 402410                     /usr/lib/libc-2.31.so
        7fe706bde000-7fe706be4000 rw-p 00000000 00:00 0 
        7fe706c22000-7fe706c24000 r--p 00000000 08:11 402398                     /usr/lib/ld-2.31.so
        7fe706c24000-7fe706c44000 r-xp 00002000 08:11 402398                     /usr/lib/ld-2.31.so
        7fe706c44000-7fe706c4c000 r--p 00022000 08:11 402398                     /usr/lib/ld-2.31.so
        7fe706c4d000-7fe706c4e000 r--p 0002a000 08:11 402398                     /usr/lib/ld-2.31.so
        7fe706c4e000-7fe706c4f000 rw-p 0002b000 08:11 402398                     /usr/lib/ld-2.31.so
        7fe706c4f000-7fe706c50000 rw-p 00000000 00:00 0 
        7fffdedad000-7fffdedce000 rw-p 00000000 00:00 0                          [stack]
        7fffdede0000-7fffdede3000 r--p 00000000 00:00 0                          [vvar]
        7fffdede3000-7fffdede4000 r-xp 00000000 00:00 0                          [vdso]
        ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0                  [vsyscall]
        ```

    - 第一列：vm_start-m_end，是一个段的起始地址和结束地址

    - 第二列：vm_flags，此段虚拟地址空间的属性，每种属性用一个字段表示：
        - r：表示可读
        - w：表示可写
        - x：表示可执行
        - p&s：p和s共用一个字段，互斥关系
            - 表示私有段（即只对本进程有效，不共享）
            - s：表示共享段。
        - 如果没有相应的权限，则使用`-`代替。

    - 第三列：vm_pgoff
        - 对有名映射，表示此段虚拟内存起始地址在文件中以页为单位的偏移。
        - 对匿名映射，它等于0或者vm_start/PAGE_SIZE

    - 第四列：vm_file->f_dentry->d_inode->i_sb->s_dev，映射文件所属设备号。
        - 对匿名映射来说，因为没有文件在磁盘上，所以没有设备号，始终为00:00。
        - 对有名映射来说，是映射的文件所在设备的设备号。

    - 第五列：vm_file->f_dentry->d_inode->i_ino，映射文件所属节点号。
        - 对匿名映射来说，因为没有文件在磁盘上，所以没有节点号，始终为00:00。
        - 对有名映射来说，是映射的文件的节点号

    - 第六列：是这个段所存放的内容所对应的文件。
        - 对有名来说，是映射的文件名。
        - 对匿名映射来说，是此段虚拟内存在进程中的角色。
        - `[stack]`：表示在进程中作为栈使用。
            - 作为进程的临时数据区，由kernel把匿名内存map到虚存空间，栈空间的增长方向是从高地址到低地址。
        - `[heap]`：表示堆。
            - 当且仅当malloc调用时存在，由kernel把匿名内存map到虚存空间，堆则在程序中没有调用malloc的情况下不存在
        - 其余情况则无显示。

- **root**：是进程根目录的符号链接。

    - ```shell
        [zh@zh-inspironn4050 3583]$ ls -lt root
        lrwxrwxrwx 1 zh zh 0  7月 16 11:17 root -> /
        ```

- **stack**：显示当前进程的内核调用栈信息，只有内核编译时打开了CONFIG_STACKTRACE编译选项，才会生成这个文件。

    - ```shell
        [zh@zh-inspironn4050 1]$ sudo cat stack 
        [<0>] do_epoll_wait+0x63b/0x690
        [<0>] __x64_sys_epoll_wait+0x1a/0x20
        [<0>] do_syscall_64+0x49/0x90
        [<0>] entry_SYSCALL_64_after_hwframe+0x44/0xa9
        ```

- **statm**：显示进程所占用内存大小的统计信息，包含七个值，度量单位是page（page大小可通过getconf PAGESIZE得到）。

    - ```shell
        [zh@zh-inspironn4050 1]$ cat statm
        43695 2313 1807 235 0 6637 0
        ```

    - 第一个数字：进程占用的总的内存；

    - 第二个数字：进程当前时刻占用的物理内存；

    - 第三个数字：同其它进程共享的内存；

    - 第四个数字：进程的代码段；

    - 第五个数字：共享库（从2.6版本起，这个值为0）；

    - 第六个数字：进程的堆栈；

    - 第七个数字：dirty pages（从2.6版本起，这个值为0）。

- **syscall**：显示当前进程正在执行的系统调用。

    - 内核编译时打开了CONFIG_HAVE_ARCH_TRACEHOOK编译选项，才会生成这个文件。

    - ```shell
        [zh@zh-inspironn4050 1]$ sudo cat syscall
        232 0x4 0x55d3a3386ea0 0x53 0xffffffff 0x0 0x9e79683abe0a2bbc 0x7ffd86b16780 0x7f55f680ef3e
        ```

    - 第一个值是系统调用号，后面跟着6个系统调用的参数值（位于寄存器中），最后两个值依次是堆栈指针和指令计数器的值。

    - 如果当前进程虽然阻塞，但阻塞函数并不是系统调用，则系统调用号的值为-1，后面只有堆栈指针和指令计数器的值。

    - 如果进程没有阻塞，则这个文件只有一个“running”的字符串。

- **wchan**：显示当进程sleep时，kernel当前运行的函数。

    - ```shell
        [zh@zh-inspironn4050 1]$ cat wchan 
        0
        ```

- **status**：包含进程的状态信息。其很多内容与`/proc/[pid]/stat`和`/proc/[pid]/statm`相同，但是却是以一种更清晰地方式展现出来。

    - ```shell
        [zh@zh-inspironn4050 1]$ cat status
        Name:	systemd
        Umask:	0000
        State:	S (sleeping)
        Tgid:	1
        Ngid:	0
        Pid:	1
        PPid:	0
        TracerPid:	0
        Uid:	0	0	0	0
        Gid:	0	0	0	0
        FDSize:	256
        Groups:	 
        NStgid:	1
        NSpid:	1
        NSpgid:	1
        NSsid:	1
        VmPeak:	  239412 kB
        VmSize:	  174780 kB
        VmLck:	       0 kB
        VmPin:	       0 kB
        VmHWM:	   11684 kB
        VmRSS:	    8872 kB
        RssAnon:	    1960 kB
        RssFile:	    6912 kB
        RssShmem:	       0 kB
        VmData:	   25512 kB
        VmStk:	    1036 kB
        VmExe:	     940 kB
        VmLib:	    8492 kB
        VmPTE:	      96 kB
        VmSwap:	    1168 kB
        HugetlbPages:	       0 kB
        CoreDumping:	0
        THP_enabled:	1
        Threads:	1
        SigQ:	0/23352
        SigPnd:	0000000000000000
        ShdPnd:	0000000000000000
        SigBlk:	7be3c0fe28014a03
        SigIgn:	0000000000001000
        SigCgt:	00000001800004ec
        CapInh:	0000000000000000
        CapPrm:	0000003fffffffff
        CapEff:	0000003fffffffff
        CapBnd:	0000003fffffffff
        CapAmb:	0000000000000000
        NoNewPrivs:	0
        Seccomp:	0
        Speculation_Store_Bypass:	thread vulnerable
        Cpus_allowed:	f
        Cpus_allowed_list:	0-3
        Mems_allowed:	00000001
        Mems_allowed_list:	0
        voluntary_ctxt_switches:	2586
        nonvoluntary_ctxt_switches:	665
        ```

- auxv：包含传递给进程的ELF解释器信息，格式是每一项都是一个unsigned long长度的ID加上一个unsigned long长度的值。最后一项以连续的两个0x00开头。

    - ```shell
        [zh@zh-inspironn4050 1]$ sudo hexdump -x auxv
        0000000    0021    0000    0000    0000    6000    86be    7ffd    0000
        0000010    0010    0000    0000    0000    fbff    b7eb    0000    0000
        0000020    0006    0000    0000    0000    1000    0000    0000    0000
        0000030    0011    0000    0000    0000    0064    0000    0000    0000
        0000040    0003    0000    0000    0000    b040    a1d4    55d3    0000
        0000050    0004    0000    0000    0000    0038    0000    0000    0000
        0000060    0005    0000    0000    0000    000b    0000    0000    0000
        0000070    0007    0000    0000    0000    6000    f691    7f55    0000
        0000080    0008    0000    0000    0000    0000    0000    0000    0000
        0000090    0009    0000    0000    0000    f3b0    a1d7    55d3    0000
        00000a0    000b    0000    0000    0000    0000    0000    0000    0000
        00000b0    000c    0000    0000    0000    0000    0000    0000    0000
        00000c0    000d    0000    0000    0000    0000    0000    0000    0000
        00000d0    000e    0000    0000    0000    0000    0000    0000    0000
        00000e0    0017    0000    0000    0000    0000    0000    0000    0000
        00000f0    0019    0000    0000    0000    6d79    86b1    7ffd    0000
        0000100    001a    0000    0000    0000    0000    0000    0000    0000
        0000110    001f    0000    0000    0000    7fed    86b1    7ffd    0000
        0000120    000f    0000    0000    0000    6d89    86b1    7ffd    0000
        0000130    0000    0000    0000    0000    0000    0000    0000    0000
        0000140
        ```

## 1.3 C/C++程序运行时的内存结构

一个正在运行着的C编译程序占用的内存分为代码区、初始化数据区、未初始化数据区、堆栈区和栈区5个部分。



![可执行文件对应到进程逻辑地址空间（即内存）的划分情况](http://static.oschina.net/uploads/img/201306/25114105_Xc9r.jpg)

图：可执行文件对应到进程逻辑地址空间（即内存）的划分情况。

- 堆栈区(stack)：堆栈是由编译器自动分配释放，存放函数的参数值，局部变量的值等。其操作方式类似于数据结构中的栈。栈的申请是由系统自动分配，如在函数内部申请一个局部变量 int h，同时判别所申请空间是否小于栈的剩余空间，如若小于的话，在堆栈中为其开辟空间，为程序提供内存，否则将报异常提示栈溢出。 
- 堆(heap)：堆一般由程序员分配释放，若程序员不释放，程序结束时可能由OS回收。注意它与数据结构中的堆是两回事，分配方式倒是类似于链表。堆的申请是由程序员自己来操作的，在C中使用malloc函数，而C++中使用new运算符，但是堆的申请过程比较复杂：当系统收到程序的申请时，会遍历记录空闲内存地址的链表，以求寻找第一个空间大于所申请空间的堆结点，然后将该结点从空闲结点链表中删除，并将该结点的空间分配给程序，此处应该注意的是有些情况下，新申请的内存块的首地址记录本次分配的内存块大小，这样在delete尤其是 delete[]时就能正确的释放内存空间。



# 2 内存分配

## 2.1 静态内存和动态内存

- 静态的内存使用的是栈空间内存，不用程序员自己来分配。因为静态变量占用的存储空间对于编译器而言是可预计的，静态内存只需要编程的时候直接声明就可以了。

- 动态内存则需要由程序员根据需要来自己分配并收回，动态内存是因为要执行一些因为外部请求而浮动占用内存的应用，所以动态的内存分配时候会用new关键字或malloc或calloc函数，之所以要程序员自己来分配内存是由于有时候不能确定程序要使用多少内存。

## 2.2 内存分配方式

- 从静态存储区域分配。内存在程序编译的时候就已经分配好，这块内存在程序的整个运行期间都存在。例如全局变量，static变量。

- 在栈上创建。在执行函数时，函数内局部变量的存储单元都可以在栈上创建，函数执行结束时这些存储单元自动被释放。栈内存分配运算内置于处理器的指令集中，效率很高，但是分配的内存容量有限。

- 从堆上分配，亦称动态内存分配。程序在运行的时候用malloc或new申请任意多少的内存，程序员自己负责在何时用free或delete释放内存。动态内存的生存期由程序员决定，使用非常灵活，但如果在堆上分配了空间，就有责任回收它，否则运行的程序会出现内存泄漏，频繁地分配和释放不同大小 的堆空间将会产生堆内碎块。

## 2.3 静态、动态内存分配的区别

- 静态内存分配是在编译时完成的，不占用CPU资源；动态分配内存运行时完成，分配与释放需要占用CPU资源；

- 静态内存分配是在栈上分配的，动态内存是堆上分配的；

- 动态内存分配需要指针或引用数据类型的支持，而静态内存分配不需要；
    - 如``

- 静态内存分配是按计划分配，在编译前确定内存块的大小，动态内存分配运行时按需分配。

- 静态分配内存是把内存的控制权交给了编译器，动态内存把内存的控制权交给了程序员；

- 静态分配内存的运行效率要比动态分配内存的效率要高，因为动态内存分配与释放需要额外的开销；动态内存管理水平严重依赖于程序员的水平，处理不当容易造成内存泄漏。

```c
int a = 0; //全局初始化区
char *p1; //全局未初始化区
int main() {
	int b; //栈
	char s[] = "abc"; //栈
	char *p2; //栈
	char *p3 = "123456"; //123456在常量区，p3在栈上。
	static int c =0;//全局（静态）初始化区
	p1 = new char[10];
	p2 = new char[20]; //分配得来的和字节的区域就在堆区。
	strcpy(p1, "123456"); //123456放在常量区，编译器可能会将它与p3所指向的"123456"优化成一个地方。
}
```

