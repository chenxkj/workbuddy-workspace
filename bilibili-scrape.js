const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: false,  // 显示浏览器窗口，用户扫码
    slowMo: 100,
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
  });

  const page = await context.newPage();

  console.log('=== 步骤1：打开B站登录页 ===');
  await page.goto('https://passport.bilibili.com/login', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  // 截图给用户看登录状态
  await page.screenshot({ path: 'bilibili-login.png', fullPage: false });
  console.log('已截图 bilibili-login.png，请扫码登录');

  // 等待用户登录（通过检测cookie或URL变化）
  // 尝试等待主页出现，说明登录成功
  try {
    await page.waitForURL('**://www.bilibili.com/**', { timeout: 120000 });
    console.log('登录成功！');
  } catch (e) {
    console.log('等待登录超时，请手动扫码后继续');
    await page.waitForTimeout(60000);
  }

  // 截图确认登录状态
  await page.screenshot({ path: 'bilibili-after-login.png', fullPage: false });
  console.log('已截图 bilibili-after-login.png');

  console.log('\n=== 步骤2：访问UP主主页 ===');
  await page.goto('https://space.bilibili.com/3546798889110260', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  // 截图主页
  await page.screenshot({ path: 'bilibili-space.png', fullPage: true });
  console.log('已截图 bilibili-space.png（主页截图）');

  console.log('\n=== 步骤3：获取视频列表 ===');

  // 等待视频列表加载
  try {
    await page.waitForSelector('.cube-list', { timeout: 10000 });
  } catch (e) {
    // 可能结构不同，尝试其他选择器
    console.log('尝试其他选择器...');
  }

  // 提取视频信息
  const videoInfo = await page.evaluate(() => {
    // B站空间视频列表选择器可能变化，尝试多个
    const items = document.querySelectorAll('.video-item, .small-item, [class*="video"], .contribution-item');

    if (items.length === 0) {
      // 尝试从链接提取
      const links = Array.from(document.querySelectorAll('a[href*="/video/BV"]'));
      return links.slice(0, 20).map(a => ({
        title: a.title || a.textContent?.trim() || '无标题',
        url: a.href,
        bvid: a.href.match(/BV[\w]+/)?.[0] || ''
      }));
    }

    return Array.from(items).slice(0, 20).map(item => {
      const link = item.querySelector('a[href*="/video/BV"]') || item.querySelector('a');
      const title = item.querySelector('.title, .t, [class*="title"]')?.textContent?.trim() ||
                    link?.title || link?.textContent?.trim() || '无标题';
      const url = link?.href || '';
      const bvid = url.match(/BV[\w]+/)?.[0] || '';
      const playInfo = item.querySelector('[class*="play"], .info .text')?.textContent?.trim() || '';
      const date = item.querySelector('[class*="date"], [class*="time"]')?.textContent?.trim() || '';

      return { title, url, bvid, playInfo, date };
    });
  });

  console.log(`找到 ${videoInfo.length} 个视频：`);
  videoInfo.forEach((v, i) => {
    console.log(`${i + 1}. ${v.title} | ${v.bvid} | ${v.url} | 播放:${v.playInfo} | 日期:${v.date}`);
  });

  // 保存结果
  const fs = require('fs');
  fs.writeFileSync('bilibili-videos.json', JSON.stringify(videoInfo, null, 2));
  console.log('\n视频列表已保存到 bilibili-videos.json');

  // 打印所有BV号，方便后续下载
  const bvids = videoInfo.filter(v => v.bvid).map(v => v.bvid);
  console.log('\n所有BV号：', bvids.join(', '));

  console.log('\n截图文件已生成，请查看浏览器截图确认页面内容。');
  console.log('浏览器保持打开状态，可以继续操作...');

})();
