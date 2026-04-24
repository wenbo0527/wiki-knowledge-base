# In Linux, filesystems can and do have things with inode number zero

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2025-12-05T04:19:15Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>A while back I wrote about <a href="https://utcc.utoronto.ca/~cks/space/blog/unix/POSIXAllowsZeroInode">how in POSIX you could theoretically
use inode (number) zero</a>. Not all
Unixes consider inode zero to be valid; prominently, OpenBSD's
<a href="https://man.openbsd.org/getdents.2">getdents(2)</a> doesn't return
valid entries with an inode number of 0, and by extension, OpenBSD's
filesystems won't have anything that uses inode zero. However, Linux
is a different beast.</p>

<p>Recently, I saw <a href="https://github.com/golang/go/commit/cec4d4303f6475475d1a632cca506e8a82072d25">a Go commit message</a>
with the interesting description of:</p>

<blockquote><p>os: allow direntries to have zero inodes on Linux</p>

<p>Some Linux filesystems have been known to return valid entries with
zero inodes. This new behavior also puts Go in agreement with recent
glibc.</p>
</blockquote>

<p>This fixes <a href="https://github.com/golang/go/issues/76428">issue #76428</a>,
and the issue has a simple reproduction to create something with inode
numbers of zero. According to the bug report:</p>

<blockquote><p>[...] On a Linux system with libfuse 3.17.1 or later, you can do this
easily with GVFS:</p>

<pre>
# Create many dir entries
(cd big &amp;&amp; printf '%04x ' {0..1023} | xargs mkdir -p)
gio mount sftp://localhost/$PWD/big
</pre>
</blockquote>

<p>The resulting filesystem mount is in /run/user/$UID/gvfs (see <a href="https://github.com/golang/go/issues/76428">the
issue</a> for the exact
long path) and can be experimentally verified to have entries with
inode numbers of zero (well, as reported by reading the directory).
On systems using glibc 2.37 and later, you can look at this directory
with 'ls' and see the zero inode numbers.</p>

<p>(Interested parties can try their favorite non-C or non-glibc
bindings to see if those environments correctly handle this case.)</p>

<p>That this requires glibc 2.37 is due to <a href="https://sourceware.org/bugzilla/show_bug.cgi?id=12165">this glibc bug</a>, first
opened in 2010 (but rejected at the time for reasons you can read
in the glibc bug) and then <a href="https://sourceware.org/bugzilla/show_bug.cgi?id=19970">resurfaced in 2016</a> and eventually
fixed in 2022 (and then again in 2024 for the thread safe version
of readdir). <a href="https://sourceware.org/bugzilla/show_bug.cgi?id=19970">The 2016 glibc issue</a> has a bit
of a discussion about the kernel side. As covered in the Go issue,
<a href="https://github.com/libfuse/libfuse/issues/1338">libfuse returning a zero inode number may be a bug itself</a>, but there are
(many) versions of libfuse out in the wild that actually do this
today.</p>

<p>Of course, libfuse (and gvfs) may not be the only Linux filesystems
and filesystem environments that can create this effect. I believe
there are alternate language bindings and APIs for the kernel <a href="https://en.wikipedia.org/wiki/Filesystem_in_Userspace">FUSE</a> (<a href="https://www.kernel.org/doc/html/next/filesystems/fuse/fuse.html">also</a>, <a href="https://wiki.archlinux.org/title/FUSE">also</a>) support, so they might
have the same bug as libfuse does.</p>

<p>(Both Go and Rust have at least one native binding to the kernel
FUSE driver. I haven't looked at either to see what they do about
inode numbers.)</p>

<p>PS: My understanding of the Linux (kernel) situation is that if you
have something inside the kernel that needs an inode number and you
ask the kernel to give you one (through get_next_ino(), an
internal function for this), the kernel will carefully avoid giving
you inode number 0. A lot of things get inode numbers this way, so
this makes life easier for everyone. However, a filesystem can
decide on inode numbers itself, and when it does it can use inode
number 0 (either explicitly or by zeroing out the d_ino field
in the <a href="https://www.man7.org/linux/man-pages/man2/getdents.2.html">getdents(2)</a> dirent
structs that it returns, which I believe is what's happening in the
libfuse situation).</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/linux/LinuxZeroInodesExist

---

*ID: 60d63c95eb58e343*
*抓取时间: 2026-03-12T13:49:26.049087*
