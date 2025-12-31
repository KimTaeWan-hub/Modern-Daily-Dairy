import api from '../api';
import { DailyStats, MonthlyStats, CategoryStats } from '../types';

export const statsApi = {
  daily: async (params?: {
    start_date?: string;
    end_date?: string;
  }): Promise<DailyStats[]> => {
    const response = await api.get<DailyStats[]>('/api/stats/daily', { params });
    return response.data;
  },

  monthly: async (params?: {
    year?: number;
    month?: number;
  }): Promise<MonthlyStats[]> => {
    const response = await api.get<MonthlyStats[]>('/api/stats/monthly', { params });
    return response.data;
  },

  category: async (params?: {
    start_date?: string;
    end_date?: string;
    transaction_type?: 'income' | 'expense';
  }): Promise<CategoryStats[]> => {
    const response = await api.get<CategoryStats[]>('/api/stats/category', { params });
    return response.data;
  },
};

