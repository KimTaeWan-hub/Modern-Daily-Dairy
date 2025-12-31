import api from '../api';
import {
  Entry,
  EntryCreate,
  EntryWithTransactionsCreate,
  EntryWithTransactions,
} from '../types';

export const entriesApi = {
  create: async (data: EntryCreate): Promise<Entry> => {
    const response = await api.post<Entry>('/api/entries', data);
    return response.data;
  },

  list: async (params?: {
    page?: number;
    page_size?: number;
    start_date?: string;
    end_date?: string;
  }): Promise<{ entries: Entry[]; total: number; page: number; page_size: number }> => {
    const response = await api.get('/api/entries', { params });
    return response.data;
  },

  get: async (id: string): Promise<Entry> => {
    const response = await api.get<Entry>(`/api/entries/${id}`);
    return response.data;
  },

  update: async (id: string, data: Partial<EntryCreate>): Promise<Entry> => {
    const response = await api.put<Entry>(`/api/entries/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/entries/${id}`);
  },

  createWithTransactions: async (
    data: EntryWithTransactionsCreate
  ): Promise<EntryWithTransactions> => {
    const response = await api.post<EntryWithTransactions>(
      '/api/entries/with-transactions',
      data
    );
    return response.data;
  },

  getFull: async (id: string): Promise<EntryWithTransactions> => {
    const response = await api.get<EntryWithTransactions>(`/api/entries/${id}/full`);
    return response.data;
  },
};

