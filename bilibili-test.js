const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    // 设置B站Cookie
    extraHTTPHeaders: {},
  });

  // 添加Cookie到context
  const cookies = [
    { name: 'buvid3', value: 'DAEC69D8-A3AE-60F3-1BFC-FC868BBE8D3A05108infoc', domain: '.bilibili.com', path: '/' },
    { name: 'bili_jct', value: '5e5e1d16b0d778efe2c1942fe2e160be', domain: '.bilibili.com', path: '/' },
    { name: 'DedeUserID', value: '1632530207', domain: '.bilibili.com', path: '/' },
    { name: 'bili_ticket', value: 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Nzc2MjEwMDYsImlhdCI6MTc3NzM2MTc0NiwicGx0IjotMX0.dv2MbjlNXpDh8Fm2OWuhvOAAOXY3-6ebEBQcT1WEcdU', domain: '.bilibili.com', path: '/' },
    { name: 'buvid_fp', value: 'f55b7f4b144ce185651faa938ab01b39', domain: '.bilibili.com', path: '/' },
    { name: 'sid', value: '8ev3r6cu', domain: '.bilibili.com', path: '/' },
    { name: 'b_nut', value: '1777361805', domain: '.bilibili.com', path: '/' },
    { name: 'b_lsid', value: '2E4E5D3F_19DD3125327', domain: '.bilibili.com', path: '/' },
    { name: 'CURRENT_FNVAL', value: '2000', domain: '.bilibili.com', path: '/' },
    { name: 'home_feed_column', value: '4', domain: '.bilibili.com', path: '/' },
  ];

  await context.addCookies(cookies);

  const page = await context.newPage();

  console.log('=== 打开B站 ===');
  await page.goto('https://www.bilibili.com', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'bilibili-check-login.png', fullPage: false });

  // 检查是否已登录
  const isLoggedIn = await page.evaluate(() => {
    const nav = document.querySelector('.header-login-entry, .header-user-entry, .user-info');
    return nav ? '可能未登录' : '未知';
  });

  // 获取页面文字判断
  const pageText = await page.evaluate(() => document.body.innerText.substring(0, 500));
  const hasLoginText = pageText.includes('登录') && !pageText.includes('已登录');
  console.log('页面判断：', hasLoginText ? '可能未登录' : '可能已登录或游客');

  console.log('\n=== 访问UP主主页 ===');
  await page.goto('https://space.bilibili.com/3546798889110260', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'bilibili-space-check.png', fullPage: true });

  // 提取视频列表
  const videoData = await page.evaluate(() => {
    const items = [];
    // 尝试多种选择器
    const cards = document.querySelectorAll('.video-card, .bili-video-card, .cover, [class*="video-card"]');

    // 尝试从链接提取
    const allLinks = Array.from(document.querySelectorAll('a[href*="/video/BV"]'));
    allLinks.forEach(link => {
      const href = link.href;
      const bvid = href.match(/BV[\w]+/)?.[0] || '';
      const title = link.title || link.getAttribute('data-title') ||
                    link.querySelector('.title')?.textContent?.trim() ||
                    link.innerText?.split('\n')[0] || '';

      if (bvid && title && !items.find(x => x.bvid === bvid)) {
        items.push({ bvid, title, url: href });
      }
    });

    return {
      items,
      rawLinks: allLinks.slice(0, 10).map(l => ({
        href: l.href,
        text: l.innerText?.substring(0, 100)
      })),
      bodySnippet: document.body.innerText?.substring(0, 1000)
    };
  });

  console.log('找到视频：', videoData.items.length);
  videoData.items.forEach(v => console.log(`  - ${v.title} | ${v.bvid}`));

  console.log('\n--- 原始链接 ---');
  videoData.rawLinks.forEach(l => console.log(`  ${l.href} | ${l.text?.substring(0, 60)}`));

  // 保存
  const fs = require('fs');
  fs.writeFileSync('bilibili-video-list.json', JSON.stringify(videoData, null, 2));
  console.log('\n已保存到 bilibili-video-list.json');
  console.log('浏览器保持打开，请截图确认页面内容');

})().catch(e => { console.error('错误：', e.message); process.exit(1); });
