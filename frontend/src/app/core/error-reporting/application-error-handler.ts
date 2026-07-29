import { ErrorHandler, Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ApplicationErrorHandler implements ErrorHandler {
  readonly hasUnhandledError = signal(false);

  handleError(error: unknown): void {
    this.hasUnhandledError.set(true);
    console.error('[Geo Planner] Unhandled application error', error);
  }
}
