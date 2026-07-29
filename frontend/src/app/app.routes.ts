import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./features/foundation/foundation-page').then(({ FoundationPage }) => FoundationPage),
    title: 'Geo Planner — fundament aplikacji',
  },
  {
    path: '**',
    redirectTo: '',
  },
];
