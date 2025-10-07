// GraniteRock Sales Journal - Documentation Page
// Premium user guides and system documentation

import React, { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

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

const DocumentationLayout = styled.div`
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: ${({ theme }) => theme.spacing[6]};

  @media (max-width: ${({ theme }) => theme.breakpoints.lg}) {
    grid-template-columns: 1fr;
  }
`;

const NavigationSidebar = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  padding: ${({ theme }) => theme.spacing[6]};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  height: fit-content;

  .nav-title {
    font-size: ${({ theme }) => theme.typography.fontSizes.lg};
    font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    color: ${({ theme }) => theme.colors.primary.darkGreen};
    margin-bottom: ${({ theme }) => theme.spacing[4]};
    display: flex;
    align-items: center;
    gap: ${({ theme }) => theme.spacing[2]};
  }

  .nav-section {
    margin-bottom: ${({ theme }) => theme.spacing[4]};

    .section-title {
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
      color: ${({ theme }) => theme.colors.primary.darkGray};
      margin-bottom: ${({ theme }) => theme.spacing[2]};
      text-transform: uppercase;
      letter-spacing: ${({ theme }) => theme.typography.letterSpacing.wide};
    }

    .nav-list {
      list-style: none;
      padding: 0;
      margin: 0;

      .nav-item {
        margin-bottom: ${({ theme }) => theme.spacing[1]};

        .nav-link {
          display: block;
          padding: ${({ theme }) => theme.spacing[2]} ${({ theme }) => theme.spacing[3]};
          border-radius: ${({ theme }) => theme.borderRadius.md};
          font-size: ${({ theme }) => theme.typography.fontSizes.sm};
          color: ${({ theme }) => theme.colors.primary.darkGray};
          text-decoration: none;
          transition: all ${({ theme }) => theme.animations.transitions.base};
          cursor: pointer;

          &:hover {
            background: ${({ theme }) => theme.colors.primary.lightCyan}40;
            color: ${({ theme }) => theme.colors.primary.darkGreen};
          }

          &.active {
            background: ${({ theme }) => theme.colors.primary.darkGreen};
            color: white;
            font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
          }
        }
      }
    }
  }
`;

const DocumentationContent = styled.div`
  background: white;
  border-radius: ${({ theme }) => theme.borderRadius['2xl']};
  box-shadow: ${({ theme }) => theme.shadows.xl};
  border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
  overflow: hidden;

  .content-header {
    background: linear-gradient(135deg, ${({ theme }) => theme.colors.primary.darkGreen} 0%, ${({ theme }) => theme.colors.primary.mediumGreen} 100%);
    color: white;
    padding: ${({ theme }) => theme.spacing[6]};

    .content-title {
      font-size: ${({ theme }) => theme.typography.fontSizes['2xl']};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
      margin-bottom: ${({ theme }) => theme.spacing[2]};
    }

    .content-subtitle {
      font-size: ${({ theme }) => theme.typography.fontSizes.base};
      opacity: 0.9;
    }
  }

  .content-body {
    padding: ${({ theme }) => theme.spacing[8]};
    line-height: ${({ theme }) => theme.typography.lineHeights.relaxed};

    h1, h2, h3, h4, h5, h6 {
      color: ${({ theme }) => theme.colors.primary.darkGreen};
      margin-bottom: ${({ theme }) => theme.spacing[4]};
      font-weight: ${({ theme }) => theme.typography.fontWeights.bold};
    }

    h1 { font-size: ${({ theme }) => theme.typography.fontSizes['2xl']}; }
    h2 { font-size: ${({ theme }) => theme.typography.fontSizes.xl}; }
    h3 { font-size: ${({ theme }) => theme.typography.fontSizes.lg}; }

    p {
      margin-bottom: ${({ theme }) => theme.spacing[4]};
      color: ${({ theme }) => theme.colors.primary.darkGray};
    }

    ul, ol {
      margin-bottom: ${({ theme }) => theme.spacing[4]};
      padding-left: ${({ theme }) => theme.spacing[6]};

      li {
        margin-bottom: ${({ theme }) => theme.spacing[2]};
        color: ${({ theme }) => theme.colors.primary.darkGray};
      }
    }

    .code-block {
      background: ${({ theme }) => theme.colors.primary.lightCyan}20;
      border: 1px solid ${({ theme }) => theme.colors.primary.lightCyan};
      border-radius: ${({ theme }) => theme.borderRadius.lg};
      padding: ${({ theme }) => theme.spacing[4]};
      margin: ${({ theme }) => theme.spacing[4]} 0;
      font-family: ${({ theme }) => theme.typography.fontFamilies.monospace};
      font-size: ${({ theme }) => theme.typography.fontSizes.sm};
      overflow-x: auto;
    }

    .info-box {
      background: linear-gradient(135deg, ${({ theme }) => theme.colors.primary.lightCyan}40 0%, ${({ theme }) => theme.colors.primary.lightCyan}20 100%);
      border-left: 4px solid ${({ theme }) => theme.colors.primary.darkGreen};
      border-radius: ${({ theme }) => theme.borderRadius.lg};
      padding: ${({ theme }) => theme.spacing[4]};
      margin: ${({ theme }) => theme.spacing[4]} 0;

      .info-title {
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        color: ${({ theme }) => theme.colors.primary.darkGreen};
        margin-bottom: ${({ theme }) => theme.spacing[2]};
      }
    }

    .warning-box {
      background: linear-gradient(135deg, ${({ theme }) => theme.colors.semantic.warning}20 0%, ${({ theme }) => theme.colors.semantic.warning}10 100%);
      border-left: 4px solid ${({ theme }) => theme.colors.semantic.warning};
      border-radius: ${({ theme }) => theme.borderRadius.lg};
      padding: ${({ theme }) => theme.spacing[4]};
      margin: ${({ theme }) => theme.spacing[4]} 0;

      .warning-title {
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        color: ${({ theme }) => theme.colors.semantic.warning};
        margin-bottom: ${({ theme }) => theme.spacing[2]};
      }
    }

    .success-box {
      background: linear-gradient(135deg, ${({ theme }) => theme.colors.semantic.success}20 0%, ${({ theme }) => theme.colors.semantic.success}10 100%);
      border-left: 4px solid ${({ theme }) => theme.colors.semantic.success};
      border-radius: ${({ theme }) => theme.borderRadius.lg};
      padding: ${({ theme }) => theme.spacing[4]};
      margin: ${({ theme }) => theme.spacing[4]} 0;

      .success-title {
        font-weight: ${({ theme }) => theme.typography.fontWeights.semibold};
        color: ${({ theme }) => theme.colors.semantic.success};
        margin-bottom: ${({ theme }) => theme.spacing[2]};
      }
    }
  }
`;

interface DocumentationSection {
  id: string;
  title: string;
  content: React.ReactNode;
}

const documentationSections: Record<string, DocumentationSection> = {
  'getting-started': {
    id: 'getting-started',
    title: 'Getting Started',
    content: (
      <>
        <h2>Welcome to GraniteRock Sales Journal</h2>
        <p>
          The GraniteRock Sales Journal is a premium financial dashboard application designed to provide
          comprehensive sales data analysis, financial reconciliation, and pipeline management capabilities.
        </p>

        <div className="info-box">
          <div className="info-title">📋 Prerequisites</div>
          <p>Before using the application, ensure you have:</p>
          <ul>
            <li>Valid GraniteRock credentials</li>
            <li>Access to the financial data systems</li>
            <li>Appropriate permissions for your role</li>
          </ul>
        </div>

        <h3>System Overview</h3>
        <p>
          The application consists of several integrated modules:
        </p>
        <ul>
          <li><strong>Dashboard:</strong> Executive-level financial metrics and KPIs</li>
          <li><strong>Sales Journal:</strong> Detailed transaction listing and analysis</li>
          <li><strong>Out of Balance:</strong> Financial reconciliation and variance monitoring</li>
          <li><strong>Pipeline Control:</strong> Data processing workflow management</li>
        </ul>

        <div className="success-box">
          <div className="success-title">✅ Quick Start</div>
          <p>
            New users should begin with the Dashboard tab to get an overview of the current
            financial status, then explore the Sales Journal for detailed transaction data.
          </p>
        </div>
      </>
    ),
  },
  'navigation': {
    id: 'navigation',
    title: 'Navigation Guide',
    content: (
      <>
        <h2>Application Navigation</h2>
        <p>
          The GraniteRock Sales Journal uses a modern sidebar navigation system with intelligent
          filtering and real-time status indicators.
        </p>

        <h3>Sidebar Features</h3>
        <ul>
          <li><strong>Page Navigation:</strong> Click any tab to switch between application modules</li>
          <li><strong>Status Indicators:</strong> Real-time badges show system health and alerts</li>
          <li><strong>Filter Controls:</strong> Apply filters that persist across all relevant pages</li>
          <li><strong>Quick Actions:</strong> Access frequently used functions directly from the sidebar</li>
        </ul>

        <div className="code-block">
          Navigation Shortcut Keys:
          - Ctrl+1: Dashboard
          - Ctrl+2: Sales Journal
          - Ctrl+3: Detail by Ticket
          - Ctrl+4: Out of Balance
          - Ctrl+R: Refresh current page
        </div>

        <h3>Filter System</h3>
        <p>
          The unified filter system allows you to apply consistent criteria across multiple views:
        </p>
        <ul>
          <li><strong>Batch Type:</strong> Filter by CASH, CREDIT, or INTRA transactions</li>
          <li><strong>Proof Mode:</strong> Toggle between proof and production data views</li>
          <li><strong>Date Ranges:</strong> Select specific time periods for analysis</li>
          <li><strong>Account Filters:</strong> Focus on specific account codes or ranges</li>
        </ul>

        <div className="warning-box">
          <div className="warning-title">⚠️ Filter Persistence</div>
          <p>
            Filters are automatically saved and will persist across browser sessions.
            Use the "Reset Filters" button to return to default settings.
          </p>
        </div>
      </>
    ),
  },
  'dashboard': {
    id: 'dashboard',
    title: 'Dashboard Usage',
    content: (
      <>
        <h2>Financial Dashboard</h2>
        <p>
          The Dashboard provides a comprehensive overview of financial performance with
          real-time metrics, trend analysis, and executive-level KPIs.
        </p>

        <h3>Key Metrics</h3>
        <ul>
          <li><strong>Total Sales Revenue:</strong> Aggregated sales across all channels and periods</li>
          <li><strong>Transaction Volume:</strong> Number of processed transactions and entries</li>
          <li><strong>Balance Status:</strong> Current reconciliation status and variance indicators</li>
          <li><strong>System Health:</strong> Real-time monitoring of data pipeline status</li>
        </ul>

        <h3>Interactive Charts</h3>
        <p>
          The dashboard includes several interactive visualization components:
        </p>
        <ul>
          <li><strong>Sales Trend Chart:</strong> Historical sales performance over time</li>
          <li><strong>Batch Type Distribution:</strong> Breakdown by payment method</li>
          <li><strong>Account Balance Summary:</strong> Current account standings</li>
          <li><strong>Pipeline Status Grid:</strong> Real-time workflow monitoring</li>
        </ul>

        <div className="info-box">
          <div className="info-title">💡 Pro Tip</div>
          <p>
            Hover over any chart element to see detailed tooltips with specific values and dates.
            Click on legend items to toggle data series visibility.
          </p>
        </div>

        <h3>Refresh and Updates</h3>
        <p>
          Dashboard data automatically refreshes every 5 minutes. You can force an immediate
          refresh using the refresh button or Ctrl+R shortcut.
        </p>
      </>
    ),
  },
  'export': {
    id: 'export',
    title: 'Export & Reports',
    content: (
      <>
        <h2>Export and Reporting</h2>
        <p>
          The application provides comprehensive export capabilities for generating reports
          and sharing data with stakeholders.
        </p>

        <h3>Available Export Formats</h3>
        <ul>
          <li><strong>PDF Reports:</strong> Professional formatted reports with GraniteRock branding</li>
          <li><strong>Excel Workbooks:</strong> Detailed spreadsheets with multiple data sheets</li>
          <li><strong>CSV Files:</strong> Raw data exports for further analysis</li>
        </ul>

        <h3>Export Options</h3>
        <p>
          When exporting data, you can customize the output:
        </p>
        <ul>
          <li><strong>Include Filters:</strong> Document the applied filter criteria</li>
          <li><strong>Summary Statistics:</strong> Add calculated totals and metrics</li>
          <li><strong>Date Range:</strong> Specify the data period covered</li>
          <li><strong>Format Preferences:</strong> Choose number formatting and layout options</li>
        </ul>

        <div className="code-block">
          Export File Naming Convention:
          - sales-journal-YYYY-MM-DD.pdf
          - financial-summary-YYYY-MM-DD.xlsx
          - transaction-data-YYYY-MM-DD.csv
        </div>

        <h3>Scheduled Reports</h3>
        <p>
          Set up automated report generation and delivery:
        </p>
        <ul>
          <li><strong>Daily Reports:</strong> End-of-day transaction summaries</li>
          <li><strong>Weekly Summaries:</strong> Comprehensive week-over-week analysis</li>
          <li><strong>Monthly Closeout:</strong> Full month financial reconciliation</li>
          <li><strong>Custom Schedules:</strong> Define your own reporting frequency</li>
        </ul>

        <div className="success-box">
          <div className="success-title">✅ Best Practices</div>
          <p>
            For large datasets, use CSV exports for maximum compatibility.
            PDF reports are ideal for executive presentations and formal documentation.
          </p>
        </div>
      </>
    ),
  },
  'troubleshooting': {
    id: 'troubleshooting',
    title: 'Troubleshooting',
    content: (
      <>
        <h2>Common Issues & Solutions</h2>
        <p>
          This section covers frequently encountered issues and their resolutions.
        </p>

        <h3>Data Loading Issues</h3>
        <div className="warning-box">
          <div className="warning-title">⚠️ Problem: Data not loading or appears stale</div>
          <p><strong>Solutions:</strong></p>
          <ul>
            <li>Check your internet connection</li>
            <li>Verify filter settings aren't too restrictive</li>
            <li>Try refreshing the page (Ctrl+R)</li>
            <li>Clear browser cache and cookies</li>
            <li>Contact IT support if issues persist</li>
          </ul>
        </div>

        <h3>Balance Discrepancies</h3>
        <div className="warning-box">
          <div className="warning-title">⚠️ Problem: Out of balance alerts or variances</div>
          <p><strong>Investigation Steps:</strong></p>
          <ul>
            <li>Check the Out of Balance page for detailed variance analysis</li>
            <li>Review recent pipeline execution history</li>
            <li>Verify source system connectivity</li>
            <li>Examine transaction details for anomalies</li>
            <li>Escalate to finance team if variances exceed tolerance</li>
          </ul>
        </div>

        <h3>Performance Issues</h3>
        <div className="info-box">
          <div className="info-title">💡 Optimizing Performance</div>
          <ul>
            <li>Use date range filters to limit data scope</li>
            <li>Close unused browser tabs</li>
            <li>Ensure browser is up to date</li>
            <li>Consider using Chrome or Firefox for best performance</li>
          </ul>
        </div>

        <h3>Export Problems</h3>
        <ul>
          <li><strong>Large Files:</strong> For datasets over 10,000 rows, use CSV format</li>
          <li><strong>PDF Issues:</strong> Ensure pop-up blockers are disabled</li>
          <li><strong>Excel Problems:</strong> Verify you have appropriate Excel version installed</li>
        </ul>

        <h3>Getting Help</h3>
        <div className="success-box">
          <div className="success-title">📞 Support Contacts</div>
          <ul>
            <li><strong>Technical Issues:</strong> IT Helpdesk - ext. 4357</li>
            <li><strong>Financial Questions:</strong> Finance Team - ext. 2891</li>
            <li><strong>Data Discrepancies:</strong> Data Analytics Team - ext. 5642</li>
            <li><strong>Emergency Issues:</strong> 24/7 Support - ext. 9999</li>
          </ul>
        </div>
      </>
    ),
  },
};

const navigationStructure = [
  {
    title: 'Getting Started',
    items: [
      { id: 'getting-started', label: 'Overview & Setup' },
      { id: 'navigation', label: 'Navigation Guide' },
    ],
  },
  {
    title: 'Application Modules',
    items: [
      { id: 'dashboard', label: 'Dashboard Usage' },
      { id: 'sales-journal', label: 'Sales Journal' },
      { id: 'balance-monitoring', label: 'Balance Monitoring' },
      { id: 'pipeline-control', label: 'Pipeline Control' },
    ],
  },
  {
    title: 'Advanced Features',
    items: [
      { id: 'export', label: 'Export & Reports' },
      { id: 'automation', label: 'Automation Setup' },
      { id: 'integrations', label: 'System Integrations' },
    ],
  },
  {
    title: 'Support',
    items: [
      { id: 'troubleshooting', label: 'Troubleshooting' },
      { id: 'faq', label: 'FAQ' },
      { id: 'release-notes', label: 'Release Notes' },
    ],
  },
];

export const Documentation: React.FC = () => {
  const [activeSection, setActiveSection] = useState('getting-started');

  const currentSection = documentationSections[activeSection] || documentationSections['getting-started'];

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <PageHeader>
        <div className="page-title">
          📚 Documentation & User Guides
        </div>
        <div className="page-subtitle">
          Comprehensive documentation, user guides, and troubleshooting resources
          for the GraniteRock Sales Journal application.
        </div>
      </PageHeader>

      <DocumentationLayout>
        <NavigationSidebar>
          <div className="nav-title">
            📖 Documentation
          </div>

          {navigationStructure.map((section) => (
            <div key={section.title} className="nav-section">
              <div className="section-title">{section.title}</div>
              <ul className="nav-list">
                {section.items.map((item) => (
                  <li key={item.id} className="nav-item">
                    <a
                      className={`nav-link ${activeSection === item.id ? 'active' : ''}`}
                      onClick={() => setActiveSection(item.id)}
                    >
                      {item.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </NavigationSidebar>

        <DocumentationContent>
          <div className="content-header">
            <div className="content-title">
              {currentSection.title}
            </div>
            <div className="content-subtitle">
              Complete guide and reference for this topic
            </div>
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={activeSection}
              className="content-body"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {currentSection.content}
            </motion.div>
          </AnimatePresence>
        </DocumentationContent>
      </DocumentationLayout>
    </PageContainer>
  );
};