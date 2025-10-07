// GraniteRock Sales Journal - Tieout Management Page
// Premium tieout process monitoring and management

import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
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

const TieoutStatusGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: ${({ theme }) => theme.spacing[6]};
  margin-bottom: ${({ theme }) => theme.spacing[8]};
`;

const StatusCard = styled(motion.div)<{ status: 'success' | 'warning' | 'error' | 'pending' | 'processing' }>`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border-left: 6px solid ${({ status, theme }) => {
    switch (status) {
      case 'success': return theme.colors.semantic.success;
      case 'warning': return theme.colors.semantic.warning;
      case 'error': return theme.colors.semantic.error;
      case 'processing': return theme.colors.primary.orange;
      default: return theme.colors.primary.grayGreen;
    }
  }};
  position: relative;
  overflow: hidden;

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

  .status-metric {
    font-size: ${({ theme }) => theme.typography.fontSizes['3xl']};
    font-weight: ${({ theme }) => theme.typography.fontWeights.black};
    font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
    margin-bottom: ${({ theme }) => theme.spacing[2]};
    color: ${({ status, theme }) => {
      switch (status) {
        case 'success': return theme.colors.semantic.success;
        case 'warning': return theme.colors.semantic.warning;
        case 'error': return theme.colors.semantic.error;
        case 'processing': return theme.colors.primary.orange;
        default: return theme.colors.primary.darkGray;
      }
    }};
  }

  .status-description {
    font-size: ${({ theme }) => theme.typography.fontSizes.sm};
    color: ${({ theme }) => theme.colors.primary.darkGray};
    line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
    margin-bottom: ${({ theme }) => theme.spacing[3]};
  }

  .status-timestamp {
    font-size: ${({ theme }) => theme.typography.fontSizes.xs};
    color: ${({ theme }) => theme.colors.primary.grayGreen};
    font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
  }

  ${({ status }) => status === 'processing' && `
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, transparent, #D9792C, transparent);
      animation: shimmer 2s infinite;
    }

    @keyframes shimmer {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
    }
  `}
`;

const TieoutProcessContainer = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  overflow: hidden;
  margin-bottom: ${({ theme }) => theme.spacing[8]};

  .process-header {
    background: linear-gradient(135deg, ${({ theme }) => theme.colors.primary.darkGreen} 0%, ${({ theme }) => theme.colors.primary.mediumGreen} 100%);
    color: white;
    padding: ${({ theme }) => theme.spacing[6]};
    display: flex;
    justify-content: space-between;
    align-items: center;

    .process-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.xl};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    }

    .process-controls {
      display: flex;
      gap: ${({ theme }) => theme.spacing[3]};
    }
  }
`;

const ProcessStep = styled(motion.div)<{ status: 'pending' | 'processing' | 'completed' | 'failed' }>`
  display: flex;
  align-items: center;
  padding: ${({ theme }) => theme.spacing[4]} ${({ theme }) => theme.spacing[6]};
  border-bottom: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  transition: all ${({ theme }) => theme.animations.transitions.base};

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background: ${({ theme }) => theme.colors.primary.lightCyan}20;
  }

  .step-icon {
    font-size: 1.5rem;
    margin-right: ${({ theme }) => theme.spacing[4]};
    color: ${({ status, theme }) => {
      switch (status) {
        case 'completed': return theme.colors.semantic.success;
        case 'processing': return theme.colors.primary.orange;
        case 'failed': return theme.colors.semantic.error;
        default: return theme.colors.primary.grayGreen;
      }
    }};
  }

  .step-content {
    flex: 1;

    .step-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.base};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
      margin-bottom: ${({ theme }) => theme.spacing[1]};
    }

    .step-description {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      color: ${({ theme }) => theme.colors.primary.darkGray};
      line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
    }
  }

  .step-meta {
    text-align: right;
    font-size: ${({ theme }) => theme.typography.fontSizes.xs};
    color: ${({ theme }) => theme.colors.primary.grayGreen};
    font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};

    .step-duration {
      margin-bottom: ${({ theme }) => theme.spacing[1]};
    }

    .step-timestamp {
      opacity: 0.7;
    }
  }

  ${({ status }) => status === 'processing' && `
    animation: pulse 2s infinite;

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.7; }
    }
  `}
`;

const ActionButton = styled(motion.button)<{ variant: 'primary' | 'secondary' | 'danger' }>`
  background: ${({ variant, theme }) => {
    switch (variant) {
      case 'primary': return 'white';
      case 'secondary': return `${theme.colors.primary.lightCyan}40`;
      case 'danger': return `${theme.colors.semantic.error}20`;
      default: return 'white';
    }
  }};
  color: ${({ variant, theme }) => {
    switch (variant) {
      case 'primary': return theme.colors.primary.darkGreen;
      case 'secondary': return theme.colors.primary.darkGreen;
      case 'danger': return theme.colors.semantic.error;
      default: return theme.colors.primary.darkGreen;
    }
  }};
  border: 2px solid ${({ variant, theme }) => {
    switch (variant) {
      case 'primary': return 'white';
      case 'secondary': return theme.colors.primary.lightCyan;
      case 'danger': return theme.colors.semantic.error;
      default: return 'white';
    }
  }};
  border-radius: ${({ theme }) => theme.borderRadius.md};
  padding: ${({ theme }) => theme.spacing[2]} ${({ theme }) => theme.spacing[4]};
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  cursor: pointer;
  transition: all ${({ theme }) => theme.animations.transitions.base};

  &:hover {
    transform: translateY(-1px);
    box-shadow: ${({ theme }) => theme.shadows.md};
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const TieoutResults = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  overflow: hidden;

  .results-header {
    background: ${({ theme }) => theme.colors.primary.lightCyan};
    padding: ${({ theme }) => theme.spacing[6]};
    border-bottom: 1px solid ${({ theme }) => theme.colors.primary.grayGreen};

    .results-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.xl};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
    }
  }

  .results-table {
    overflow-x: auto;
    max-height: 400px;
    overflow-y: auto;

    table {
      width: 100%;
      border-collapse: collapse;

      th {
        background: ${({ theme }) => theme.colors.primary.lightCyan}80;
        padding: ${({ theme }) => theme.spacing[3]};
        text-align: left;
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        color: ${({ theme }) => theme.colors.primary.darkGreen};
        font-size: ${({ theme }) => theme.typography.fontSizes.sm};
        position: sticky;
        top: 0;
        z-index: 1;
      }

      td {
        padding: ${({ theme }) => theme.spacing[3]};
        border-bottom: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
        font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
        font-size: ${({ theme }) => theme.typography.fontSizes.sm};

        &.currency {
          text-align: right;
          font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        }

        &.status {
          text-align: center;
        }
      }

      tr:hover {
        background: ${({ theme }) => theme.colors.primary.lightCyan}30;
      }
    }
  }
`;

interface TieoutStatus {
  id: string;
  name: string;
  status: 'success' | 'warning' | 'error' | 'pending' | 'processing';
  value: number | string;
  description: string;
  lastUpdated: string;
}

interface TieoutStep {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  duration?: string;
  timestamp?: string;
}

interface TieoutResult {
  account: string;
  sourceSystem: string;
  sourceBalance: number;
  warehouseBalance: number;
  variance: number;
  status: 'tied' | 'variance' | 'missing';
  lastChecked: string;
}

export const TieoutManagement: React.FC = () => {
  const { isLoading } = useFinancialStore();
  const [tieoutStatuses, setTieoutStatuses] = useState<TieoutStatus[]>([]);
  const [processSteps, setProcessSteps] = useState<TieoutStep[]>([]);
  const [tieoutResults, setTieoutResults] = useState<TieoutResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);

  // Mock data
  const mockStatuses: TieoutStatus[] = [
    {
      id: 'overall-status',
      name: 'Overall Tieout Status',
      status: 'warning',
      value: '94.7%',
      description: 'Percentage of accounts successfully tied out',
      lastUpdated: new Date().toISOString(),
    },
    {
      id: 'variance-total',
      name: 'Total Variance',
      status: 'error',
      value: 15847.32,
      description: 'Sum of all balance variances requiring attention',
      lastUpdated: new Date().toISOString(),
    },
    {
      id: 'accounts-processed',
      name: 'Accounts Processed',
      status: 'success',
      value: 1247,
      description: 'Total number of accounts in tieout process',
      lastUpdated: new Date().toISOString(),
    },
    {
      id: 'last-run',
      name: 'Last Complete Run',
      status: 'success',
      value: '2 hours ago',
      description: 'Time since last successful tieout completion',
      lastUpdated: new Date().toISOString(),
    },
  ];

  const mockSteps: TieoutStep[] = [
    {
      id: 'extract-source',
      title: 'Extract Source System Data',
      description: 'Pull balance data from ERP and subsidiary systems',
      status: 'completed',
      duration: '3m 24s',
      timestamp: '2024-01-15T14:00:00Z',
    },
    {
      id: 'extract-warehouse',
      title: 'Extract Warehouse Data',
      description: 'Pull corresponding balances from Snowflake data warehouse',
      status: 'completed',
      duration: '1m 15s',
      timestamp: '2024-01-15T14:03:24Z',
    },
    {
      id: 'reconcile-balances',
      title: 'Reconcile Account Balances',
      description: 'Compare source system and warehouse balances for variances',
      status: 'processing',
      duration: '5m 12s',
      timestamp: '2024-01-15T14:04:39Z',
    },
    {
      id: 'identify-variances',
      title: 'Identify Variances',
      description: 'Flag accounts with material balance differences',
      status: 'pending',
    },
    {
      id: 'generate-reports',
      title: 'Generate Tieout Reports',
      description: 'Create detailed variance reports and exception listings',
      status: 'pending',
    },
    {
      id: 'notify-stakeholders',
      title: 'Notify Stakeholders',
      description: 'Send alerts and reports to finance team and system administrators',
      status: 'pending',
    },
  ];

  const mockResults: TieoutResult[] = [
    {
      account: '1100-Cash Operating',
      sourceSystem: 'ERP',
      sourceBalance: 2456789.45,
      warehouseBalance: 2456789.45,
      variance: 0,
      status: 'tied',
      lastChecked: '2024-01-15T14:05:00Z',
    },
    {
      account: '1200-Accounts Receivable',
      sourceSystem: 'ERP',
      sourceBalance: 1875432.10,
      warehouseBalance: 1873298.67,
      variance: -2133.43,
      status: 'variance',
      lastChecked: '2024-01-15T14:05:00Z',
    },
    {
      account: '4000-Sales Revenue',
      sourceSystem: 'POS',
      sourceBalance: 5678901.23,
      warehouseBalance: 5691234.56,
      variance: 12333.33,
      status: 'variance',
      lastChecked: '2024-01-15T14:05:00Z',
    },
    {
      account: '1140-Prepaid Insurance',
      sourceSystem: 'ERP',
      sourceBalance: 45000.00,
      warehouseBalance: 45000.00,
      variance: 0,
      status: 'tied',
      lastChecked: '2024-01-15T14:05:00Z',
    },
  ];

  useEffect(() => {
    setTieoutStatuses(mockStatuses);
    setProcessSteps(mockSteps);
    setTieoutResults(mockResults);
  }, []);

  const getStatusIcon = (status: TieoutStatus['status']) => {
    switch (status) {
      case 'success': return '✅';
      case 'warning': return '⚠️';
      case 'error': return '❌';
      case 'processing': return '🔄';
      default: return '⏸️';
    }
  };

  const getStepIcon = (status: TieoutStep['status']) => {
    switch (status) {
      case 'completed': return '✅';
      case 'processing': return '🔄';
      case 'failed': return '❌';
      default: return '⏸️';
    }
  };

  const getResultStatusIcon = (status: TieoutResult['status']) => {
    switch (status) {
      case 'tied': return '✅';
      case 'variance': return '⚠️';
      case 'missing': return '❌';
      default: return '❓';
    }
  };

  const handleStartTieout = async () => {
    setIsRunning(true);
    console.log('Starting tieout process...');

    // Reset steps to pending
    setProcessSteps(steps => steps.map(step => ({ ...step, status: 'pending' as const })));

    // Simulate step progression
    for (let i = 0; i < mockSteps.length; i++) {
      setTimeout(() => {
        setProcessSteps(steps => steps.map((step, index) =>
          index === i
            ? { ...step, status: 'processing' as const, timestamp: new Date().toISOString() }
            : step
        ));

        setTimeout(() => {
          setProcessSteps(steps => steps.map((step, index) =>
            index === i
              ? { ...step, status: 'completed' as const, duration: `${Math.floor(Math.random() * 5) + 1}m ${Math.floor(Math.random() * 60)}s` }
              : step
          ));
        }, 2000);
      }, i * 3000);
    }

    setTimeout(() => {
      setIsRunning(false);
    }, mockSteps.length * 3000);
  };

  const handleStopTieout = () => {
    setIsRunning(false);
    console.log('Stopping tieout process...');
  };

  const handleRefresh = () => {
    console.log('Refreshing tieout data...');
    setTieoutStatuses(statuses => statuses.map(status => ({
      ...status,
      lastUpdated: new Date().toISOString()
    })));
  };

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <div className="page-title">
          🔗 Tieout Management
        </div>
        <div className="page-subtitle">
          Monitor and manage financial tieout processes between source systems and data warehouse.
          Track balance reconciliation, identify variances, and ensure data integrity.
        </div>
      </PageHeader>

      <TieoutStatusGrid>
        {tieoutStatuses.map((status) => (
          <StatusCard
            key={status.id}
            status={status.status}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div className="status-header">
              <div className="status-title">{status.name}</div>
              <div className="status-icon">{getStatusIcon(status.status)}</div>
            </div>
            <div className="status-metric">
              {typeof status.value === 'number' ? formatCurrency(status.value) : status.value}
            </div>
            <div className="status-description">{status.description}</div>
            <div className="status-timestamp">
              Updated: {formatTimestamp(status.lastUpdated)}
            </div>
          </StatusCard>
        ))}
      </TieoutStatusGrid>

      <TieoutProcessContainer>
        <div className="process-header">
          <div className="process-title">🔄 Tieout Process Monitor</div>
          <div className="process-controls">
            <ActionButton
              variant="primary"
              onClick={handleStartTieout}
              disabled={isRunning}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              ▶️ Start Tieout
            </ActionButton>
            <ActionButton
              variant="danger"
              onClick={handleStopTieout}
              disabled={!isRunning}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              ⏹️ Stop
            </ActionButton>
            <ActionButton
              variant="secondary"
              onClick={handleRefresh}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              🔄 Refresh
            </ActionButton>
          </div>
        </div>

        <AnimatePresence>
          {processSteps.map((step) => (
            <ProcessStep
              key={step.id}
              status={step.status}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="step-icon">{getStepIcon(step.status)}</div>
              <div className="step-content">
                <div className="step-title">{step.title}</div>
                <div className="step-description">{step.description}</div>
              </div>
              <div className="step-meta">
                {step.duration && <div className="step-duration">{step.duration}</div>}
                {step.timestamp && (
                  <div className="step-timestamp">{formatTimestamp(step.timestamp)}</div>
                )}
              </div>
            </ProcessStep>
          ))}
        </AnimatePresence>
      </TieoutProcessContainer>

      <TieoutResults>
        <div className="results-header">
          <div className="results-title">📊 Tieout Results Summary</div>
        </div>
        <div className="results-table">
          <table>
            <thead>
              <tr>
                <th>Account</th>
                <th>Source System</th>
                <th>Source Balance</th>
                <th>Warehouse Balance</th>
                <th>Variance</th>
                <th>Status</th>
                <th>Last Checked</th>
              </tr>
            </thead>
            <tbody>
              {tieoutResults.map((result, index) => (
                <tr key={index}>
                  <td>{result.account}</td>
                  <td>{result.sourceSystem}</td>
                  <td className="currency">{formatCurrency(result.sourceBalance)}</td>
                  <td className="currency">{formatCurrency(result.warehouseBalance)}</td>
                  <td className="currency">
                    {result.variance === 0 ? '—' : formatCurrency(result.variance)}
                  </td>
                  <td className="status">
                    {getResultStatusIcon(result.status)}
                  </td>
                  <td>{formatTimestamp(result.lastChecked)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </TieoutResults>
    </PageContainer>
  );
};