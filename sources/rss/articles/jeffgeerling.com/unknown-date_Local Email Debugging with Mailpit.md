# Local Email Debugging with Mailpit

> 来源: jeffgeerling.com  
> 发布时间: Thu, 08 Jan 2026 21:30:00 -0600  
> 分类: 海外技术博客  
> 优先级: medium

## 摘要

<p>For the past decade, I've used <a href="https://github.com/mailhog/MailHog">Mailhog</a> for local email debugging. Besides working on web applications that deal with email, I've long used email as the primary notification system for comments on the blog.</p>
<p>I built an <a href="https://github.com/geerlingguy/ansible-role-mailhog">Ansible role for Mailhog</a>, and it was one of the main features of <a href="https://www.jeffgeerling.com/blog/2015/major-improvements-drupal-vm/">Drupal VM</a>, a popular local development environment for Drupal I sunset 3 years ago.</p>
<p>Unfortunately, barring any future updates from the maintainers, it seems like <a href="https://github.com/mailhog/MailHog/issues/466">Mailhog has not been maintained</a> for four years now. It still <em>works</em>, but something as complex as an email debugging environment needs ongoing maintenance to stay relevant.</p>

## 链接

https://www.jeffgeerling.com/blog/2026/mailpit-local-email-debugging/

---

*ID: 8671949e99937a3a*
*抓取时间: 2026-03-05T10:01:52.005268*
