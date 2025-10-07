// GraniteRock Sales Journal - Utility Functions
// Premium formatting and export utilities for financial data

import { JournalEntry, FilterState, ExportOptions } from '../types/financial';

/**
 * Format currency values with proper locale support
 */
export const formatCurrency = (value: number | string): string => {
  const numericValue = typeof value === 'string' ? parseFloat(value) : value;

  if (isNaN(numericValue)) return '$0.00';

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(numericValue);
};

/**
 * Format number values with proper locale support
 */
export const formatNumber = (value: number | string): string => {
  const numericValue = typeof value === 'string' ? parseFloat(value) : value;

  if (isNaN(numericValue)) return '0';

  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(numericValue);
};

/**
 * Format percentage values
 */
export const formatPercentage = (value: number, decimals: number = 1): string => {
  if (isNaN(value)) return '0%';

  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value / 100);
};

/**
 * Format date values consistently
 */
export const formatDate = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;

  if (isNaN(dateObj.getTime())) return 'Invalid Date';

  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(dateObj);
};

/**
 * Format timestamp for display
 */
export const formatTimestamp = (timestamp: string | Date): string => {
  try {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();

    // Less than 1 minute ago
    if (diff < 60000) {
      return 'Just now';
    }

    // Less than 1 hour ago
    if (diff < 3600000) {
      const minutes = Math.floor(diff / 60000);
      return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    }

    // Less than 1 day ago
    if (diff < 86400000) {
      const hours = Math.floor(diff / 3600000);
      return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    }

    // More than 1 day ago - show full date
    return formatDate(date);
  } catch {
    return 'Unknown';
  }
};

/**
 * Safe value formatter for any type
 */
export const safeFormat = (value: any, formatter: (val: any) => string, fallback: string = 'N/A'): string => {
  try {
    if (value === null || value === undefined) return fallback;
    return formatter(value);
  } catch {
    return fallback;
  }
};

/**
 * Download data as CSV file
 */
export const downloadCSV = (data: JournalEntry[], filename: string = 'sales-journal'): void => {
  if (!data.length) return;

  // Define headers
  const headers = [
    'Account Code Adjusted',
    'Batch Type',
    'Invalid Account',
    'Account Entry Qty',
    'Amount'
  ];

  // Convert data to CSV format
  const csvContent = [
    headers.join(','),
    ...data.map(row => [
      `"${row.accountcode_adjusted}"`,
      `"${row.batch_type}"`,
      `"${row.invalid_acount}"`,
      row.account_entry_qty,
      row.amount
    ].join(','))
  ].join('\n');

  // Create and download file
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');

  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `${filename}-${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
};

/**
 * Download data as Excel file (requires external library in production)
 */
export const downloadExcel = async (
  data: JournalEntry[],
  filters: FilterState,
  options: ExportOptions
): Promise<void> => {
  // This is a placeholder - in production you would use a library like xlsx
  console.log('Excel export requested:', { data, filters, options });

  // For now, fallback to CSV
  downloadCSV(data, 'sales-journal-excel');

  // TODO: Implement actual Excel export with proper styling
  // Example with xlsx library:
  /*
  import * as XLSX from 'xlsx';

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Sales Journal');

  // Add filters as a separate sheet if requested
  if (options.includeFilters) {
    const filterSheet = XLSX.utils.json_to_sheet([filters]);
    XLSX.utils.book_append_sheet(workbook, filterSheet, 'Filters');
  }

  XLSX.writeFile(workbook, `sales-journal-${new Date().toISOString().split('T')[0]}.xlsx`);
  */
};

/**
 * Generate PDF report (requires external library in production)
 */
export const downloadPDF = async (
  data: JournalEntry[],
  filters: FilterState,
  totalAmount: number,
  options: ExportOptions
): Promise<void> => {
  // This is a placeholder - in production you would use a library like jsPDF
  console.log('PDF export requested:', { data, filters, totalAmount, options });

  // For development, create a simple HTML report and print
  const reportWindow = window.open('', '_blank');
  if (!reportWindow) return;

  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>GraniteRock Sales Journal Report</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .logo { color: #003F2C; font-size: 24px; font-weight: bold; }
        .filters { background: #f5f5f5; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
        .summary { display: flex; justify-content: space-around; margin-bottom: 20px; }
        .metric { text-align: center; padding: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #003F2C; color: white; }
        .invalid { background-color: #ffebee; color: #c62828; }
        .currency { text-align: right; font-family: monospace; }
        .footer { margin-top: 30px; text-align: center; font-size: 12px; color: #666; }
      </style>
    </head>
    <body>
      <div class="header">
        <div class="logo">🏗️ GraniteRock Sales Journal Report</div>
        <p>Generated on ${formatDate(new Date())}</p>
      </div>

      ${options.includeFilters ? `
      <div class="filters">
        <h3>Applied Filters</h3>
        <p><strong>Batch Type:</strong> ${filters.shared_batch_type}</p>
        <p><strong>Proof Mode:</strong> ${filters.shared_is_proof}</p>
        <p><strong>Batch ID:</strong> ${filters.shared_batch_id}</p>
        <p><strong>Invalid Account:</strong> ${filters.shared_invalid_account}</p>
      </div>
      ` : ''}

      <div class="summary">
        <div class="metric">
          <h3>${formatNumber(data.length)}</h3>
          <p>Total Entries</p>
        </div>
        <div class="metric">
          <h3>${formatCurrency(totalAmount)}</h3>
          <p>Total Amount</p>
        </div>
        <div class="metric">
          <h3>${formatNumber(data.filter(d => d.invalid_acount === 'N').length)}</h3>
          <p>Valid Entries</p>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Account Code</th>
            <th>Batch Type</th>
            <th>Invalid Account</th>
            <th>Entry Qty</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          ${data.map(row => `
            <tr ${row.invalid_acount === 'Y' ? 'class="invalid"' : ''}>
              <td>${row.accountcode_adjusted}</td>
              <td>${row.batch_type}</td>
              <td>${row.invalid_acount === 'Y' ? '❌ Yes' : '✅ No'}</td>
              <td>${formatNumber(row.account_entry_qty)}</td>
              <td class="currency">${formatCurrency(row.amount)}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <div class="footer">
        <p>GraniteRock Sales Journal Report - Generated by Premium React Application</p>
        <p>For internal use only - Contains confidential financial data</p>
      </div>

      <script>
        window.print();
        window.onafterprint = function() { window.close(); };
      </script>
    </body>
    </html>
  `;

  reportWindow.document.write(htmlContent);
  reportWindow.document.close();
};

/**
 * Generate filename with timestamp
 */
export const generateFilename = (baseName: string, extension: string): string => {
  const timestamp = new Date().toISOString().split('T')[0];
  return `${baseName}-${timestamp}.${extension}`;
};

/**
 * Validate financial data
 */
export const validateJournalEntry = (entry: Partial<JournalEntry>): string[] => {
  const errors: string[] = [];

  if (!entry.accountcode_adjusted || entry.accountcode_adjusted.trim() === '') {
    errors.push('Account code is required');
  }

  if (!entry.batch_type || !['CASH', 'CREDIT', 'INTRA'].includes(entry.batch_type)) {
    errors.push('Valid batch type is required (CASH, CREDIT, or INTRA)');
  }

  if (!entry.invalid_acount || !['Y', 'N'].includes(entry.invalid_acount)) {
    errors.push('Invalid account flag must be Y or N');
  }

  if (entry.account_entry_qty === undefined || entry.account_entry_qty < 0) {
    errors.push('Account entry quantity must be a positive number');
  }

  if (entry.amount === undefined || isNaN(entry.amount)) {
    errors.push('Amount must be a valid number');
  }

  return errors;
};

/**
 * Calculate financial metrics
 */
export const calculateMetrics = (data: JournalEntry[]) => {
  if (!data?.length) {
    return {
      totalEntries: 0,
      totalAmount: 0,
      validEntries: 0,
      invalidEntries: 0,
      averageAmount: 0,
      batchBreakdown: {},
      validPercentage: 0,
    };
  }

  const validEntries = data.filter(entry => entry.invalid_acount === 'N');
  const invalidEntries = data.filter(entry => entry.invalid_acount === 'Y');
  const totalAmount = data.reduce((sum, entry) => sum + entry.amount, 0);

  // Calculate batch breakdown
  const batchBreakdown = data.reduce((acc, entry) => {
    const key = entry.batch_type;
    if (!acc[key]) {
      acc[key] = { count: 0, amount: 0 };
    }
    acc[key].count++;
    acc[key].amount += entry.amount;
    return acc;
  }, {} as Record<string, { count: number; amount: number }>);

  return {
    totalEntries: data.length,
    totalAmount,
    validEntries: validEntries.length,
    invalidEntries: invalidEntries.length,
    averageAmount: totalAmount / data.length,
    batchBreakdown,
    validPercentage: (validEntries.length / data.length) * 100,
  };
};

/**
 * Debounce function for search inputs
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(null, args), wait);
  };
};

/**
 * Get color for financial values
 */
export const getValueColor = (value: number): string => {
  if (value > 0) return '#8EA449'; // Success green
  if (value < 0) return '#920009'; // Error red
  return '#58595B'; // Neutral gray
};

/**
 * Format large numbers with abbreviations (K, M, B)
 */
export const formatAbbreviatedNumber = (value: number): string => {
  if (Math.abs(value) >= 1e9) {
    return (value / 1e9).toFixed(1) + 'B';
  }
  if (Math.abs(value) >= 1e6) {
    return (value / 1e6).toFixed(1) + 'M';
  }
  if (Math.abs(value) >= 1e3) {
    return (value / 1e3).toFixed(1) + 'K';
  }
  return value.toString();
};