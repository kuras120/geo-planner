import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PageFrame } from 'ui';

import { ApplicationErrorHandler } from './core/error-reporting/application-error-handler';

@Component({
  selector: 'app-root',
  imports: [PageFrame, RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App {
  protected readonly errorHandler = inject(ApplicationErrorHandler);
}
