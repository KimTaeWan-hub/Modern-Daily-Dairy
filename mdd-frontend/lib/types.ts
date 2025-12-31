// 사용자 타입
export interface User {
  id: string;
  email: string;
  username: string;
  created_at: string;
}

// 인증 관련
export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// 일상 기록
export interface Entry {
  id: string;
  user_id: string;
  date: string;
  title?: string;
  content?: string;
  mood?: string;
  photos: string[];
  tags: string[];
  created_at: string;
  updated_at?: string;
}

export interface EntryCreate {
  date: string;
  title?: string;
  content?: string;
  mood?: string;
  photos?: string[];
  tags?: string[];
}

// 경제 기록
export type TransactionType = 'income' | 'expense';

export interface Transaction {
  id: string;
  entry_id?: string;
  user_id: string;
  date: string;
  type: TransactionType;
  category: string;
  amount: number;
  description?: string;
  payment_method?: string;
  created_at: string;
  updated_at?: string;
}

export interface TransactionCreate {
  date: string;
  type: TransactionType;
  category: string;
  amount: number;
  description?: string;
  payment_method?: string;
  entry_id?: string;
}

// 통합
export interface EntryWithTransactionsCreate {
  entry: EntryCreate;
  transactions: TransactionCreate[];
}

export interface EntryWithTransactions {
  entry: Entry;
  transactions: Transaction[];
}

// 통계
export interface DailyStats {
  date: string;
  total_income: number;
  total_expense: number;
  net: number;
}

export interface MonthlyStats {
  year: number;
  month: number;
  total_income: number;
  total_expense: number;
  net: number;
  transaction_count: number;
}

export interface CategoryStats {
  category: string;
  total_amount: number;
  transaction_count: number;
  percentage: number;
}

