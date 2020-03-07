---
title: 6 开发MapReduce应用
toc: false
date: 2017-10-30
---

### 1 The Configuration API

Components in Hadoop are configured using Hadoop’s own configuration API. An instance of the `org.apache.hadoop.conf.Configuration` represents a collection of configuration `properties` and their values.

`Configuration`s read their properties from  XML files, which have a simple structure for defining name-value pairs.
    
#### Combining Resources

==When more than one resource is used to define a `Configuration`, properties added later override the earlier definitions==. However, properties that are marked as `final` cannot be overridden in later definitions.

```Java tab="conf"
Configuration conf = new Configuration();
conf.addResource("configuration-1.xml");
conf.addResource("configuration-2.xml");
assertThat(conf.getInt("size", 0), is(12));
assertThat(conf.get("weight"), is("heavy"));
```

```xml tab="configuration-1.xml"
<?xml version="1.0"?> 
<configuration>
    <property> 
        <name>color</name> 
        <value>yellow</value> 
        <description>Color</description> 
    </property>

    <property> 
        <name>size</name> 
        <value>10</value> 
        <description>Size</description> 
    </property>

    <property> 
        <name>weight</name> 
        <value>heavy</value> 
        <final>true</final> 
        <description>Weight</description> 
    </property>

    <property> 
        <name>size-weight</name> 
        <value>${size},${weight}</value> 
        <description>Size and weight</description> 
    </property> 
</configuration>
```

```xml tab="configuration-2.xml"
<?xml version="1.0"?> 
<configuration>
    <property> 
        <name>size</name> 
        <value>12</value> 
    </property>

    <property> 
        <name>weight</name> 
        <value>light</value> 
    </property> 
</configuration>
```

#### Variable Expansion

Configuration properties can be defined in terms of other properties, or system properties. For example, the property `size-weight` in `configuration-1.xml` file is defined as ` ${size}$, ${weight}$`.

### 2 Setting Up the Development Environment

The first step is to create a project so you can build MapReduce programs and run them in local (standalone) mode from the command line or within your IDE. 

Using the Maven POM to manage your project is an easy way to start. Specifically, for building MapReduce jobs, you only need to have the `hadoop-client` dependency, which contains all the Hadoop client-side classes needed to interact with HDFS and MapReduce. For running unit tests, use `junit`, and for writing MapReduce tests, use `mrunit`. The `hadoop-minicluster` library contains the “mini-” clusters that are useful for testing with Hadoop clusters running in a single JVM.

#### Managing Configuration

When developing Hadoop applications, it is common to switch between running the application locally and running it on a cluster.

One way to accommodate these variations is to have different versions of Hadoop configuration files and use them with the `-conf` command-line switch.

For example, the following command shows a directory listing on the HDFS server running in pseudodistributed mode on localhost:

```
$ hadoop fs -conf conf/hadoop-localhost.xml -ls
```


Another way of managing configuration settings is to copy the etc/hadoop directory from your Hadoop installation to another location, place the `*-site.xml` configuration files there (with appropriate settings), and set the `HADOOP_CONF_DIR `environment variable to the alternative location. The main advantage of this approach is that you don’t need to specify `-conf` for every command.

<!--driver-->

### 4 Running Locally on Test Data


#### Running a Job in a Local Job Runner

Using the `Tool` interface, it’s easy to write a driver to run our MapReduce job for finding the maximum temperature by year.

```Java
public class MaxTemperatureDriver extends Configured implements Tool {

  @Override
  public int run(String[] args) throws Exception {
    if (args.length != 2) {
      System.err.printf("Usage: %s [generic options] <input> <output>\n",
          getClass().getSimpleName());
      ToolRunner.printGenericCommandUsage(System.err);
      return -1;
    }
    
    Job job = new Job(getConf(), "Max temperature");
    job.setJarByClass(getClass());

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    
    job.setMapperClass(MaxTemperatureMapper.class);
    job.setCombinerClass(MaxTemperatureReducer.class);
    job.setReducerClass(MaxTemperatureReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    
    return job.waitForCompletion(true) ? 0 : 1;
  }
  
  public static void main(String[] args) throws Exception {
    int exitCode = ToolRunner.run(new MaxTemperatureDriver(), args);
    System.exit(exitCode);
  }
}
```

From the command line, we can run the driver by typing:




#### Testing the Driver
### 5 Running on a Cluster

#### packaging a job

In a distributed setting, a job's classes must be packaged into a *job JAR file* to send to the cluster. Creating a job JAR file is conveniently achieved using build tools, such as Maven.


```xml
<!-- Make this jar executable -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-jar-plugin</artifactId>
    <version>3.0.2</version>
    <configuration>
        <outputDirectory>${basedir}</outputDirectory>
    </configuration>
</plugin>
```

!!! note "在Intellij IDEA中提交Job"
    
    在resource文件夹中放入Hadoop 配置文件/或者将，并且在用`job.setJar()`方法设置Jar即可。



#### Retrieving the Results

The `hadoop fs -getmerge` command gets all the files in the directory specified in the source pattern and merges them into a single file on the local filesystem:

```sh
 hadoop fs -getmerge /flowsum/output localfile
 ```
 
 
#### Hadoop Logs

| Logs | Primary audience | Description |
| --- | --- | --- |
| System daemon logs | Administrators  | Each Hadoop daemon produces a logfile (using log4j) and another file that combines standard out and error. Written in the directory defined by the HADOOP_LOG_DIR environment variable. |
| HDFS audit logs | Administrators | A log of all HDFS requests, turned off by default. Written to the namenode’s log, although this is configurable. |
| MapReduce job history logs | Users | A log of the events (such as task completion) that occur in the course of running a job. Saved centrally in HDFS. |
| MapReduce task logs | Users | Each task child process produces a logfile using log4j (called `syslog`), a file for data sent to standard out (`stdout`), and a file for standard error (`stderr`). Written in the userlogs subdirectory of the directory defined by the YARN_LOG_DIR environment variable. | 
 
 
#### Remote Debugging
 
 
 
### 6 Tuning a Job
### 7 MapReduce Workflows