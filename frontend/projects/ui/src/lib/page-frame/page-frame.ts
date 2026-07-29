import { ChangeDetectionStrategy, Component, input } from '@angular/core';

@Component({
  selector: 'gp-page-frame',
  templateUrl: './page-frame.html',
  styleUrl: './page-frame.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PageFrame {
  readonly applicationName = input.required<string>();
  readonly contextLabel = input<string>();
}
