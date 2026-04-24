# A Go question: how do you test <code>select</code> based code?

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-02T03:24:17Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>A while back I wrote an entry about <a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GoReadAllFromChannelWithTimeout">understanding reading all
available things from a Go channel (with a timeout)</a>, where the code used two <code>select</code>s
to, well, let me quote myself:</p>

<blockquote><p>The goal of waitReadAll() is to either receive (read) all currently
available items from a channel (possibly a buffered one) or to time
out if nothing shows up in time. This requires two nested selects,
with the inner one in a for loop.</p>
</blockquote>

<p>In a recent comment on that entry, <a href="http://plasmasturm.org/">Aristotle Pagaltzis</a> proposed a code variation that only used
a single <code>select</code>:</p>

<blockquote><pre style="white-space: pre-wrap;">
func waitReadAll[T any](c chan T, d time.Duration) ([]T, bool) {
    var out []T
    for {
        select {
        case v, ok := &lt;-c:
            if !ok {
               return out, false
    	       }
            out = append(out, v)

        case &lt;-time.After(d):
            if len(out) == 0 {
               return out, true
            }

        default:
            return out, true
        }
    }
}
</pre>
</blockquote>

<p><a href="http://plasmasturm.org/">Aristotle Pagaltzis</a> wrote tests for this code <a href="https://go.dev/play/p/mtfcd011cTx">in the Go
playground</a>, but despite passing
those tests, this code has an intrinsic bug that means it can't work
as designed. The bug is that if this code is entered with nothing in
the channel, the <code>default</code> case is immediately triggered rather than
it waiting for the length of the timeout.
When I saw this code, I was convinced it had the bug and so I tried
to modify <a href="https://go.dev/play/p/mtfcd011cTx">the Go playground code</a>
to have a test that would expose the bug. However, I couldn't find
an easy way to do so at the time, and even now my attempts have
been somewhat awkward, so at the least I think it's not obvious how
to do this.</p>

<p>In Go 1.25 (and later), the primary tool for testing synchronization
and concurrency is the <a href="https://pkg.go.dev/testing/synctest">testing/synctest</a> package (<a href="https://go.dev/blog/synctest">also</a>). Running our hypothetical test with
<a href="https://pkg.go.dev/testing/synctest#Test">synctest.Test()</a> do it
in an environment where time won't advance arbitrarily on us,
insuring that the timeout in <code>waitReadAll()</code> won't trigger before
we can do other things, like send to the channel. To create ordering
in our case, I believe we can use <a href="https://pkg.go.dev/testing/synctest#Wait">synctest.Wait()</a>.  Consider this sketched
code inside a synctest.Test():</p>

<blockquote><pre style="white-space: pre-wrap;">
c := make(chan int)
// sending goroutine:
go func() {
    // Point 1
    synctest.Wait()
    // Point 2
    time.Sleep(1*time.Second)
    c &lt;- 1
}

// Point 3 (receiving goroutine)
out, ok = waitReadAll(c, 2*time.Second)
// assert ok and len(out) == 1
</pre>
</blockquote>

<p>The synctest.Wait() in the sending goroutine at point 1 will wait
until everything is 'durably blocked'; the first durable block point
is in theory a working <code>select</code> inside <code>waitReadAll()</code>, called at
point 3 in a different goroutine. Then in our sending goroutine at
point 2 we use <code>time.Sleep()</code> to wait less than the timeout, forcing
ordering, and finally we send to the channel, which <code>waitReadAll()</code>
should pick up before it times out. This (and a related test for a
timeout) works properly with a working <code>waitReadAll()</code>, but it took
a bunch of contortions to avoid having it panic in various ways
with the buggy version of waitReadAll(). I'm also not convinced my
testing code is completely correct.</p>

<p>(Some of the initial panics came from me learning that you often
want to avoid using t.Fatal() inside a synctest bubble; instead you
want to call t.Error() and arrange to have the rest of your code
still work right.)</p>

<p>Effectively I'm using synctest to try to create an ordering of
events between two goroutines without modifying any code to have
explicit locking or synchronization. Synctest doesn't completely
serialize execution but it does create predictable 'durable blocking'
points where I know where everything is if things are working
correctly. But it's awkward, and I can't directly wait and check
for a blocked <code>select</code> at point 1.</p>

<p>Synctest also makes certain things that normally would be races
into safer, probably race-free operations. Consider a version of
this test with a bit more checking:</p>

<blockquote><pre style="white-space: pre-wrap;">
c := make(chan int)
readall := false
go func() {
    // Point 1
    synctest.Wait()
    // Point 2
    time.Sleep(1*time.Second)
    if readall {
       // failure!
    }
    c &lt;- 1
}

// Point 3
out, ok = waitReadAll(c, 2*time.Second)
readall = true
// assert ok and len(out) == 1
</pre>
</blockquote>

<p>Because of how synctest.Wait() and time work within synctest bubbles,
I believe in theory the only way that the two goroutines can access
<code>readall</code> at the same time is if waitReadAll() is delaying for the
same amount of time as our sending goroutine (instead of the amount
of time we told it to). But the whole area is alarmingly subtle and
I'm not sure I'm right.</p>

<p>(<a href="https://pkg.go.dev/testing/synctest#hdr-Example__Context_AfterFunc">One of the synctest examples</a>
uses an unguarded variable in broadly this way.)</p>

<p>It's entirely possible that there's an easier way to do this sort
of testing of <code>select</code> expressions, and I'd certainly hope so.
However, <a href="https://pkg.go.dev/testing/synctest">synctest</a> itself
is quite new, so perhaps there's no better way right now. Also,
possibly this sort of low level testing isn't necessary very often
in practice. Both <a href="http://plasmasturm.org/">Aristotle Pagaltzis</a> and I are in a sort of
artificial situation where we're narrowly focused on a single
peculiar function.</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/programming/GoTestingSelectQuestion?showcomments#comments">5 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/GoTestingSelectQuestion

---

*ID: 2b76aa967104959b*
*抓取时间: 2026-03-12T13:49:26.048796*
