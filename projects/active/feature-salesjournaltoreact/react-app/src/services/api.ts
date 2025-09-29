// GraniteRock Sales Journal - API Service Layer
// Enterprise-grade data access with PostgreSQL, Snowflake, and REST APIs

import { JournalEntry, FilterState, OutOfBalanceData, APIResponse, QueryResult } from '../types/financial';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';
const API_TIMEOUT = 30000; // 30 seconds

// Authentication token management
let authToken: string | null = null;

/**
 * Set authentication token for API requests
 */
export const setAuthToken = (token: string): void => {
  authToken = token;
};

/**
 * Clear authentication token
 */
export const clearAuthToken = (): void => {
  authToken = null;
};

/**
 * Generic API request wrapper with error handling
 */
const apiRequest = async <T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (authToken) {
    defaultHeaders['Authorization'] = `Bearer ${authToken}`;
  }

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  // Add timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const response = await fetch(url, {
      ...config,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    clearTimeout(timeoutId);

    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timeout - please try again');
    }

    throw error;
  }
};

/**
 * Build WHERE conditions and parameters from filters
 */
const buildWhereConditions = (filters: FilterState): { where: string; params: Record<string, any> } => {
  const conditions: string[] = [];
  const params: Record<string, any> = {};

  // Batch type filter
  if (filters.shared_batch_type && filters.shared_batch_type !== 'All' as any) {
    conditions.push('batch_type = $batch_type');
    params.batch_type = filters.shared_batch_type;
  }

  // Proof mode filter
  if (filters.shared_is_proof && filters.shared_is_proof !== 'All' as any) {
    conditions.push('is_proof = $is_proof');
    params.is_proof = filters.shared_is_proof;
  }

  // Batch ID filter
  if (filters.shared_batch_id && filters.shared_batch_id !== 'All') {
    conditions.push('batch_id = $batch_id');
    params.batch_id = filters.shared_batch_id;
  }

  // Invalid account filter
  if (filters.shared_invalid_account && filters.shared_invalid_account !== 'All') {
    conditions.push('error = $invalid_account');
    params.invalid_account = filters.shared_invalid_account;
  }

  // Branch ID filter
  if (filters.shared_branch_id && filters.shared_branch_id !== 'All') {
    conditions.push('branch_id = $branch_id');
    params.branch_id = filters.shared_branch_id;
  }

  return {
    where: conditions.length > 0 ? conditions.join(' AND ') : '',
    params,
  };
};

/**
 * Query financial journal data from database
 */
export const queryFinancialData = async (filters: FilterState): Promise<JournalEntry[]> => {
  try {
    const { where, params } = buildWhereConditions(filters);

    const response = await apiRequest<APIResponse<QueryResult<JournalEntry>>>('/journal/data', {
      method: 'POST',
      body: JSON.stringify({
        query: {
          table: 'dbt_dev_accounting.dash_r245a_apex_sales_journal_review_summary',
          select: [
            'accountcode_adjusted',
            'batch_type',
            'error as invalid_acount',
            'SUM(account_entry_qty) AS account_entry_qty',
            'SUM(amount) AS amount'
          ],
          where,
          groupBy: ['accountcode_adjusted', 'batch_type', 'error'],
          orderBy: ['error', 'accountcode_adjusted'],
        },
        params,
      }),
    });

    if (!response.success) {
      throw new Error(response.error || 'Failed to fetch journal data');
    }

    return response.data.data;
  } catch (error) {
    console.error('Error querying financial data:', error);
    throw error;
  }
};

/**
 * Query out of balance data
 */
export const queryOutOfBalanceData = async (filters: FilterState): Promise<OutOfBalanceData> => {
  try {
    // Only query if proof mode is enabled
    if (filters.shared_is_proof !== 'Y') {
      return { total: 0, color: 'success', status: 'Not applicable (Proof mode disabled)' };
    }

    const { where, params } = buildWhereConditions(filters);

    const response = await apiRequest<APIResponse<{ total: number; status: string }>>('/journal/out-of-balance', {
      method: 'POST',
      body: JSON.stringify({
        query: {
          table: 'dbt_dev_accounting.dash_r245a_apex_sales_journal_review_summary',
          where,
        },
        params,
      }),
    });

    if (!response.success) {
      throw new Error(response.error || 'Failed to fetch out of balance data');
    }

    const { total, status } = response.data;

    // Determine color based on amount
    let color: 'success' | 'warning' | 'error' = 'success';
    if (Math.abs(total) > 100) {
      color = 'error';
    } else if (Math.abs(total) > 10) {
      color = 'warning';
    }

    return { total, color, status };
  } catch (error) {
    console.error('Error querying out of balance data:', error);
    throw error;
  }
};

/**
 * Query batch ID options for dropdown
 */
export const queryBatchOptions = async (batchType: string, isProof: string): Promise<string[]> => {
  try {
    const response = await apiRequest<APIResponse<string[]>>('/journal/batch-options', {
      method: 'POST',
      body: JSON.stringify({
        batch_type: batchType,
        is_proof: isProof,
      }),
    });

    if (!response.success) {
      throw new Error(response.error || 'Failed to fetch batch options');
    }

    return ['All', ...response.data];
  } catch (error) {
    console.error('Error querying batch options:', error);
    throw error;
  }
};

/**
 * Query invalid account options for dropdown
 */
export const queryInvalidAccountOptions = async (
  batchType: string,
  isProof: string,
  batchId: string
): Promise<string[]> => {
  try {
    const response = await apiRequest<APIResponse<string[]>>('/journal/invalid-account-options', {
      method: 'POST',
      body: JSON.stringify({
        batch_type: batchType,
        is_proof: isProof,
        batch_id: batchId,
      }),
    });

    if (!response.success) {
      throw new Error(response.error || 'Failed to fetch invalid account options');
    }

    return ['All', ...response.data];
  } catch (error) {
    console.error('Error querying invalid account options:', error);
    throw error;
  }
};

/**
 * Query branch ID options for dropdown
 */
export const queryBranchOptions = async (batchType: string): Promise<string[]> => {
  try {
    const response = await apiRequest<APIResponse<string[]>>('/journal/branch-options', {
      method: 'POST',
      body: JSON.stringify({
        batch_type: batchType,
      }),
    });

    if (!response.success) {
      throw new Error(response.error || 'Failed to fetch branch options');
    }

    return ['All', ...response.data];
  } catch (error) {
    console.error('Error querying branch options:', error);
    throw error;
  }
};

/**
 * Get Orchestra authentication token
 */
export const getOrchestraToken = async (): Promise<string> => {
  try {
    const response = await apiRequest<APIResponse<{ token: string; expires_at: string }>>('/auth/orchestra-token', {
      method: 'POST',
    });

    if (!response.success) {
      throw new Error(response.error || 'Failed to get Orchestra token');
    }

    const { token } = response.data;
    setAuthToken(token);
    return token;
  } catch (error) {
    console.error('Error getting Orchestra token:', error);
    throw error;
  }
};

/**
 * Trigger pipeline execution
 */
export const triggerPipeline = async (pipelineId: string, pipelineType: string): Promise<{ run_id: string }> => {
  try {
    const response = await apiRequest<APIResponse<{ run_id: string }>>('/pipeline/trigger', {
      method: 'POST',
      body: JSON.stringify({
        pipeline_id: pipelineId,
        pipeline_type: pipelineType,
      }),
    });

    if (!response.success) {
      throw new Error(response.error || 'Failed to trigger pipeline');
    }

    return response.data;
  } catch (error) {
    console.error('Error triggering pipeline:', error);
    throw error;
  }
};

/**
 * Get pipeline status
 */
export const getPipelineStatus = async (runId: string): Promise<{ status: string; logs: string[] }> => {
  try {
    const response = await apiRequest<APIResponse<{ status: string; logs: string[] }>>(`/pipeline/status/${runId}`);

    if (!response.success) {
      throw new Error(response.error || 'Failed to get pipeline status');
    }

    return response.data;
  } catch (error) {
    console.error('Error getting pipeline status:', error);
    throw error;
  }
};

/**
 * Get pipeline execution history
 */
export const getPipelineHistory = async (
  pipelineIds: string[],
  limit: number = 10
): Promise<Array<{ run_id: string; status: string; started_at: string; completed_at?: string }>> => {
  try {
    const response = await apiRequest<APIResponse<Array<any>>>('/pipeline/history', {
      method: 'POST',
      body: JSON.stringify({
        pipeline_ids: pipelineIds,
        limit,
      }),
    });

    if (!response.success) {
      throw new Error(response.error || 'Failed to get pipeline history');
    }

    return response.data;
  } catch (error) {
    console.error('Error getting pipeline history:', error);
    throw error;
  }
};

/**
 * Test database connection
 */
export const testDatabaseConnection = async (): Promise<{ connected: boolean; message: string }> => {
  try {
    const response = await apiRequest<APIResponse<{ connected: boolean; message: string }>>('/health/database');

    return response.data;
  } catch (error) {
    console.error('Error testing database connection:', error);
    return { connected: false, message: 'Connection test failed' };
  }
};

/**
 * Get tieout status
 */
export const getTieoutStatus = async (): Promise<{ emoji: string; status: string }> => {
  try {
    const response = await apiRequest<APIResponse<{ emoji: string; status: string }>>('/tieout/status');

    if (!response.success) {
      throw new Error(response.error || 'Failed to get tieout status');
    }

    return response.data;
  } catch (error) {
    console.error('Error getting tieout status:', error);
    // Return fallback status
    return { emoji: '⚠️', status: 'Status unavailable' };
  }
};

/**
 * Health check endpoint
 */
export const healthCheck = async (): Promise<{ status: string; version: string; timestamp: string }> => {
  try {
    const response = await apiRequest<{ status: string; version: string; timestamp: string }>('/health');
    return response;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

// Development/Demo mode - Mock API responses when backend is not available
if (process.env.NODE_ENV === 'development') {
  // Override API functions with mock implementations for development
  const originalQueryFinancialData = queryFinancialData;

  // Mock financial data generator
  const generateMockData = (filters: FilterState): JournalEntry[] => {
    const accountCodes = [
      '1100-Cash',
      '1200-Receivables',
      '4000-Sales',
      '5000-COGS',
      '6000-Expenses',
      '1300-Inventory'
    ];

    const data: JournalEntry[] = [];
    const count = Math.floor(Math.random() * 50) + 20; // 20-70 records

    for (let i = 0; i < count; i++) {
      data.push({
        accountcode_adjusted: accountCodes[Math.floor(Math.random() * accountCodes.length)],
        batch_type: (filters.shared_batch_type === 'All' as any) ?
          (['CASH', 'CREDIT', 'INTRA'] as const)[Math.floor(Math.random() * 3)] :
          filters.shared_batch_type,
        invalid_acount: Math.random() > 0.85 ? 'Y' : 'N', // 15% invalid
        account_entry_qty: Math.floor(Math.random() * 100) + 1,
        amount: Math.round((Math.random() * 50000 + 500) * 100) / 100,
      });
    }

    return data;
  };

  // Override functions to use mock data when API fails
  (window as any).mockApiEnabled = true;
}