# Single sign on systems versus X.509 certificates for the web

> 来源: utcc.utoronto.ca/~cks  
> 发布时间: 2026-01-19T03:59:11Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<div class="wikitext"><p>Modern single sign on specifications such as <a href="https://en.wikipedia.org/wiki/OpenID#OpenID_Connect_(OIDC)">OIDC</a> and
<a href="https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language">SAML</a>
and systems built on top of them are fairly complex things with a
lot of moving parts. It's possible to have <a href="https://utcc.utoronto.ca/~cks/space/blog/web/ApacheMellonAndOpenIDCViews">a somewhat simple
surface appearance for using them in web servers</a>, but the actual behind the scenes
implementation is typically complicated, and of course you need an
identity provider server and its supporting environment as well
(<a href="https://utcc.utoronto.ca/~cks/space/blog/sysadmin/SimpleSAMLphpWithDuo">which can get complicated</a>).
One reaction to this is to suggest using X.509 certificates to
authenticate people (as a recent comment on <a href="https://utcc.utoronto.ca/~cks/space/blog/web/ApacheMellonAndOpenIDCViews">this entry</a> did).</p>

<p>There are a variety of technical considerations here, like to what
extent browsers (and other software) might support personal X.509
certificates and make them easy to use, but to my mind there's also
an overriding broad consideration that makes the two significantly
different. Namely, <strong>people can remember passwords but they have
to store X.509 certificates</strong>. OIDC and SAML may pass around tokens
and programs dealing with them may store tokens, but the root of
everything is in passwords, and you can recover all the tokens from
there. This is not true with X.509 certificates; the certificate is
the thing.</p>

<p>(There are also challenges around issuing, managing, <a href="https://utcc.utoronto.ca/~cks/space/blog/web/WebServerMTLSHazards">checking</a>, and revoking personal X.509 certificates,
but let's ignore them.)</p>

<p>To make using X.509 certificate practical for authenticating people,
people have to be able to use them on multiple devices and move
them between browsers. Many people have multiple devices and people
do change what browsers they use (for all that browser and platform
vendors like them not to, or at least the ones that are currently
popular are often all for that). Today, there is basically nothing
that helps people deal with this, and as a result X.509 certificates
are at best awkward for people to use (and remember, <a href="https://utcc.utoronto.ca/~cks/space/blog/tech/SecurityIsPeople">security is
people</a>).</p>

<p>(In common use, it's easy to move passwords between browsers and
devices because they're in your head (excluding password managers,
which are still not used by a lot of people).)</p>

<p>Of course you could develop standards and software for moving and
managing X.509 certificates. In many ways, <a href="https://utcc.utoronto.ca/~cks/space/blog/web/PasskeysWhatIWant">passkeys</a>
show what's possible here, and also show many of the hazards of
using things for authentication that can't be memorized (or copied)
by people in order to transport them between environments. However,
no such standards and software exist today, and no one has every
shown much interest in developing them, even back in the days when
personal X.509 certificates were close to your only game in town.</p>

<p>(You could also develop much better browser UIs for dealing with
personal X.509 certificates, something that was extremely under-developed
back in the days when they were sometimes in use. Even importing
such a certificate into your browser could be awkward, never mind using
it.)</p>

<p>In the past, people have authenticated web applications through the
use of personal X.509 certificates (as a more secure form of
passwords). As far as I know, pretty much everyone has given up on
that and moved to better options, first passwords (sometimes plus
some form of additional confirmation) and then these days trying
to get people to use passkeys. One reason they gave up was that
actually using X.509 certificates in practice was awkward and
something that people found quite annoying.</p>

<p>(I had to use a personal X.509 certificate for a while in order to
get free TLS certificates for <a href="https://support.cs.toronto.edu/">our</a>
servers. It wasn't a particularly great experience and I'm not in
the least bit surprised that everyone ditched it for single sign
on systems.)</p>

<p>PS: It's no good saying that X.509 certificates would be great if
all of the required technology was magically developed, because
<a href="https://utcc.utoronto.ca/~cks/space/blog/tech/SocialProblemsMatter">that's not going to just happen</a>.
If you want personal X.509 certificates to be a thing, you have a
great deal of work ahead of you and there is no guarantee you'll
be successful. No one else is going to do that work for you.</p>

<p>PPS: You can imagine a system where people use their passwords and
other multi-factor authentication to issue themselves new personal
X.509 certificates signed by your local Certificate Authority, so
they can recover from losing the X.509 certificate blob (or get a
new certificate for a new device). Congratulations, you have just
re-invented a manual version of OIDC tokens (also, it's worse in
various ways).</p>
</div>
<div> (<a href="https://utcc.utoronto.ca/~cks/space/blog/web/WebSSOVsX509Certificates?showcomments#comments">6 comments</a>.) </div>

## 链接

https://utcc.utoronto.ca/~cks/space/blog/web/WebSSOVsX509Certificates

---

*ID: a4cea48efc97797a*
*抓取时间: 2026-03-12T13:49:26.048617*
