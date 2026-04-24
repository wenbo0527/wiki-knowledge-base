# 详解 EMV 3DS：从责任转移到完整技术流程

> 来源: 人人都是产品经理  
> 发布时间: Thu, 12 Mar 2026 00:50:19 +0000  
> 分类: 专业技能类  
> 优先级: low

## 摘要

<blockquote><p>本文是对EMV 3DS的标准架构做了一个介绍。关于3DS，不同的MPI实现也有差别，具体的流程和细节，在后续我会基于Worldpay、MPGS、Cybersource、dLocal以及国内一些收单公司的3DS服务做一个抽象，实践MPI的3DS通用流程。</p>
</blockquote><p><img class="aligncenter" src="https://image.woshipm.com/2023/04/17/bb8a9e0e-dcf5-11ed-9781-00163e0b5ff3.png" /></p>
<p>在跨境信用卡支付中，很多用户都遇到过这样的场景：</p>
<p>输入卡号后，支付页面突然跳转到银行页面，需要输入短信验证码，或者在银行 App 中确认交易。</p>
<p><img class="aligncenter" src="https://image.woshipm.com/2026/03/11/663f2db8-1d32-11f1-a31b-00163e09d72f.png" width="750" /></p>
<p>这一步就是信用卡支付中的身份验证机制：<strong>3-D Secure</strong></p>
<p>随着支付行业的发展，这一体系已经升级为新的标准：<strong>EMV 3-D Secure</strong></p>
<blockquote><p>EMVCo在前面讲EMV QR code的文章有提供到过，3DS是他们的另一个标准。</p></blockquote>
<p>EMV 3DS 不仅提高了安全性，也显著改善了用户体验，使得大部分交易可以在用户几乎无感知的情况下完成认证。</p>
<div class="js-star yyp--fancyPost"></div>
<p>但在理解技术流程之前，需要先回答三个核心问题：</p>
<ol>
<li>为什么支付行业需要 3DS</li>
<li>为什么很多商户主动启用 3DS</li>
<li>为什么有些交易不需要 3DS</li>
</ol>
<h2>一、为什么需要 3DS？</h2>
<p>在传统的线上信用卡支付中，通常只需要三项信息：</p>
<ol>
<li>卡号</li>
<li>有效期</li>
<li>CVV</li>
</ol>
<p>这些信息一旦泄露，就可能被盗刷。</p>
<p>对于商户来说，这带来了一个非常严重的问题：<strong>欺诈拒付（Fraud Chargeback）</strong></p>
<p>当持卡人发现交易不是自己发起时，可以向发卡行申请拒付。</p>
<p>如果交易被认定为欺诈，商户通常需要承担损失。</p>
<p>因此，卡组织推出了 <strong>3DS 身份验证体系</strong>，在支付过程中增加一次 <strong>发卡行参与的身份验证</strong>。</p>
<p>常见的验证方式包括：</p>
<ul>
<li>短信 OTP</li>
<li>银行 App 确认</li>
<li>生物识别</li>
</ul>
<p>通过这一机制，可以确认：</p>
<p><strong>发起交易的人确实是持卡人本人。</strong></p>
<h2>二、为什么商户会主动使用 3DS？</h2>
<p>对于商户来说，3DS 最大的价值不是验证码，而是：<strong>Liability Shift（责任转移）</strong></p>
<p>当一笔交易成功完成 3DS 认证后，如果之后发生欺诈拒付，责任通常会从商户转移到发卡行。</p>
<p>简单理解：</p>
<p><strong>没有 3DS</strong></p>
<p>欺诈责任 → 商户承担</p>
<p><strong>完成 3DS</strong></p>
<p>欺诈责任 → 发卡行承担</p>
<p>因此在以下场景中，商户通常会主动开启 3DS：</p>
<ul>
<li>高风险国家交易</li>
<li>高金额交易</li>
<li>数字商品</li>
<li>跨境电商</li>
</ul>
<p>对于支付公司和 PSP 来说，3DS 也是风控体系的重要组成部分。</p>
<h2>三、为什么有些交易不需要 3DS？</h2>
<p>虽然 3DS 可以提高安全性，但它也会增加支付步骤。</p>
<p>如果每一笔交易都强制验证，用户体验会明显下降。</p>
<p>因此在很多情况下，交易可以 <strong>豁免（Exemption）</strong> 3DS。</p>
<p>常见的豁免场景包括：</p>
<h3>1.低金额交易</h3>
<p>例如欧洲监管规定：30 欧元以下交易可以豁免强认证。</p>
<h3>2.低风险交易</h3>
<p>如果发卡行或收单行的风险评估认为交易风险较低，可以直接通过认证。</p>
<h3>3.信任商户</h3>
<p>持卡人可能将某些商户标记为信任商户。</p>
<p>后续交易可以减少验证。</p>
<h3>4.风控评分较低</h3>
<p>当交易设备、历史行为和交易模式都正常时，系统可能直接允许交易通过。</p>
<h2>四、3DS 的三大 Domain 架构</h2>
<p>在 3-D Secure 架构中，整个系统被划分为三个 Domain。</p>
<h3>1.Acquirer Domain（收单域）</h3>
<p>Acquirer Domain 是 <strong>商户侧所在的系统域</strong>。</p>
<p>主要组件包括：</p>
<ul>
<li>Merchant（商户系统）</li>
<li>Payment Gateway / PSP</li>
<li>3DS Server</li>
<li>Acquirer（收单行）</li>
</ul>
<p>其中最核心的组件是 <strong>3DS Server</strong>。</p>
<p>3DS Server 负责：</p>
<ul>
<li>查询卡是否支持 3DS</li>
<li>向发卡行发起认证请求</li>
<li>接收认证结果</li>
<li>将认证数据传递给授权系统</li>
</ul>
<h3>2.Interoperability Domain（互操作域）</h3>
<p>这个域由卡组织运营。</p>
<p>核心组件：</p>
<p><strong>Directory Server（DS）</strong></p>
<p>DS 的作用：</p>
<ul>
<li>判断卡是否支持 3DS</li>
<li>查询发卡行 ACS</li>
<li>路由认证请求</li>
</ul>
<p>Directory Server 通常由卡组织维护，例如：</p>
<ul>
<li>Visa</li>
<li>Mastercard</li>
</ul>
<h3>3.Issuer Domain（发卡域）</h3>
<p>Issuer Domain 是 <strong>发卡银行所在的系统域</strong>。</p>
<p>核心组件：</p>
<p><strong>ACS（Access Control Server）</strong></p>
<p>ACS 负责：</p>
<ul>
<li>风险评估</li>
<li>用户验证</li>
<li>生成认证结果</li>
</ul>
<p>用户在支付过程中看到的验证码页面，通常就是 ACS 提供的，例如引言部分这个图就是EMV定义的一个设计规范，由各个发卡行实现。</p>
<p><img class="aligncenter" src="https://image.woshipm.com/2026/03/11/663f2db8-1d32-11f1-a31b-00163e09d72f.png" width="750" /></p>
<h2>五、3DS 系统整体架构</h2>
<p>在 EMV 3DS 中，交易通常会进入两种验证模式。</p>
<h3>1. Frictionless（无感验证）</h3>
<p>发卡行认为交易风险较低。</p>
<p>交易直接完成认证，用户不会看到任何验证页面。</p>
<p>目前大部分交易都属于这种情况。</p>
<p><img class="aligncenter" src="https://image.woshipm.com/2026/03/11/7c179d00-1d32-11f1-9440-00163e09d72f.png" width="750" /></p>
<blockquote><p>这是EMV 3DS的规范，里面的几个名词都是逻辑角色，在实际支付系统里，它们的职责和部署方式是不同的。下面做一下简单的介绍：</p>
<p>3DS Requestor是发起3DS认证请求的实体，通常是商户或者支付公司以及收单行，例如Shopify、Stripe、Checkout等。</p>
<p>3DS Client是 运行在持卡人设备或商户前端环境中的组件。例如前端浏览器中的JS SDK代码。</p>
<p>3DS Server一般也可以称为MPI，供应服务商，用来和DS对接实现3DS交互过程中的各种接口。例如Cardinal、Netcetera(欧洲)、GPayments(亚洲)。</p></blockquote>
<blockquote><p>在全球主流的收单机构里面，每家的能力和发展线路不一样，这几个组件之间有交叉。</p>
<p>例如Cybersource作为Requestor使用的是Cardinal的3DS Server，同时提供了自己的SDK作为Client。</p>
<p>Adyen、Worldpay拥有自建 3DS Server，EMVCo 认证可以同时作为3DS Requestor、3DS Client 、3DS Server。大部分的支付公司还是</p>
<p>使用第三方的3DS Server。</p></blockquote>
<p>Frictionless包含以下步骤：</p>
<p>开始：持卡人在消费设备上发起交易。持卡人提供身份验证所需的信息（持卡人输入或商户已存档的信息）。</p>
<p>1）3DS Requestor Environment收集必要的3-D Secure 信息并将其提供给 3DS Server，以便包含在AReq(Authentication Reqesut) 消息中。</p>
<p>信息的提供方式和来源取决于以下因素：</p>
<ul>
<li>设备渠道——基于应用程序或基于浏览器</li>
<li>消息类别——Payment or Non-Payment</li>
<li>3DS Requestor 的 3-D Secure 实现</li>
</ul>
<p>2）3DS Server使用持卡人提供的信息以及在3DS Requestor Environment中收集的数据，创建并向 DS 发送 AReq 消息，然后 DS 将该消息转发给相应的ACS。</p>
<p>3）ACS 收到 AReq 消息后，向 DS 返回 ARes(Authentication Response) 消息，DS 再将该消息转发给发起 3DS Server。</p>
<p>在返回响应之前，ACS 会评估 AReq 消息中提供的数据。</p>
<p>在Frictionless流程中，ACS 会判断无需持卡人进一步交互即可完成身份验证。</p>
<p>4）3DS Server将 ARes 消息的结果传递给 3DS Requestor Environment，后者随后通知持卡人。</p>
<p>到这一步3DS已经认证完成，可以继续发起授权请求了。</p>
<p>5）商户和收单机构——商户与其收单机构进行Authorisation。</p>
<p>6）收单机构可以通过支付网络向发卡机构处理授权，并将授权结果返回给商户。</p>
<h3>2. Challenge（挑战验证）</h3>
<p>如果发卡行认为交易风险较高，就会要求用户验证身份，例如：</p>
<ul>
<li>OTP 短信验证码</li>
<li>银行 App 确认</li>
<li>生物识别</li>
</ul>
<p><img class="aligncenter" src="https://image.woshipm.com/2026/03/11/908acbc2-1d32-11f1-9440-00163e09d72f.png" width="750" /></p>
<p>挑战流程包含以下步骤：</p>
<p>开始：持卡人——与无摩擦流程相同。</p>
<p>1）3DS Requestor Environment——与无摩擦流程相同。</p>
<p>2）3DS 服务器通过 DS 到 ACS——与无摩擦流程相同。</p>
<p>3）ACS 通过 DS 到 3DS Server——与无摩擦流程相同，但 ARes消息指示需要持卡人进一步交互才能完成 身份验证。</p>
<p>4）3DS Server到 3DS Requestor Environment——与无摩擦流程相同，但需要持卡人进一步交互才能完成 身份验证。</p>
<p>5）3DS Client到 ACS——3DS Client根据 ARes 消息中接收到的信息发起 CReq 消息。具体方式取决于模型：</p>
<ul>
<li>基于应用程序——CReq 消息由 3DS SDK 生成并发布到从 ARes 消息中接收到的 ACS URL。</li>
<li>基于浏览器——3DS Server生成 CReq 消息，并由 3DS Requestor通过持卡人浏览器发送至从 ARes 消息中收到的 ACS URL。</li>
</ul>
<p>6）ACS 与 3DS Client——ACS 接收 CReq 消息并与 3DS Client交互，以促进持卡人交互。</p>
<p>具体方式取决于模型：</p>
<ul>
<li>基于应用程序——ACS 使用 CReq 和 CRes 消息对执行挑战。ACS 响应 CReq 消息，生成 CRes 消息，请求持卡人输入身份验证数据，并将其发送至 3DS SDK。</li>
<li>基于浏览器——ACS 将身份验证用户界面发送至持卡人浏览器。持卡人通过浏览器输入身份验证数据，供 ACS 验证。为响应 CReq 消息，ACS 生成 CRes 消息并将其发送至 3DS Server，以指示身份验证结果。</li>
</ul>
<p>注：对于基于应用程序的模型，步骤 5 和步骤 6 将重复执行，直至 ACS 做出判断。</p>
<p>注：对于基于浏览器的模型，CRes 消息在步骤 8 之后发送。</p>
<p>7）ACS 通过 DS 发送至 3DS Server——ACS 向 DS 发送包含身份验证值 (AV) 的 RReq 消息，DS 随后使用从 AReq 消息中收到的 3DS 服务器 URL 将该消息路由至相应的 3DS Server。</p>
<p>8）3DS Server经 DS 到 ACS——3DS Server接收到 RReq 消息，并响应地向 DS 返回 RRes 消息，DS 随后将该消息路由至ACS。</p>
<p>3DS处理到此结束。</p>
<ol>
<li>商户和收单机构——与无摩擦流程相同。</li>
<li>支付授权——与无摩擦流程相同。</li>
</ol>
<h2>六、结语</h2>
<p>3DS 是现代信用卡支付体系中的核心安全机制。</p>
<p>它通过 <strong>三大 Domain 协同工作</strong>：</p>
<ol>
<li>Acquirer Domain</li>
<li>Interoperability Domain</li>
<li>Issuer Domain</li>
</ol>
<p>完成一次完整的持卡人身份验证。</p>
<p>对于支付系统来说，3DS 不仅仅是验证码，更重要的是：</p>
<ul>
<li>降低欺诈风险</li>
<li>提供责任转移</li>
<li>提升支付成功率</li>
</ul>
<p>随着 <strong>EMV 3DS</strong> 的普及，大部分交易已经可以在用户几乎无感知的情况下完成认证。</p>
<div class="article--copyright"><p>本文由 @Amour 原创发布于人人都是产品经理，未经许可，禁止转载</p>
<p>题图来自 Unsplash，基于 CC0 协议。</p>
</div>

## 链接

https://www.woshipm.com/pd/6351820.html

---

*ID: 30632d4513a893aa*
*抓取时间: 2026-03-12T10:14:20.891402*
