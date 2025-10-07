// GraniteRock Sales Journal - Modern Sidebar Navigation
// Premium financial dashboard with enterprise-grade navigation

import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { graniteRockTheme } from '../../theme/graniterock';
import { NavigationTab, OutOfBalanceData } from '../../types/financial';
import { useFinancialStore } from '../../store/financialStore';

// Navigation configuration - matching Streamlit application structure
const navigationTabs: NavigationTab[] = [
  { id: 'dashboard', label: '🏠 Dashboard', icon: '🏠', component: 'Dashboard', enabled: true },
  { id: 'journal', label: '📊 Sales Journal', icon: '📊', component: 'SalesJournal', enabled: true },
  { id: 'details', label: '📋 Detail by Ticket', icon: '📋', component: 'DetailByTicket', enabled: true },
  { id: 'balance', label: '⚖️ Out of Balance', icon: '⚖️', component: 'OutOfBalance', enabled: true },
  { id: 'research', label: '🔍 1140 Research', icon: '🔍', component: 'Research1140', enabled: true },
  { id: 'pipeline', label: '🚀 Pipeline Control', icon: '🚀', component: 'PipelineControl', enabled: true },
  { id: 'tieout', label: '⚙️ Tieout Management', icon: '⚙️', component: 'TieoutManagement', enabled: true },
  { id: 'history', label: '📈 Pipeline History', icon: '📈', component: 'PipelineHistory', enabled: true },
  { id: 'documentation', label: '📖 Documentation', icon: '📖', component: 'Documentation', enabled: true },
  { id: 'debug', label: '🔧 Debug Tools', icon: '🔧', component: 'DebugTools', enabled: true },
];

const SidebarContainer = styled(motion.aside)`
  width: 280px;
  height: 100vh;
  background: linear-gradient(180deg, ${graniteRockTheme.colors.primary.darkGreen} 0%, #2a5c47 100%);
  color: white;
  padding: ${graniteRockTheme.spacing[6]};
  position: fixed;
  left: 0;
  top: 0;
  z-index: ${graniteRockTheme.zIndex.docked};
  overflow-y: auto;
  box-shadow: ${graniteRockTheme.shadows.xl};

  /* Custom scrollbar */
  &::-webkit-scrollbar {
    width: 6px;
  }
  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
  }
  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
  }
  &::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }
`;

const LogoSection = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: ${graniteRockTheme.spacing[8]};
  padding-bottom: ${graniteRockTheme.spacing[4]};
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);

  h1 {
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-size: ${graniteRockTheme.typography.fontSizes['2xl']};
    font-weight: ${graniteRockTheme.typography.fontWeights.black};
    color: white;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, ${graniteRockTheme.colors.primary.lightCyan} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .logo-icon {
    font-size: 2rem;
    margin-right: ${graniteRockTheme.spacing[3]};
  }
`;

const NavigationSection = styled.div`
  margin-bottom: ${graniteRockTheme.spacing[6]};

  h3 {
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: ${graniteRockTheme.spacing[4]};
    text-transform: uppercase;
    letter-spacing: ${graniteRockTheme.typography.letterSpacing.wide};
  }
`;

const NavigationItem = styled(motion.button)<{ $isActive: boolean }>`
  width: 100%;
  display: flex;
  align-items: center;
  padding: ${graniteRockTheme.spacing[3]} ${graniteRockTheme.spacing[4]};
  margin-bottom: ${graniteRockTheme.spacing[1]};
  background: ${props => props.$isActive
    ? `linear-gradient(135deg, ${graniteRockTheme.colors.primary.orange} 0%, ${graniteRockTheme.colors.primary.lightOrange} 100%)`
    : 'transparent'
  };
  color: ${props => props.$isActive ? 'white' : 'rgba(255, 255, 255, 0.9)'};
  border: none;
  border-radius: ${graniteRockTheme.borderRadius.lg};
  font-family: ${graniteRockTheme.typography.fontFamilies.primary};
  font-size: ${graniteRockTheme.typography.fontSizes.sm};
  font-weight: ${graniteRockTheme.typography.fontWeights.medium};
  cursor: pointer;
  transition: all ${graniteRockTheme.animations.transitions.base};
  text-align: left;

  &:hover {
    background: ${props => props.$isActive
      ? `linear-gradient(135deg, ${graniteRockTheme.colors.primary.orange} 0%, ${graniteRockTheme.colors.primary.lightOrange} 100%)`
      : 'rgba(255, 255, 255, 0.1)'
    };
    color: white;
    transform: translateX(4px);
  }

  &:focus {
    outline: 2px solid ${graniteRockTheme.colors.accessible.focusRing};
    outline-offset: 2px;
  }

  .nav-icon {
    margin-right: ${graniteRockTheme.spacing[3]};
    font-size: ${graniteRockTheme.typography.fontSizes.lg};
  }

  .nav-label {
    flex: 1;
  }
`;

const AlertSection = styled(motion.div)<{ $alertType: 'success' | 'warning' | 'error' }>`
  background: ${props => {
    switch (props.$alertType) {
      case 'error': return `linear-gradient(135deg, ${graniteRockTheme.colors.semantic.error} 0%, #b91c1c 100%)`;
      case 'warning': return `linear-gradient(135deg, ${graniteRockTheme.colors.semantic.warning} 0%, #f59e0b 100%)`;
      default: return `linear-gradient(135deg, ${graniteRockTheme.colors.semantic.success} 0%, #16a34a 100%)`;
    }
  }};
  color: white;
  padding: ${graniteRockTheme.spacing[4]};
  border-radius: ${graniteRockTheme.borderRadius.lg};
  margin-bottom: ${graniteRockTheme.spacing[6]};
  box-shadow: ${graniteRockTheme.shadows.md};

  .alert-title {
    font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    margin-bottom: ${graniteRockTheme.spacing[2]};
    display: flex;
    align-items: center;
    gap: ${graniteRockTheme.spacing[2]};
  }

  .alert-amount {
    font-family: ${graniteRockTheme.typography.fontFamilies.monospace};
    font-size: ${graniteRockTheme.typography.fontSizes.lg};
    font-weight: ${graniteRockTheme.typography.fontWeights.bold};
  }
`;

const FilterSection = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: ${graniteRockTheme.borderRadius.lg};
  padding: ${graniteRockTheme.spacing[4]};
  margin-bottom: ${graniteRockTheme.spacing[6]};
  backdrop-filter: blur(10px);

  h4 {
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: ${graniteRockTheme.spacing[3]};
  }
`;

const FilterItem = styled.div`
  margin-bottom: ${graniteRockTheme.spacing[3]};

  label {
    display: block;
    font-size: ${graniteRockTheme.typography.fontSizes.xs};
    font-weight: ${graniteRockTheme.typography.fontWeights.medium};
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: ${graniteRockTheme.spacing[1]};
    text-transform: uppercase;
    letter-spacing: ${graniteRockTheme.typography.letterSpacing.wide};
  }

  select {
    width: 100%;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: ${graniteRockTheme.borderRadius.md};
    padding: ${graniteRockTheme.spacing[2]} ${graniteRockTheme.spacing[3]};
    color: white;
    font-size: ${graniteRockTheme.typography.fontSizes.sm};
    cursor: pointer;
    transition: all ${graniteRockTheme.animations.transitions.base};

    &:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
    }

    &:focus {
      outline: none;
      background: rgba(255, 255, 255, 0.2);
      border-color: ${graniteRockTheme.colors.primary.lightCyan};
    }

    option {
      background: ${graniteRockTheme.colors.primary.darkGreen};
      color: white;
    }
  }
`;

const QuickActionsSection = styled.div`
  margin-top: auto;
  padding-top: ${graniteRockTheme.spacing[4]};
  border-top: 1px solid rgba(255, 255, 255, 0.2);
`;

const QuickActionButton = styled(motion.button)`
  width: 100%;
  background: linear-gradient(135deg, ${graniteRockTheme.colors.accessible.primaryAction} 0%, #4f46e5 100%);
  color: white;
  border: none;
  border-radius: ${graniteRockTheme.borderRadius.lg};
  padding: ${graniteRockTheme.spacing[3]} ${graniteRockTheme.spacing[4]};
  font-family: ${graniteRockTheme.typography.fontFamilies.primary};
  font-size: ${graniteRockTheme.typography.fontSizes.sm};
  font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
  cursor: pointer;
  margin-bottom: ${graniteRockTheme.spacing[2]};
  transition: all ${graniteRockTheme.animations.transitions.base};

  &:hover {
    transform: translateY(-2px);
    box-shadow: ${graniteRockTheme.shadows.lg};
  }

  &:active {
    transform: translateY(0);
  }

  &:focus {
    outline: 2px solid ${graniteRockTheme.colors.accessible.focusRing};
    outline-offset: 2px;
  }
`;

interface SidebarProps {
  activeTab: string;
  onTabChange: (tabId: string) => void;
  outOfBalanceData?: OutOfBalanceData;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  onTabChange,
  outOfBalanceData
}) => {
  const {
    filters,
    setFilter,
    batchOptions,
    invalidAccountOptions,
    branchOptions,
    refreshFilters
  } = useFinancialStore();

  const [tieoutEmoji, setTieoutEmoji] = useState('⏳');

  useEffect(() => {
    // Simulate tieout status updates
    const interval = setInterval(() => {
      const emojis = ['✅', '⚠️', '❌', '⏳'];
      setTieoutEmoji(emojis[Math.floor(Math.random() * emojis.length)]);
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <SidebarContainer
      initial={{ x: -300 }}
      animate={{ x: 0 }}
      transition={{ type: "spring", stiffness: 100, damping: 20 }}
    >
      <LogoSection>
        <span className="logo-icon">🏗️</span>
        <h1>GraniteRock</h1>
      </LogoSection>

      <NavigationSection>
        <h3>📋 Navigation</h3>
        {navigationTabs.map((tab) => (
          <NavigationItem
            key={tab.id}
            $isActive={activeTab === tab.id}
            onClick={() => onTabChange(tab.id)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <span className="nav-icon">{tab.icon}</span>
            <span className="nav-label">{tab.label.replace(/^[^\s]+ /, '')}</span>
          </NavigationItem>
        ))}
      </NavigationSection>

      <AnimatePresence>
        {outOfBalanceData && Math.abs(outOfBalanceData.total) > 0.02 && filters.shared_is_proof === 'Y' && (
          <AlertSection
            $alertType={outOfBalanceData.color}
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <div className="alert-title">
              ⚖️ Critical Alert
            </div>
            <div className="alert-amount">
              {outOfBalanceData.total < 0 ? '-' : '+'}$
              {Math.abs(outOfBalanceData.total).toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
              })}
            </div>
            <div style={{ fontSize: '0.75rem', opacity: 0.9, marginTop: '0.5rem' }}>
              {outOfBalanceData.status}
            </div>
          </AlertSection>
        )}
      </AnimatePresence>

      <FilterSection>
        <h4>🎛️ Data Filters</h4>

        <FilterItem>
          <label>Batch Type</label>
          <select
            value={filters.shared_batch_type}
            onChange={(e) => setFilter('shared_batch_type', e.target.value as any)}
          >
            <option value="CASH">CASH</option>
            <option value="CREDIT">CREDIT</option>
            <option value="INTRA">INTRA</option>
          </select>
        </FilterItem>

        <FilterItem>
          <label>Proof Mode</label>
          <select
            value={filters.shared_is_proof}
            onChange={(e) => setFilter('shared_is_proof', e.target.value as any)}
          >
            <option value="Y">Yes (Y)</option>
            <option value="N">No (N)</option>
          </select>
        </FilterItem>

        <FilterItem>
          <label>Batch ID</label>
          <select
            value={filters.shared_batch_id}
            onChange={(e) => setFilter('shared_batch_id', e.target.value)}
          >
            <option value="All">All Batches</option>
            {batchOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </FilterItem>

        <FilterItem>
          <label>Invalid Account</label>
          <select
            value={filters.shared_invalid_account}
            onChange={(e) => setFilter('shared_invalid_account', e.target.value)}
          >
            <option value="All">All Accounts</option>
            {invalidAccountOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </FilterItem>
      </FilterSection>

      <QuickActionsSection>
        <QuickActionButton
          onClick={refreshFilters}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          🔄 Refresh Data
        </QuickActionButton>

        <QuickActionButton
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {tieoutEmoji} Tieout Status
        </QuickActionButton>
      </QuickActionsSection>
    </SidebarContainer>
  );
};