import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./features/auth/pages/login/login').then((m) => m.Login),
  },
  {
    path: 'applications',
    loadComponent: () =>
      import('./features/applications/pages/application-list/application-list').then(
        (m) => m.ApplicationList,
      ),
  },
  { path: '', redirectTo: 'applications', pathMatch: 'full' },
];
