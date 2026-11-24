import { HttpClient } from '@angular/common/http';
import { inject, Service } from '@angular/core';
import { map, Observable } from 'rxjs';
import { LoginRequest, toUser, User, UserApiResponse } from './user';

@Service()
export class AuthApi {
  private readonly http = inject(HttpClient);

  me(): Observable<User> {
    return this.http.get<UserApiResponse>('/api/auth/me/').pipe(map(toUser));
  }

  csrf(): Observable<void> {
    return this.http.get<void>('/api/auth/csrf/');
  }

  login(request: LoginRequest): Observable<User> {
    return this.http.post<UserApiResponse>('/api/auth/login/', request).pipe(map(toUser));
  }

  logout(): Observable<void> {
    return this.http.post<void>('/api/auth/logout/', {});
  }
}
