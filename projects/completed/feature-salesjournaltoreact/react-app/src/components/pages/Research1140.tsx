// GraniteRock Sales Journal - 1140 Research Page
// Premium account research and analysis tools

import React, { useState, useEffect, useMemo } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useFinancialStore } from '../../store/financialStore';
import { formatCurrency, formatNumber, formatDate, downloadCSV } from '../../utils/formatters';

const PageContainer = styled(motion.div)`
  padding: ${({ theme }) => theme.spacing[6]};
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);

  @media (max-width: ${({ theme }) => theme.breakpoints.lg}) {
    padding: ${({ theme }) => theme.spacing[4]};
  }
`;

const PageHeader = styled.div`
  margin-bottom: ${({ theme }) => theme.spacing[8]};

  .page-title {
    font-size: ${({ theme }) => theme.typography.fontSizes['3xl']};
    font-weight: ${({ theme }) => theme.typography.fontWeights.black};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
    margin-bottom: ${({ theme }) => theme.spacing[2]};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[3]};
  }

  .page-subtitle {
    font-size: ${({ theme }) => theme.typography.fontSizes.lg};
    color: ${({ theme }) => theme.colors.primary.darkGray};
    line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
  }
`;

const ResearchContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: ${({ theme }) => theme.spacing[6]};
  margin-bottom: ${({ theme }) => theme.spacing[8]};

  @media (max-width: ${({ theme }) => theme.breakpoints.lg}) {
    grid-template-columns: 1fr;
  }
`;

const SearchPanel = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};

  .panel-title {
    font-size: ${({ theme }) => theme.typography.fontSizes.xl};
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[2]};
  }

  .search-form {
    display: flex;
    flex-direction: column;
    gap: ${({ theme }) => theme.spacing[4]};
  }
`;

const FilterPanel = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};

  .panel-title {
    font-size: ${({ theme }) => theme.typography.fontSizes.xl};
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[2]};
  }

  .filter-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: ${({ theme }) => theme.spacing[4]};
  }
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing[2]};

  label {
    font-size: ${({ theme }) => theme.typography.fontSizes.sm};
    font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
  }

  input, select {
    padding: ${({ theme }) => theme.spacing[3]};
    border: 2px solid ${({ theme }) => theme.colors.primary.lightCyan};
    border-radius: ${({ theme }) => theme.borderRadius.lg};
    font-size: ${({ theme }) => theme.typography.fontSizes.base};
    font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
    transition: all ${({ theme }) => theme.animations.transitions.base};

    &:focus {
      outline: none;
      border-color: ${({ theme }) => theme.colors.primary.darkGreen};
      box-shadow: 0 0 0 3px ${({ theme }) => theme.colors.primary.darkGreen}20;
    }
  }

  .help-text {
    font-size: ${({ theme }) => theme.typography.fontSizes.xs};
    color: ${({ theme }) => theme.colors.primary.grayGreen};
    line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
  }
`;

const ActionButton = styled(motion.button)<{ variant?: 'primary' | 'secondary' }>`
  background: ${({ variant, theme }) =>
    variant === 'secondary'
      ? `linear-gradient(135deg, ${theme.colors.primary.grayGreen} 0%, ${theme.colors.primary.lightCyan} 100%)`
      : `linear-gradient(135deg, ${theme.colors.primary.darkGreen} 0%, ${theme.colors.primary.mediumGreen} 100%)`
  };
  color: ${({ variant, theme }) => variant === 'secondary' ? theme.colors.primary.darkGreen : 'white'};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius.lg};
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[6]};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  cursor: pointer;
  transition: all ${({ theme }) => theme.animations.transitions.base};
  width: 100%;

  &:hover {
    transform: translateY(-2px);
    box-shadow: ${({ theme }) => theme.shadows.lg};
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const ResultsContainer = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  overflow: hidden;

  .results-header {
    background: linear-gradient(135deg, ${({ theme }) => theme.colors.primary.darkGreen} 0%, ${({ theme }) => theme.colors.primary.mediumGreen} 100%);
    color: white;
    padding: ${({ theme }) => theme.spacing[6]};
    display: flex;
    justify-content: space-between;
    align-items: center;

    .results-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.xl};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    }

    .results-count {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      opacity: 0.9;
    }
  }
`;

const ResultsTable = styled.div`
  overflow-x: auto;
  max-height: 500px;
  overflow-y: auto;

  table {
    width: 100%;
    border-collapse: collapse;

    th {
      background: ${({ theme }) => theme.colors.primary.lightCyan};
      padding: ${({ theme }) => theme.spacing[4]};
      text-align: left;
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
      border-bottom: 2px solid ${({ theme }) => theme.colors.primary.darkGreen};
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      position: sticky;
      top: 0;
      z-index: 1;
    }

    td {
      padding: ${({ theme }) => theme.spacing[4]};
      border-bottom: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
      font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};

      &.currency {
        text-align: right;
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      }

      &.account-code {
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        color: ${({ theme }) => theme.colors.primary.darkGreen};
      }

      &.date {
        font-family: ${({ theme }) => theme.typography.fontFamilies.primary};
      }
    }

    tr:hover {
      background: ${({ theme }) => theme.colors.primary.lightCyan}50;
    }
  }
`;

const SummaryMetrics = styled.div`
  padding: ${({ theme }) => theme.spacing[6]};
  border-top: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  background: ${({ theme }) => theme.colors.primary.lightCyan}20;

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: ${({ theme }) => theme.spacing[4]};
  }

  .metric-item {
    text-align: center;
    padding: ${({ theme }) => theme.spacing[3]};
    background: white;
    border-radius: ${({ theme }) => theme.borderRadius.lg};
    box-shadow: ${({ theme }) => theme.shadows.sm};

    .metric-value {
      font-size: ${({ theme }) => theme.typography.fontSizes.xl};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
      font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
      margin-bottom: ${({ theme }) => theme.spacing[1]};
    }

    .metric-label {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      color: ${({ theme }) => theme.colors.primary.darkGray};
    }
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: ${({ theme }) => theme.spacing[12]};
  color: ${({ theme }) => theme.colors.primary.darkGray};

  .empty-icon {
    font-size: 4rem;
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    opacity: 0.5;
  }

  .empty-title {
    font-size: ${({ theme }) => theme.typography.fontSizes.xl};
    font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
    margin-bottom: ${({ theme }) => theme.spacing[2]};
  }

  .empty-description {
    font-size: ${({ theme }) => theme.typography.fontSizes.base};
    line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
  }
`;

interface ResearchResult {
  account_code: string;
  transaction_date: string;
  description: string;
  reference_number: string;
  debit_amount: number;
  credit_amount: number;
  batch_id: string;
  branch_id: string;
}

export const Research1140: React.FC = () => {
  const { filters, isLoading } = useFinancialStore();
  const [searchCriteria, setSearchCriteria] = useState({
    accountCode: '1140',
    dateFrom: '',
    dateTo: '',
    referenceNumber: '',
    description: '',
    minAmount: '',
    maxAmount: '',
  });
  const [searchResults, setSearchResults] = useState<ResearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // Mock research data
  const mockResults: ResearchResult[] = [
    {
      account_code: '1140-Prepaid Insurance',
      transaction_date: '2024-01-15',
      description: 'Annual insurance premium payment',
      reference_number: 'INS-2024-001',
      debit_amount: 12000.00,
      credit_amount: 0,
      batch_id: 'CASH-20240115-001',
      branch_id: 'BR001',
    },
    {
      account_code: '1140-Prepaid Insurance',
      transaction_date: '2024-01-31',
      description: 'Monthly insurance amortization',
      reference_number: 'AMT-2024-001',
      debit_amount: 0,
      credit_amount: 1000.00,
      batch_id: 'ADJ-20240131-001',
      branch_id: 'BR001',
    },
    {
      account_code: '1140-Prepaid Maintenance',
      transaction_date: '2024-01-10',
      description: 'Equipment maintenance contract',
      reference_number: 'MNT-2024-003',
      debit_amount: 5000.00,
      credit_amount: 0,
      batch_id: 'CASH-20240110-002',
      branch_id: 'BR002',
    },
    {
      account_code: '1140-Prepaid Software',
      transaction_date: '2024-01-05',
      description: 'Software license renewal',
      reference_number: 'SFT-2024-001',
      debit_amount: 3600.00,
      credit_amount: 0,
      batch_id: 'CASH-20240105-001',
      branch_id: 'BR001',
    },
  ];

  const handleSearch = async () => {
    setIsSearching(true);
    setHasSearched(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Filter mock results based on search criteria
      let filteredResults = mockResults;

      if (searchCriteria.accountCode) {
        filteredResults = filteredResults.filter(result =>
          result.account_code.toLowerCase().includes(searchCriteria.accountCode.toLowerCase())
        );
      }

      if (searchCriteria.description) {
        filteredResults = filteredResults.filter(result =>
          result.description.toLowerCase().includes(searchCriteria.description.toLowerCase())
        );
      }

      if (searchCriteria.referenceNumber) {
        filteredResults = filteredResults.filter(result =>
          result.reference_number.toLowerCase().includes(searchCriteria.referenceNumber.toLowerCase())
        );
      }

      setSearchResults(filteredResults);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleExport = () => {
    if (searchResults.length > 0) {
      downloadCSV(searchResults as any, '1140-research-results');
    }
  };

  const summaryMetrics = useMemo(() => {
    if (!searchResults.length) return null;

    const totalDebits = searchResults.reduce((sum, result) => sum + result.debit_amount, 0);
    const totalCredits = searchResults.reduce((sum, result) => sum + result.credit_amount, 0);
    const netAmount = totalDebits - totalCredits;
    const uniqueAccounts = new Set(searchResults.map(result => result.account_code)).size;

    return {
      totalRecords: searchResults.length,
      totalDebits,
      totalCredits,
      netAmount,
      uniqueAccounts,
    };
  }, [searchResults]);

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <div className="page-title">
          🔍 1140 Account Research
        </div>
        <div className="page-subtitle">
          Advanced research tools for account 1140 (Prepaid Expenses) analysis.
          Search transaction history, analyze patterns, and export detailed reports.
        </div>
      </PageHeader>

      <ResearchContainer>
        <SearchPanel>
          <div className="panel-title">
            🎯 Search Criteria
          </div>
          <div className="search-form">
            <FormGroup>
              <label htmlFor="accountCode">Account Code</label>
              <input
                id="accountCode"
                type="text"
                placeholder="1140 (default)"
                value={searchCriteria.accountCode}
                onChange={(e) => setSearchCriteria(prev => ({ ...prev, accountCode: e.target.value }))}
              />
              <div className="help-text">
                Enter full account code or partial match (e.g., 1140, 1140-Insurance)
              </div>
            </FormGroup>

            <FormGroup>
              <label htmlFor="dateFrom">Date Range</label>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                <input
                  id="dateFrom"
                  type="date"
                  value={searchCriteria.dateFrom}
                  onChange={(e) => setSearchCriteria(prev => ({ ...prev, dateFrom: e.target.value }))}
                />
                <input
                  type="date"
                  value={searchCriteria.dateTo}
                  onChange={(e) => setSearchCriteria(prev => ({ ...prev, dateTo: e.target.value }))}
                />
              </div>
            </FormGroup>

            <FormGroup>
              <label htmlFor="referenceNumber">Reference Number</label>
              <input
                id="referenceNumber"
                type="text"
                placeholder="INS-2024-001"
                value={searchCriteria.referenceNumber}
                onChange={(e) => setSearchCriteria(prev => ({ ...prev, referenceNumber: e.target.value }))}
              />
            </FormGroup>

            <FormGroup>
              <label htmlFor="description">Description Contains</label>
              <input
                id="description"
                type="text"
                placeholder="insurance, maintenance, software"
                value={searchCriteria.description}
                onChange={(e) => setSearchCriteria(prev => ({ ...prev, description: e.target.value }))}
              />
            </FormGroup>

            <ActionButton
              onClick={handleSearch}
              disabled={isSearching}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {isSearching ? '🔍 Searching...' : '🔍 Search Transactions'}
            </ActionButton>
          </div>
        </SearchPanel>

        <FilterPanel>
          <div className="panel-title">
            ⚙️ Advanced Filters
          </div>
          <div className="filter-grid">
            <FormGroup>
              <label htmlFor="minAmount">Amount Range</label>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                <input
                  id="minAmount"
                  type="number"
                  placeholder="Min Amount"
                  value={searchCriteria.minAmount}
                  onChange={(e) => setSearchCriteria(prev => ({ ...prev, minAmount: e.target.value }))}
                />
                <input
                  type="number"
                  placeholder="Max Amount"
                  value={searchCriteria.maxAmount}
                  onChange={(e) => setSearchCriteria(prev => ({ ...prev, maxAmount: e.target.value }))}
                />
              </div>
            </FormGroup>

            <FormGroup>
              <label htmlFor="sortBy">Sort Results By</label>
              <select id="sortBy" defaultValue="date_desc">
                <option value="date_desc">Date (Newest First)</option>
                <option value="date_asc">Date (Oldest First)</option>
                <option value="amount_desc">Amount (Highest First)</option>
                <option value="amount_asc">Amount (Lowest First)</option>
                <option value="account">Account Code</option>
              </select>
            </FormGroup>

            <FormGroup>
              <label htmlFor="exportFormat">Export Format</label>
              <select id="exportFormat" defaultValue="csv">
                <option value="csv">CSV Spreadsheet</option>
                <option value="pdf">PDF Report</option>
                <option value="excel">Excel Workbook</option>
              </select>
            </FormGroup>

            <ActionButton
              variant="secondary"
              onClick={handleExport}
              disabled={!searchResults.length}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              📊 Export Results
            </ActionButton>
          </div>
        </FilterPanel>
      </ResearchContainer>

      {hasSearched && (
        <ResultsContainer>
          <div className="results-header">
            <div className="results-title">
              📋 Search Results
            </div>
            <div className="results-count">
              {searchResults.length} transaction{searchResults.length !== 1 ? 's' : ''} found
            </div>
          </div>

          {searchResults.length > 0 ? (
            <>
              <ResultsTable>
                <table>
                  <thead>
                    <tr>
                      <th>Account Code</th>
                      <th>Date</th>
                      <th>Description</th>
                      <th>Reference</th>
                      <th>Debit</th>
                      <th>Credit</th>
                      <th>Batch ID</th>
                    </tr>
                  </thead>
                  <tbody>
                    {searchResults.map((result, index) => (
                      <tr key={index}>
                        <td className="account-code">{result.account_code}</td>
                        <td className="date">{formatDate(result.transaction_date)}</td>
                        <td>{result.description}</td>
                        <td>{result.reference_number}</td>
                        <td className="currency">
                          {result.debit_amount > 0 ? formatCurrency(result.debit_amount) : '—'}
                        </td>
                        <td className="currency">
                          {result.credit_amount > 0 ? formatCurrency(result.credit_amount) : '—'}
                        </td>
                        <td>{result.batch_id}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </ResultsTable>

              {summaryMetrics && (
                <SummaryMetrics>
                  <div className="metrics-grid">
                    <div className="metric-item">
                      <div className="metric-value">{formatNumber(summaryMetrics.totalRecords)}</div>
                      <div className="metric-label">Total Records</div>
                    </div>
                    <div className="metric-item">
                      <div className="metric-value">{formatCurrency(summaryMetrics.totalDebits)}</div>
                      <div className="metric-label">Total Debits</div>
                    </div>
                    <div className="metric-item">
                      <div className="metric-value">{formatCurrency(summaryMetrics.totalCredits)}</div>
                      <div className="metric-label">Total Credits</div>
                    </div>
                    <div className="metric-item">
                      <div className="metric-value">{formatCurrency(summaryMetrics.netAmount)}</div>
                      <div className="metric-label">Net Amount</div>
                    </div>
                    <div className="metric-item">
                      <div className="metric-value">{formatNumber(summaryMetrics.uniqueAccounts)}</div>
                      <div className="metric-label">Unique Accounts</div>
                    </div>
                  </div>
                </SummaryMetrics>
              )}
            </>
          ) : (
            <EmptyState>
              <div className="empty-icon">🔍</div>
              <div className="empty-title">No Results Found</div>
              <div className="empty-description">
                No transactions match your search criteria. Try adjusting your filters or search terms.
              </div>
            </EmptyState>
          )}
        </ResultsContainer>
      )}
    </PageContainer>
  );
};