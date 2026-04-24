# How to Block the ‘Upgrade to Tahoe’ Alerts and System Settings Indicator

> 来源: daringfireball.net  
> 发布时间: 2026-02-27T18:45:16Z  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p><a href="https://robservatory.com/block-the-upgrade-to-tahoe-alerts-and-system-settings-indicator/">Rob Griffiths, writing at The Robservatory</a>:</p>

<blockquote>
  <p>So I have macOS Tahoe on my laptop, but I’m keeping my desktop
Mac on macOS Sequoia for now. Which means I have the joy of
seeing things like this wonderful notification on a regular
basis. Or I did, until I found a way to block them, at least in
90 day chunks. [...]</p>

<p>The secret? Using <a href="https://support.apple.com/guide/deployment/intro-to-device-management-profiles-depc0aadd3fe/web">device management profiles</a>, which let you
enforce policies on Macs in your organization, even if that
“organization” is one Mac on your desk. One of the available
policies is the ability to block activities related to major macOS
updates for up to 90 days at a time (the max the policy allows),
which seems like exactly what I needed.</p>
</blockquote>

<p>I followed Griffiths’s instructions about a week or so ago, and I’ve been enjoying a no-red-badge System Settings icon ever since. And the Tahoe upgrade doesn’t even show up in General → Software Update. With this profile installed, the <a href="https://daringfireball.net/2025/11/software_update_tahoe_confusing">confusing interface presented after clicking the “ⓘ” button next to any available update</a> cannot result in your upgrading to 26 Tahoe accidentally.</p>

<p>I waited to link to Griffiths’s post until I saw the pending update from Sequoia 15.7.3 to 15.7.4, just to make sure that was still working. <a href="https://daringfireball.net/misc/2026/02/no-tahoe-software-update-via-profile.png">And here it is</a>. My Software Update panels makes it look like Tahoe doesn’t even exist. A delicious glass of ice water, <a href="https://www.youtube.com/watch?v=Vp18clQ1tjE">without the visit to hell</a>.</p>

<p>I have one small clarification to Griffiths’s instructions though. He writes:</p>

<blockquote>
  <p>4/. <em>Optional step:</em> I didn’t want to defer normal updates, just
  the major OS update, so I changed the Optional (set to your
  taste) section to look like this:</p>

<p><!-- Optional (set to your taste) -->
      forceDelayedSoftwareUpdates</p>

<p>This way, I’ll still get notifications for updates other than the
major OS update, in case Apple releases anything further for macOS
Sequoia. Remember to save your changes, then quit the editor.</p>
</blockquote>

<p>I was confused by this step, initially, and only edited the first line after <code>&lt;!-- Optional (set to your taste) --&gt;</code>, to change <code>&lt;true/&gt;</code> to <code>&lt;false/&gt;</code> in the next line. But what Griffiths means, and is necessary to get the behavior I wanted, requires deleting the other two lines in that section of the plist file. I don’t want to defer updates like going from 15.7.3 to 15.7.4.</p>

<p>Before editing:</p>

<pre><code>&lt;!-- Optional (set to your taste) --&gt;
&lt;key&gt;forceDelayedSoftwareUpdates&lt;/key&gt;&lt;true/&gt;
&lt;key&gt;enforcedSoftwareUpdateMinorOSDeferredInstallDelay&lt;/key&gt;&lt;integer&gt;30&lt;/integer&gt;
&lt;key&gt;enforcedSoftwareUpdateNonOSDeferredInstallDelay&lt;/key&gt;&lt;integer&gt;30&lt;/integer&gt;
</code></pre>

<p>After:</p>

<pre><code>&lt;!-- Optional (set to your taste) --&gt;
&lt;key&gt;forceDelayedSoftwareUpdates&lt;/key&gt;&lt;false/&gt;
</code></pre>

<p>I’ll bet that’s the behavior most of my fellow MacOS 15 Sequoia holdouts want too.</p>

<div>
<a href="https://daringfireball.net/linked/2026/02/27/how-to-block-the-upgrade-to-tahoe-alerts-and-system-settings-indicator" title="Permanent link to ‘How to Block the ‘Upgrade to Tahoe’ Alerts and System Settings Indicator’">&nbsp;★&nbsp;</a>
</div>

## 链接

https://robservatory.com/block-the-upgrade-to-tahoe-alerts-and-system-settings-indicator/

---

*ID: 93775c8109ec2dcc*
*抓取时间: 2026-03-05T10:01:55.507140*
