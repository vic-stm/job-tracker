export interface UserApiResponse {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
}

export function toUser({ id, username, email, first_name, last_name }: UserApiResponse): User {
  return {
    id,
    username,
    email,
    firstName: first_name,
    lastName: last_name,
  };
}

export interface LoginRequest {
  username: string;
  password: string;
}
