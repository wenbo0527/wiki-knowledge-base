# Forcing a Go generic type to be a pointer type (and some challenges)

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-27T04:48:16Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Recently I saw a Go example that made me scratch my head and decode
what was going on (you can see it <a href="https://go.dev/play/p/DXisBJspguP">here</a>). Here's what I understand about
what's going on. Suppose that you want to create a <a href="https://go.dev/ref/spec#General_interfaces">general interface</a> for a generic type
that requires any concrete implementation to be a pointer type.
We can do this by literally requiring a pointer:</p>

<blockquote><pre style="white-space: pre-wrap;">
type Pointer[P any] interface {
   *P
}
</pre>
</blockquote>

<p>That this is allowed is not entirely obvious from the specification,
but it's not forbidden. We're not allowed to use just '<code>P</code>' or
'<code>~P</code>' in the interface type, because you're not allowed to directly
or indirectly embed yourself as a type parameter, but '<code>*P</code>' isn't
doing that directly; instead, it's forcing a pointer version of
some underlying type. Actually using it is a bit awkward, but I'll
get to that.</p>

<p>We can then require such a generic type to have some methods, for
example:</p>

<blockquote><pre style="white-space: pre-wrap;">
type Index[P any] interface {
   New() *P
   *P
}
</pre>
</blockquote>

<p>This can be implemented by, for example:</p>

<blockquote><pre style="white-space: pre-wrap;">
type base struct {
	i int
}

func (b *base) New() *base {
	return &amp;base{-1}
}
</pre>
</blockquote>

<p>But suppose we want to have a derived generic type, for example a
struct containing an <code>Index</code> field of this Index (generic) type.
We'd like to write this in the straightforward way:</p>

<blockquote><pre style="white-space: pre-wrap;">
type Example[P any] struct {
	Index Index[P]
}
</pre>
</blockquote>

<p>This doesn't work (at least not today); you can't write '<code>Index[P]</code>'
outside of a type constraint. In order to make this work you must
create the type with two related generic type constraints:</p>

<blockquote><pre style="white-space: pre-wrap;">
type Example[T Index[P], P any] struct {
	Index T
}
</pre>
</blockquote>

<p>This unfortunately means that when we use this generic type to
construct values of some concrete type, we have to repeat ourselves:</p>

<blockquote><pre style="white-space: pre-wrap;">
e := Example[*base, base]{&amp;base{0}}
</pre>
</blockquote>

<p>However, requiring both type constraints means that we can write
generic methods that use both of them:</p>

<blockquote><pre style="white-space: pre-wrap;">
func (e *Example[T, P]) Do() {
	e.Index = (T)(new(P))
}
</pre>
</blockquote>

<p>I believe that the P type would otherwise be inaccessible and you'd
be unable to construct this, but I could be wrong; these are somewhat
deep waters in Go generics.</p>

<p>You run into a similar issue with functions that you simply want
to take an argument that is a Pointer (or an Index), because our
Pointer (and Index) generic types are specified relative to an
underlying type and can't be used without specifying that underlying
type, either explicitly or through <a href="https://go.dev/ref/spec#Type_inference">type inference</a>. So you have to write
generic functions that look like:</p>

<blockquote><pre style="white-space: pre-wrap;">
func Something[T Pointer[P], P any] (p T) {
   [...]
}
</pre>
</blockquote>

<p>This generic function can successfully use <a href="https://go.dev/ref/spec#Type_inference">type inference</a> when
invoked, but it has to be declared this way and if type inference
doesn't work in your specific case you'll need to repeat yourself,
as with constructing <code>Example</code> values.</p>

<p>Looking into all of this and writing it out has left me less
enlightened than I hoped at the start of the process, but Go generics
are a complicated thing in general (or at least I find all of their
implications and dark corners to be complicated).</p>

<p>(<a href="https://mastodon.social/@tef/115942325269040186">Original source and background</a>, which is slightly
different from what I've done here.)</p>

<h3>Sidebar: The type inference way out for constructing values</h3>

<p>In the computer science tradition, we can add a layer of indirection.</p>

<blockquote><pre style="white-space: pre-wrap;">
func NewExample[T Index[P], P any] (p *P) Example[T,P] {
    var e Example[T,P]
    e.Index = p
    return e
}
</pre>
</blockquote>

<p>Then you can call this as '<code>NewExample(&amp;base{0})</code>' and type inference
will fill in al of the types, at least in this case. Of course this
isn't an in-place construction, which might be important in some
situations.</p>

<h3>Sidebar: The mind-bending original version</h3>

<p>The original version was like this:</p>

<blockquote><pre style="white-space: pre-wrap;">
type Index[P any, T any] interface {
	New() T
	*P
}

type Example[T Index[P, T], P any] struct {
	Index T
}
</pre>
</blockquote>

<p>In this version, <code>Example</code> has a type parameter that refers to
itself, '<code>T Index[P, T]</code>'. This is legal in a <a href="https://go.dev/ref/spec#Type_parameter_declarations">type parameter
declaration</a>;
what would be illegal is referring to '<code>Example</code>' in the type
parameters. It's also satisfiable (which isn't guaranteed).</p>
</div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/programming/GoGenericTypeIsPointer

---

*ID: fc24060fbc4255b1*
*抓取时间: 2026-03-12T13:49:26.048534*
