import { expect, test } from '@playwright/test';

test('shows the accessible foundation shell', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveTitle('Geo Planner — fundament aplikacji');
  await expect(page.getByRole('banner')).toContainText('Geo Planner');
  await expect(page.getByRole('main')).toBeVisible();
  await expect(
    page.getByRole('heading', {
      name: 'Nowy interfejs jest przygotowany do migracji funkcji.',
    }),
  ).toBeVisible();
  await expect(page.getByRole('link', { name: 'Przejdź do treści' })).toHaveAttribute(
    'href',
    '#main-content',
  );
});
