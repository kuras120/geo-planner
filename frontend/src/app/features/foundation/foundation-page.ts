import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-foundation-page',
  templateUrl: './foundation-page.html',
  styleUrl: './foundation-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FoundationPage {}
