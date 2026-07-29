import {
  ApplicationConfig,
  ErrorHandler,
  inject,
  provideAppInitializer,
  provideBrowserGlobalErrorListeners,
} from '@angular/core';
import { provideRouter } from '@angular/router';

import { ApplicationErrorHandler } from './core/error-reporting/application-error-handler';
import { RuntimeConfigService } from './core/runtime-config/runtime-config';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    {
      provide: ErrorHandler,
      useExisting: ApplicationErrorHandler,
    },
    provideAppInitializer(() => inject(RuntimeConfigService).load()),
  ],
};
