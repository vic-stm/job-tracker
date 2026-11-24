import { Component, inject } from '@angular/core';
import { AuthStore } from './core/auth/auth-store';

@Component({
  selector: 'app-root',
  styleUrl: './app.scss',
  templateUrl: './app.html',
})
export class App {
  protected readonly authStore = inject(AuthStore);
}
