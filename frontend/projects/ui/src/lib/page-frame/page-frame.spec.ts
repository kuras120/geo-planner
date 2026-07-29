import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';

import { PageFrame } from './page-frame';

@Component({
  imports: [PageFrame],
  template: `
    <gp-page-frame applicationName="Geo Planner" contextLabel="Test">
      <h1>Treść strony</h1>
    </gp-page-frame>
  `,
})
class TestHost {}

describe('PageFrame', () => {
  it('renders landmarks, projected content, and a skip link', async () => {
    const fixture = TestBed.createComponent(TestHost);
    await fixture.whenStable();

    const element = fixture.nativeElement as HTMLElement;

    expect(element.querySelector('header')?.textContent).toContain('Geo Planner');
    expect(element.querySelector('main h1')?.textContent).toBe('Treść strony');
    expect(element.querySelector<HTMLAnchorElement>('.skip-link')?.hash).toBe('#main-content');
  });
});
