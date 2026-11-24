import { computed, inject } from '@angular/core';
import { patchState, signalStore, withComputed, withMethods, withState } from '@ngrx/signals';
import { firstValueFrom } from 'rxjs';
import { AuthApi } from './auth-api';
import { LoginRequest, User } from './user';

type AuthState = { user: User | null };

const initialState: AuthState = { user: null };

export const AuthStore = signalStore(
  { providedIn: 'root' },
  withState(initialState),
  withComputed(({ user }) => ({
    isAuthenticated: computed(() => user() !== null),
  })),
  withMethods((store, authApi = inject(AuthApi)) => ({
    async init(): Promise<void> {
      await firstValueFrom(authApi.csrf());
      try {
        const user = await firstValueFrom(authApi.me());
        patchState(store, { user });
      } catch {
        patchState(store, { user: null });
      }
    },
    async login(request: LoginRequest): Promise<void> {
      const user = await firstValueFrom(authApi.login(request));
      patchState(store, { user });
    },
    async logout(): Promise<void> {
      await firstValueFrom(authApi.logout());
      patchState(store, { user: null });
    },
  })),
);
