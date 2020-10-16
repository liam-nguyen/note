---
title: Java record
toc: true
date: 2018-07-12
tags: [Java]
---


记录在开发过程中遇到的java常见小问题、细节问题。

#### 获得二维数组长度

```Java
char[][] board
int n = board.length;
int m = n > 0 ? board[0].length : 0;
```


#### 初始化二维数组

https://stackoverflow.com/questions/13832880/initialize-2d-array


```Java
private char[][] table = {{'1', '2', '3'}, {'4', '5', '6'}, {'7', '8', '9'}};
```

#### 排序二维数组

按照第1个元素排序：

```Java
Arrays.sort(myArr, (a, b) -> Double.compare(a[0], b[0]));
Arrays.sort(queries, Comparator.comparing(a -> a[0]));
Arrays.sort(queries, (a, b) -> a[0] - b[0]);
```

#### 打印数组

https://stackoverflow.com/questions/409784/whats-the-simplest-way-to-print-a-java-array

```Java
System.out.println(Arrays.toString(array));
Nested Array:
System.out.println(Arrays.deepToString(deepArray));
```

#### java中int转成String位数不足前面补零

```Java
String.format("%06",12);//其中0表示补零而不是补空格，6表示至少6位  
```

#### Java最小值和最大值

`Integer.MIN_VALUE`和`Integer.MAX_VALUE`

#### 将List转化为数组

使用

```Java
List<String> list = new ArrayList<String>();
String[] a = list.toArray(new String[0]);
```

而不是

```Java
List<String> list = new ArrayList<String>();
...
String[] a = (String[]) list.toArray(list);
```

但是一下做法是错误的

```Java
List<Integer> list = new ArrayList<Integer>();
...
int[] a = list.toArray(new int[0]);
```
原因就在与`int`不能作为范型类型参数(use int as a type argument for generics)。所以只能利用Java8的新特性了：

```Java
int[] array = list.stream().mapToInt(i->i).toArray();
```


#### 将数组转化为List
https://stackoverflow.com/questions/1073919/how-to-convert-int-into-listinteger-in-java


There is no shortcut for converting from `int[]` to `List<Integer>` as `Arrays.asList` does not deal with boxing and will just create a `List<int[]>` which is not what you want. 

```java
int[] ints = {1, 2, 3};
List<Integer> intList = new ArrayList<Integer>();
for (int i : ints) intList.add(i);
```


```Java
List<Integer> list = Arrays.stream(ints).boxed().collect(Collectors.toList());
```


#### Java数组拷贝

##### clone

clone方法是从Object类继承过来的，基本数据类型（String ，boolean，char，byte，short，float ，double，long）都可以直接使用clone方法进行克隆，注意String类型是因为其值不可变所以才可以使用。

```Java
int[] a1 = {1, 3};
int[] a2 = a1.clone();
```


##### System.arraycopy

```Java
public static native void arraycopy(Object src, int srcPos, 
        Object dest, int desPos, int length)
```

由于是native方法，所以效率非常高，在频繁拷贝数组的时候，建议使用。

##### 反射

https://stackoverflow.com/questions/1196192/how-to-read-the-value-of-a-private-field-from-a-different-class-in-java

```java
Field f = obj.getClass().getDeclaredField("stuffIWant"); //NoSuchFieldException
f.setAccessible(true);
Hashtable iWantThis = (Hashtable) f.get(obj); //IllegalAccessException
```

https://stackoverflow.com/questions/34571/how-do-i-test-a-private-function-or-a-class-that-has-private-methods-fields-or

```java
Field field = TargetClass.getDeclaredField(fieldName);
field.setAccessible(true);
field.set(object, value);
```


##### native

在`Class Object`中一个`wait()`方法定义为：

```Java
public final native void wait(long timeout) throws InterruptedException;
```

这里的native修饰词说明其修饰的方法的实现，是用其他语言(C/C++)实现的，该方法通过JNI调用本地代码。


**JNI**(Java Native Interface, Java本地接口)使Java虚拟机中的Java程序可以调用本地代码。

![JNI](figures/JNI.png)
