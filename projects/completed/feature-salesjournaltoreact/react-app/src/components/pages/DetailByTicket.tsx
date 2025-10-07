// GraniteRock Sales Journal - Detail by Ticket Page
// Premium ticket-level transaction details with advanced filtering

import React, { useState, useEffect, useMemo } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useFinancialStore } from '../../store/financialStore';
import { formatCurrency, formatNumber, formatDate } from '../../utils/formatters';

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

const TicketSearchContainer = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  margin-bottom: ${({ theme }) => theme.spacing[6]};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};

  .search-header {
    font-size: ${({ theme }) => theme.typography.fontSizes.xl};
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
  }

  .search-form {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: ${({ theme }) => theme.spacing[4]};
    align-items: end;

    @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
      grid-template-columns: 1fr;
    }
  }
`;

const SearchInput = styled.input`
  width: 100%;
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

  &::placeholder {
    color: ${({ theme }) => theme.colors.primary.grayGreen};
  }
`;

const SearchButton = styled(motion.button)`
  background: linear-gradient(135deg, ${({ theme }) => theme.colors.primary.darkGreen} 0%, ${({ theme }) => theme.colors.primary.mediumGreen} 100%);
  color: white;
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius.lg};
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[6]};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  cursor: pointer;
  transition: all ${({ theme }) => theme.animations.transitions.base};
  white-space: nowrap;

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

const TicketDetailsContainer = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  overflow: hidden;
`;

const TicketHeader = styled.div`
  background: linear-gradient(135deg, ${({ theme }) => theme.colors.primary.darkGreen} 0%, ${({ theme }) => theme.colors.primary.mediumGreen} 100%);
  color: white;
  padding: ${({ theme }) => theme.spacing[6]};

  .ticket-title {
    font-size: ${({ theme }) => theme.typography.fontSizes['2xl']};
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    margin-bottom: ${({ theme }) => theme.spacing[2]};
  }

  .ticket-meta {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: ${({ theme }) => theme.spacing[4]};
    margin-top: ${({ theme }) => theme.spacing[4]};
  }

  .meta-item {
    .label {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      opacity: 0.8;
      margin-bottom: ${({ theme }) => theme.spacing[1]};
    }

    .value {
      font-size: ${({ theme }) => theme.typography.fontSizes.lg};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
    }
  }
`;

const TransactionTable = styled.div`
  overflow-x: auto;

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
    }

    tr:hover {
      background: ${({ theme }) => theme.colors.primary.lightCyan}50;
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

const LoadingSpinner = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  padding: ${({ theme }) => theme.spacing[12]};

  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid ${({ theme }) => theme.colors.primary.lightCyan};
    border-top: 4px solid ${({ theme }) => theme.colors.primary.darkGreen};
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

interface TicketDetail {
  ticket_id: string;
  customer_name: string;
  created_date: string;
  total_amount: number;
  batch_type: string;
  branch_id: string;
  transactions: Array<{
    account_code: string;
    description: string;
    debit_amount: number;
    credit_amount: number;
    line_number: number;
  }>;
}

export const DetailByTicket: React.FC = () => {
  const { filters, isLoading } = useFinancialStore();
  const [ticketSearch, setTicketSearch] = useState('');
  const [ticketData, setTicketData] = useState<TicketDetail | null>(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);

  // Mock ticket data for development
  const mockTicketData: TicketDetail = {
    ticket_id: 'TKT-2024-001234',
    customer_name: 'ABC Construction Company',
    created_date: '2024-01-15T10:30:00Z',
    total_amount: 45678.90,
    batch_type: 'CASH',
    branch_id: 'BR001',
    transactions: [
      {
        account_code: '1100-Cash',
        description: 'Payment received for materials',
        debit_amount: 45678.90,
        credit_amount: 0,
        line_number: 1,
      },
      {
        account_code: '4000-Sales Revenue',
        description: 'Concrete materials sale',
        debit_amount: 0,
        credit_amount: 38065.75,
        line_number: 2,
      },
      {
        account_code: '2200-Sales Tax Payable',
        description: 'Sales tax collected',
        debit_amount: 0,
        credit_amount: 7613.15,
        line_number: 3,
      },
    ],
  };

  const handleTicketSearch = async () => {
    if (!ticketSearch.trim()) return;

    setSearchLoading(true);
    setSearchError(null);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      if (ticketSearch.toLowerCase().includes('001234')) {
        setTicketData(mockTicketData);
      } else {
        setTicketData(null);
        setSearchError('Ticket not found');
      }
    } catch (error) {
      setSearchError('Failed to search ticket');
    } finally {
      setSearchLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleTicketSearch();
    }
  };

  const transactionSummary = useMemo(() => {
    if (!ticketData) return null;

    const totalDebits = ticketData.transactions.reduce((sum, tx) => sum + tx.debit_amount, 0);
    const totalCredits = ticketData.transactions.reduce((sum, tx) => sum + tx.credit_amount, 0);
    const isBalanced = Math.abs(totalDebits - totalCredits) < 0.01;

    return { totalDebits, totalCredits, isBalanced };
  }, [ticketData]);

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <div className="page-title">
          🎫 Detail by Ticket
        </div>
        <div className="page-subtitle">
          Search and view detailed transaction information for specific tickets.
          Enter a ticket ID to see all associated journal entries and account details.
        </div>
      </PageHeader>

      <TicketSearchContainer>
        <div className="search-header">Ticket Search</div>
        <div className="search-form">
          <SearchInput
            type="text"
            placeholder="Enter ticket ID (e.g., TKT-2024-001234)"
            value={ticketSearch}
            onChange={(e) => setTicketSearch(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <SearchButton
            onClick={handleTicketSearch}
            disabled={!ticketSearch.trim() || searchLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {searchLoading ? '🔍 Searching...' : '🔍 Search'}
          </SearchButton>
        </div>
      </TicketSearchContainer>

      {searchLoading && (
        <LoadingSpinner>
          <div className="spinner" />
        </LoadingSpinner>
      )}

      {searchError && (
        <EmptyState>
          <div className="empty-icon">❌</div>
          <div className="empty-title">Search Error</div>
          <div className="empty-description">{searchError}</div>
        </EmptyState>
      )}

      {ticketData && !searchLoading && (
        <TicketDetailsContainer>
          <TicketHeader>
            <div className="ticket-title">
              Ticket: {ticketData.ticket_id}
            </div>
            <div className="ticket-meta">
              <div className="meta-item">
                <div className="label">Customer</div>
                <div className="value">{ticketData.customer_name}</div>
              </div>
              <div className="meta-item">
                <div className="label">Created Date</div>
                <div className="value">{formatDate(ticketData.created_date)}</div>
              </div>
              <div className="meta-item">
                <div className="label">Total Amount</div>
                <div className="value">{formatCurrency(ticketData.total_amount)}</div>
              </div>
              <div className="meta-item">
                <div className="label">Batch Type</div>
                <div className="value">{ticketData.batch_type}</div>
              </div>
              <div className="meta-item">
                <div className="label">Branch ID</div>
                <div className="value">{ticketData.branch_id}</div>
              </div>
              {transactionSummary && (
                <div className="meta-item">
                  <div className="label">Balance Status</div>
                  <div className="value">
                    {transactionSummary.isBalanced ? '✅ Balanced' : '❌ Out of Balance'}
                  </div>
                </div>
              )}
            </div>
          </TicketHeader>

          <TransactionTable>
            <table>
              <thead>
                <tr>
                  <th>Line #</th>
                  <th>Account Code</th>
                  <th>Description</th>
                  <th>Debit Amount</th>
                  <th>Credit Amount</th>
                </tr>
              </thead>
              <tbody>
                {ticketData.transactions.map((transaction, index) => (
                  <tr key={index}>
                    <td>{transaction.line_number}</td>
                    <td className="account-code">{transaction.account_code}</td>
                    <td>{transaction.description}</td>
                    <td className="currency">
                      {transaction.debit_amount > 0 ? formatCurrency(transaction.debit_amount) : '—'}
                    </td>
                    <td className="currency">
                      {transaction.credit_amount > 0 ? formatCurrency(transaction.credit_amount) : '—'}
                    </td>
                  </tr>
                ))}
                {transactionSummary && (
                  <tr style={{ borderTop: '2px solid #003F2C', fontWeight: 'bold' }}>
                    <td colSpan={3} style={{ textAlign: 'right', padding: '16px' }}>
                      <strong>TOTALS:</strong>
                    </td>
                    <td className="currency">
                      <strong>{formatCurrency(transactionSummary.totalDebits)}</strong>
                    </td>
                    <td className="currency">
                      <strong>{formatCurrency(transactionSummary.totalCredits)}</strong>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </TransactionTable>
        </TicketDetailsContainer>
      )}

      {!ticketData && !searchLoading && !searchError && (
        <EmptyState>
          <div className="empty-icon">🔍</div>
          <div className="empty-title">Search for a Ticket</div>
          <div className="empty-description">
            Enter a ticket ID above to view detailed transaction information.
            Use format TKT-YYYY-NNNNNN or similar ticket identifiers.
          </div>
        </EmptyState>
      )}
    </PageContainer>
  );
};