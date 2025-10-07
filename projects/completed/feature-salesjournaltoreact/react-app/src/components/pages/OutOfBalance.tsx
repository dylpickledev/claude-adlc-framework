// GraniteRock Sales Journal - Out of Balance Page
// Premium financial reconciliation and balance monitoring

import React, { useState, useEffect, useMemo } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useFinancialStore } from '../../store/financialStore';
import { formatCurrency, formatNumber, formatTimestamp } from '../../utils/formatters';

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

const StatusGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${({ theme }) => theme.spacing[6]};
  margin-bottom: ${({ theme }) => theme.spacing[8]};
`;

const StatusCard = styled(motion.div)<{ status: 'success' | 'warning' | 'error' }>`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border-left: 6px solid ${({ status, theme }) => {
    switch (status) {
      case 'success': return theme.colors.semantic.success;
      case 'warning': return theme.colors.semantic.warning;
      case 'error': return theme.colors.semantic.error;
      default: return theme.colors.primary.grayGreen;
    }
  }};

  .status-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: ${({ theme }) => theme.spacing[4]};

    .status-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.lg};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
    }

    .status-icon {
      font-size: 2rem;
    }
  }

  .status-amount {
    font-size: ${({ theme }) => theme.typography.fontSizes['3xl']};
    font-weight: ${({ theme }) => theme.typography.fontWeights.black};
    font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
    margin-bottom: ${({ theme }) => theme.spacing[2]};
    color: ${({ status, theme }) => {
      switch (status) {
        case 'success': return theme.colors.semantic.success;
        case 'warning': return theme.colors.semantic.warning;
        case 'error': return theme.colors.semantic.error;
        default: return theme.colors.primary.darkGray;
      }
    }};
  }

  .status-description {
    font-size: ${({ theme }) => theme.typography.fontSizes.sm};
    color: ${({ theme }) => theme.colors.primary.darkGray};
    line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
  }

  .status-timestamp {
    font-size: ${({ theme }) => theme.typography.fontSizes.xs};
    color: ${({ theme }) => theme.colors.primary.grayGreen};
    margin-top: ${({ theme }) => theme.spacing[3]};
    font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
  }
`;

const BalanceDetailsContainer = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  overflow: hidden;
  margin-bottom: ${({ theme }) => theme.spacing[8]};

  .details-header {
    background: linear-gradient(135deg, ${({ theme }) => theme.colors.primary.darkGreen} 0%, ${({ theme }) => theme.colors.primary.mediumGreen} 100%);
    color: white;
    padding: ${({ theme }) => theme.spacing[6]};

    .details-title {
      font-size: ${({ theme }) => theme.typography.fontSizes['2xl']};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
      margin-bottom: ${({ theme }) => theme.spacing[2]};
    }

    .details-subtitle {
      opacity: 0.9;
      font-size: ${({ theme }) => theme.typography.fontSizes.base};
    }
  }
`;

const BalanceBreakdown = styled.div`
  padding: ${({ theme }) => theme.spacing[6]};

  .breakdown-section {
    margin-bottom: ${({ theme }) => theme.spacing[6]};

    &:last-child {
      margin-bottom: 0;
    }

    .section-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.lg};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
      margin-bottom: ${({ theme }) => theme.spacing[4]};
      display: flex;
      align-items: center;
      gap: ${({ theme }) => theme.spacing[2]};
    }

    .breakdown-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: ${({ theme }) => theme.spacing[4]};
    }

    .breakdown-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: ${({ theme }) => theme.spacing[3]};
      background: ${({ theme }) => theme.colors.primary.lightCyan}20;
      border-radius: ${({ theme }) => theme.borderRadius.lg};

      .item-label {
        font-size: ${({ theme }) => theme.typography.fontSizes.sm};
        color: ${({ theme }) => theme.colors.primary.darkGray};
      }

      .item-value {
        font-size: ${({ theme }) => theme.typography.fontSizes.base};
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
        color: ${({ theme }) => theme.colors.primary.darkGreen};
      }
    }
  }
`;

const ActionButtons = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing[4]};
  margin-bottom: ${({ theme }) => theme.spacing[8]};

  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    flex-direction: column;
  }
`;

const ActionButton = styled(motion.button)<{ variant: 'primary' | 'secondary' | 'danger' }>`
  background: ${({ variant, theme }) => {
    switch (variant) {
      case 'primary': return `linear-gradient(135deg, ${theme.colors.primary.darkGreen} 0%, ${theme.colors.primary.mediumGreen} 100%)`;
      case 'secondary': return `linear-gradient(135deg, ${theme.colors.primary.grayGreen} 0%, ${theme.colors.primary.lightCyan} 100%)`;
      case 'danger': return `linear-gradient(135deg, ${theme.colors.semantic.error} 0%, #d32f2f 100%)`;
      default: return theme.colors.primary.darkGreen;
    }
  }};
  color: ${({ variant, theme }) => variant === 'secondary' ? theme.colors.primary.darkGreen : 'white'};
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius.lg};
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[6]};
  font-size: ${({ theme }) => theme.typography.fontSizes.sm};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  cursor: pointer;
  transition: all ${({ theme }) => theme.animations.transitions.base};
  flex: 1;

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

const ResolutionHistory = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  overflow: hidden;

  .history-header {
    background: ${({ theme }) => theme.colors.primary.lightCyan};
    padding: ${({ theme }) => theme.spacing[6]};
    border-bottom: 1px solid ${({ theme }) => theme.colors.primary.grayGreen};

    .history-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.xl};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
    }
  }

  .history-list {
    max-height: 400px;
    overflow-y: auto;
  }

  .history-item {
    padding: ${({ theme }) => theme.spacing[4]};
    border-bottom: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[4]};

    &:last-child {
      border-bottom: none;
    }

    .item-icon {
      font-size: 1.5rem;
      width: 40px;
      text-align: center;
    }

    .item-content {
      flex: 1;

      .item-title {
        font-size: ${({ theme }) => theme.typography.fontSizes.sm};
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        color: ${({ theme }) => theme.colors.primary.darkGreen};
        margin-bottom: ${({ theme }) => theme.spacing[1]};
      }

      .item-description {
        font-size: ${({ theme }) => theme.typography.fontSizes.xs};
        color: ${({ theme }) => theme.colors.primary.darkGray};
        line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
      }
    }

    .item-timestamp {
      font-size: ${({ theme }) => theme.typography.fontSizes.xs};
      color: ${({ theme }) => theme.colors.primary.grayGreen};
      font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
    }
  }
`;

interface BalanceData {
  totalOutOfBalance: number;
  status: 'success' | 'warning' | 'error';
  details: {
    totalDebits: number;
    totalCredits: number;
    variance: number;
    affectedBatches: number;
    lastCheck: string;
  };
  breakdown: {
    batchType: Record<string, number>;
    accountCode: Record<string, number>;
  };
}

interface ResolutionItem {
  id: string;
  type: 'manual_adjustment' | 'system_correction' | 'investigation';
  title: string;
  description: string;
  timestamp: string;
  amount?: number;
}

export const OutOfBalance: React.FC = () => {
  const { outOfBalanceData, filters, refreshOutOfBalanceData, isLoading } = useFinancialStore();
  const [resolutionHistory, setResolutionHistory] = useState<ResolutionItem[]>([]);

  // Mock balance data with realistic values
  const mockBalanceData: BalanceData = {
    totalOutOfBalance: -247.83,
    status: 'warning',
    details: {
      totalDebits: 2456789.45,
      totalCredits: 2457037.28,
      variance: -247.83,
      affectedBatches: 3,
      lastCheck: new Date().toISOString(),
    },
    breakdown: {
      batchType: {
        'CASH': -125.50,
        'CREDIT': -89.33,
        'INTRA': -33.00,
      },
      accountCode: {
        '1100-Cash': -125.50,
        '1200-Receivables': -89.33,
        '4000-Sales': -33.00,
      },
    },
  };

  const mockResolutionHistory: ResolutionItem[] = [
    {
      id: '1',
      type: 'manual_adjustment',
      title: 'Manual Adjustment Applied',
      description: 'Corrected rounding difference in batch CASH-20240115-003',
      timestamp: '2024-01-15T14:30:00Z',
      amount: 2.47,
    },
    {
      id: '2',
      type: 'system_correction',
      title: 'Automatic System Correction',
      description: 'System identified and corrected duplicate posting in account 1100',
      timestamp: '2024-01-15T10:15:00Z',
      amount: 125.50,
    },
    {
      id: '3',
      type: 'investigation',
      title: 'Balance Investigation Initiated',
      description: 'Started investigation into discrepancy in CREDIT batch processing',
      timestamp: '2024-01-15T09:00:00Z',
    },
  ];

  useEffect(() => {
    setResolutionHistory(mockResolutionHistory);
  }, []);

  const handleRefresh = () => {
    refreshOutOfBalanceData();
  };

  const handleManualAdjustment = () => {
    // Simulate manual adjustment
    console.log('Opening manual adjustment dialog...');
  };

  const handleInvestigate = () => {
    // Simulate investigation start
    console.log('Starting balance investigation...');
  };

  const balanceData = mockBalanceData;

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <div className="page-title">
          ⚖️ Out of Balance Monitor
        </div>
        <div className="page-subtitle">
          Monitor and resolve financial balance discrepancies. Track variance amounts,
          investigate root causes, and maintain audit trails for all reconciliation activities.
        </div>
      </PageHeader>

      <StatusGrid>
        <StatusCard
          status={balanceData.status}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <div className="status-header">
            <div className="status-title">Current Balance Status</div>
            <div className="status-icon">
              {balanceData.status === 'success' ? '✅' :
               balanceData.status === 'warning' ? '⚠️' : '❌'}
            </div>
          </div>
          <div className="status-amount">
            {formatCurrency(balanceData.totalOutOfBalance)}
          </div>
          <div className="status-description">
            {Math.abs(balanceData.totalOutOfBalance) < 10
              ? 'Within acceptable tolerance range'
              : Math.abs(balanceData.totalOutOfBalance) < 100
              ? 'Requires monitoring and potential correction'
              : 'Immediate attention required for resolution'
            }
          </div>
          <div className="status-timestamp">
            Last checked: {formatTimestamp(balanceData.details.lastCheck)}
          </div>
        </StatusCard>

        <StatusCard
          status="success"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.2 }}
        >
          <div className="status-header">
            <div className="status-title">Affected Batches</div>
            <div className="status-icon">📦</div>
          </div>
          <div className="status-amount">
            {formatNumber(balanceData.details.affectedBatches)}
          </div>
          <div className="status-description">
            Number of batches with balance discrepancies requiring review
          </div>
          <div className="status-timestamp">
            Total variance: {formatCurrency(Math.abs(balanceData.details.variance))}
          </div>
        </StatusCard>

        <StatusCard
          status="success"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.3 }}
        >
          <div className="status-header">
            <div className="status-title">Balance Percentage</div>
            <div className="status-icon">📊</div>
          </div>
          <div className="status-amount">
            {(Math.abs(balanceData.details.variance) / balanceData.details.totalDebits * 100).toFixed(4)}%
          </div>
          <div className="status-description">
            Variance as percentage of total transaction volume
          </div>
          <div className="status-timestamp">
            Total volume: {formatCurrency(balanceData.details.totalDebits)}
          </div>
        </StatusCard>
      </StatusGrid>

      <ActionButtons>
        <ActionButton
          variant="primary"
          onClick={handleRefresh}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          🔄 Refresh Balance Data
        </ActionButton>
        <ActionButton
          variant="secondary"
          onClick={handleInvestigate}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          🔍 Start Investigation
        </ActionButton>
        <ActionButton
          variant="danger"
          onClick={handleManualAdjustment}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          ⚡ Manual Adjustment
        </ActionButton>
      </ActionButtons>

      <BalanceDetailsContainer>
        <div className="details-header">
          <div className="details-title">Balance Analysis</div>
          <div className="details-subtitle">
            Detailed breakdown of balance discrepancies by batch type and account code
          </div>
        </div>

        <BalanceBreakdown>
          <div className="breakdown-section">
            <div className="section-title">
              📊 Summary Totals
            </div>
            <div className="breakdown-grid">
              <div className="breakdown-item">
                <span className="item-label">Total Debits</span>
                <span className="item-value">{formatCurrency(balanceData.details.totalDebits)}</span>
              </div>
              <div className="breakdown-item">
                <span className="item-label">Total Credits</span>
                <span className="item-value">{formatCurrency(balanceData.details.totalCredits)}</span>
              </div>
              <div className="breakdown-item">
                <span className="item-label">Net Variance</span>
                <span className="item-value">{formatCurrency(balanceData.details.variance)}</span>
              </div>
              <div className="breakdown-item">
                <span className="item-label">Affected Batches</span>
                <span className="item-value">{formatNumber(balanceData.details.affectedBatches)}</span>
              </div>
            </div>
          </div>

          <div className="breakdown-section">
            <div className="section-title">
              🏷️ Variance by Batch Type
            </div>
            <div className="breakdown-grid">
              {Object.entries(balanceData.breakdown.batchType).map(([batchType, amount]) => (
                <div key={batchType} className="breakdown-item">
                  <span className="item-label">{batchType}</span>
                  <span className="item-value">{formatCurrency(amount)}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="breakdown-section">
            <div className="section-title">
              🏦 Variance by Account Code
            </div>
            <div className="breakdown-grid">
              {Object.entries(balanceData.breakdown.accountCode).map(([accountCode, amount]) => (
                <div key={accountCode} className="breakdown-item">
                  <span className="item-label">{accountCode}</span>
                  <span className="item-value">{formatCurrency(amount)}</span>
                </div>
              ))}
            </div>
          </div>
        </BalanceBreakdown>
      </BalanceDetailsContainer>

      <ResolutionHistory>
        <div className="history-header">
          <div className="history-title">📋 Resolution History</div>
        </div>
        <div className="history-list">
          {resolutionHistory.map((item) => (
            <div key={item.id} className="history-item">
              <div className="item-icon">
                {item.type === 'manual_adjustment' ? '⚡' :
                 item.type === 'system_correction' ? '🔧' : '🔍'}
              </div>
              <div className="item-content">
                <div className="item-title">{item.title}</div>
                <div className="item-description">{item.description}</div>
              </div>
              <div className="item-timestamp">
                {formatTimestamp(item.timestamp)}
                {item.amount && (
                  <div style={{ marginTop: '4px', fontWeight: 'bold' }}>
                    {formatCurrency(item.amount)}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </ResolutionHistory>
    </PageContainer>
  );
};