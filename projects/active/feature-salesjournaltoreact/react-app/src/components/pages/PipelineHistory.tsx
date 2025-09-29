// GraniteRock Sales Journal - Pipeline History Page
// Premium pipeline execution history and analytics

import React, { useState, useEffect, useMemo } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useFinancialStore } from '../../store/financialStore';
import { formatTimestamp, formatNumber } from '../../utils/formatters';

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

const FilterBar = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  margin-bottom: ${({ theme }) => theme.spacing[6]};

  .filter-header {
    font-size: ${({ theme }) => theme.typography.fontSizes.lg};
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[2]};
  }

  .filter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: ${({ theme }) => theme.spacing[4]};
    align-items: end;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: ${({ theme }) => theme.spacing[2]};

    label {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
    }

    select, input {
      padding: ${({ theme }) => theme.spacing[2]} ${({ theme }) => theme.spacing[3]};
      border: 2px solid ${({ theme }) => theme.colors.primary.lightCyan};
      border-radius: ${({ theme }) => theme.borderRadius.md};
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      transition: all ${({ theme }) => theme.animations.transitions.base};

      &:focus {
        outline: none;
        border-color: ${({ theme }) => theme.colors.primary.darkGreen};
        box-shadow: 0 0 0 3px ${({ theme }) => theme.colors.primary.darkGreen}20;
      }
    }
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${({ theme }) => theme.spacing[4]};
  margin-bottom: ${({ theme }) => theme.spacing[6]};
`;

const StatCard = styled(motion.div)`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius.xl};
  padding: ${({ theme }) => theme.spacing[4]};
  box-shadow: ${({ theme }) => theme.shadows.lg};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};

  .stat-header {
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[2]};
    margin-bottom: ${({ theme }) => theme.spacing[3]};

    .stat-icon {
      font-size: 1.5rem;
    }

    .stat-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
    }
  }

  .stat-value {
    font-size: ${({ theme }) => theme.typography.fontSizes['2xl']};
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
    margin-bottom: ${({ theme }) => theme.spacing[1]};
  }

  .stat-change {
    font-size: ${({ theme }) => theme.typography.fontSizes.xs};
    color: ${({ theme }) => theme.colors.primary.grayGreen};
  }
`;

const HistoryContainer = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  overflow: hidden;

  .history-header {
    background: linear-gradient(135deg, ${({ theme }) => theme.colors.primary.darkGreen} 0%, ${({ theme }) => theme.colors.primary.mediumGreen} 100%);
    color: white;
    padding: ${({ theme }) => theme.spacing[6]};
    display: flex;
    justify-content: space-between;
    align-items: center;

    .history-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.xl};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    }

    .history-count {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      opacity: 0.9;
    }
  }

  .history-table {
    overflow-x: auto;
    max-height: 600px;
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
        font-size: ${({ theme }) => theme.typography.fontSizes.sm};

        &.pipeline-name {
          font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
          color: ${({ theme }) => theme.colors.primary.darkGreen};
        }

        &.status {
          text-align: center;
        }

        &.duration {
          font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
          text-align: right;
        }

        &.timestamp {
          font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
          font-size: ${({ theme }) => theme.typography.fontSizes.xs};
          color: ${({ theme }) => theme.colors.primary.grayGreen};
        }
      }

      tr:hover {
        background: ${({ theme }) => theme.colors.primary.lightCyan}30;
      }
    }
  }
`;

const StatusBadge = styled.span<{ status: string }>`
  display: inline-flex;
  align-items: center;
  gap: ${({ theme }) => theme.spacing[1]};
  padding: ${({ theme }) => theme.spacing[1]} ${({ theme }) => theme.spacing[2]};
  border-radius: ${({ theme }) => theme.borderRadius.full};
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  text-transform: uppercase;
  letter-spacing: ${({ theme }) => theme.typography.letterSpacing.wide};
  background: ${({ status, theme }) => {
    switch (status) {
      case 'success': return theme.colors.semantic.success + '20';
      case 'failed': return theme.colors.semantic.error + '20';
      case 'running': return theme.colors.primary.orange + '20';
      case 'cancelled': return theme.colors.primary.grayGreen + '20';
      default: return theme.colors.primary.lightCyan;
    }
  }};
  color: ${({ status, theme }) => {
    switch (status) {
      case 'success': return theme.colors.semantic.success;
      case 'failed': return theme.colors.semantic.error;
      case 'running': return theme.colors.primary.orange;
      case 'cancelled': return theme.colors.primary.grayGreen;
      default: return theme.colors.primary.darkGray;
    }
  }};
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

interface PipelineExecution {
  id: string;
  pipelineName: string;
  type: 'dbt' | 'airbyte' | 'prefect' | 'custom';
  status: 'success' | 'failed' | 'running' | 'cancelled';
  startTime: string;
  endTime?: string;
  duration: string;
  triggeredBy: 'schedule' | 'manual' | 'api' | 'webhook';
  runId: string;
}

export const PipelineHistory: React.FC = () => {
  const { isLoading } = useFinancialStore();
  const [executions, setExecutions] = useState<PipelineExecution[]>([]);
  const [filters, setFilters] = useState({
    pipeline: 'all',
    status: 'all',
    type: 'all',
    dateRange: '7d',
  });

  // Mock execution data
  const mockExecutions: PipelineExecution[] = [
    {
      id: 'exec-001',
      pipelineName: 'Sales Journal ETL',
      type: 'dbt',
      status: 'success',
      startTime: '2024-01-15T06:00:00Z',
      endTime: '2024-01-15T06:12:34Z',
      duration: '12m 34s',
      triggeredBy: 'schedule',
      runId: 'dbt-20240115-060000',
    },
    {
      id: 'exec-002',
      pipelineName: 'Customer Data Sync',
      type: 'airbyte',
      status: 'success',
      startTime: '2024-01-15T05:30:00Z',
      endTime: '2024-01-15T05:35:12Z',
      duration: '5m 12s',
      triggeredBy: 'schedule',
      runId: 'airbyte-20240115-053000',
    },
    {
      id: 'exec-003',
      pipelineName: 'Financial Reconciliation',
      type: 'prefect',
      status: 'failed',
      startTime: '2024-01-15T04:00:00Z',
      endTime: '2024-01-15T04:08:45Z',
      duration: '8m 45s',
      triggeredBy: 'schedule',
      runId: 'prefect-20240115-040000',
    },
    {
      id: 'exec-004',
      pipelineName: 'Data Quality Checks',
      type: 'custom',
      status: 'success',
      startTime: '2024-01-15T03:15:00Z',
      endTime: '2024-01-15T03:18:21Z',
      duration: '3m 21s',
      triggeredBy: 'manual',
      runId: 'custom-20240115-031500',
    },
    {
      id: 'exec-005',
      pipelineName: 'Report Generation',
      type: 'dbt',
      status: 'success',
      startTime: '2024-01-15T02:00:00Z',
      endTime: '2024-01-15T02:06:18Z',
      duration: '6m 18s',
      triggeredBy: 'schedule',
      runId: 'dbt-20240115-020000',
    },
    {
      id: 'exec-006',
      pipelineName: 'Backup Operations',
      type: 'custom',
      status: 'cancelled',
      startTime: '2024-01-14T23:00:00Z',
      endTime: '2024-01-14T23:10:00Z',
      duration: '10m 0s',
      triggeredBy: 'schedule',
      runId: 'custom-20240114-230000',
    },
  ];

  useEffect(() => {
    setExecutions(mockExecutions);
  }, []);

  const filteredExecutions = useMemo(() => {
    return executions.filter(execution => {
      if (filters.pipeline !== 'all' && execution.pipelineName !== filters.pipeline) {
        return false;
      }
      if (filters.status !== 'all' && execution.status !== filters.status) {
        return false;
      }
      if (filters.type !== 'all' && execution.type !== filters.type) {
        return false;
      }
      return true;
    });
  }, [executions, filters]);

  const statistics = useMemo(() => {
    const total = filteredExecutions.length;
    const successful = filteredExecutions.filter(e => e.status === 'success').length;
    const failed = filteredExecutions.filter(e => e.status === 'failed').length;
    const running = filteredExecutions.filter(e => e.status === 'running').length;
    const successRate = total > 0 ? (successful / total) * 100 : 0;

    // Calculate average duration (convert duration strings to minutes)
    const durations = filteredExecutions
      .filter(e => e.duration && e.status !== 'running')
      .map(e => {
        const match = e.duration.match(/(\d+)m\s*(\d+)s/);
        if (match) {
          return parseInt(match[1]) + parseInt(match[2]) / 60;
        }
        return 0;
      });

    const avgDuration = durations.length > 0
      ? durations.reduce((sum, dur) => sum + dur, 0) / durations.length
      : 0;

    return {
      total,
      successful,
      failed,
      running,
      successRate,
      avgDuration: `${Math.floor(avgDuration)}m ${Math.round((avgDuration % 1) * 60)}s`,
    };
  }, [filteredExecutions]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success': return '✅';
      case 'failed': return '❌';
      case 'running': return '🔄';
      case 'cancelled': return '⏹️';
      default: return '❓';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'dbt': return '🔨';
      case 'airbyte': return '🔄';
      case 'prefect': return '🌊';
      case 'custom': return '⚙️';
      default: return '❓';
    }
  };

  const getTriggerIcon = (trigger: string) => {
    switch (trigger) {
      case 'schedule': return '⏰';
      case 'manual': return '👤';
      case 'api': return '🔌';
      case 'webhook': return '🪝';
      default: return '❓';
    }
  };

  // Get unique pipeline names for filter dropdown
  const uniquePipelines = [...new Set(executions.map(e => e.pipelineName))];

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <div className="page-title">
          📊 Pipeline Execution History
        </div>
        <div className="page-subtitle">
          Track and analyze pipeline execution history, performance metrics, and success rates.
          Monitor trends and identify issues across all automated workflows.
        </div>
      </PageHeader>

      <FilterBar>
        <div className="filter-header">
          🔍 Filter & Search
        </div>
        <div className="filter-grid">
          <div className="filter-group">
            <label htmlFor="pipeline-filter">Pipeline</label>
            <select
              id="pipeline-filter"
              value={filters.pipeline}
              onChange={(e) => setFilters(prev => ({ ...prev, pipeline: e.target.value }))}
            >
              <option value="all">All Pipelines</option>
              {uniquePipelines.map(pipeline => (
                <option key={pipeline} value={pipeline}>{pipeline}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="status-filter">Status</label>
            <select
              id="status-filter"
              value={filters.status}
              onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
            >
              <option value="all">All Statuses</option>
              <option value="success">Success</option>
              <option value="failed">Failed</option>
              <option value="running">Running</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="type-filter">Type</label>
            <select
              id="type-filter"
              value={filters.type}
              onChange={(e) => setFilters(prev => ({ ...prev, type: e.target.value }))}
            >
              <option value="all">All Types</option>
              <option value="dbt">dbt</option>
              <option value="airbyte">Airbyte</option>
              <option value="prefect">Prefect</option>
              <option value="custom">Custom</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="date-filter">Date Range</label>
            <select
              id="date-filter"
              value={filters.dateRange}
              onChange={(e) => setFilters(prev => ({ ...prev, dateRange: e.target.value }))}
            >
              <option value="1d">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
            </select>
          </div>
        </div>
      </FilterBar>

      <StatsGrid>
        <StatCard
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <div className="stat-header">
            <div className="stat-icon">📊</div>
            <div className="stat-title">Total Executions</div>
          </div>
          <div className="stat-value">{formatNumber(statistics.total)}</div>
          <div className="stat-change">in selected period</div>
        </StatCard>

        <StatCard
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.2 }}
        >
          <div className="stat-header">
            <div className="stat-icon">✅</div>
            <div className="stat-title">Success Rate</div>
          </div>
          <div className="stat-value">{statistics.successRate.toFixed(1)}%</div>
          <div className="stat-change">{statistics.successful} successful</div>
        </StatCard>

        <StatCard
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.3 }}
        >
          <div className="stat-header">
            <div className="stat-icon">⏱️</div>
            <div className="stat-title">Avg Duration</div>
          </div>
          <div className="stat-value">{statistics.avgDuration}</div>
          <div className="stat-change">average execution time</div>
        </StatCard>

        <StatCard
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.4 }}
        >
          <div className="stat-header">
            <div className="stat-icon">❌</div>
            <div className="stat-title">Failed Runs</div>
          </div>
          <div className="stat-value">{formatNumber(statistics.failed)}</div>
          <div className="stat-change">requiring attention</div>
        </StatCard>
      </StatsGrid>

      <HistoryContainer>
        <div className="history-header">
          <div className="history-title">🕒 Execution History</div>
          <div className="history-count">
            {filteredExecutions.length} execution{filteredExecutions.length !== 1 ? 's' : ''} found
          </div>
        </div>

        {filteredExecutions.length > 0 ? (
          <div className="history-table">
            <table>
              <thead>
                <tr>
                  <th>Pipeline</th>
                  <th>Type</th>
                  <th>Status</th>
                  <th>Duration</th>
                  <th>Triggered By</th>
                  <th>Start Time</th>
                  <th>Run ID</th>
                </tr>
              </thead>
              <tbody>
                {filteredExecutions.map((execution) => (
                  <tr key={execution.id}>
                    <td className="pipeline-name">
                      {execution.pipelineName}
                    </td>
                    <td>
                      {getTypeIcon(execution.type)} {execution.type.toUpperCase()}
                    </td>
                    <td className="status">
                      <StatusBadge status={execution.status}>
                        {getStatusIcon(execution.status)}
                        {execution.status}
                      </StatusBadge>
                    </td>
                    <td className="duration">{execution.duration}</td>
                    <td>
                      {getTriggerIcon(execution.triggeredBy)} {execution.triggeredBy}
                    </td>
                    <td className="timestamp">
                      {formatTimestamp(execution.startTime)}
                    </td>
                    <td className="timestamp">{execution.runId}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState>
            <div className="empty-icon">📊</div>
            <div className="empty-title">No Executions Found</div>
            <div className="empty-description">
              No pipeline executions match your current filter criteria.
              Try adjusting the filters to see more results.
            </div>
          </EmptyState>
        )}
      </HistoryContainer>
    </PageContainer>
  );
};