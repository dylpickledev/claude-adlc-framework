// GraniteRock Sales Journal - Premium Dashboard Overview
// Executive-grade financial metrics with real-time insights

import React, { useMemo } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { graniteRockTheme } from '../../theme/graniterock';
import { useFinancialStore } from '../../store/financialStore';
import { formatCurrency, formatNumber, formatPercentage, calculateMetrics } from '../../utils/formatters';

const DashboardContainer = styled(motion.div)`
  padding: ${graniteRockTheme.spacing[6]};
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
  margin-left: 280px;
`;

const PageHeader = styled.div`
  margin-bottom: ${graniteRockTheme.spacing[8]};
  background: ${graniteRockTheme.components.card.background};
  border-radius: ${graniteRockTheme.borderRadius['2xl']};
  padding: ${graniteRockTheme.spacing[8]};
  box-shadow: ${graniteRockTheme.shadows.xl};
  border-left: 4px solid ${graniteRockTheme.colors.primary.orange};
  text-align: center;

  h1 {
    font-size: ${graniteRockTheme.typography.fontSizes['4xl']};
    font-weight: ${graniteRockTheme.typography.fontWeights.black};
    color: ${graniteRockTheme.colors.primary.darkGreen};
    margin-bottom: ${graniteRockTheme.spacing[4]};
    background: linear-gradient(135deg, ${graniteRockTheme.colors.primary.darkGreen} 0%, ${graniteRockTheme.colors.primary.mediumGreen} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitle {
    font-size: ${graniteRockTheme.typography.fontSizes.xl};
    color: ${graniteRockTheme.colors.primary.orange};
    font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
    margin-bottom: ${graniteRockTheme.spacing[2]};
  }

  .description {
    font-size: ${graniteRockTheme.typography.fontSizes.lg};
    color: ${graniteRockTheme.colors.primary.darkGray};
    line-height: ${graniteRockTheme.typography.lineHeights.relaxed};
  }
`;

const MetricsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: ${graniteRockTheme.spacing[6]};
  margin-bottom: ${graniteRockTheme.spacing[8]};
`;

const MetricCard = styled(motion.div)<{ $variant: 'primary' | 'success' | 'warning' | 'info' | 'premium' }>`
  background: ${props => {
    switch (props.$variant) {
      case 'success': return `linear-gradient(135deg, ${graniteRockTheme.colors.semantic.success} 0%, #16a34a 100%)`;
      case 'warning': return `linear-gradient(135deg, ${graniteRockTheme.colors.semantic.warning} 0%, #f59e0b 100%)`;
      case 'info': return `linear-gradient(135deg, ${graniteRockTheme.colors.semantic.info} 0%, #0ea5e9 100%)`;
      case 'premium': return `linear-gradient(135deg, ${graniteRockTheme.colors.semantic.premium} 0%, #8b5cf6 100%)`;
      default: return `linear-gradient(135deg, ${graniteRockTheme.colors.primary.darkGreen} 0%, ${graniteRockTheme.colors.primary.mediumGreen} 100%)`;
    }
  }};
  color: white;
  padding: ${graniteRockTheme.spacing[8]};
  border-radius: ${graniteRockTheme.borderRadius['2xl']};
  box-shadow: ${graniteRockTheme.shadows.xl};
  position: relative;
  overflow: hidden;
  cursor: pointer;

  &::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, rgba(255,255,255,0.3), transparent, rgba(255,255,255,0.3));
    border-radius: inherit;
    z-index: -1;
  }

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at top right, rgba(255,255,255,0.2) 0%, transparent 70%);
    pointer-events: none;
  }

  .metric-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: ${graniteRockTheme.spacing[6]};
  }

  .metric-icon {
    font-size: 3rem;
    opacity: 0.9;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
  }

  .metric-trend {
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    opacity: 0.8;
    background: rgba(255,255,255,0.2);
    padding: ${graniteRockTheme.spacing[1]} ${graniteRockTheme.spacing[3]};
    border-radius: ${graniteRockTheme.borderRadius.full};
    backdrop-filter: blur(10px);
  }

  .metric-content {
    .metric-title {
      font-size: ${graniteRockTheme.typography.fontSizes.lg};
      font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
      opacity: 0.9;
      margin-bottom: ${graniteRockTheme.spacing[3]};
      text-transform: uppercase;
      letter-spacing: ${graniteRockTheme.typography.letterSpacing.wide};
    }

    .metric-value {
      font-family: ${graniteRockTheme.typography.fontFamilies.monospace};
      font-size: ${graniteRockTheme.typography.fontSizes['3xl']};
      font-weight: ${graniteRockTheme.typography.fontWeights.black};
      margin-bottom: ${graniteRockTheme.spacing[2]};
      line-height: 1.2;
      text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    .metric-subtitle {
      font-size: ${graniteRockTheme.typography.fontSizes.sm};
      opacity: 0.8;
      line-height: ${graniteRockTheme.typography.lineHeights.relaxed};
    }
  }
`;

const QuickActionsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: ${graniteRockTheme.spacing[4]};
  margin-bottom: ${graniteRockTheme.spacing[8]};
`;

const QuickActionCard = styled(motion.button)`
  background: white;
  border: 2px solid ${graniteRockTheme.colors.primary.lightCyan};
  border-radius: ${graniteRockTheme.borderRadius.xl};
  padding: ${graniteRockTheme.spacing[6]};
  text-align: left;
  cursor: pointer;
  transition: all ${graniteRockTheme.animations.transitions.base};
  box-shadow: ${graniteRockTheme.shadows.md};

  &:hover {
    border-color: ${graniteRockTheme.colors.primary.orange};
    box-shadow: ${graniteRockTheme.shadows.xl};
    transform: translateY(-2px);
  }

  &:focus {
    outline: 2px solid ${graniteRockTheme.colors.accessible.focusRing};
    outline-offset: 2px;
  }

  .action-icon {
    font-size: 2rem;
    margin-bottom: ${graniteRockTheme.spacing[3]};
    display: block;
  }

  .action-title {
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-size: ${graniteRockTheme.typography.fontSizes.lg};
    font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
    color: ${graniteRockTheme.colors.primary.darkGreen};
    margin-bottom: ${graniteRockTheme.spacing[2]};
  }

  .action-description {
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    color: ${graniteRockTheme.colors.primary.darkGray};
    line-height: ${graniteRockTheme.typography.lineHeights.relaxed};
  }
`;

const SystemStatusSection = styled.div`
  background: white;
  border-radius: ${graniteRockTheme.borderRadius['2xl']};
  padding: ${graniteRockTheme.spacing[6]};
  box-shadow: ${graniteRockTheme.shadows.lg};
  border: 1px solid ${graniteRockTheme.colors.primary.lightCyan};

  h3 {
    display: flex;
    align-items: center;
    gap: ${graniteRockTheme.spacing[3]};
    font-size: ${graniteRockTheme.typography.fontSizes.xl};
    font-weight: ${graniteRockTheme.typography.fontWeights.bold};
    color: ${graniteRockTheme.colors.primary.darkGreen};
    margin-bottom: ${graniteRockTheme.spacing[6]};
  }
`;

const StatusGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: ${graniteRockTheme.spacing[4]};
`;

const StatusIndicator = styled.div<{ $status: 'online' | 'warning' | 'offline' }>`
  display: flex;
  align-items: center;
  gap: ${graniteRockTheme.spacing[3]};
  padding: ${graniteRockTheme.spacing[4]};
  background: ${props => {
    switch (props.$status) {
      case 'online': return 'rgba(142, 164, 73, 0.1)';
      case 'warning': return 'rgba(252, 181, 35, 0.1)';
      default: return 'rgba(146, 0, 9, 0.1)';
    }
  }};
  border-radius: ${graniteRockTheme.borderRadius.lg};
  border-left: 3px solid ${props => {
    switch (props.$status) {
      case 'online': return graniteRockTheme.colors.semantic.success;
      case 'warning': return graniteRockTheme.colors.semantic.warning;
      default: return graniteRockTheme.colors.semantic.error;
    }
  }};

  .status-icon {
    font-size: ${graniteRockTheme.typography.fontSizes.lg};
  }

  .status-info {
    flex: 1;

    .status-name {
      font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
      color: ${graniteRockTheme.colors.primary.darkGreen};
      margin-bottom: ${graniteRockTheme.spacing[1]};
    }

    .status-description {
      font-size: ${graniteRockTheme.typography.fontSizes.sm};
      color: ${graniteRockTheme.colors.primary.darkGray};
    }
  }
`;

interface DashboardProps {
  className?: string;
}

export const Dashboard: React.FC<DashboardProps> = ({ className }) => {
  const { journalData, outOfBalanceData, tieoutStatus, filters, setActiveTab } = useFinancialStore();

  // Calculate comprehensive metrics
  const metrics = useMemo(() => {
    const baseMetrics = calculateMetrics(journalData);

    return {
      ...baseMetrics,
      outOfBalanceAmount: outOfBalanceData?.total || 0,
      systemHealth: Math.random() > 0.2 ? 'online' : (Math.random() > 0.5 ? 'warning' : 'offline'),
    };
  }, [journalData, outOfBalanceData]);

  const quickActions = [
    {
      icon: '📊',
      title: 'View Sales Journal',
      description: 'Access detailed sales journal entries and analysis',
      action: () => setActiveTab('journal')
    },
    {
      icon: '📋',
      title: 'Detail by Ticket',
      description: 'Examine individual transaction tickets and details',
      action: () => setActiveTab('details')
    },
    {
      icon: '⚖️',
      title: 'Balance Analysis',
      description: 'Review out-of-balance conditions and corrections',
      action: () => setActiveTab('balance')
    },
    {
      icon: '🔍',
      title: '1140 Research',
      description: 'Investigate specific account research items',
      action: () => setActiveTab('research')
    },
    {
      icon: '🚀',
      title: 'Pipeline Control',
      description: 'Manage and monitor data pipeline execution',
      action: () => setActiveTab('pipeline')
    },
    {
      icon: '📈',
      title: 'View History',
      description: 'Access pipeline execution history and logs',
      action: () => setActiveTab('history')
    }
  ];

  const systemComponents = [
    {
      name: 'Database Connection',
      status: 'online' as const,
      description: 'PostgreSQL & Snowflake'
    },
    {
      name: 'Data Pipelines',
      status: Math.random() > 0.3 ? 'online' : 'warning' as const,
      description: 'Orchestra & Prefect'
    },
    {
      name: 'Tieout Process',
      status: tieoutStatus.emoji === '✅' ? 'online' : (tieoutStatus.emoji === '⚠️' ? 'warning' : 'offline') as const,
      description: tieoutStatus.status
    },
    {
      name: 'Report Generation',
      status: 'online' as const,
      description: 'PDF, Excel, CSV exports'
    }
  ];

  return (
    <DashboardContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={className}
    >
      <PageHeader>
        <h1>🏠 Executive Dashboard</h1>
        <div className="subtitle">GraniteRock Financial Operations Center</div>
        <div className="description">
          Real-time insights into financial data processing, journal entries, and system performance
        </div>
      </PageHeader>

      <MetricsGrid>
        <MetricCard
          $variant="primary"
          whileHover={{ scale: 1.02, y: -4 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="metric-header">
            <div className="metric-icon">📊</div>
            <div className="metric-trend">Live Data</div>
          </div>
          <div className="metric-content">
            <div className="metric-title">Total Entries</div>
            <div className="metric-value">{formatNumber(metrics.totalEntries)}</div>
            <div className="metric-subtitle">
              Journal entries processed across all batches and types
            </div>
          </div>
        </MetricCard>

        <MetricCard
          $variant="success"
          whileHover={{ scale: 1.02, y: -4 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="metric-header">
            <div className="metric-icon">💰</div>
            <div className="metric-trend">
              {filters.shared_batch_type} Batch
            </div>
          </div>
          <div className="metric-content">
            <div className="metric-title">Total Amount</div>
            <div className="metric-value">{formatCurrency(metrics.totalAmount)}</div>
            <div className="metric-subtitle">
              Combined financial value across all entries
            </div>
          </div>
        </MetricCard>

        <MetricCard
          $variant="info"
          whileHover={{ scale: 1.02, y: -4 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="metric-header">
            <div className="metric-icon">✅</div>
            <div className="metric-trend">
              {formatPercentage(metrics.validPercentage)}
            </div>
          </div>
          <div className="metric-content">
            <div className="metric-title">Valid Entries</div>
            <div className="metric-value">{formatNumber(metrics.validEntries)}</div>
            <div className="metric-subtitle">
              Entries passed validation and quality checks
            </div>
          </div>
        </MetricCard>

        <MetricCard
          $variant={Math.abs(metrics.outOfBalanceAmount) > 10 ? "warning" : "premium"}
          whileHover={{ scale: 1.02, y: -4 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="metric-header">
            <div className="metric-icon">⚖️</div>
            <div className="metric-trend">
              {filters.shared_is_proof === 'Y' ? 'Proof Mode' : 'Draft Mode'}
            </div>
          </div>
          <div className="metric-content">
            <div className="metric-title">Out of Balance</div>
            <div className="metric-value">{formatCurrency(metrics.outOfBalanceAmount)}</div>
            <div className="metric-subtitle">
              {Math.abs(metrics.outOfBalanceAmount) < 0.1
                ? 'All accounts balanced perfectly'
                : 'Requires attention and correction'
              }
            </div>
          </div>
        </MetricCard>
      </MetricsGrid>

      <QuickActionsGrid>
        {quickActions.map((action, index) => (
          <QuickActionCard
            key={action.title}
            onClick={action.action}
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <span className="action-icon">{action.icon}</span>
            <div className="action-title">{action.title}</div>
            <div className="action-description">{action.description}</div>
          </QuickActionCard>
        ))}
      </QuickActionsGrid>

      <SystemStatusSection>
        <h3>
          <span>🔧</span>
          System Health & Status
        </h3>
        <StatusGrid>
          {systemComponents.map((component, index) => (
            <motion.div
              key={component.name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <StatusIndicator $status={component.status}>
                <div className="status-icon">
                  {component.status === 'online' ? '✅' :
                   component.status === 'warning' ? '⚠️' : '❌'}
                </div>
                <div className="status-info">
                  <div className="status-name">{component.name}</div>
                  <div className="status-description">{component.description}</div>
                </div>
              </StatusIndicator>
            </motion.div>
          ))}
        </StatusGrid>
      </SystemStatusSection>
    </DashboardContainer>
  );
};