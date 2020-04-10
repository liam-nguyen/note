---
title: 11 Mass-Storage Structure
toc: false
date: 2017-10-30
---

### 1 Overview of Mass-Storage Structure

The bulk of secondary storage for modern computers is provided by **hard disk drives**(**HDD**) and **nonvolatile memory**(**NVM**) devices.

#### Hard Disk Drives

![hdd_moving-head_disk_mechanis](figures/hdd_moving-head_disk_mechanism.png)

#### Nonvolatile Memory Devices

Most commonly, NVM is composed of a controller and flash NAND die semiconductor chips, which are used to store data.

* more reliable: no moving parts;
* faster: no seek time or rotational latency;
* consume less power

For NVM devices, data cannot be overwritten -- rather, the NAND cells have to be erased first. The erasure, which occurs in a "block" increment that is several pages in size, takes much more time than a read (the fastest operation) or a write ( slower than read, but much faster than erase).

**Drive Writes Per Day**(DWPD, 每日全盘写入次数) measure how much times the drive capacity can be written per day before the drive fails.

Because for NVM, data can't be written before pages are erased, data are commonly written to other free blocks instead of original blocks containing original data. The mechanism decreases the latency of data written. Thus, a NAND block containing valid pages (contains new data) and invalid pages (contains old and deprecated data). 

![a_nand_with_valid_and_invalid_pages](figures/a_nand_with_valid_and_invalid_pages.png)


To track which logical blocks contain valid data, the controller maintains a **flash translation layer**(FTL，闪存转换层)。This table maps which physical pages contain currently valid logical blocks. It also tracks physical block state -- which blocks contain only invalid pages and therefore can be erased.


![](figures/flash_translation_layer.jpg)

If there are no free blocks, **garbage collection** could occur -- good data could be copied to other locations, freeing up blocks that could be erased and could then receive the writes. The NVM devices uses **overprovisioning** to store good data from garbage collection -- set asides a number of pages(frequently 20 percentage of the total).

### 2 HDD Scheduling


### 3 NVM Scheduling

NVM devices do not contain moving disk heads and commonly uses an FCFS policy but modifies it to merge adjacent requests. The observed behavior of NVM devices indicates that the time required to service reads is uniform but that, because of the properties of flash memory, write service time is not uniform. Some SSD schedulers have exploited this property and merge only adjacent write requests, servicing all read request in FCFS order.

One way to improve the lifespan and performance of NVM devices over time is to have the file system inform the device when files are deleted, so that the device can erase those files were stored on (known as **TRIM**).

Assume that all blocks have been written to, but there is free space available. Garbage collection must occur to reclaim space taken by invalid data. That means that a write might cause a read of one or more pages, a write of the good data in those pages to overprovisioning space, an erase of the all-invalid-data block, and the placement of that block into overprovisioning space. In summary, one write request eventually causes a page write, one or more page reads (by garbage collection) and one or more page writes ( of good data from the garbage-collected blocks). The creation of I/O requests not by applications but by the NVM device doing garbage collection and space management is called **write amplification**(写入放大) and can greatly impact the write performance of the device.

### 4 Error Detection and Correction

Memory systems have long detected certain errors by using **parity bits**(奇偶校验位). Each byte in a memory system has a parity bit associated with it that records whether the number of bits in the byte set to 1 is even (parity = 0) or odd (parity = 1).

![](figures/example_of_even_parity.png)

<small> In even parity, the second one fails because one bit was read incorrectly, evaluating to an odd number </small>

An **error-correction code** (ECC, 纠错码) not only detects the problem, but also corrects it. For example, disks drives use per-sector and flash drives per-page ECC.

### 5 Storage Device Management

Before it can use a drive to hold files, Storage devices needs:

1. **Low-level formatting**(低级格式化) or physical formatting(物理格式化): fills the device with a special data structure for each storage location. Storage device must be divided into sectors that the controller can read and write. NVM pages must be initialized and the FTL created.
2. **partition**(分区): the operating system can treat each partition as though it were a separate device. For instance, one partition can hold a file system containing a copy of the operating system's executable code, another the swap space, and another a file system containing the user files.
3. **volume creation and management**(卷): implicit creation with partition
4. **logical formatting**(逻辑格式化)：the operating system stores the initial file-system data structures onto the device.

![low_level_formatting](figures/low_level_formatting.png)



!!! note ""Partition v.s. Volume"
    
    A partition is a collection of (physically) consecutive sectors. A volume is a collection of (logically) addressable sector, typically (though not necessarily) resident on a single partition of a hard disk.
    
    E.g, For RAID 0 (strip), a volume of size 4TB may consists of two partitions(2TB) from two disks.




### 7 Swap-Space Management

Swap space is either 

* simply a large file within the file system
    * storage efficiency 
*  a separate raw partition
    *  optimized for speed

### 8 RAID Structure

A variety of disk-organization techniques, collectively called **redundant arrays of independent disks** (RAIDs，独立硬盘冗余阵列), are commonly used to address the performance and reliability issues.

![](figures/raid_levels.jpg)

* RAID level 0. RAID level 0 refers to drive arrays with striping at the level of blocks but without any redundancy (such as mirroring or parity bits).
* RAID level 1. RAID level 1 refers to drive mirroring.
* RAID level 4. RAID level 4 is also known as memory-style error-correcting code (ECC) organization. ECC is also used in RAID 5 and 6.