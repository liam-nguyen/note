---
title: 3 Hadoop分布式文件系统
toc: false
date: 2017-10-30
---


Filesystems that manage the storage across a network of machines are called ***distributed filesystems***(分布式文件系统) . Hadoop comes with a distributed filesystem called HDFS, which stands for ***Hadoop Distributed Filesystem***(Hadoop 分布式文件系统).


### 1 The Design of HDFS

HDFS is a filesystem designed for storing very large files with streaming data access patterns, running on clusters of commodity hardware.

* Very large files: files that are hundreds of megabytes, gigabytes, or terabytes in size.
* Streaming data access: HDFS is built around the idea that the most efficient data processing pattern is a ***write-once, read-many-times***(一次写入，多次读取) pattern.
* Commodity hardware: It’s designed to run on clusters of commodity hardware.

These are areas where HDFS is not a good fit today:

* Low-latency data access
* Lots of small files
* Multiple writers, arbitrary file modifications


### 2 HDFS Concepts

#### Blocks

A disk has a block size, which is the minimum amount of data that it can read or write. Filesystems for a single disk build on this by dealing with data in blocks, which are an integral multiple of the disk block size.

HDFS, too, has the concept of a ***block***(块), but it is a much larger unit — 128 MB by default (typically a few kilobytes for ordinary file system). Unlike a filesystem for a single disk, ==a file in HDFS that is smaller than a single block does not occupy a full block’s worth of underlying storage==. (For example, a 1 MB file stored with a block size of 128 MB uses 1 MB of disk space, not 128 MB.)

!!! Question "HDFS中的块为什么这么大?"

    为了最小化寻址时间。如果块足够大，从磁盘传输数据的时间会明显大于定位这个块所需要的时间。因而，传输一个由多个块组成的大文件取决于磁盘传输速率。
    
Having a block abstraction for a distributed filesystem brings several benefits.

* A file can be larger than any single disk in the network.
* Making the unit of abstraction a block rather than a file simplifies the storage subsystem.
    * storage management: because blocks are a fixed size, it is easy to calculate how many can be stored on a given disk.
    * metadata concerns: because blocks are just chunks of data to be stored, file metadata such as permissions information does not need to be stored with the blocks.
* Blocks fit well with replication for providing fault tolerance and availability.
    * To insure against corrupted blocks and disk and machine failure, each block is replicated to a small number of physically separate machines (typically three).





#### Namenodes and Datanodes

An HDFS cluster has two types of nodes: a ***namenode*** (the master) and a number of ***datanodes*** (workers). 

* The namenode manages the filesystem namespace. It maintains the filesystem tree and the metadata for all the files and directories in the tree. This information is stored persistently on the local disk in the form of two files: the *namespace image* and the *edit log*. 
* The namenode also knows the datanodes on which all the blocks for a given file are located;
* Datanodes are the workhorses of the filesystem. They store and retrieve blocks when they are told to (by clients or the namenode), and they report back to the namenode periodically with lists of blocks that they are storing.




If the machine running the namenode were obliterated, all the files on the filesystem would be lost since there would be no way of knowing how to reconstruct the files from the blocks on the datanodes. Possible solution:

* to back up the files that make up the persistent state of the filesystem metadata.
* to run a secondary namenode, which keeps a copy of the merged namespace image.





#### Block Caching

For frequently accessed files, the blocks may be *explicitly* cached in the datanode’s memory, in an **off-heap block cache**(堆外块缓存). Users or applications instruct the namenode which files to cache (and for how long) by adding a *cache directive* to a *cache pool*.

#### HDFS Federation

Problem: On very large clusters with many files, memory becomes the limiting factor for scaling, since namenode keeps a reference to every file and block in the filesystem in memory.

For example, a 200-node cluster with 24 TB of disk space per node, a block size of 128 MB, and a replication factor of 3 has room for about 2 million blocks (or more): $200\times 24TB⁄(128MB×3)$, So in this case, setting the namenode memory to 12,000 MB would be a good starting point.

Solution: HDFS federation, allows a cluster to scale by adding namenodes, each of which manages a portion of the filesystem namespace.

#### HDFS High Availability

To remedy a failed namenode, a pair of namenodes in an ***active-standby*** configuration is introduced in Hadoop 2. In the event of the failure of the active namenode, the standby takes over its duties to continue servicing client requests *without* a significant interruption.

### 3 The Command-Line Interface

#### Basic Filesystem Operations

Hadoop’s filesystem shell command is `fs`, which supports a number of subcommands (type `hadoop fs -help` to get detailed help).

Copying a file from the local filesystem to HDFS:

```bash
#The local file is copied tothe HDFS instance running on localhost.
$ hadoop fs -copyFromLocal test.copy /test.copy
# works as the same
$ hadoop fs -copyFromLocal test.copy hdfs://localhost:9000/test2.copy
```

Copying the file from the HDFS to the local filesystem:

```bash
$ hadoop fs -copyToLocal /test.copy test.copy.txt
```

### 4 Hadoop Filesystems

Hadoop has an abstract notion of filesystems, of which HDFS is just one implementation. The Java abstract class `org.apache.hadoop.fs.FileSystem` represents the client interface to a filesystem in Hadoop, and there are several concrete implementations.



| Filesystem | URI scheme | Java implementation | Description |
| --- | --- | --- | --- |
| Local | file | fs.LocalFileSystem | A filesystem for a locally connected disk with client-side checksums |
| HDFS | hfs | hdfs.DistributedFileSystem | Hadoop’s distributed filesystem |
| WebHDFS | webhdfs | hdfs.web.WebHdfsFileSystem | Providing authenticated read/write access to HDFS over HTTP. |
| Secure WebHDFS | swebhdfs | hdfs.web.SWebHdfsFileSystem | The HTTPS version of WebHDFS. |

When you are processing large volumes of data you should choose a distributed filesystem that has the data locality optimization, notably HDFS.

#### HTTP

The HTTP REST API exposed by the WebHDFS protocol makes it easier for other languages to interact with HDFS. Note that the HTTP interface is slower than the native Java client, so should be avoided for very large data transfers if possible.

There are two ways of accessing HDFS over HTTP:

* Directly, where the HDFS daemons serve HTTP requests to clients;
* Via a proxy (or proxies), which accesses HDFS on the client’s behalf using the usual DistributedFileSystem API.

![](figures/AccessingHdfsOverHttpOrHdfsProxies.jpg)

HDFS proxy allows for stricter firewall and bandwidth-limiting policies to be put in place. It’s common to use a proxy for transfers between Hadoop clusters located in different data centers, or when accessing a Hadoop cluster running in the cloud from an external network.

### 5 The Java Interface

Hadoop `FileSystem` class is the API for interacting with one of Hadoop’s filesystems. In general you should strive to ***write your code against the `FileSystem` abstract class*** , to retain portability across filesystems. This is very useful when testing your program, for example, because you can rapidly run tests using data stored on the local filesystem.

#### Reading Data from a Hadoop URL

NOT recommended, because `setURLStreamHandlerFactory()` method can be called only once per JVM, which means that if some other part of your program sets it, you won't be able to use.

#### Reading Data Using the FileSystem API

A file in a Hadoop filesystem is represented by a Hadoop `Path` object(`org.apache.hadoop.fs.Path`, not `java.io.File`). You can think of a `Path`  as a Hadoop filesystem URI, such as `hdfs://localhost/user/tom/test.copy`


Since `FileSystem` is a general filesystem API, so the first step is to retrieve an instance for the filesystem we want. There are several static factory methods for getting a `FileSystem` instance:

```Java
// Returns the default filesystem
public static FileSystem get(Configuration conf) throws IOException 
// Uses the given URI’s scheme and authority to determine the filesystem to use
public static FileSystem get(URI uri, Configuration conf) throws IOException 
// Retrieves the filesystem as the given user
public static FileSystem get(URI uri, Configuration conf, String user) throws IOException
// Retrieves a local filesystem instance
public static LocalFileSystem getLocal(Configuration conf) throws IOException
```

A `Configuration` object encapsulates a client or server's configuration, which is set using configuration files read from the classpath, such as `etc/hadoop/core-site.xml`.


With a `FileSystem` instance in hand, we invoke an `open()` method to get the input stream for a file:

```Java
// Uses a default buffer size of 4 KB
public FSDataInputStream open(Path f) throws IOException
// Uses a buffer size of bufferSize
public abstract FSDataInputStream open(Path f, int bufferSize) throws IOException
```

Displaying files from a Hadoop filesystem on standard output by using the FileSystem directly:

```Java
// $ hdfs://localhost:9000/test2.copy
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;

import java.io.InputStream;
import java.net.URI;

public class FileSystemCat {
    public static void main(String[] args) throws Exception {
        String uri = args[0];
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(URI.create(uri), conf);
        InputStream in = null;
        try {
            in = fs.open(new Path(uri));
            IOUtils.copyBytes(in, System.out, 4096, false);
        } finally {
            IOUtils.closeStream(in);
        }
    }
}
```

#### FSDataInputStream

The `open()` method on `FileSystem` actually returns an `FSDataInputStream` rather than a standard java.io class. This class is a specialization of `java.io.DataInputStream` with support for random access, so you can read from any part of the stream:

![FSDataInputStrea](figures/FSDataInputStream.png)


The `Seekable` interface permits seeking to a position in the file and provides a query method for the *current* offset from the start of the file (`getPos()`):

```Java
public interface Seekable { 
    void seek(long pos) throws IOException; 
    long getPos() throws IOException; }
```

Displaying files from a Hadoop filesystem on standard output twice, by using `seek()`:

```Java
// hdfs://localhost:9000/test2.copy

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;
import java.net.URI;

public class FileSystemDoubleCat {
    public static void main(String[] args) throws Exception {
        String uri = args[0];
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(URI.create(uri), conf);
        FSDataInputStream in = null;
        try {
            in = fs.open(new Path(uri));
            IOUtils.copyBytes(in, System.out, 4096, false);
            in.seek(0); // go back to the start of the file
            IOUtils.copyBytes(in, System.out, 4096, false);
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            IOUtils.closeStream(in);
        }
    }
}
```
#### Writing Data

The `FileSystem` class has a number of methods for creating a file. 

```Java
// takes a Path object for the file to be created 
// and returns an output stream to write to
public FSDataOutputStream create(Path f) throws IOException
// appends to an existing file
public FSDataOutputStream append(Path f) throws IOException
```

!!! Warning

    The `create()` methods create any parent directories of the file to be written that don’t already exist.
    
    
There’s an overloaded method of `create()` for passing a callback interface, `Progressable`, so your application can be notified of the progress of the data being written to the datanodes:

```
public interface Progressable { 
    public void progress(); 
}
```

!!! example 

    下面例子中将本地文件复制到Hadoop文件系统。每次将64KB数据包写入datanode pipeline之后， Hadoop调用`progress()`方法，打印一个句号。

    ```Java
    // args: /Users/larry/test.copy hdfs://localhost:9000/test4.copy
    // Copying a local file to a Hadoop filesystem
    public class FileCopyWithProgress {
    
        public static void main(String[] args) throws Exception {
            String localsrc = args[0];
            String dstsrc = args[1];
            BufferedInputStream in = new BufferedInputStream(new FileInputStream(localsrc));
    
            Configuration conf = new Configuration();
            FileSystem fs = FileSystem.get(URI.create(dstsrc), conf);
            try {
                OutputStream out = fs.create(new Path(dstsrc), new Progressable() {
                    @Override
                    public void progress() {
                        System.out.println(".");
                    }
                });
                IOUtils.copyBytes(in, out, 4096, true);
    
            } finally {
                IOUtils.closeStream(in);
            } //end try
        }// end main
    }
    ```


#### FSDataOutputStream

The `create()` method on `FileSystem` returns an `FSDataOutputStream`, which, like `FSDataInputStream`, has a method for querying the current position in the file:

```Java
public class FSDataOutputStream extends DataOutputStream implements Syncable {
    public long getPos() throws IOException { 
        // implementation elided 
    }// implementation elided
}
```

However, because HDFS allows only sequential writes to an open file or appends to an already written file, `FSDataOutputStream` does not permit seeking.

#### Directories

`FileSystem` provides a method to create a directory:

```Java
public boolean mkdirs(Path f) throws IOException
```

This method creates all of the necessary parent directories if they don’t already exist.

#### Querying the Filesystem

<hh>File metadata: FileStatus</hh>
<hh>Listing files</hh>
<hh>File patterns</hh>


#### Deleting Data

Use the `delete()` method on `FileSystem` to permanently remove files or directories:

```Java
public boolean delete(Path f, boolean recursive) throws IOException
```

If `f` is a file or an empty directory, the value of `recursive` is ignored.


### 6 Data Flow

#### 剖析文件读取

The figure below shows the main sequence of events when reading a file.

![](figures/AClientReadingDataFromHDFS.jpg)


* step 1: The client opens the file it wishes to read by calling `open()` on the `FileSystem` object, which for HDFS is an instance of `DistributedFileSystem`. 
* step 2: `DistributedFileSystem` calls the namenode, using remote procedure calls (RPCs), to determine the locations of the first few blocks in the file. 
* step 3: For each block, the namenode returns the addresses of the datanodes that have a copy of that block. Furthermore, the datanodes are sorted according to their proximity to the client. 
    * If the client is itself a datanode, the client will read from the local datanode if that datanode hosts a copy of the block.
    * The `DistributedFileSystem` returns an `FSDataInputStream` to the client for it to read data from. `FSDataInputStream` in turn wraps a `DFSInputStream`, which manages the datanode and namenode I/O.
    * The client then calls `read()` on the stream. 
* step 4: `DFSInputStream`, which has stored the datanode addresses for the first few blocks in the file, then connects to the first (closest) datanode for the first block in the file. Data is streamed from the datanode back to the client, which calls `read()` repeatedly on the stream. 
* step 5: When the end of the block is reached, `DFSInputStream` will close the connection to the datanode, then find the best datanode for the next block. 
* step 6: This happens transparently to the client, which from its point of view is just reading a continuous stream.
    * Blocks are read in order, with the `DFSInputStream` opening new connections to datanodes as the client reads through the stream. 
    * It will also call the namenode to retrieve the datanode locations for the next batch of blocks as needed. When the client has finished reading, it calls `close()` on the `FSDataInputStream`.

#### 剖析文件写入

The figure below illustrates the case of creating a new file, writing data to it, then closing the file.

![](figures/AClientWritingDataToHDFS.jpg)


* step 1: The client creates the file by calling `create()` on `DistributedFileSystem`. 
* step 2: `DistributedFileSystem` makes an RPC call to the namenode to create a new file in the filesystem’s namespace, with no blocks associated with it. 
    * The namenode performs various checks to make sure the file doesn’t already exist and that the client has the right permissions to create the file. 
    * If these checks pass, the namenode makes a record of the new file; otherwise, file creation fails and the client is thrown an `IOException`. 
    * The `DistributedFileSystem` returns an `FSDataOutputStream` for the client to start writing data to. Just as in the read case, `FSDataOutputStream` wraps a `DFSOutputStream`, which handles communication with the datanodes and namenode.
* step 3: As the client writes data, the `DFSOutputStream` splits it into packets, which it writes to an internal queue called the ***data queue***(数据队列) . The data queue is consumed by the `DataStreamer`, which is responsible for asking the namenode to allocate new blocks by picking a list of suitable datanodes to store the replicas. 
* step 4: The list of datanodes forms a pipeline, and here we’ll assume the replication level is three, so there are three nodes in the pipeline. The `DataStreamer` streams the packets to the first datanode in the pipeline, which stores each packet and forwards it to the second datanode in the pipeline. Similarly, the second datanode stores the packet and forwards it to the third (and last) datanode in the pipeline .
* step 5: The `DFSOutputStream` also maintains an internal queue of packets that are waiting to be acknowledged by datanodes, called the ***ack queue***(确认队列). A packet is removed from the ack queue only when it has been acknowledged by all the datanodes in the pipeline.
* step 6: When the client has finished writing data, it calls `close()` on the stream. This action flushes all the remaining packets to the datanode pipeline.
* step 7:  It waits for acknowledgments before contacting the namenode to signal that the file is complete. 

!!! note "怎么放副本"
    
    Hadoop的默认布局策略是
    
    * 在运行客户端的节点上放置第一个副本。如果客户端运行在集群之外，则随机挑选一个节点
    * 随机选择另一个机架上的节点，放置第二个副本
    * 随机选择与副本2同一个机架上的另一个节点，放置第三个副本

    一旦选定副本的放置位置，就根据网络拓扑创建一个管线，例如：
    
    
    ![](figures/a_typical_replica_pipeline.jpg)



#### 一致性模型

A coherency model for a filesystem describes the data visibility of reads and writes for a file.

* After creating a file, it is visible in the filesystem namespace.
* Any content written to the file is NOT guaranteed to be visible, even if the stream is flushed.
* Once more than a block’s worth of data has been written, the first block will be visible to new readers.
* The `FSDataOutputStream.hflush()` method force all buffers to be flushed to the datanodes.
    * The `hflush()` guarantees that the data written up to that point in the file has reached all the datanodes in the write pipeline and is visible to all new readers.
    * But it does NOT guarantee that the datanodes have written the data to *disk*, only that it’s in the datanodes’ *memory*.
    * Closing a file in HDFS performs an implicit `hflush()`.
* The `hsync()` method syncs to *disk* for a file descriptor.

```Java
FileOutputStream out = new FileOutputStream(localFile); 
out.write("content".getBytes("UTF-8")); 
out.flush(); // flush to operating system 
out.getFD().sync(); // sync to disk 
assertThat(localFile.length(), is(((long) "content".length())));
```

<hh>Consequences for application design</hh>

You should call `hflush()` at suitable points, such as after writing a certain number of records or number of bytes.


### 7 通过distcp并行复制

`distcp` 并行地把数据拷入/拷出Hdoop文件系统：

```bash
$ hadoop distcp file1 file2
```

`distcp`是作为一个MapReduce作业来实现的，该复制作业是通过集群中并行运行的map来完成的，没有reducer。