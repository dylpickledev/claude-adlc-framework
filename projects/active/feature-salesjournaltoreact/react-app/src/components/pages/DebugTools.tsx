// GraniteRock Sales Journal - Debug Tools Page
// Premium development and debugging utilities

import React, { useState, useEffect } from 'react';
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

  .warning-banner {
    background: linear-gradient(135deg, ${({ theme }) => theme.colors.semantic.warning}20 0%, ${({ theme }) => theme.colors.semantic.warning}10 100%);
    border: 1px solid ${({ theme }) => theme.colors.semantic.warning};
    border-radius: ${({ theme }) => theme.borderRadius.lg};
    padding: ${({ theme }) => theme.spacing[4]};
    margin-top: ${({ theme }) => theme.spacing[4]};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[3]};

    .warning-icon {
      font-size: 1.5rem;
      color: ${({ theme }) => theme.colors.semantic.warning};
    }

    .warning-text {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      color: ${({ theme }) => theme.colors.semantic.warning};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
    }
  }
`;

const DebugGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: ${({ theme }) => theme.spacing[6]};
  margin-bottom: ${({ theme }) => theme.spacing[8]};
`;

const DebugPanel = styled(motion.div)`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  overflow: hidden;

  .panel-header {
    background: linear-gradient(135deg, ${({ theme }) => theme.colors.primary.darkGreen} 0%, ${({ theme }) => theme.colors.primary.mediumGreen} 100%);
    color: white;
    padding: ${({ theme }) => theme.spacing[4]};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[2]};

    .panel-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.lg};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    }

    .panel-icon {
      font-size: 1.2rem;
    }
  }

  .panel-content {
    padding: ${({ theme }) => theme.spacing[6]};
  }
`;

const StateInspector = styled.div`
  .state-item {
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    padding: ${({ theme }) => theme.spacing[3]};
    background: ${({ theme }) => theme.colors.primary.lightCyan}20;
    border-radius: ${({ theme }) => theme.borderRadius.md};
    border-left: 3px solid ${({ theme }) => theme.colors.primary.darkGreen};

    .state-label {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
      margin-bottom: ${({ theme }) => theme.spacing[2]};
    }

    .state-value {
      font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
      font-size: ${({ theme }) => theme.typography.fontSizes.xs};
      background: white;
      padding: ${({ theme }) => theme.spacing[2]};
      border-radius: ${({ theme }) => theme.borderRadius.sm};
      border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
      white-space: pre-wrap;
      max-height: 200px;
      overflow-y: auto;
    }
  }
`;

const LogViewer = styled.div`
  .log-controls {
    display: flex;
    gap: ${({ theme }) => theme.spacing[2]};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
  }

  .log-container {
    background: #1a1a1a;
    color: #e0e0e0;
    font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
    font-size: ${({ theme }) => theme.typography.fontSizes.xs};
    padding: ${({ theme }) => theme.spacing[4]};
    border-radius: ${({ theme }) => theme.borderRadius.md};
    height: 300px;
    overflow-y: auto;
    border: 1px solid ${({ theme }) => theme.colors.primary.grayGreen};

    .log-entry {
      margin-bottom: ${({ theme }) => theme.spacing[1]};
      padding: ${({ theme }) => theme.spacing[1]} 0;
      border-bottom: 1px solid #333;

      .log-timestamp {
        color: #888;
        margin-right: ${({ theme }) => theme.spacing[2]};
      }

      .log-level {
        margin-right: ${({ theme }) => theme.spacing[2]};
        font-weight: bold;

        &.info { color: #4CAF50; }
        &.warn { color: #FF9800; }
        &.error { color: #F44336; }
        &.debug { color: #2196F3; }
      }

      .log-message {
        color: #e0e0e0;
      }
    }
  }
`;

const ActionButton = styled(motion.button)<{ variant?: 'primary' | 'secondary' | 'danger' }>`
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

const PerformanceMetrics = styled.div`
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: ${({ theme }) => theme.spacing[3]};
  }

  .metric-item {
    text-align: center;
    padding: ${({ theme }) => theme.spacing[3]};
    background: ${({ theme }) => theme.colors.primary.lightCyan}20;
    border-radius: ${({ theme }) => theme.borderRadius.md};

    .metric-value {
      font-size: ${({ theme }) => theme.typography.fontSizes.lg};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
      font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
      color: ${({ theme }) => theme.colors.primary.darkGreen};
      margin-bottom: ${({ theme }) => theme.spacing[1]};
    }

    .metric-label {
      font-size: ${({ theme }) => theme.typography.fontSizes.xs};
      color: ${({ theme }) => theme.colors.primary.darkGray};
      text-transform: uppercase;
      letter-spacing: ${({ theme }) => theme.typography.letterSpacing.wide};
    }
  }
`;

const APITester = styled.div`
  .api-form {
    display: flex;
    flex-direction: column;
    gap: ${({ theme }) => theme.spacing[3]};
    margin-bottom: ${({ theme }) => theme.spacing[4]};

    .form-group {
      display: flex;
      flex-direction: column;
      gap: ${({ theme }) => theme.spacing[1]};

      label {
        font-size: ${({ theme }) => theme.typography.fontSizes.sm};
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        color: ${({ theme }) => theme.colors.primary.darkGreen};
      }

      select, input, textarea {
        padding: ${({ theme }) => theme.spacing[2]};
        border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
        border-radius: ${({ theme }) => theme.borderRadius.md};
        font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
        font-size: ${({ theme }) => theme.typography.fontSizes.sm};

        &:focus {
          outline: none;
          border-color: ${({ theme }) => theme.colors.primary.darkGreen};
        }
      }

      textarea {
        min-height: 100px;
        resize: vertical;
      }
    }
  }

  .api-response {
    background: #1a1a1a;
    color: #e0e0e0;
    font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
    font-size: ${({ theme }) => theme.typography.fontSizes.xs};
    padding: ${({ theme }) => theme.spacing[4]};
    border-radius: ${({ theme }) => theme.borderRadius.md};
    min-height: 200px;
    overflow-y: auto;
    border: 1px solid ${({ theme }) => theme.colors.primary.grayGreen};
    white-space: pre-wrap;
  }
`;

interface LogEntry {
  timestamp: string;
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
}

interface PerformanceData {
  renderTime: number;
  apiResponseTime: number;
  memoryUsage: number;
  componentCount: number;
  rerenderCount: number;
  cacheHitRate: number;
}

export const DebugTools: React.FC = () => {
  const store = useFinancialStore();
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [performance, setPerformance] = useState<PerformanceData | null>(null);
  const [apiEndpoint, setApiEndpoint] = useState('/health');
  const [apiMethod, setApiMethod] = useState('GET');
  const [apiPayload, setApiPayload] = useState('');
  const [apiResponse, setApiResponse] = useState('');
  const [logLevel, setLogLevel] = useState<'all' | 'info' | 'warn' | 'error' | 'debug'>('all');

  // Mock performance data
  const mockPerformance: PerformanceData = {
    renderTime: 23.4,
    apiResponseTime: 156,
    memoryUsage: 45.2,
    componentCount: 847,
    rerenderCount: 12,
    cacheHitRate: 94.7,
  };

  // Mock log entries
  const mockLogs: LogEntry[] = [
    {
      timestamp: new Date().toISOString(),
      level: 'info',
      message: 'Application initialized successfully',
    },
    {
      timestamp: new Date(Date.now() - 30000).toISOString(),
      level: 'debug',
      message: 'Loading financial data from API endpoint',
    },
    {
      timestamp: new Date(Date.now() - 45000).toISOString(),
      level: 'warn',
      message: 'Cache miss for out-of-balance data, fetching from server',
    },
    {
      timestamp: new Date(Date.now() - 60000).toISOString(),
      level: 'error',
      message: 'Failed to connect to Snowflake instance, retrying...',
    },
    {
      timestamp: new Date(Date.now() - 90000).toISOString(),
      level: 'info',
      message: 'User authenticated successfully',
    },
  ];

  useEffect(() => {
    setPerformance(mockPerformance);
    setLogs(mockLogs);

    // Simulate real-time log updates
    const logInterval = setInterval(() => {
      const newLog: LogEntry = {
        timestamp: new Date().toISOString(),
        level: ['info', 'warn', 'error', 'debug'][Math.floor(Math.random() * 4)] as LogEntry['level'],
        message: [
          'Data refresh completed',
          'Cache updated successfully',
          'API request processed',
          'Component rendered',
          'Filter applied',
          'Export generated',
        ][Math.floor(Math.random() * 6)],
      };

      setLogs(prev => [newLog, ...prev.slice(0, 49)]); // Keep last 50 logs
    }, 5000);

    return () => clearInterval(logInterval);
  }, []);

  const handleClearState = () => {
    console.log('Clearing application state...');
    localStorage.clear();
    sessionStorage.clear();
    window.location.reload();
  };

  const handleTestAPI = async () => {
    setApiResponse('Loading...');

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      const mockResponse = {
        status: 200,
        timestamp: new Date().toISOString(),
        endpoint: apiEndpoint,
        method: apiMethod,
        data: {
          message: 'API test successful',
          version: '1.0.0',
          uptime: '24h 15m',
        },
      };

      setApiResponse(JSON.stringify(mockResponse, null, 2));
    } catch (error) {
      setApiResponse(`Error: ${error}`);
    }
  };

  const handleExportState = () => {
    const stateData = {
      store: store,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent,
    };

    const blob = new Blob([JSON.stringify(stateData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `debug-state-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const filteredLogs = logLevel === 'all' ? logs : logs.filter(log => log.level === logLevel);

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <div className="page-title">
          🛠️ Debug Tools
        </div>
        <div className="page-subtitle">
          Development and debugging utilities for troubleshooting application issues,
          monitoring performance, and testing system integrations.
        </div>
        <div className="warning-banner">
          <div className="warning-icon">⚠️</div>
          <div className="warning-text">
            These tools are intended for development and debugging purposes only.
            Use with caution in production environments.
          </div>
        </div>
      </PageHeader>

      <DebugGrid>
        <DebugPanel
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <div className="panel-header">
            <div className="panel-icon">🔍</div>
            <div className="panel-title">State Inspector</div>
          </div>
          <div className="panel-content">
            <StateInspector>
              <div className="state-item">
                <div className="state-label">Current Filters</div>
                <div className="state-value">
                  {JSON.stringify(store.filters, null, 2)}
                </div>
              </div>
              <div className="state-item">
                <div className="state-label">Loading States</div>
                <div className="state-value">
                  {JSON.stringify({
                    isLoading: store.isLoading,
                    lastUpdated: store.lastUpdated,
                  }, null, 2)}
                </div>
              </div>
              <div className="state-item">
                <div className="state-label">Active Tab</div>
                <div className="state-value">
                  {store.activeTab}
                </div>
              </div>
            </StateInspector>
            <div style={{ display: 'flex', gap: '8px', marginTop: '16px' }}>
              <ActionButton
                variant="secondary"
                onClick={handleExportState}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                📁 Export State
              </ActionButton>
              <ActionButton
                variant="danger"
                onClick={handleClearState}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                🗑️ Clear State
              </ActionButton>
            </div>
          </div>
        </DebugPanel>

        <DebugPanel
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.2 }}
        >
          <div className="panel-header">
            <div className="panel-icon">📊</div>
            <div className="panel-title">Performance Metrics</div>
          </div>
          <div className="panel-content">
            {performance && (
              <PerformanceMetrics>
                <div className="metrics-grid">
                  <div className="metric-item">
                    <div className="metric-value">{performance.renderTime}ms</div>
                    <div className="metric-label">Render Time</div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-value">{performance.apiResponseTime}ms</div>
                    <div className="metric-label">API Response</div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-value">{performance.memoryUsage}MB</div>
                    <div className="metric-label">Memory Usage</div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-value">{formatNumber(performance.componentCount)}</div>
                    <div className="metric-label">Components</div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-value">{performance.rerenderCount}</div>
                    <div className="metric-label">Re-renders</div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-value">{performance.cacheHitRate}%</div>
                    <div className="metric-label">Cache Hits</div>
                  </div>
                </div>
              </PerformanceMetrics>
            )}
          </div>
        </DebugPanel>

        <DebugPanel
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.3 }}
        >
          <div className="panel-header">
            <div className="panel-icon">📝</div>
            <div className="panel-title">Application Logs</div>
          </div>
          <div className="panel-content">
            <LogViewer>
              <div className="log-controls">
                <select value={logLevel} onChange={(e) => setLogLevel(e.target.value as any)}>
                  <option value="all">All Levels</option>
                  <option value="info">Info</option>
                  <option value="warn">Warnings</option>
                  <option value="error">Errors</option>
                  <option value="debug">Debug</option>
                </select>
                <ActionButton
                  variant="secondary"
                  onClick={() => setLogs([])}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  Clear Logs
                </ActionButton>
              </div>
              <div className="log-container">
                {filteredLogs.map((log, index) => (
                  <div key={index} className="log-entry">
                    <span className="log-timestamp">
                      {formatTimestamp(log.timestamp)}
                    </span>
                    <span className={`log-level ${log.level}`}>
                      [{log.level.toUpperCase()}]
                    </span>
                    <span className="log-message">
                      {log.message}
                    </span>
                  </div>
                ))}
              </div>
            </LogViewer>
          </div>
        </DebugPanel>

        <DebugPanel
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3, delay: 0.4 }}
        >
          <div className="panel-header">
            <div className="panel-icon">🔌</div>
            <div className="panel-title">API Testing</div>
          </div>
          <div className="panel-content">
            <APITester>
              <div className="api-form">
                <div className="form-group">
                  <label htmlFor="api-method">HTTP Method</label>
                  <select
                    id="api-method"
                    value={apiMethod}
                    onChange={(e) => setApiMethod(e.target.value)}
                  >
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                    <option value="PUT">PUT</option>
                    <option value="DELETE">DELETE</option>
                  </select>
                </div>
                <div className="form-group">
                  <label htmlFor="api-endpoint">Endpoint</label>
                  <input
                    id="api-endpoint"
                    type="text"
                    value={apiEndpoint}
                    onChange={(e) => setApiEndpoint(e.target.value)}
                    placeholder="/api/endpoint"
                  />
                </div>
                {(apiMethod === 'POST' || apiMethod === 'PUT') && (
                  <div className="form-group">
                    <label htmlFor="api-payload">Request Body (JSON)</label>
                    <textarea
                      id="api-payload"
                      value={apiPayload}
                      onChange={(e) => setApiPayload(e.target.value)}
                      placeholder='{"key": "value"}'
                    />
                  </div>
                )}
                <ActionButton
                  variant="primary"
                  onClick={handleTestAPI}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  🚀 Send Request
                </ActionButton>
              </div>
              <div className="api-response">
                {apiResponse || 'No response yet. Click "Send Request" to test an API endpoint.'}
              </div>
            </APITester>
          </div>
        </DebugPanel>
      </DebugGrid>
    </PageContainer>
  );
};