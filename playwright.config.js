const { defineConfig, devices } = require('@playwright/test');

const port = process.env.PLAYWRIGHT_PORT || '8123';
const baseURL = `http://127.0.0.1:${port}`;

module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30 * 1000,
  expect: {
    timeout: 5 * 1000,
  },
  fullyParallel: false,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? 'github' : 'list',
  use: {
    baseURL,
    trace: 'on-first-retry',
    video: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: `.\\.venv\\Scripts\\python.exe manage.py runserver 127.0.0.1:${port} --noreload`,
    url: baseURL,
    reuseExistingServer: false,
    timeout: 120 * 1000,
    env: {
      DJANGO_SETTINGS_MODULE: 'aerula.settings',
    },
  },
  projects: [
    {
      name: 'desktop-chromium',
      use: {
        browserName: 'chromium',
        viewport: { width: 1280, height: 900 },
      },
    },
    {
      name: 'mobile-chromium',
      use: {
        ...devices['Pixel 5'],
        browserName: 'chromium',
      },
    },
  ],
});
