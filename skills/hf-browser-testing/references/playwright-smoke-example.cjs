// Copy this into a project and adapt routes/selectors. It is a reference only;
// HarnessFlow does not require Playwright as a dependency.
const { chromium } = require('playwright');

const baseUrl = process.env.SMOKE_BASE_URL || 'http://localhost:5173';
const apiHost = process.env.SMOKE_API_HOST || 'localhost:8080';
const routes = (process.env.SMOKE_ROUTES || '/,/login,/articles').split(',');

const observations = [];

function observe(severity, layer, scenario, message, detail = '') {
  observations.push({ severity, layer, scenario, message, detail });
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  let scenario = 'startup';
  page.on('console', (message) => {
    if (message.type() === 'error') {
      observe('blocking', 'console', scenario, 'console error', message.text());
    }
  });
  page.on('pageerror', (error) => {
    observe('blocking', 'console', scenario, 'uncaught page error', error.message);
  });
  page.on('requestfailed', (request) => {
    observe('major', 'network', scenario, 'request failed', `${request.method()} ${request.url()} ${request.failure()?.errorText || ''}`);
  });
  page.on('response', (response) => {
    const url = response.url();
    if (url.includes('/api/') && !url.includes(apiHost)) {
      observe('major', 'network', scenario, 'api request used unexpected host', url);
    }
    if (response.status() >= 400) {
      observe('major', 'network', scenario, `http ${response.status()}`, url);
    }
  });

  for (const route of routes) {
    scenario = `route ${route}`;
    await page.goto(`${baseUrl}${route}`, { waitUntil: 'domcontentloaded' });
    await page.waitForLoadState('networkidle', { timeout: 5000 }).catch(() => {});

    const bodyText = await page.locator('body').innerText().catch(() => '');
    if (!bodyText.trim()) {
      observe('blocking', 'dom', scenario, 'empty body / possible white screen');
    }
  }

  await browser.close();
  console.log(JSON.stringify({ observations }, null, 2));
  if (observations.some((item) => item.severity === 'blocking' || item.severity === 'major')) {
    process.exitCode = 1;
  }
})();
