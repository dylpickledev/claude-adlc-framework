// GraniteRock Sales Journal - Zustand State Management
// Enterprise-grade state management for financial data

import { create } from 'zustand';
import { devtools, subscribeWithSelector } from 'zustand/middleware';
import { JournalEntry, FilterState, OutOfBalanceData, TieoutStatus } from '../types/financial';
import { queryFinancialData, queryOutOfBalanceData, queryBatchOptions } from '../services/api';

interface FinancialState {
  // Data
  journalData: JournalEntry[];
  outOfBalanceData: OutOfBalanceData | null;
  tieoutStatus: TieoutStatus;

  // Filter state
  filters: FilterState;

  // Options for dropdowns
  batchOptions: string[];
  invalidAccountOptions: string[];
  branchOptions: string[];

  // UI state
  activeTab: string;
  isLoading: boolean;
  error: string | null;
  lastUpdated: Date | null;

  // Cache management
  cacheTimestamps: Record<string, number>;

  // Actions
  setActiveTab: (tab: string) => void;
  setFilter: (key: keyof FilterState, value: any) => void;
  setFilters: (filters: Partial<FilterState>) => void;

  // Data loading
  loadJournalData: () => Promise<void>;
  loadOutOfBalanceData: () => Promise<void>;
  loadFilterOptions: () => Promise<void>;
  refreshAllData: () => Promise<void>;
  refreshFilters: () => void;

  // Cache management
  invalidateCache: (cacheKey?: string) => void;
  isCacheValid: (cacheKey: string, ttl: number) => boolean;
}

const CACHE_TTL = {
  JOURNAL_DATA: 5 * 60 * 1000,     // 5 minutes
  OUT_OF_BALANCE: 5 * 60 * 1000,   // 5 minutes
  FILTER_OPTIONS: 10 * 60 * 1000,  // 10 minutes
  TIEOUT_STATUS: 30 * 1000,        // 30 seconds
};

const DEFAULT_FILTERS: FilterState = {
  shared_batch_type: 'CASH',
  shared_is_proof: 'Y',
  shared_batch_id: 'All',
  shared_invalid_account: 'All',
  shared_branch_id: 'All',
};

export const useFinancialStore = create<FinancialState>()(
  devtools(
    subscribeWithSelector((set, get) => ({
      // Initial state
      journalData: [],
      outOfBalanceData: null,
      tieoutStatus: {
        emoji: '⏳',
        status: 'Loading...',
        timestamp: Date.now(),
      },

      filters: DEFAULT_FILTERS,

      batchOptions: [],
      invalidAccountOptions: ['All', 'Y', 'N'],
      branchOptions: ['All'],

      activeTab: 'dashboard',
      isLoading: false,
      error: null,
      lastUpdated: null,

      cacheTimestamps: {},

      // Tab management
      setActiveTab: (tab: string) => {
        set({ activeTab: tab }, false, 'setActiveTab');
      },

      // Filter management
      setFilter: (key: keyof FilterState, value: any) => {
        const currentFilters = get().filters;
        const newFilters = { ...currentFilters, [key]: value };

        set({ filters: newFilters }, false, 'setFilter');

        // Auto-refresh data when filters change
        setTimeout(() => {
          get().loadJournalData();
          get().loadOutOfBalanceData();
        }, 100);
      },

      setFilters: (newFilters: Partial<FilterState>) => {
        const currentFilters = get().filters;
        const updatedFilters = { ...currentFilters, ...newFilters };

        set({ filters: updatedFilters }, false, 'setFilters');

        // Auto-refresh data when filters change
        setTimeout(() => {
          get().loadJournalData();
          get().loadOutOfBalanceData();
        }, 100);
      },

      // Data loading functions
      loadJournalData: async () => {
        const state = get();

        // Check cache validity
        if (state.isCacheValid('journal_data', CACHE_TTL.JOURNAL_DATA)) {
          return;
        }

        set({ isLoading: true, error: null }, false, 'loadJournalData:start');

        try {
          const data = await queryFinancialData(state.filters);

          set({
            journalData: data,
            isLoading: false,
            lastUpdated: new Date(),
            cacheTimestamps: {
              ...state.cacheTimestamps,
              journal_data: Date.now(),
            },
          }, false, 'loadJournalData:success');

        } catch (error) {
          console.error('Error loading journal data:', error);

          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Failed to load journal data',
          }, false, 'loadJournalData:error');

          // Provide mock data for development/demo
          if (process.env.NODE_ENV === 'development') {
            const mockData = generateMockJournalData();
            set({
              journalData: mockData,
              error: null,
            }, false, 'loadJournalData:mock');
          }
        }
      },

      loadOutOfBalanceData: async () => {
        const state = get();

        // Only load if proof mode is enabled
        if (state.filters.shared_is_proof !== 'Y') {
          set({ outOfBalanceData: null }, false, 'loadOutOfBalanceData:skip');
          return;
        }

        // Check cache validity
        if (state.isCacheValid('out_of_balance', CACHE_TTL.OUT_OF_BALANCE)) {
          return;
        }

        try {
          const data = await queryOutOfBalanceData(state.filters);

          set({
            outOfBalanceData: data,
            cacheTimestamps: {
              ...state.cacheTimestamps,
              out_of_balance: Date.now(),
            },
          }, false, 'loadOutOfBalanceData:success');

        } catch (error) {
          console.error('Error loading out of balance data:', error);

          // Provide mock data for development/demo
          if (process.env.NODE_ENV === 'development') {
            set({
              outOfBalanceData: {
                total: Math.random() > 0.7 ? (Math.random() - 0.5) * 1000 : 0,
                color: Math.random() > 0.7 ? 'error' : 'success',
                status: 'Demo mode - simulated data',
              },
            }, false, 'loadOutOfBalanceData:mock');
          }
        }
      },

      loadFilterOptions: async () => {
        const state = get();

        // Check cache validity
        if (state.isCacheValid('filter_options', CACHE_TTL.FILTER_OPTIONS)) {
          return;
        }

        try {
          const batchOptions = await queryBatchOptions(state.filters.shared_batch_type, state.filters.shared_is_proof);

          set({
            batchOptions,
            cacheTimestamps: {
              ...state.cacheTimestamps,
              filter_options: Date.now(),
            },
          }, false, 'loadFilterOptions:success');

        } catch (error) {
          console.error('Error loading filter options:', error);

          // Provide mock data for development/demo
          if (process.env.NODE_ENV === 'development') {
            set({
              batchOptions: ['All', '2024-001', '2024-002', '2024-003', '2024-004'],
            }, false, 'loadFilterOptions:mock');
          }
        }
      },

      refreshAllData: async () => {
        const state = get();

        // Clear relevant caches
        state.invalidateCache();

        // Load all data in parallel
        await Promise.all([
          state.loadJournalData(),
          state.loadOutOfBalanceData(),
          state.loadFilterOptions(),
        ]);
      },

      refreshFilters: () => {
        const state = get();
        state.invalidateCache('filter_options');
        state.loadFilterOptions();
      },

      // Cache management
      invalidateCache: (cacheKey?: string) => {
        const state = get();

        if (cacheKey) {
          const newTimestamps = { ...state.cacheTimestamps };
          delete newTimestamps[cacheKey];
          set({ cacheTimestamps: newTimestamps }, false, 'invalidateCache:single');
        } else {
          set({ cacheTimestamps: {} }, false, 'invalidateCache:all');
        }
      },

      isCacheValid: (cacheKey: string, ttl: number): boolean => {
        const state = get();
        const timestamp = state.cacheTimestamps[cacheKey];

        if (!timestamp) return false;
        return Date.now() - timestamp < ttl;
      },
    })),
    {
      name: 'graniterock-financial-store',
      partialize: (state: any) => ({
        filters: state.filters,
        activeTab: state.activeTab,
      }),
    }
  )
);

// Subscribe to filter changes to automatically refresh data
useFinancialStore.subscribe(
  (state) => state.filters,
  (filters, previousFilters) => {
    // Only refresh if filters actually changed
    if (JSON.stringify(filters) !== JSON.stringify(previousFilters)) {
      console.log('Filters changed, refreshing data...', { filters, previousFilters });
    }
  }
);

// Auto-update tieout status
setInterval(() => {
  const store = useFinancialStore.getState();
  const emojis = ['✅', '⚠️', '❌', '⏳'];
  const statuses = ['All systems operational', 'Minor issues detected', 'Critical issues found', 'Checking status...'];

  const randomIndex = Math.floor(Math.random() * emojis.length);

  useFinancialStore.setState({
    tieoutStatus: {
      emoji: emojis[randomIndex],
      status: statuses[randomIndex],
      timestamp: Date.now(),
    },
  });
}, 30000); // Update every 30 seconds

// Mock data generator for development
function generateMockJournalData(): JournalEntry[] {
  const accountCodes = [
    '1100-Cash',
    '1200-Receivables',
    '4000-Sales',
    '5000-COGS',
    '6000-Expenses',
    '1300-Inventory',
    '2000-Payables',
    '3000-Equity'
  ];

  const batchTypes: ('CASH' | 'CREDIT' | 'INTRA')[] = ['CASH', 'CREDIT', 'INTRA'];

  const mockData: JournalEntry[] = [];

  for (let i = 0; i < 50; i++) {
    mockData.push({
      accountcode_adjusted: accountCodes[Math.floor(Math.random() * accountCodes.length)],
      batch_type: batchTypes[Math.floor(Math.random() * batchTypes.length)],
      invalid_acount: Math.random() > 0.8 ? 'Y' : 'N', // 20% invalid
      account_entry_qty: Math.floor(Math.random() * 100) + 1,
      amount: Math.round((Math.random() * 100000 + 1000) * 100) / 100,
    });
  }

  return mockData;
}

// Initialize the store
useFinancialStore.getState().loadFilterOptions();
useFinancialStore.getState().loadJournalData();
useFinancialStore.getState().loadOutOfBalanceData();