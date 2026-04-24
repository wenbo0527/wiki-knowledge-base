# Why does C have the best file API?

> 来源: maurycyz.com  
> 发布时间: Sat, 28 Feb 2026 00:00:00 +0000  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<!-- mksite: start of content -->
<p>

Ok, the title is a tongue-in-cheek, but there's very little thought put into files in most languages. 
It always feels a bit out of place... except in C.
In fact, what you get is usually a worse version of C.
</p><p>
In C, files can be accessed in the same way as memory:
</p><p>
<!-- snip -->
</p>
<p>
</p>

<pre>
#include &lt;sys/mman.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdint.h&gt;
#include &lt;fcntl.h&gt;
#include &lt;unistd.h&gt;

void main() {
	// Create/open a file containing 1000 unsigned integers
	// Initialized to all zeros.
	int len = 1000 * sizeof(uint32_t);
	int file = open("numbers.u32", O_RDWR | O_CREAT, 0600);
	ftruncate(file, len);

	// Map it into memory.
	uint32_t* numbers = mmap(NULL, len, 
		PROT_READ | PROT_WRITE, MAP_SHARED,
		file, 0);

	// Do something:
	printf("%d\n", numbers[42]);
	numbers[42] = numbers[42] + 1;

	// Clean up
	munmap(numbers, len);
	close(file);
}
</pre>
<p>
Memory mapping isn't the same as loading a file into memory:
It still works if the file doesn't fit in RAM.
Data is loaded as needed, so it won't take all day to open a terabyte file.
</p><p>
It works with all datatypes and is automatically cached.
This cache is cleared if the system needs memory for something else.
</p><p>
<em>mmap() is actually a OS feature</em>, so many other languages have it.
However, it's almost always limited to byte arrays:
You have to grab a chunk of data, parse, process and finally serialize it before writing back to the disk.
It's nicer then manually calling read() and write(), but not by much.
</p><p>
These languages have all these nice features for manipulating data in memory, but nothing for manipulating data on disk. 
In memory, you get dynamically sized strings and vectors, enumerated types, objects, etc, etc.
On disk, you get... a bunch of bytes. 
</p><p>
Considering that most already support custom allocators and the such, adding a better way to access files seems very doable, but no one's actually done it. 
It's very weird to me that C &mdash;
a language known for being unergonomic &mdash;
actually does this the best. 
</p><p>
C's implementation isn't even very good:
Memory mapping comes some overhead (page faults, TLB flushes) and C does nothing to handle endianness or errors...
but it doesn't take much to beat nothing. 
</p><p>
<em>Sure, you might want to do some parsing and validation</em>, but it shouldn't be required every time data leaves the disk. 
RAM is much smaller then the disk, so it's often impossible to just parse everything into memory.
</p><p>
<!--
Just look at Python's pickle:
it's a completely insecure serialization format.
Loading a file can cause code execution even if you just wanted some numbers...
but still very widely used because it fits the mix-code-and-data model of python.
</p><p>
-->
A lot of files are not untrusted data. 
</p><p>
In the case of binary files, parsing is usually redundant. 
There's no reason code can't directly manipulate the on-disk representation, and for "scratchpad" temporary files, save the data as it exists in RAM.
Sure, you wouldn't want to directly manipulate JSON, but there's no reason to do a bunch of work to save some integers.
</p><p>
<em>File manipulation</em> is similarly neglected. 
The filesystem is the original NoSQL database, but you seldom get more then a wrapper around C's readdir().
</p><p>
This usually results in people running another database, such as SQLite, on top of the filesystem,
but relational databases never quite fit your program. 
</p><p>
... and SQL integrates even worse than files:
On top of having to serialize all your data, you have to write code in a whole separate language just to access it!
</p><p>
Most programmers will use it as a key-value store, and implement their own indexing:
creating a bizarre triple nested database.
<!--
</p><p>
<em>So to answer the title,</em>
I think it's a result of a bad assumption:
That data being read from a file is coming from somewhere else and needs to be parsed...
and that data being written to disk is being sent somewhere and needs to be serialized into a standard format. 
</p><p>
This simply isn't true on memory constrained systems &mdash;
and with 100 GB files &mdash; 
every system is memory constrained.
-->
</p>
<!-- mksite: end of content -->

## 链接

https://maurycyz.com/misc/c_files/

---

*ID: 278c2595d86de850*
*抓取时间: 2026-03-05T10:02:14.134484*
