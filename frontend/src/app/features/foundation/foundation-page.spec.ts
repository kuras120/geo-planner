import { TestBed } from '@angular/core/testing';

import { FoundationPage } from './foundation-page';

describe('FoundationPage', () => {
  it('states that product functionality has not migrated yet', async () => {
    const fixture = TestBed.createComponent(FoundationPage);
    await fixture.whenStable();

    expect((fixture.nativeElement as HTMLElement).textContent).toContain(
      'nie zastępuje jeszcze działającej mapy',
    );
  });
});
