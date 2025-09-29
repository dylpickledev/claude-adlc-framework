// GraniteRock Sales Journal - Premium Financial Data Table
// Enterprise-grade financial reporting with modern React architecture

import React, { useState, useMemo, useCallback, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { useTable, useSortBy, useFilters, Column } from 'react-table';
import { FixedSizeList as List } from 'react-window';
import { graniteRockTheme } from '../../theme/graniterock';
import { JournalEntry, ExportOptions } from '../../types/financial';
import { useFinancialStore } from '../../store/financialStore';
import { formatCurrency, formatNumber, downloadPDF, downloadExcel, downloadCSV } from '../../utils/formatters';

const PageContainer = styled(motion.div)`
  flex: 1;
  padding: ${graniteRockTheme.spacing[6]};
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
  margin-left: 280px; /* Sidebar width */
`;

const PageHeader = styled.div`
  display: flex;
  justify-content: between;
  align-items: center;
  margin-bottom: ${graniteRockTheme.spacing[8]};
  background: ${graniteRockTheme.components.card.background};
  border-radius: ${graniteRockTheme.borderRadius['2xl']};
  padding: ${graniteRockTheme.spacing[6]};
  box-shadow: ${graniteRockTheme.shadows.lg};
  border-left: 4px solid ${graniteRockTheme.colors.primary.orange};

  h1 {
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-size: ${graniteRockTheme.typography.fontSizes['3xl']};
    font-weight: ${graniteRockTheme.typography.fontWeights.black};
    color: ${graniteRockTheme.colors.primary.darkGreen};
    margin: 0;
    background: linear-gradient(135deg, ${graniteRockTheme.colors.primary.darkGreen} 0%, ${graniteRockTheme.colors.primary.mediumGreen} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitle {
    font-size: ${graniteRockTheme.typography.fontSizes.lg};
    font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
    color: ${graniteRockTheme.colors.primary.orange};
    margin-top: ${graniteRockTheme.spacing[2]};
  }
`;

const MetricsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: ${graniteRockTheme.spacing[6]};
  margin-bottom: ${graniteRockTheme.spacing[8]};
`;

const MetricCard = styled(motion.div)<{ $variant: 'primary' | 'secondary' | 'success' | 'warning' }>`
  background: ${props => {
    switch (props.$variant) {
      case 'success': return `linear-gradient(135deg, ${graniteRockTheme.colors.semantic.success} 0%, #16a34a 100%)`;
      case 'warning': return `linear-gradient(135deg, ${graniteRockTheme.colors.semantic.warning} 0%, #f59e0b 100%)`;
      case 'secondary': return `linear-gradient(135deg, ${graniteRockTheme.colors.primary.grayGreen} 0%, ${graniteRockTheme.colors.primary.lightCyan} 100%)`;
      default: return `linear-gradient(135deg, ${graniteRockTheme.colors.primary.darkGreen} 0%, ${graniteRockTheme.colors.primary.mediumGreen} 100%)`;
    }
  }};
  color: white;
  padding: ${graniteRockTheme.spacing[6]};
  border-radius: ${graniteRockTheme.borderRadius['2xl']};
  box-shadow: ${graniteRockTheme.shadows.lg};
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
    pointer-events: none;
  }

  .metric-icon {
    font-size: 2.5rem;
    margin-bottom: ${graniteRockTheme.spacing[3]};
    opacity: 0.9;
  }

  .metric-title {
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
    opacity: 0.9;
    margin-bottom: ${graniteRockTheme.spacing[2]};
    text-transform: uppercase;
    letter-spacing: ${graniteRockTheme.typography.letterSpacing.wide};
  }

  .metric-value {
    font-family: ${graniteRockTheme.typography.fontFamilies.monospace};
    font-size: ${graniteRockTheme.typography.fontSizes['2xl']};
    font-weight: ${graniteRockTheme.typography.fontWeights.bold};
    margin-bottom: ${graniteRockTheme.spacing[1]};
  }

  .metric-subtitle {
    font-size: ${graniteRockTheme.typography.fontSizes.xs};
    opacity: 0.8;
  }
`;

const ControlsSection = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${graniteRockTheme.spacing[6]};
  padding: ${graniteRockTheme.spacing[4]};
  background: white;
  border-radius: ${graniteRockTheme.borderRadius.xl};
  box-shadow: ${graniteRockTheme.shadows.md};
  border: 1px solid ${graniteRockTheme.colors.primary.lightCyan};
`;

const SearchInput = styled.input`
  flex: 1;
  max-width: 400px;
  padding: ${graniteRockTheme.spacing[3]} ${graniteRockTheme.spacing[4]};
  border: 1px solid ${graniteRockTheme.colors.primary.grayGreen};
  border-radius: ${graniteRockTheme.borderRadius.lg};
  font-size: ${graniteRockTheme.typography.fontSizes.sm};
  transition: all ${graniteRockTheme.animations.transitions.base};

  &:focus {
    outline: none;
    border-color: ${graniteRockTheme.colors.accessible.focusRing};
    box-shadow: 0 0 0 2px ${graniteRockTheme.colors.accessible.focusRing}25;
  }

  &::placeholder {
    color: ${graniteRockTheme.colors.primary.darkGray};
  }
`;

const ExportButtonGroup = styled.div`
  display: flex;
  gap: ${graniteRockTheme.spacing[2]};
`;

const ExportButton = styled(motion.button)<{ $variant: 'pdf' | 'excel' | 'csv' }>`
  background: ${props => {
    switch (props.$variant) {
      case 'pdf': return `linear-gradient(135deg, #dc2626 0%, #ef4444 100%)`;
      case 'excel': return `linear-gradient(135deg, #16a34a 0%, #22c55e 100%)`;
      default: return `linear-gradient(135deg, ${graniteRockTheme.colors.accessible.primaryAction} 0%, #4f46e5 100%)`;
    }
  }};
  color: white;
  border: none;
  border-radius: ${graniteRockTheme.borderRadius.lg};
  padding: ${graniteRockTheme.spacing[3]} ${graniteRockTheme.spacing[4]};
  font-family: ${graniteRockTheme.typography.fontFamilies.primary};
  font-size: ${graniteRockTheme.typography.fontSizes.sm};
  font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: ${graniteRockTheme.spacing[2]};
  transition: all ${graniteRockTheme.animations.transitions.base};

  &:hover {
    transform: translateY(-2px);
    box-shadow: ${graniteRockTheme.shadows.lg};
  }

  &:active {
    transform: translateY(0);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
`;

const TableContainer = styled.div`
  background: white;
  border-radius: ${graniteRockTheme.borderRadius['2xl']};
  box-shadow: ${graniteRockTheme.shadows.xl};
  overflow: hidden;
  border: 1px solid ${graniteRockTheme.colors.primary.lightCyan};
`;

const TableHeader = styled.div`
  background: linear-gradient(135deg, ${graniteRockTheme.colors.primary.darkGreen} 0%, ${graniteRockTheme.colors.primary.mediumGreen} 100%);
  color: white;
  padding: ${graniteRockTheme.spacing[4]} ${graniteRockTheme.spacing[6]};
  display: flex;
  justify-content: space-between;
  align-items: center;

  h3 {
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-size: ${graniteRockTheme.typography.fontSizes.lg};
    font-weight: ${graniteRockTheme.typography.fontWeights.bold};
    margin: 0;
  }

  .record-count {
    font-family: ${graniteRockTheme.typography.fontFamilies.monospace};
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    opacity: 0.9;
  }
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;

  th {
    background: ${graniteRockTheme.colors.primary.lightCyan};
    color: ${graniteRockTheme.colors.primary.darkGreen};
    padding: ${graniteRockTheme.spacing[4]} ${graniteRockTheme.spacing[6]};
    text-align: left;
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
    text-transform: uppercase;
    letter-spacing: ${graniteRockTheme.typography.letterSpacing.wide};
    cursor: pointer;
    transition: all ${graniteRockTheme.animations.transitions.base};
    position: relative;

    &:hover {
      background: ${graniteRockTheme.colors.primary.mediumGreen};
      color: white;
    }

    &[aria-sort="ascending"]::after,
    &[aria-sort="descending"]::after {
      content: '';
      position: absolute;
      right: ${graniteRockTheme.spacing[4]};
      top: 50%;
      transform: translateY(-50%);
      width: 0;
      height: 0;
    }

    &[aria-sort="ascending"]::after {
      border-left: 4px solid transparent;
      border-right: 4px solid transparent;
      border-bottom: 6px solid currentColor;
    }

    &[aria-sort="descending"]::after {
      border-left: 4px solid transparent;
      border-right: 4px solid transparent;
      border-top: 6px solid currentColor;
    }
  }

  td {
    padding: ${graniteRockTheme.spacing[4]} ${graniteRockTheme.spacing[6]};
    border-bottom: 1px solid ${graniteRockTheme.colors.primary.lightCyan};
    font-family: ${graniteRockTheme.typography.fontFamilies.monospace};
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    transition: all ${graniteRockTheme.animations.transitions.base};

    &.currency {
      text-align: right;
      font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
      color: ${graniteRockTheme.colors.primary.darkGreen};
    }

    &.number {
      text-align: right;
      font-family: ${graniteRockTheme.typography.fontFamilies.monospace};
    }

    &.invalid-account {
      text-align: center;
      font-weight: ${graniteRockTheme.typography.fontWeights.bold};

      &.invalid-yes {
        color: ${graniteRockTheme.colors.semantic.error};
        background: rgba(146, 0, 9, 0.1);
      }

      &.invalid-no {
        color: ${graniteRockTheme.colors.semantic.success};
      }
    }

    &.batch-type {
      font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
      text-transform: uppercase;

      &.batch-cash {
        color: ${graniteRockTheme.colors.semantic.success};
      }

      &.batch-credit {
        color: ${graniteRockTheme.colors.accessible.primaryAction};
      }

      &.batch-intra {
        color: ${graniteRockTheme.colors.primary.orange};
      }
    }
  }

  tbody tr {
    &:hover {
      background: rgba(182, 216, 204, 0.3);
      transform: scale(1.002);
    }

    &.invalid-row {
      background: rgba(146, 0, 9, 0.05);
      border-left: 3px solid ${graniteRockTheme.colors.semantic.error};
    }
  }
`;

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: ${graniteRockTheme.spacing[12]};
  color: ${graniteRockTheme.colors.primary.darkGray};

  .loading-spinner {
    width: 60px;
    height: 60px;
    border: 4px solid ${graniteRockTheme.colors.primary.lightCyan};
    border-top: 4px solid ${graniteRockTheme.colors.primary.orange};
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: ${graniteRockTheme.spacing[4]};
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .loading-text {
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-size: ${graniteRockTheme.typography.fontSizes.lg};
    font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
  }
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: ${graniteRockTheme.spacing[12]};
  color: ${graniteRockTheme.colors.primary.darkGray};

  .empty-icon {
    font-size: 4rem;
    margin-bottom: ${graniteRockTheme.spacing[4]};
    opacity: 0.5;
  }

  .empty-title {
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-size: ${graniteRockTheme.typography.fontSizes.xl};
    font-weight: ${graniteRockTheme.typography.fontWeights.bold};
    margin-bottom: ${graniteRockTheme.spacing[2]};
  }

  .empty-message {
    font-size: ${graniteRockTheme.typography.fontSizes.base};
    text-align: center;
    max-width: 400px;
    line-height: ${graniteRockTheme.typography.lineHeights.relaxed};
  }
`;

interface SalesJournalProps {
  className?: string;
}

export const SalesJournal: React.FC<SalesJournalProps> = ({ className }) => {
  const { journalData, isLoading, error, filters } = useFinancialStore();
  const [searchTerm, setSearchTerm] = useState('');

  // Calculate metrics from journal data
  const metrics = useMemo(() => {
    if (!journalData?.length) {
      return {
        totalEntries: 0,
        totalAmount: 0,
        validEntries: 0,
        invalidEntries: 0,
        averageAmount: 0
      };
    }

    const validEntries = journalData.filter(entry => entry.invalid_acount === 'N');
    const invalidEntries = journalData.filter(entry => entry.invalid_acount === 'Y');
    const totalAmount = journalData.reduce((sum, entry) => sum + entry.amount, 0);

    return {
      totalEntries: journalData.length,
      totalAmount,
      validEntries: validEntries.length,
      invalidEntries: invalidEntries.length,
      averageAmount: totalAmount / journalData.length
    };
  }, [journalData]);

  // Filter data based on search term
  const filteredData = useMemo(() => {
    if (!journalData?.length || !searchTerm) return journalData || [];

    return journalData.filter(entry =>
      entry.accountcode_adjusted.toLowerCase().includes(searchTerm.toLowerCase()) ||
      entry.batch_type.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [journalData, searchTerm]);

  // Table columns configuration
  const columns: Column<JournalEntry>[] = useMemo(() => [
    {
      Header: 'Account Code',
      accessor: 'accountcode_adjusted',
      Cell: ({ value }) => (
        <span className="account-code">{value}</span>
      )
    },
    {
      Header: 'Batch Type',
      accessor: 'batch_type',
      Cell: ({ value }) => (
        <span className={`batch-type batch-${value.toLowerCase()}`}>
          {value}
        </span>
      )
    },
    {
      Header: 'Invalid Account',
      accessor: 'invalid_acount',
      Cell: ({ value }) => (
        <span className={`invalid-account invalid-${value === 'Y' ? 'yes' : 'no'}`}>
          {value === 'Y' ? '❌ Yes' : '✅ No'}
        </span>
      )
    },
    {
      Header: 'Entry Qty',
      accessor: 'account_entry_qty',
      Cell: ({ value }) => (
        <span className="number">{formatNumber(value)}</span>
      )
    },
    {
      Header: 'Amount',
      accessor: 'amount',
      Cell: ({ value }) => (
        <span className="currency">{formatCurrency(value)}</span>
      )
    }
  ], []);

  // Table instance
  const tableInstance = useTable(
    {
      columns,
      data: filteredData,
    },
    useFilters,
    useSortBy
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow
  } = tableInstance;

  // Export handlers
  const handleExportPDF = useCallback(async () => {
    if (!filteredData?.length) return;

    const exportOptions: ExportOptions = {
      format: 'pdf',
      includeFilters: true,
      includeCharts: false
    };

    await downloadPDF(filteredData, filters, metrics.totalAmount, exportOptions);
  }, [filteredData, filters, metrics.totalAmount]);

  const handleExportExcel = useCallback(async () => {
    if (!filteredData?.length) return;

    const exportOptions: ExportOptions = {
      format: 'excel',
      includeFilters: true,
      includeCharts: true
    };

    await downloadExcel(filteredData, filters, exportOptions);
  }, [filteredData, filters]);

  const handleExportCSV = useCallback(() => {
    if (!filteredData?.length) return;

    downloadCSV(filteredData, 'sales-journal');
  }, [filteredData]);

  return (
    <PageContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={className}
    >
      <PageHeader>
        <div>
          <h1>📊 Sales Journal by Acct-R245A</h1>
          <div className="subtitle">APEX UPGRADE TEST VERSION</div>
        </div>
      </PageHeader>

      <MetricsGrid>
        <MetricCard
          $variant="primary"
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="metric-icon">📊</div>
          <div className="metric-title">Total Entries</div>
          <div className="metric-value">{formatNumber(metrics.totalEntries)}</div>
          <div className="metric-subtitle">Journal entries processed</div>
        </MetricCard>

        <MetricCard
          $variant="success"
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="metric-icon">💰</div>
          <div className="metric-title">Total Amount</div>
          <div className="metric-value">{formatCurrency(metrics.totalAmount)}</div>
          <div className="metric-subtitle">Combined journal value</div>
        </MetricCard>

        <MetricCard
          $variant="secondary"
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="metric-icon">✅</div>
          <div className="metric-title">Valid Entries</div>
          <div className="metric-value">{formatNumber(metrics.validEntries)}</div>
          <div className="metric-subtitle">{metrics.totalEntries ? Math.round((metrics.validEntries / metrics.totalEntries) * 100) : 0}% of total</div>
        </MetricCard>

        <MetricCard
          $variant="warning"
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="metric-icon">⚠️</div>
          <div className="metric-title">Invalid Entries</div>
          <div className="metric-value">{formatNumber(metrics.invalidEntries)}</div>
          <div className="metric-subtitle">Require attention</div>
        </MetricCard>
      </MetricsGrid>

      <ControlsSection>
        <SearchInput
          type="text"
          placeholder="🔍 Search account codes or batch types..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        <ExportButtonGroup>
          <ExportButton
            $variant="pdf"
            onClick={handleExportPDF}
            disabled={!filteredData?.length}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            📄 PDF
          </ExportButton>
          <ExportButton
            $variant="excel"
            onClick={handleExportExcel}
            disabled={!filteredData?.length}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            📊 Excel
          </ExportButton>
          <ExportButton
            $variant="csv"
            onClick={handleExportCSV}
            disabled={!filteredData?.length}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            📋 CSV
          </ExportButton>
        </ExportButtonGroup>
      </ControlsSection>

      <TableContainer>
        <TableHeader>
          <h3>Sales Journal Data</h3>
          <div className="record-count">
            {formatNumber(filteredData?.length || 0)} records
            {searchTerm && ` (filtered from ${formatNumber(journalData?.length || 0)})`}
          </div>
        </TableHeader>

        {isLoading ? (
          <LoadingContainer>
            <div className="loading-spinner" />
            <div className="loading-text">Loading sales journal data...</div>
          </LoadingContainer>
        ) : error ? (
          <EmptyState>
            <div className="empty-icon">⚠️</div>
            <div className="empty-title">Error Loading Data</div>
            <div className="empty-message">{error}</div>
          </EmptyState>
        ) : !filteredData?.length ? (
          <EmptyState>
            <div className="empty-icon">📊</div>
            <div className="empty-title">No Data Available</div>
            <div className="empty-message">
              {searchTerm
                ? `No results found for "${searchTerm}". Try adjusting your search terms.`
                : 'No sales journal data available for the selected filters.'
              }
            </div>
          </EmptyState>
        ) : (
          <StyledTable {...getTableProps()}>
            <thead>
              {headerGroups.map(headerGroup => (
                <tr {...headerGroup.getHeaderGroupProps()}>
                  {headerGroup.headers.map(column => (
                    <th
                      {...column.getHeaderProps(column.getSortByToggleProps())}
                      aria-sort={
                        column.isSorted
                          ? column.isSortedDesc
                            ? 'descending'
                            : 'ascending'
                          : 'none'
                      }
                    >
                      {column.render('Header')}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody {...getTableBodyProps()}>
              {rows.map(row => {
                prepareRow(row);
                return (
                  <motion.tr
                    {...row.getRowProps()}
                    className={row.original.invalid_acount === 'Y' ? 'invalid-row' : ''}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.2 }}
                  >
                    {row.cells.map(cell => (
                      <td {...cell.getCellProps()}>
                        {cell.render('Cell')}
                      </td>
                    ))}
                  </motion.tr>
                );
              })}
            </tbody>
          </StyledTable>
        )}
      </TableContainer>
    </PageContainer>
  );
};