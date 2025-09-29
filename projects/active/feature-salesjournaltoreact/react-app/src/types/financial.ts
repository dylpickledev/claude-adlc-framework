// GraniteRock Sales Journal - Type Definitions
// Premium Financial Application with Enterprise-Grade Type Safety

export interface JournalEntry {
  accountcode_adjusted: string;
  batch_type: 'CASH' | 'CREDIT' | 'INTRA';
  invalid_acount: 'Y' | 'N';
  account_entry_qty: number;
  amount: number;
}

export interface FilterState {
  shared_batch_type: 'CASH' | 'CREDIT' | 'INTRA';
  shared_is_proof: 'Y' | 'N';
  shared_batch_id: string;
  shared_invalid_account: string;
  shared_branch_id?: string;
}

export interface PipelineStatus {
  pipeline_run_id: string;
  pipeline_id: string;
  pipeline_type: string;
  status: 'running' | 'completed' | 'failed' | 'pending';
  created_at: string;
  updated_at: string;
  duration?: number;
}

export interface OutOfBalanceData {
  total: number;
  color: 'success' | 'warning' | 'error';
  status: string;
}

export interface TieoutStatus {
  emoji: string;
  status: string;
  timestamp: number;
}

export interface NavigationTab {
  id: string;
  label: string;
  icon: string;
  component: string;
  enabled: boolean;
}

export interface ExportOptions {
  format: 'pdf' | 'excel' | 'csv';
  includeFilters: boolean;
  includeCharts: boolean;
  dateRange?: {
    start: Date;
    end: Date;
  };
}

export interface DatabaseConnection {
  host: string;
  port: number;
  database: string;
  user: string;
  connection_timeout: number;
  max_retries: number;
}

export interface QueryResult<T = any> {
  data: T[];
  total_count: number;
  execution_time: number;
  success: boolean;
  error?: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'viewer';
  permissions: string[];
}

export interface APIResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
  timestamp: string;
}

// Chart data types for financial visualizations
export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
  metadata?: Record<string, any>;
}

export interface FinancialMetric {
  title: string;
  value: number | string;
  delta?: number;
  deltaType?: 'positive' | 'negative' | 'neutral';
  format: 'currency' | 'number' | 'percentage';
  trend?: ChartDataPoint[];
}