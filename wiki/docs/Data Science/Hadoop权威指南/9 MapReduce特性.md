---
title: 9 MapReduce特性
toc: false
date: 2017-10-30
---

### 1 Counters
Counters are a useful channel for gathering statistics about the job: for quality control or for application-level statistics.

### 2 Sorting

#### Partial Sort

In the Default MapReduce Job, MapReduce will sort input records by their keys by default.

!!! note "控制排列顺序"
    
    键的排列顺序是由`RawComparator`控制的，规则如下：
    
    1. 若属性`mapreduce.job.output.key.comparator.class`已经显式设置，或者通过`Job`类的`setSortComparatorClass()`方法进行设置，则使用该类的实例；
    2. 否则，键必须是`WritableComparable`的子类，并使用针对该键类的已登记的comparator；
    3. 如果还没有已登记的comparator，则使用`RawComparator`: 它将字节流反序列化为一个对象，再由`WritableComparable`的`CompareTo()`方法进行操作(参见[Hadoop IO](5 Hadoop IO.md))。


#### Total Sort

The naive answer to produce a globally sorted file using hadoop is to use a single partition. However, it is incredibly inefficient for large files, since one machine needs to process all of the output. The best way is to ==use a partitioner and keep partition sizes fairly even==. A possible way to get a fairly even set of partitions is to sample the key space.

#### Secondary Sort

How to get the effect of sorting by value:

* Make the key a composite of the natural key and the natural value.
* The sort comparator should order by the composite key
* The partitioner and grouping comparator for the composite key should consider only the natural key for partitioning and grouping

!!! example "计算每年的最高气温"

    ```java
    public class MaxTemperatureUsingSecondarySort {
        static class MaxTemperatureMapper extends Mapper<LongWritable, Text, IntPair, NullWritable> {
            private NcdcRecordParser parser = new NcdcRecordParser();
    
            @Override
            protected void map(LongWritable key, Text value, Context context)
                    throws IOException, InterruptedException {
                parser.parse(value);
                if (parser.isValidTemperature())
                    context.write(new IntPair(parser.getYearInt(),
                            parser.getAirTemperature()), NullWritable.get());
            }
        }
    
        static class MaxTemperatureReducer extends Reducer<IntPair, NullWritable, IntPair, NullWritable> {
            @Override
            protected void reduce(IntPair key, Iterable<NullWritable> values, Context context)
                    throws IOException, InterruptedException {
                context.write(key, NullWritable.get());
            }
        }
    
    
        public static class FirstPartitioner extends Partitioner<IntPair, NullWritable> {
            @Override
            public int getPartition(IntPair intPair, NullWritable nullWritable, int numPartitions) {
                return Math.abs(intPair.getYear()*127) % numPartitions;
            }
        }
    
        public static class KeyComparator extends WritableComparator {
            protected KeyComparator() {
                super(IntPair.class, true);
            }
    
            @Override
            public int compare(WritableComparable w1, WritableComparable w2) {
                IntPair ip1 = (IntPair) w1;
                IntPair ip2 = (IntPair) w2;
                if (ip1.getYear() != ip2.getYear())
                    return ip1.getYear() - ip2.getYear();
                return ip2.getTemperature() - ip1.getTemperature();
            }
        }
    
    
        public static class GroupComparator extends WritableComparator {
            protected GroupComparator() {
                super(IntPair.class, true);
            }
    
            @Override
            public int compare(WritableComparable w1, WritableComparable w2) {
                IntPair ip1 = (IntPair) w1;
                IntPair ip2 = (IntPair) w2;
                return ip1.getYear() - ip2.getYear();
            }
        }
    
        public static void main(String[] args) throws Exception {
            Configuration conf = new Configuration();
            Job job = Job.getInstance(conf);
    
            job.setJarByClass(MaxTemperatureUsingSecondarySort.class);
            job.setJar("/Users/larry/Documents/codes/bigdata/bigdata-1.0-SNAPSHOT.jar");
    
    
            job.setMapperClass(MaxTemperatureMapper.class);
            job.setPartitionerClass(FirstPartitioner.class);
            job.setSortComparatorClass(KeyComparator.class);
            job.setGroupingComparatorClass(GroupComparator.class);
            job.setReducerClass(MaxTemperatureReducer.class);
            job.setOutputKeyClass(IntPair.class);
            job.setOutputValueClass(NullWritable.class);
    
    
            FileInputFormat.setInputPaths(job, new Path("hdfs://centos1:9000/ncdc/input/ncdc"));
            Path outputPath = new Path("hdfs://centos1:9000/ncdc/output/");
            FileOutputFormat.setOutputPath(job, outputPath);
            FileSystem fs = FileSystem.get(new URI("hdfs://centos1:9000"), conf, "root");
            if (fs.exists(outputPath)) fs.delete(outputPath, true);
    
            System.exit(job.waitForCompletion(true) ? 0 : 1);
        }
    }
    ```

### 3 Joins

!!! Tip
    
    Writing MapReduce program from scratch to perform joins between large datasets is fairly involved. Using a higher-level framework such as Pig, Hive or Spark is a better choice.


连接操作如果由mapper执行，则称为map端连接(*map-side join*); 如果由reducer执行，则称为reduce端连接(*reduce-side join*)。至于到底采用哪种连接，取决于数据的组织方式。

#### map端连接



#### reduce端连接




### 4 Side Data Distribution

***Side data*** can be defined as extra read-only data needed by a job to process the main dataset. The challenge is to make side data available to all the map or reduce tasks (which are spread across the cluster) in a convenient and efficient fashion.

#### Distributed Cache

Distribute cache mechanism provides a service for copying files and archives to the task nodes in time for the tasks to use them when they run.

When you launch a job, Hadoop copies the files to the HDFS. Then, before a task is run, the node manager copies the files from the HDFS to a local disk -- the cache -- so the task can access the files. MapReduce always create a symbolic link from the task's working directory to every file or archive added to the distributed cache, so you can directly access the localized file by name. 