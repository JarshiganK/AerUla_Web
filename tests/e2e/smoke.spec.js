const { test, expect } = require('@playwright/test');

const uniqueEmail = () => `traveller-${Date.now()}-${Math.floor(Math.random() * 10000)}@example.com`;

async function signUpAndVerify(page) {
  const email = uniqueEmail();
  const password = 'AerUlaPass123!';

  await page.goto('/accounts/signup/');
  await page.getByLabel('First name').fill('Maya');
  await page.getByLabel('Email address').fill(email);
  await page.getByLabel('Password', { exact: true }).fill(password);
  await page.getByLabel('Password confirmation').fill(password);
  await page.getByRole('button', { name: 'Create account' }).click();

  await expect(page.getByRole('heading', { name: 'Verify your AerUla account.' })).toBeVisible();
  const verificationUrl = await page.locator('.dev-verification-box a').getAttribute('href');
  expect(verificationUrl).toBeTruthy();

  await page.goto(verificationUrl);
  await expect(page).toHaveURL(/\/dashboard\/$/);
  await expect(page.getByRole('heading', { name: /Welcome back, Maya\./ })).toBeVisible();

  return { email, password };
}

async function answerPotteryQuiz(page) {
  await page.goto('/simulations/pottery/quiz/');
  await page.getByLabel('It helps the clay harden evenly').check();
  await page.getByRole('button', { name: 'Check Answer' }).click();
}

async function logOut(page) {
  const logoutButton = page.getByRole('button', { name: 'Log out' });
  if (!(await logoutButton.isVisible())) {
    await page.getByLabel('Toggle navigation').click();
  }
  await logoutButton.click();
}

test.describe('AerUla public experience', () => {
  test('home page exposes the core journey and guide modal', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByRole('heading', { name: 'Explore Sri Lanka beyond the surface.' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Explore the Village' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Browse Experiences' })).toBeVisible();

    await page.getByLabel('Open cultural guide chatbot').click();
    await expect(page.getByRole('heading', { name: 'Chat with AerUla' })).toBeVisible();

    const messageBox = page.getByLabel('Ask about a hut, product, or tradition');
    await messageBox.fill('What does the pottery hut teach?');
    await page.getByRole('button', { name: 'Send' }).click();

    await expect(page.locator('[data-guide-transcript] .guide-chat-row.is-user').last()).toContainText('What does the pottery hut teach?');
    await expect(page.locator('[data-guide-transcript] .guide-chat-row.is-assistant').last()).toBeVisible();
  });

  test('guide modal does not invent hut matches for unrelated text', async ({ page }) => {
    await page.goto('/');

    await page.getByLabel('Open cultural guide chatbot').click();
    const messageBox = page.getByLabel('Ask about a hut, product, or tradition');
    await messageBox.fill('Jarshigan');
    await page.getByRole('button', { name: 'Send' }).click();

    const latestAnswer = page.locator('[data-guide-transcript] .guide-chat-row.is-assistant').last();
    await expect(latestAnswer).toContainText('could not find an AerUla knowledge-base match');
    await expect(latestAnswer).not.toContainText('Pottery Hut is the closest match');
    await expect(page.locator('[data-guide-source-count]')).toContainText('0 matched');
  });

  test('guide modal keeps booking follow-ups on the matching experience', async ({ page }) => {
    await page.goto('/');

    await page.getByLabel('Open cultural guide chatbot').click();
    const messageBox = page.getByLabel('Ask about a hut, product, or tradition');
    await messageBox.fill('book pottery');
    await page.getByRole('button', { name: 'Send' }).click();

    let latestAnswer = page.locator('[data-guide-transcript] .guide-chat-row.is-assistant').last();
    await expect(latestAnswer).toContainText('Pottery Workshop Visit');
    await expect(latestAnswer).toContainText('cannot submit the booking for you in chat yet');
    await expect(latestAnswer).not.toContainText('Clay Serving Bowl is the closest match');

    await messageBox.fill('can you book for me');
    await page.getByRole('button', { name: 'Send' }).click();

    latestAnswer = page.locator('[data-guide-transcript] .guide-chat-row.is-assistant').last();
    await expect(latestAnswer).toContainText('Pottery Workshop Visit');
    await expect(latestAnswer).not.toContainText('Folk Song Booklet');
    await expect(page.locator('[data-guide-sources]')).toContainText('Pottery Workshop Visit');
  });

  test('guide modal can add a clear product to cart and open checkout', async ({ page }) => {
    await page.goto('/');

    await page.getByLabel('Open cultural guide chatbot').click();
    const messageBox = page.getByLabel('Ask about a hut, product, or tradition');
    await messageBox.fill('add Clay Serving Bowl to cart');
    await page.getByRole('button', { name: 'Send' }).click();

    const latestAnswer = page.locator('[data-guide-transcript] .guide-chat-row.is-assistant').last();
    await expect(latestAnswer).toContainText('I added Clay Serving Bowl to your cart');
    await expect(latestAnswer.getByRole('link', { name: 'Go to checkout' })).toBeVisible();

    await latestAnswer.getByRole('link', { name: 'Go to checkout' }).click();
    await expect(page).toHaveURL(/\/marketplace\/checkout\/$/);
    await expect(page.getByRole('heading', { name: 'Place your order.' })).toBeVisible();
    await expect(page.getByText('LKR 2,400', { exact: true })).toBeVisible();
  });

  test('village map links to a hut, simulation preview, and guide page', async ({ page }) => {
    await page.goto('/village/');

    await expect(page.getByRole('heading', { name: 'Choose a cultural hut and continue your journey.' })).toBeVisible();
    await page.getByRole('button', { name: /Palmyrah Available/ }).click();
    await expect(page.locator('[data-hut-detail-name]')).toContainText('Palmyrah Craft Hut');

    await page.locator('[data-hut-action]').click();
    await expect(page).toHaveURL(/\/village\/palmyrah\/$/);
    await expect(page.getByRole('heading', { name: 'Palmyrah Craft Hut' })).toBeVisible();

    await page.getByRole('link', { name: 'Start Simulation Preview' }).click();
    await expect(page).toHaveURL(/\/simulations\/palmyrah\/$/);
    await expect(page.getByRole('heading', { name: /Match leaf strips/ })).toBeVisible();

    await page.goto('/guide/?q=palmyrah');
    await expect(page.getByRole('heading', { name: "Chat with AerUla's cultural guide." })).toBeVisible();
    await expect(page.getByText('Palmyrah Craft Hut').first()).toBeVisible();
  });

  test('marketplace filtering, cart, checkout, and booking requests work', async ({ page }) => {
    await page.goto('/marketplace/');
    await expect(page.getByRole('heading', { name: 'Products connected to the cultural village journey.' })).toBeVisible();

    await page.getByRole('link', { name: 'Pottery' }).first().click();
    await expect(page).toHaveURL(/\/marketplace\/\?hut=pottery$/);
    await expect(page.getByRole('heading', { name: 'Clay Serving Bowl' })).toBeVisible();

    await page.getByRole('link', { name: 'Add to Cart' }).first().click();
    await expect(page).toHaveURL(/\/marketplace\/cart\/$/);
    await expect(page.getByRole('heading', { name: 'Clay Serving Bowl' })).toBeVisible();

    await page.getByRole('link', { name: 'Continue to Checkout' }).click();
    await page.getByLabel('Full name').fill('Maya Traveller');
    await page.getByLabel('Email').fill(uniqueEmail());
    await page.getByRole('button', { name: 'Place Order' }).click();
    await expect(page.getByRole('heading', { name: /^AER-/ })).toBeVisible();

    await page.goto('/bookings/pottery-workshop/request/');
    await page.getByLabel('Preferred date').fill('2026-06-15');
    await page.getByLabel('Guests').fill('2');
    await page.getByLabel('Notes for host').fill('Prefer a morning workshop.');
    await page.getByRole('button', { name: 'Submit Request' }).click();
    await expect(page.getByText('Request received')).toBeVisible();
  });
});

test.describe('AerUla authenticated journey', () => {
  test('signup verification, login protection, and logout flow work', async ({ page }) => {
    const account = await signUpAndVerify(page);

    await logOut(page);
    await expect(page).toHaveURL('/');

    await page.goto('/dashboard/');
    await expect(page).toHaveURL(/\/accounts\/login\/\?next=\/dashboard\/$/);
    await page.getByLabel('Email address').fill(account.email);
    await page.getByLabel('Password').fill(account.password);
    await page.getByRole('button', { name: 'Login' }).click();

    await expect(page).toHaveURL(/\/dashboard\/$/);
    await expect(page.getByRole('link', { name: 'View Passport' })).toBeVisible();
  });

  test('verified user can complete a hut quiz and see passport progress', async ({ page }) => {
    await signUpAndVerify(page);

    await page.goto('/simulations/pottery/');
    const csrfCookie = (await page.context().cookies()).find((cookie) => cookie.name === 'csrftoken');
    expect(csrfCookie).toBeTruthy();
    const response = await page.request.post('/simulations/pottery/complete/', {
      headers: {
        'X-CSRFToken': csrfCookie.value,
      },
      data: {
        watched_seconds: 20,
        coverage_degrees: 240,
        hotspots: ['clay-wheel', 'drying-shelf', 'kiln-fire'],
      },
    });
    expect(response.ok()).toBeTruthy();
    expect((await response.json()).completed).toBeTruthy();

    await answerPotteryQuiz(page);
    await expect(page.getByRole('heading', { name: 'Badge recorded.' })).toBeVisible();

    await page.getByRole('link', { name: 'View Passport' }).click();
    await expect(page).toHaveURL(/\/dashboard\/passport\/$/);
    await expect(page.getByText('1/5')).toBeVisible();
    await expect(page.locator('.passport-card').filter({ hasText: 'Pottery Hut' })).toContainText('100');
  });
});
