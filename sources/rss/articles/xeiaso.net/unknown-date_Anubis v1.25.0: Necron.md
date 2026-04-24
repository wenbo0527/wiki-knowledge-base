# Anubis v1.25.0: Necron

> 来源: xeiaso.net  
> 发布时间: Wed, 18 Feb 2026 00:00:00 GMT  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p>Hey all,</p>
        <p>I'm sure you've all been aware that things have been slowing down a little with Anubis development, and I want to apologize for that. A lot has been going on in my life lately (my blog will have a post out on Friday with more information), and as a result I haven't really had the energy to work on Anubis in publicly visible ways. There are things going on behind the scenes, but nothing is really shippable yet, sorry!</p>
        <p>I've also been feeling some burnout in the wake of perennial waves of anger directed towards me. I'm handling it, I'll be fine, I've just had a lot going on in my life and it's been rough.</p>
        <p>I've been missing the sense of wanderlust and discovery that comes with the artistic way I playfully develop software. I suspect that some of the stresses I've been through (setting up a complicated surgery in a country whose language you aren't fluent in is kind of an experience) have been sapping my energy. I'd gonna try to mess with things on my break, but realistically I'm probably just gonna be either watching Stargate SG-1 or doing unreasonable amounts of ocean fishing in Final Fantasy 14. Normally I'd love to keep the details about my medical state fairly private, but I'm more of a public figure now than I was this time last year so I don't really get the invisibility I'm used to for this.</p>
        <p>I've also had a fair amount of negativity directed at me for simply being much more visible than the anonymous threat actors running the scrapers that are ruining everything, which though understandable has not helped.</p>
        <p>Anyways, it all worked out and I'm about to be in the hospital for a week, so if things go really badly with this release please downgrade to the last version and/or upgrade to the main branch when the fix PR is inevitably merged. I hoped to have time to tame GPG and set up full release automation in the Anubis repo, but that didn't work out this time and that's okay.</p>
        <p>If I can challenge you all to do something, go out there and try to actually create something new somehow. Combine ideas you've never mixed before. Be creative, be human, make something purely for yourself to scratch an itch that you've always had yet never gotten around to actually mending.</p>
        <p>At the very least, try to be an example of how you want other people to act, even when you're in a situation where software written by someone else is configured to require a user agent to execute javascript to access a webpage.</p>
        <p>Be well,</p>
        <p>Xe</p>
        <p>PS: if you're well-versed in FFXIV lore, the release title should give you an idea of the kind of stuff I've been going through mentally.</p>
        <ul>
        <li>Add iplist2rule tool that lets admins turn an IP address blocklist into an Anubis ruleset.</li>
        <li>Add Polish locale (<a href="https://github.com/TecharoHQ/anubis/pull/1309">#1292</a>)</li>
        <li>Fix honeypot and imprint links missing <code>BASE_PREFIX</code> when deployed behind a path prefix (<a href="https://github.com/TecharoHQ/anubis/issues/1402">#1402</a>)</li>
        <li>Add ANEXIA Sponsor logo to docs (<a href="https://github.com/TecharoHQ/anubis/pull/1409">#1409</a>)</li>
        <li>Improve idle performance in memory storage</li>
        <li>Add HAProxy Configurations to Docs (<a href="https://github.com/TecharoHQ/anubis/pull/1424">#1424</a>)</li>
        </ul>
        <h2>What's Changed</h2>
        <ul>
        <li>build(deps): bump the github-actions group with 4 updates by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1355">https://github.com/TecharoHQ/anubis/pull/1355</a></li>
        <li>feat(localization): add Polish language translation by @btomaev in <a href="https://github.com/TecharoHQ/anubis/pull/1363">https://github.com/TecharoHQ/anubis/pull/1363</a></li>
        <li>docs(known-instances): Alphabetical order + Add Valve Corporation by @p0008874 in <a href="https://github.com/TecharoHQ/anubis/pull/1352">https://github.com/TecharoHQ/anubis/pull/1352</a></li>
        <li>test: basic nginx smoke test by @Xe in <a href="https://github.com/TecharoHQ/anubis/pull/1365">https://github.com/TecharoHQ/anubis/pull/1365</a></li>
        <li>build(deps): bump the github-actions group with 3 updates by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1369">https://github.com/TecharoHQ/anubis/pull/1369</a></li>
        <li>build(deps-dev): bump esbuild from 0.27.1 to 0.27.2 in the npm group by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1368">https://github.com/TecharoHQ/anubis/pull/1368</a></li>
        <li>fix(test): remove interactive flag from nginx smoke test docker run c… by @JasonLovesDoggo in <a href="https://github.com/TecharoHQ/anubis/pull/1371">https://github.com/TecharoHQ/anubis/pull/1371</a></li>
        <li>test(nginx): fix tests to work in GHA by @Xe in <a href="https://github.com/TecharoHQ/anubis/pull/1372">https://github.com/TecharoHQ/anubis/pull/1372</a></li>
        <li>feat: iplist2rule utility command by @Xe in <a href="https://github.com/TecharoHQ/anubis/pull/1373">https://github.com/TecharoHQ/anubis/pull/1373</a></li>
        <li>Update check-spelling metadata by @JasonLovesDoggo in <a href="https://github.com/TecharoHQ/anubis/pull/1379">https://github.com/TecharoHQ/anubis/pull/1379</a></li>
        <li>fix: Update SSL Labs IP addresses by @majiayu000 in <a href="https://github.com/TecharoHQ/anubis/pull/1377">https://github.com/TecharoHQ/anubis/pull/1377</a></li>
        <li>fix: respect Accept-Language quality factors in language detection by @majiayu000 in <a href="https://github.com/TecharoHQ/anubis/pull/1380">https://github.com/TecharoHQ/anubis/pull/1380</a></li>
        <li>build(deps): bump the gomod group across 1 directory with 3 updates by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1370">https://github.com/TecharoHQ/anubis/pull/1370</a></li>
        <li>Revert &quot;build(deps): bump the gomod group across 1 directory with 3 updates&quot; by @JasonLovesDoggo in <a href="https://github.com/TecharoHQ/anubis/pull/1386">https://github.com/TecharoHQ/anubis/pull/1386</a></li>
        <li>build(deps): bump preact from 10.28.0 to 10.28.1 in the npm group by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1387">https://github.com/TecharoHQ/anubis/pull/1387</a></li>
        <li>docs: document how to import the default config by @Xe in <a href="https://github.com/TecharoHQ/anubis/pull/1392">https://github.com/TecharoHQ/anubis/pull/1392</a></li>
        <li>fix sponsor (Databento) logo size by @ayoung5555 in <a href="https://github.com/TecharoHQ/anubis/pull/1395">https://github.com/TecharoHQ/anubis/pull/1395</a></li>
        <li>fix: correct typos by @antonkesy in <a href="https://github.com/TecharoHQ/anubis/pull/1398">https://github.com/TecharoHQ/anubis/pull/1398</a></li>
        <li>fix(web): include base prefix in generated URLs by @Xe in <a href="https://github.com/TecharoHQ/anubis/pull/1403">https://github.com/TecharoHQ/anubis/pull/1403</a></li>
        <li>docs: clarify botstopper kubernetes instructions by @tarrow in <a href="https://github.com/TecharoHQ/anubis/pull/1404">https://github.com/TecharoHQ/anubis/pull/1404</a></li>
        <li>Add IP mapped Perplexity user agents by @tdgroot in <a href="https://github.com/TecharoHQ/anubis/pull/1393">https://github.com/TecharoHQ/anubis/pull/1393</a></li>
        <li>build(deps): bump astral-sh/setup-uv from 7.1.6 to 7.2.0 in the github-actions group by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1413">https://github.com/TecharoHQ/anubis/pull/1413</a></li>
        <li>build(deps): bump preact from 10.28.1 to 10.28.2 in the npm group by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1412">https://github.com/TecharoHQ/anubis/pull/1412</a></li>
        <li>chore: add comments back to Challenge struct. by @JasonLovesDoggo in <a href="https://github.com/TecharoHQ/anubis/pull/1419">https://github.com/TecharoHQ/anubis/pull/1419</a></li>
        <li>performance: remove significant overhead of decaymap/memory by @brainexe in <a href="https://github.com/TecharoHQ/anubis/pull/1420">https://github.com/TecharoHQ/anubis/pull/1420</a></li>
        <li>web: fix spacing/indent by @bjacquin in <a href="https://github.com/TecharoHQ/anubis/pull/1423">https://github.com/TecharoHQ/anubis/pull/1423</a></li>
        <li>build(deps): bump the github-actions group with 4 updates by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1425">https://github.com/TecharoHQ/anubis/pull/1425</a></li>
        <li>Improve Dutch translations by @louwers in <a href="https://github.com/TecharoHQ/anubis/pull/1446">https://github.com/TecharoHQ/anubis/pull/1446</a></li>
        <li>chore: set up commitlint, husky, and prettier by @Xe in <a href="https://github.com/TecharoHQ/anubis/pull/1451">https://github.com/TecharoHQ/anubis/pull/1451</a></li>
        <li>Fix a CI warning: &quot;The set-output command is deprecated&quot; by @kurtmckee in <a href="https://github.com/TecharoHQ/anubis/pull/1443">https://github.com/TecharoHQ/anubis/pull/1443</a></li>
        <li>feat(apps): add updown.io policy by @hyperdefined in <a href="https://github.com/TecharoHQ/anubis/pull/1444">https://github.com/TecharoHQ/anubis/pull/1444</a></li>
        <li>docs: add AI coding tools policy by @Xe in <a href="https://github.com/TecharoHQ/anubis/pull/1454">https://github.com/TecharoHQ/anubis/pull/1454</a></li>
        <li>feat(docs): Add ANEXIA Sponsor logo by @Earl0fPudding in <a href="https://github.com/TecharoHQ/anubis/pull/1409">https://github.com/TecharoHQ/anubis/pull/1409</a></li>
        <li>chore: sync logo submissions by @Xe in <a href="https://github.com/TecharoHQ/anubis/pull/1455">https://github.com/TecharoHQ/anubis/pull/1455</a></li>
        <li>build(deps): bump the github-actions group across 1 directory with 6 updates by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1453">https://github.com/TecharoHQ/anubis/pull/1453</a></li>
        <li>build(deps): bump the npm group across 1 directory with 2 updates by @dependabot[bot] in <a href="https://github.com/TecharoHQ/anubis/pull/1452">https://github.com/TecharoHQ/anubis/pull/1452</a></li>
        <li>feat(docs): Add HAProxy Configurations to Docs by @Earl0fPudding in <a href="https://github.com/TecharoHQ/anubis/pull/1424">https://github.com/TecharoHQ/anubis/pull/1424</a></li>
        </ul>
        <h2>New Contributors</h2>
        <ul>
        <li>@majiayu000 made their first contribution in <a href="https://github.com/TecharoHQ/anubis/pull/1377">https://github.com/TecharoHQ/anubis/pull/1377</a></li>
        <li>@ayoung5555 made their first contribution in <a href="https://github.com/TecharoHQ/anubis/pull/1395">https://github.com/TecharoHQ/anubis/pull/1395</a></li>
        <li>@antonkesy made their first contribution in <a href="https://github.com/TecharoHQ/anubis/pull/1398">https://github.com/TecharoHQ/anubis/pull/1398</a></li>
        <li>@tarrow made their first contribution in <a href="https://github.com/TecharoHQ/anubis/pull/1404">https://github.com/TecharoHQ/anubis/pull/1404</a></li>
        <li>@tdgroot made their first contribution in <a href="https://github.com/TecharoHQ/anubis/pull/1393">https://github.com/TecharoHQ/anubis/pull/1393</a></li>
        <li>@brainexe made their first contribution in <a href="https://github.com/TecharoHQ/anubis/pull/1420">https://github.com/TecharoHQ/anubis/pull/1420</a></li>
        <li>@bjacquin made their first contribution in <a href="https://github.com/TecharoHQ/anubis/pull/1423">https://github.com/TecharoHQ/anubis/pull/1423</a></li>
        <li>@louwers made their first contribution in <a href="https://github.com/TecharoHQ/anubis/pull/1446">https://github.com/TecharoHQ/anubis/pull/1446</a></li>
        <li>@kurtmckee made their first contribution in <a href="https://github.com/TecharoHQ/anubis/pull/1443">https://github.com/TecharoHQ/anubis/pull/1443</a></li>
        </ul>
        <p><strong>Full Changelog</strong>: <a href="https://github.com/TecharoHQ/anubis/compare/v1.24.0...v1.25.0">https://github.com/TecharoHQ/anubis/compare/v1.24.0...v1.25.0</a></p>

## 链接

https://github.com/TecharoHQ/anubis/releases/tag/v1.25.0

---

*ID: abbbbd6fe8dc8b96*
*抓取时间: 2026-03-05T10:02:34.457752*
