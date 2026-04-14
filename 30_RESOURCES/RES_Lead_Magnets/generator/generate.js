const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const htmlPath = process.argv[2] || path.join(__dirname, 'checklist.html');
  const outputPath = process.argv[3] || path.join(__dirname, '..', 'Checklist_AI_w_Firmie.pdf');

  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(`file://${path.resolve(htmlPath)}`, { waitUntil: 'networkidle' });

  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '0', bottom: '0', left: '0', right: '0' },
  });

  console.log(`PDF saved: ${outputPath}`);
  await browser.close();
})();
