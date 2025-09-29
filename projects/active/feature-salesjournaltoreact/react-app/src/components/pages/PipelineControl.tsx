// GraniteRock Sales Journal - Pipeline Control Page
// Premium workflow orchestration and pipeline management

import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { useFinancialStore } from '../../store/financialStore';
import { formatTimestamp } from '../../utils/formatters';

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

const PipelineGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: ${({ theme }) => theme.spacing[6]};
  margin-bottom: ${({ theme }) => theme.spacing[8]};
`;

const PipelineCard = styled(motion.div)<{ status: 'idle' | 'running' | 'success' | 'error' | 'warning' }>`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border-left: 6px solid ${({ status, theme }) => {
    switch (status) {
      case 'running': return theme.colors.primary.orange;
      case 'success': return theme.colors.semantic.success;
      case 'error': return theme.colors.semantic.error;
      case 'warning': return theme.colors.semantic.warning;
      default: return theme.colors.primary.grayGreen;
    }
  }};
  position: relative;
  overflow: hidden;

  .pipeline-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: ${({ theme }) => theme.spacing[4]};

    .pipeline-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.lg};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
    }

    .pipeline-status {
      display: flex;
      align-items: center;
      gap: ${({ theme }) => theme.spacing[2]};
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ status, theme }) => {
        switch (status) {
          case 'running': return theme.colors.primary.orange;
          case 'success': return theme.colors.semantic.success;
          case 'error': return theme.colors.semantic.error;
          case 'warning': return theme.colors.semantic.warning;
          default: return theme.colors.primary.grayGreen;
        }
      }};

      .status-icon {
        font-size: 1.2rem;
      }
    }
  }

  .pipeline-description {
    font-size: ${({ theme }) => theme.typography.fontSizes.sm};
    color: ${({ theme }) => theme.colors.primary.darkGray};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};
  }

  .pipeline-meta {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: ${({ theme }) => theme.spacing[3]};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    font-size: ${({ theme }) => theme.typography.fontSizes.xs};
    color: ${({ theme }) => theme.colors.primary.grayGreen};

    .meta-item {
      .label {
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        margin-bottom: ${({ theme }) => theme.spacing[1]};
      }
      .value {
        font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
      }
    }
  }

  .pipeline-actions {
    display: flex;
    gap: ${({ theme }) => theme.spacing[2]};
  }

  ${({ status }) => status === 'running' && `
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
  border-radius: ${({ theme }) => theme.borderRadius.md};
  padding: ${({ theme }) => theme.spacing[2]} ${({ theme }) => theme.spacing[4]};
  font-size: ${({ theme }) => theme.typography.fontSizes.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
  cursor: pointer;
  transition: all ${({ theme }) => theme.animations.transitions.base};
  flex: 1;

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

const GlobalControls = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  margin-bottom: ${({ theme }) => theme.spacing[6]};

  .controls-header {
    font-size: ${({ theme }) => theme.typography.fontSizes.xl};
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[2]};
  }

  .controls-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: ${({ theme }) => theme.spacing[4]};
  }
`;

const SystemStatus = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};

  .status-header {
    font-size: ${({ theme }) => theme.typography.fontSizes.xl};
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[2]};
  }

  .status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: ${({ theme }) => theme.spacing[4]};
  }

  .status-item {
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[3]};
    padding: ${({ theme }) => theme.spacing[3]};
    background: ${({ theme }) => theme.colors.primary.lightCyan}20;
    border-radius: ${({ theme }) => theme.borderRadius.lg};

    .status-icon {
      font-size: 1.5rem;
    }

    .status-content {
      .label {
        font-size: ${({ theme }) => theme.typography.fontSizes.sm};
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        color: ${({ theme }) => theme.colors.primary.darkGreen};
        margin-bottom: ${({ theme }) => theme.spacing[1]};
      }

      .value {
        font-size: ${({ theme }) => theme.typography.fontSizes.xs};
        color: ${({ theme }) => theme.colors.primary.darkGray};
        font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
      }
    }
  }
`;

interface Pipeline {
  id: string;
  name: string;
  description: string;
  status: 'idle' | 'running' | 'success' | 'error' | 'warning';
  lastRun: string;
  nextRun: string;
  duration: string;
  type: 'dbt' | 'airbyte' | 'prefect' | 'custom';
}

interface SystemHealth {
  orchestraStatus: 'healthy' | 'degraded' | 'down';
  dbtCloudStatus: 'healthy' | 'degraded' | 'down';
  snowflakeStatus: 'healthy' | 'degraded' | 'down';
  airbyteStatus: 'healthy' | 'degraded' | 'down';
  lastHealthCheck: string;
}

export const PipelineControl: React.FC = () => {
  const { isLoading } = useFinancialStore();
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Mock pipeline data
  const mockPipelines: Pipeline[] = [
    {
      id: 'sales-journal-etl',
      name: 'Sales Journal ETL',
      description: 'Daily sales data extraction, transformation, and loading process',
      status: 'success',
      lastRun: '2024-01-15T06:00:00Z',
      nextRun: '2024-01-16T06:00:00Z',
      duration: '12m 34s',
      type: 'dbt',
    },
    {
      id: 'customer-sync',
      name: 'Customer Data Sync',
      description: 'Synchronize customer information from ERP to data warehouse',
      status: 'running',
      lastRun: '2024-01-15T14:30:00Z',
      nextRun: '2024-01-15T18:30:00Z',
      duration: '5m 12s',
      type: 'airbyte',
    },
    {
      id: 'financial-reconciliation',
      name: 'Financial Reconciliation',
      description: 'Automated balance validation and out-of-balance detection',
      status: 'warning',
      lastRun: '2024-01-15T12:15:00Z',
      nextRun: '2024-01-15T16:15:00Z',
      duration: '8m 45s',
      type: 'prefect',
    },
    {
      id: 'data-quality-checks',
      name: 'Data Quality Checks',
      description: 'Comprehensive data validation and quality monitoring',
      status: 'error',
      lastRun: '2024-01-15T10:00:00Z',
      nextRun: '2024-01-15T14:00:00Z',
      duration: '3m 21s',
      type: 'custom',
    },
    {
      id: 'backup-operations',
      name: 'Backup Operations',
      description: 'Daily database backup and archival processes',
      status: 'idle',
      lastRun: '2024-01-14T23:00:00Z',
      nextRun: '2024-01-15T23:00:00Z',
      duration: '45m 12s',
      type: 'custom',
    },
    {
      id: 'report-generation',
      name: 'Report Generation',
      description: 'Generate and distribute automated financial reports',
      status: 'success',
      lastRun: '2024-01-15T07:30:00Z',
      nextRun: '2024-01-16T07:30:00Z',
      duration: '6m 18s',
      type: 'dbt',
    },
  ];

  const mockSystemHealth: SystemHealth = {
    orchestraStatus: 'healthy',
    dbtCloudStatus: 'healthy',
    snowflakeStatus: 'degraded',
    airbyteStatus: 'healthy',
    lastHealthCheck: new Date().toISOString(),
  };

  useEffect(() => {
    setPipelines(mockPipelines);
    setSystemHealth(mockSystemHealth);
  }, []);

  const getStatusIcon = (status: Pipeline['status']) => {
    switch (status) {
      case 'running': return '🔄';
      case 'success': return '✅';
      case 'error': return '❌';
      case 'warning': return '⚠️';
      default: return '⏸️';
    }
  };

  const getStatusText = (status: Pipeline['status']) => {
    switch (status) {
      case 'running': return 'Running';
      case 'success': return 'Success';
      case 'error': return 'Failed';
      case 'warning': return 'Warning';
      default: return 'Idle';
    }
  };

  const getTypeIcon = (type: Pipeline['type']) => {
    switch (type) {
      case 'dbt': return '🔨';
      case 'airbyte': return '🔄';
      case 'prefect': return '🌊';
      default: return '⚙️';
    }
  };

  const getHealthIcon = (status: SystemHealth[keyof Omit<SystemHealth, 'lastHealthCheck'>]) => {
    switch (status) {
      case 'healthy': return '✅';
      case 'degraded': return '⚠️';
      case 'down': return '❌';
      default: return '❓';
    }
  };

  const handlePipelineAction = async (pipelineId: string, action: 'run' | 'stop' | 'restart') => {
    console.log(`${action} pipeline:`, pipelineId);

    // Simulate action
    setPipelines(prev => prev.map(pipeline =>
      pipeline.id === pipelineId
        ? {
            ...pipeline,
            status: action === 'stop' ? 'idle' : 'running',
            lastRun: action !== 'stop' ? new Date().toISOString() : pipeline.lastRun
          }
        : pipeline
    ));

    // Simulate completion after delay
    if (action !== 'stop') {
      setTimeout(() => {
        setPipelines(prev => prev.map(pipeline =>
          pipeline.id === pipelineId
            ? { ...pipeline, status: 'success' }
            : pipeline
        ));
      }, 3000);
    }
  };

  const handleGlobalAction = async (action: 'refresh' | 'pause_all' | 'resume_all' | 'emergency_stop') => {
    setIsRefreshing(true);
    console.log('Global action:', action);

    // Simulate action
    await new Promise(resolve => setTimeout(resolve, 1000));

    if (action === 'refresh') {
      setSystemHealth({ ...mockSystemHealth, lastHealthCheck: new Date().toISOString() });
    }

    setIsRefreshing(false);
  };

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <div className="page-title">
          🎛️ Pipeline Control Center
        </div>
        <div className="page-subtitle">
          Monitor and control data pipeline executions. Manage Orchestra workflows,
          dbt transformations, Airbyte syncs, and custom automation processes.
        </div>
      </PageHeader>

      <GlobalControls>
        <div className="controls-header">
          🌐 Global Pipeline Controls
        </div>
        <div className="controls-grid">
          <ActionButton
            variant="primary"
            onClick={() => handleGlobalAction('refresh')}
            disabled={isRefreshing}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            🔄 Refresh All
          </ActionButton>
          <ActionButton
            variant="secondary"
            onClick={() => handleGlobalAction('pause_all')}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            ⏸️ Pause All
          </ActionButton>
          <ActionButton
            variant="secondary"
            onClick={() => handleGlobalAction('resume_all')}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            ▶️ Resume All
          </ActionButton>
          <ActionButton
            variant="danger"
            onClick={() => handleGlobalAction('emergency_stop')}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            🛑 Emergency Stop
          </ActionButton>
        </div>
      </GlobalControls>

      {systemHealth && (
        <SystemStatus>
          <div className="status-header">
            💓 System Health Monitor
          </div>
          <div className="status-grid">
            <div className="status-item">
              <div className="status-icon">{getHealthIcon(systemHealth.orchestraStatus)}</div>
              <div className="status-content">
                <div className="label">Orchestra</div>
                <div className="value">{systemHealth.orchestraStatus}</div>
              </div>
            </div>
            <div className="status-item">
              <div className="status-icon">{getHealthIcon(systemHealth.dbtCloudStatus)}</div>
              <div className="status-content">
                <div className="label">dbt Cloud</div>
                <div className="value">{systemHealth.dbtCloudStatus}</div>
              </div>
            </div>
            <div className="status-item">
              <div className="status-icon">{getHealthIcon(systemHealth.snowflakeStatus)}</div>
              <div className="status-content">
                <div className="label">Snowflake</div>
                <div className="value">{systemHealth.snowflakeStatus}</div>
              </div>
            </div>
            <div className="status-item">
              <div className="status-icon">{getHealthIcon(systemHealth.airbyteStatus)}</div>
              <div className="status-content">
                <div className="label">Airbyte</div>
                <div className="value">{systemHealth.airbyteStatus}</div>
              </div>
            </div>
          </div>
        </SystemStatus>
      )}

      <PipelineGrid>
        <AnimatePresence>
          {pipelines.map((pipeline) => (
            <PipelineCard
              key={pipeline.id}
              status={pipeline.status}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.3 }}
            >
              <div className="pipeline-header">
                <div className="pipeline-title">
                  {getTypeIcon(pipeline.type)} {pipeline.name}
                </div>
                <div className="pipeline-status">
                  <span className="status-icon">{getStatusIcon(pipeline.status)}</span>
                  {getStatusText(pipeline.status)}
                </div>
              </div>

              <div className="pipeline-description">
                {pipeline.description}
              </div>

              <div className="pipeline-meta">
                <div className="meta-item">
                  <div className="label">Last Run</div>
                  <div className="value">{formatTimestamp(pipeline.lastRun)}</div>
                </div>
                <div className="meta-item">
                  <div className="label">Next Run</div>
                  <div className="value">{formatTimestamp(pipeline.nextRun)}</div>
                </div>
                <div className="meta-item">
                  <div className="label">Duration</div>
                  <div className="value">{pipeline.duration}</div>
                </div>
                <div className="meta-item">
                  <div className="label">Type</div>
                  <div className="value">{pipeline.type.toUpperCase()}</div>
                </div>
              </div>

              <div className="pipeline-actions">
                <ActionButton
                  variant="primary"
                  onClick={() => handlePipelineAction(pipeline.id, 'run')}
                  disabled={pipeline.status === 'running'}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  ▶️ Run
                </ActionButton>
                <ActionButton
                  variant="secondary"
                  onClick={() => handlePipelineAction(pipeline.id, 'restart')}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  🔄 Restart
                </ActionButton>
                <ActionButton
                  variant="danger"
                  onClick={() => handlePipelineAction(pipeline.id, 'stop')}
                  disabled={pipeline.status === 'idle'}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  ⏹️ Stop
                </ActionButton>
              </div>
            </PipelineCard>
          ))}
        </AnimatePresence>
      </PipelineGrid>
    </PageContainer>
  );
};