---
title: 8 DeadLocks
toc: false
date: 2017-10-30
---

### 1 Introduction


**Deadlock**(死锁) is a situation in which every process in a set of processes is waiting for an event that can be caused only by another process in the set.

![](figures/deadlock_demo.png)


#### Examples


!!! example "Bridge Crossing" 
    
    Each segment of road can be viewed as a resource: A Car must own the segment under it and must acquire the segment that they are moving to. For bridge, traffic only in one direction at a time. Problem occurs when two cars in opposite directions on the bridge: each acquires one segment and needs next.
    
    ![bridge_crosssing](figures/bridge_crosssing.png)

    If a deadlock occurs, it can be resolved if one car backs up (preempt resources and rollback)
    
!!! example "Dining-Philosophers"
    
    See [7 Synchronization Examples](7 Synchronization Examples.md) 
    
    
#### Comparsion
    
##### Starvation
    
**Starvation**(饥饿) describes a situation where a thread is ==unable to gain regular access to shared resources== and is ==unable to make progress==. This happens when shared resources are made unavailable for long periods by "greedy" threads.

Deadlock vs. Starvation
    
| Starvation | Deadlock | 
| --- | --- |
| thread waits indefinitely | circular waiting for resources |
| can end (but don't have to) | can't end without external intervention |
| e.g. low-priority thread waiting for resources constantly in use by high- priority threads | e.g. thread A owns Res 1 and waiting for Res 2, Thread B owns Res 2 and is waiting for Res 2 | 
    
##### Livelock

Threads in deadlock will block indefinitely because each is waiting on the other, while threads in **livelock**(活锁) can ==continue execution but make no meaningful progress==.
    

A real-world example of livelock occurs when two people meet in a narrow corridor, and each tries to be polite by moving aside to let the other pass, but they end up swaying from side to side without making any progress because they both repeatedly move the same way at the same time.
    
Consider a situation where two threads want to access a shared common resource via a `Worker` object but when they see that other `Worker` (invoked on another thread) is also 'active', they attempt to hand over the resource to other worker and wait for it to finish. If initially we make both workers active they will suffer from livelock.
    
![](figures/thread_livelock.png)

Livelock typically occurs when threads retry failing operations at the same time. It thus can generally be avoided by having each thread retry the failing operation at random times. This is precisely the approach taken by Ethernet networks when a network collision occurs. Rather than trying to retransmit a packet immediately after a collision occurs, a host involved in a collision will backoff a random period of time before attempting to transmit again.
    


#### Four requirements for Deadlock

A deadlock situation can arise if the following four conditions hold simultaneously in a system:

* 互斥(**Mutual exclusion**)：资源不能被共享，只能由一个进程使用。
* 请求与保持**(Hold and wait**)：进程已获得了一些资源，但因请求其它资源被阻塞时，对已获得的资源保持不放。
* 非抢占式(**No pre-emption**)：有些系统资源是不可抢占的，当某个进程已获得这种资源后，系统不能强行收回，只能由进程使用完时自己释放。
* 循环等待(**Circular wait**)：若干个进程形成环形链，每个都占用对方申请的下一个资源。

### 2 Handling Deadlocks

Generally speaking, we can deal with the deadlock problem in one of three ways:

* ignore the problem altogether and pretend that deadlocks never occur in the system.
    * used by most operating systems, including Linux and Windows. It is then up to kernel and application developers to write programs that handle deadlocks
* use a protocol to prevent or avoid deadlocks, ensuring that the system will never enter a deadlocked state.
    * **Deadlock prevention**(死锁预防) provides a set of methods to ensure that at least one of the necessary conditions  cannot hold. 
    * **Deadlock avoidance**(死锁避免) requires that the operating system be given additional information in advance concerning which resources a thread will request and use during its lifetime. With this additional knowledge, the operating system can decide for each request whether or not the thread should wait.
* allow the system to enter a deadlocked state, detect it, and recover.
    * used by some database systems 


#### Deadlock Prevention
1. Mutual Exclusion
The mutual-exclusion condition must hold.

2. Hold and Wait

SOLUTION: Allows a thread to request resources only when it has none.

e.g [多线程设计模式 - Balking模式](多线程设计模式.md)

3. No Preemption

SOLUTION: If a thread is holding some resources and requests another resource that cannot be immediately allocated to it (that is, the thread must wait), then all resources the thread is currently holding are preempted. 



4. Circular Wait

SOLUTION: impose a total ordering of all resource types and to require that each thread requests resources in an increasing order of enumeration.
    
* Each thread can request resources only in an increasing order of enumeration.
* OR A thread requesting an instance of resource $R_j$ must have released any resources $R_i$ such that $F(R_i) ≥ F(R_j)$.

Java developers have adopted the strategy of using the method `System.identityHashCode(Object)` (which returns the default hash code value of the Object parameter it has been passed) as the function for ordering lock acquisition.





#### Deadlock Avoidance

Banker's Algorithm