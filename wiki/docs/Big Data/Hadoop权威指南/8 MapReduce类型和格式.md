---
title: 8 MapReduce类型和格式
toc: false
date: 2017-10-30
---

### 1 MapReduce Types

The map and reduce functions in Hadoop MapReduce have the following general form:

    map: (K1, V1) → list(K2, V2) 
    reduce: (K2, list(V2)) → list(K3, V3)

!!! note "why can’t the types be determined from a combination of the mapper and the reducer?"

    The answer has to do with a limitation in Java generics: [type erasure](../../Java/深入理解Java虚拟机/10 早期(编译期)优化.md) means that the type information isn’t always present at runtime, so Hadoop has to be given it explicitly.
    
#### 默认的MapReduce作业

默认的mapper是`Mapper`类，它将输入的键(文件中每行中开始的偏移量，`LongWritable`)和值(文本行, `Text`)原封不动地写入到输出中。

```java
public class Mapper<KEYIN, VALUEIN, KEYOUT, VALUEOUT> {
  protected void map(KEYIN key, VALUEIN value, 
                     Context context) throws IOException, InterruptedException {
    context.write((KEYOUT) key, (VALUEOUT) value);
  }
```


默认的partitioner是`HashPartitioner`，它对每条记录的键进行哈希操作以决定该记录属于哪个分区。每个分区由一个reduce任务处理，所以分区数等于作业的reduce任务个数。

```java
public class HashPartitioner<K2, V2> implements Partitioner<K2, V2> {
  public void configure(JobConf job) {}
  public int getPartition(K2 key, V2 value,
                          int numReduceTasks) {
    return (key.hashCode() & Integer.MAX_VALUE) % numReduceTasks;
    }
}
```

由于默认情况下只有一个reducer，因此也就只有一个分区，在这种情况下，由于所有数据都放入同一个分区，partitioner操作将变得无关紧要了。但是，如果有多个reducer任务，则partitioner非常重要。

默认的reducer是`Reducer`类型，它把所有的输入写入到输出中。默认的输出格式为`TextOutputFormat`，它将键和值转换成字符串并用制表符分隔开，然后一条记录一行地进行输出。

```java
public class Reducer<KEYIN,VALUEIN,KEYOUT,VALUEOUT> {
  protected void reduce(KEYIN key, Iterable<VALUEIN> values, Context context
                        ) throws IOException, InterruptedException {
    for(VALUEIN value: values) {
      context.write((KEYOUT) key, (VALUEOUT) value);
    }
  }
```



### 2 输入格式
#### 输入分片和格式

An **input split**(输入分片) is a chunk of the input that is processed by a single map. Each map processes a single split. Each split is divided into **records**(记录，a key-value pair). Splits and records are ==***logical***==: input files are not physically split into chunks. In a database context, a split might correspond to a range of rows from a table and a record to a row in that range.


Input splits are represented by the Java class `InputSplit`:

```java
public abstract class InputSplit {
    public abstract long getLength() 
            throws IOException, InterruptedException;
    public abstract String[] getLocations() 
            throws IOException, InterruptedException;
}
```

!!! note

      A split doesn't contain the input data; it is just a reference to the data. 
      

An `InputFormat` is responsible for creating the `InputSplit`s and dividing them into records.


```java
public abstract class InputFormat<K, V> {
  // Logically split the set of input files for the job.
  public abstract List<InputSplit> getSplits(JobContext context)
         throws IOException, InterruptedException;
  
  // Create a record reader for a given split. The framework will call
  // RecordReader.initialize(InputSplit, TaskAttemptContext)} before
  // the split is used.
  public abstract RecordReader<K,V> 
        createRecordReader(InputSplit split, TaskAttemptContext context)
            throws IOException, InterruptedException;
}
```

The client running the job calculates the splits for the job by calling `getSplits()`, then sends them to the application master, which uses their storage locations to schedule map tasks that will process them on the cluster. The map task passes the split to the `createRecordReader()` method on `InputFormat` to obtain a `RecordReader` for that split.

A `RecordReader` is little more than an iterator over records, and the map task uses one to generate record key-value pairs, which it passes to the map function.

For the `Mapper`'s `run()` method, after running `setup()`, the `nextKeyValue()` is called repeatedly on the `Context` to populate the key and value objects for the mapper. The key and value are retrieved from the `RecordReader` by way of the `Context` and are passed to the `map()` method for it to do its work.

```java
public void run(Context context) throws IOException, InterruptedException {
    setup(context);
    try {
        while (context.nextKeyValue()) {
            map(context.getCurrentKey(), context.getCurrentValue(), context);
        }
    } finally {
        cleanup(context);
    }
}
```

![](figures/InputFormat_hierarchy.jpg)

##### FileInputFormat

`FileInputFormat` is the base class for all implementations of `InputFormat` that use files as their data source. It provides two things:

* input paths: a collection of paths 
    * set by `addInputPath`, `addInputPaths`, `setInputPaths`
* input splits: splits only large files (larger than split size, normally the size of an HDFS block). 
    * The split size is calculated by `max(minimumSize, min(maximumSize, blockSize)`, where `minimumSize` and `maximumSize` are minimum(usually 1 byte) and maximum (usually, `Long.max.MAX_VALUE`) size in bytes for a file split. 

Hadoop works better with a small number of large files than a large number of small files. One reason for this is that `FileInputFormat` generates splits in such a way that ==each split is all or part of a single file==.

##### CombineFileInputFormat

Using `CombineFileInputFormat` to packs many files into each split so that each mapper has more to process.

<!--or merge small files into larger files by using a sequence file ( keys are filenames and values are file contents).

!!! example "packaging a collection of small files as a single SequenceFile"
    ```java
    public class SmallFilesToSequenceFileConverter extends Configured
        implements Tool {
      
      static class SequenceFileMapper
          extends Mapper<NullWritable, BytesWritable, Text, BytesWritable> {
        
        private Text filenameKey;
        
        @Override
        protected void setup(Context context) throws IOException,
            InterruptedException {
          InputSplit split = context.getInputSplit();
          Path path = ((FileSplit) split).getPath();
          filenameKey = new Text(path.toString());
        }
        
        @Override
        protected void map(NullWritable key, BytesWritable value, Context context)
            throws IOException, InterruptedException {
          context.write(filenameKey, value);
        }
        
      }
    
      @Override
      public int run(String[] args) throws Exception {
        Job job = JobBuilder.parseInputAndOutput(this, getConf(), args);
        if (job == null) {
          return -1;
        }
        
        job.setInputFormatClass(WholeFileInputFormat.class);
        job.setOutputFormatClass(SequenceFileOutputFormat.class);
        
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(BytesWritable.class);
    
        job.setMapperClass(SequenceFileMapper.class);
    
        return job.waitForCompletion(true) ? 0 : 1;
      }
      
      public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new SmallFilesToSequenceFileConverter(), args);
        System.exit(exitCode);
      }
    }
    ```-->

#### Text Input
##### TextInputFormat

`TextInputFormat` is the default `InputFormat`. 

* Each record is a line of input. 
* The key is the ==byte offset== (字节偏移量) within the file. 
* The value is the contents of the line, excluding any line terminators (e.g., newline or carriage return), and is packaged as a `Text` object.

!!! note "THE RELATIONSHIP BETWEEN INPUT SPLITS AND HDFS BLOCKS"
    
    The logical records that `FileInputFormats` define usually do not fit neatly into HDFS blocks. This has no bearing on the functioning of programs. Data-local maps will perform some remote reads.
    
    ![](figures/FileInputFormat_InputSplit_HDFSBlocks.jpg)

##### KeyValueTextInputFormat

Using `KeyValueTextInputFormat`, each line in a file is a key-value pair, separated by a delimiter such as a tab character. The separator can be specified by the `mapreduce.input.keyvaluelinerecordreader.key.value.separator` property.

##### NLineInputFormat

Using `NLineInputFormat`, mappers receive a fixed number of lines of input. Like with `TextInputFormat`, the keys are the byte offsets within the file and the values are the lines themselves.

##### Multiple Inputs

`MultipleInputs` allows to specify which `InputFormat` and `Mapper` to use on a per-path basis. For example, if you had weather data from the UK Met Office that you wanted to combine with the NCDC data for your maximum temperature analysis, you might set up the input as follows:

```java
MultipleInputs.addInputPath(job, ncdcInputPath,
    TextInputFormat.class, MaxTemperatureMapper.class);
MultipleInputs.addInputPath(job, metofficeInputPath,
    TextInputFormat.class, MetOfficeTemperatureMapper.class);
```

#### Binary Input
##### SequenceFileInputFormat

Using `SequenceFileInputFormat`, the keys and values are determined by the [sequence file](5 Hadoop IO.md).

### 3 Output Formats

![](figures/outputformat.jpg)
#### TextOuput

`TextOutputFormat` is the default output format, which writes records as lines of text. Its keys and values may be of any type, since `TextOutputFormat` turns them into strings by calling `toString()` on them. Each key-value pair is separated by a tab character by default.

#### Multiple Outputs

`FileOuputFormat`及其子类产生的文件放在输出目录下。每个reducer一个文件并且文件由分区号命名：*part-r-00000*, *part-r-00001*, 等等。`MultipleOuput`累可以让每个reducer输出多个文件，采用*name-m-nnnnn*形式的文件名用于map输出，*name-r-nnnnn*形式的文件名用户reduce输出，其中*name*是由程序设定的任务名字，*nnnnn*是一个指明块号的整数(从00000开始）。