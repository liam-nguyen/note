---
title: Zero Copy
toc: false
date: 2017-10-30
hidden: true
---



```c
read(file, tmp_buf, len);
write(socket, tmp_buf, len);
```

![](figures/15844914015169.jpg)

* Step one: the read system call causes a context switch from user mode to kernel mode. The first copy is performed by the DMA engine, which reads file contents from the disk and stores them into a kernel address space buffer.

* Step two: data is copied from the kernel buffer into the user buffer, and the read system call returns. The return from the call caused a context switch from kernel back to user mode. Now the data is stored in the user address space buffer, and it can begin its way down again.

* Step three: the write system call causes a context switch from user mode to kernel mode. A third copy is performed to put the data into a kernel address space buffer again. This time, though, the data is put into a different buffer, a buffer that is associated with sockets specifically.

* Step four: the write system call returns, creating our fourth context switch. Independently and asynchronously, a fourth copy happens as the DMA engine passes the data from the kernel buffer to the protocol engine. You are probably asking yourself, “What do you mean independently and asynchronously? Wasn't the data transmitted before the call returned?” Call return, in fact, doesn't guarantee transmission; it doesn't even guarantee the start of the transmission. It simply means the Ethernet driver had free descriptors in its queue and has accepted our data for transmission. There could be numerous packets queued before ours. Unless the driver/hardware implements priority rings or queues, data is transmitted on a first-in-first-out basis. (The forked DMA copy in Figure 1 illustrates the fact that the last copy can be delayed).


#### mmap

One way to eliminate a copy is to skip calling read and instead call mmap. For example:

```c
tmp_buf = mmap(file, len);
write(socket, tmp_buf, len);
```

![](figures/15844916713529.jpg)

* Step one: the `mmap` system call causes the file contents to be copied into a kernel buffer by the DMA engine. The buffer is shared then with the user process, without any copy being performed between the kernel and user memory spaces.

* Step two: the write system call causes the kernel to copy the data from the original kernel buffers into the kernel buffers associated with sockets.

* Step three: the third copy happens as the DMA engine passes the data from the kernel socket buffers to the protocol engine.


#### Sendfile

In kernel version 2.1, the sendfile system call was introduced to simplify the transmission of data over the network and between two local files. Introduction of sendfile not only reduces data copying, it also reduces context switches. Use it like this:

```c
sendfile(socket, file, len);
```

![](figures/15844919851931.jpg)

* Step one: the sendfile system call causes the file contents to be copied into a kernel buffer by the DMA engine. Then the data is copied by the kernel into the kernel buffer associated with sockets.
* Step two: the third copy happens as the DMA engine passes the data from the kernel socket buffers to the protocol engine.

[^1]: https://www.ibm.com/developerworks/cn/java/j-zerocopy/
[^2]: https://www.linuxjournal.com/article/6345