import api from '../api';
import { LoginRequest, SignupRequest, AuthResponse } from '../types';

export const authApi = {
  signup: async (data: SignupRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/signup', data);
    return response.data;
  },

  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/login', data);
    return response.data;
  },

  me: async (): Promise<{ user: any }> => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

