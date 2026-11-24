import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { form, FormField, FormRoot, required } from '@angular/forms/signals';
import { Router } from '@angular/router';
import { AuthStore } from '../../../../core/auth/auth-store';
import { LoginRequest } from '../../../../core/auth/user';

@Component({
  imports: [FormRoot, FormField],
  selector: 'app-login',
  styleUrl: './login.scss',
  templateUrl: './login.html',
})
export class Login {
  private readonly authStore = inject(AuthStore);
  private readonly router = inject(Router);

  protected readonly model = signal<LoginRequest>({ username: '', password: '' });

  protected readonly loginError = signal<string | null>(null);

  protected readonly loginForm = form(
    this.model,
    (path) => {
      required(path.username, { message: $localize`Username is required` });
      required(path.password, { message: $localize`Password is required` });
    },
    {
      submission: {
        action: async (field) => {
          this.loginError.set(null);
          try {
            await this.authStore.login(field().value());
          } catch (error) {
            const message = this.toLoginErrorMessage(error);
            if (message === null) throw error;
            this.loginError.set(message);
            return;
          }
          await this.router.navigate(['/applications']);
        },
        onInvalid: (field) => {
          const firstError = field().errorSummary()[0];
          firstError?.fieldTree().focusBoundControl();
        },
      },
    },
  );

  private toLoginErrorMessage(error: unknown): string | null {
    if (error instanceof HttpErrorResponse) {
      if (error.status === 400) {
        return $localize`Invalid username or password`;
      }
      if (error.status === 429) {
        const seconds = error.headers.get('Retry-After');
        return seconds
          ? $localize`Too many attempts. Try again in ${seconds}:seconds: seconds.`
          : $localize`Too many attempts. Try again later.`;
      }
    }
    return null;
  }
}
