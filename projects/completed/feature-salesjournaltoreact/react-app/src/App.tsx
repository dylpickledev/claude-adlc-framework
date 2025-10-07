// GraniteRock Sales Journal - Main Application
// Premium React Financial Dashboard with Modern Architecture

import React, { useEffect, useState } from 'react';
import styled, { ThemeProvider, createGlobalStyle } from 'styled-components';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { graniteRockTheme } from './theme/graniterock';
import { useFinancialStore } from './store/financialStore';

// Layout Components
import { Sidebar } from './components/layout/Sidebar';

// Page Components
import { SalesJournal } from './components/pages/SalesJournal';
import { Dashboard } from './components/pages/Dashboard';
import { DetailByTicket } from './components/pages/DetailByTicket';
import { OutOfBalance } from './components/pages/OutOfBalance';
import { Research1140 } from './components/pages/Research1140';
import { PipelineControl } from './components/pages/PipelineControl';
import { TieoutManagement } from './components/pages/TieoutManagement';
import { PipelineHistory } from './components/pages/PipelineHistory';
import { Documentation } from './components/pages/Documentation';
import { DebugTools } from './components/pages/DebugTools';

// Global Styles with GraniteRock Design System
const GlobalStyles = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  html {
    scroll-behavior: smooth;
  }

  body {
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-size: ${graniteRockTheme.typography.fontSizes.base};
    line-height: ${graniteRockTheme.typography.lineHeights.normal};
    color: ${graniteRockTheme.colors.primary.black};
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
  }

  /* Premium Typography Enhancements */
  h1, h2, h3, h4, h5, h6 {
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-weight: ${graniteRockTheme.typography.fontWeights.bold};
    letter-spacing: ${graniteRockTheme.typography.letterSpacing.tight};
    color: ${graniteRockTheme.colors.primary.darkGreen};
    text-rendering: optimizeLegibility;
  }

  /* Enhanced Focus Styles for Accessibility */
  *:focus {
    outline: 2px solid ${graniteRockTheme.colors.accessible.focusRing};
    outline-offset: 2px;
  }

  /* Custom Scrollbar Styling */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  ::-webkit-scrollbar-track {
    background: ${graniteRockTheme.colors.primary.lightCyan};
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb {
    background: ${graniteRockTheme.colors.primary.grayGreen};
    border-radius: 4px;
    transition: background ${graniteRockTheme.animations.transitions.base};
  }

  ::-webkit-scrollbar-thumb:hover {
    background: ${graniteRockTheme.colors.primary.darkGreen};
  }

  /* High Contrast Support */
  @media (prefers-contrast: high) {
    body {
      background: white;
    }

    * {
      border-color: black !important;
    }

    button, input, select, textarea {
      border: 2px solid black !important;
    }
  }

  /* Reduced Motion Support */
  @media (prefers-reduced-motion: reduce) {
    * {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }

  /* Print Styles */
  @media print {
    body {
      background: white !important;
      color: black !important;
    }

    nav, .sidebar, .print-hidden {
      display: none !important;
    }

    .print-full-width {
      width: 100% !important;
      margin-left: 0 !important;
    }
  }

  /* Dark mode variables (for future implementation) */
  @media (prefers-color-scheme: dark) {
    :root {
      --background: ${graniteRockTheme.colors.primary.darkGreen};
      --foreground: ${graniteRockTheme.colors.primary.lightCyan};
    }
  }
`;

const AppContainer = styled.div`
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  position: relative;

  /* Ensure proper layout on all screen sizes */
  @media (max-width: ${graniteRockTheme.breakpoints.lg}) {
    flex-direction: column;
  }
`;

const MainContent = styled(motion.main)`
  flex: 1;
  margin-left: 280px; /* Sidebar width */
  min-height: 100vh;
  background: transparent;
  position: relative;
  overflow-x: hidden;

  @media (max-width: ${graniteRockTheme.breakpoints.lg}) {
    margin-left: 0;
    margin-top: 80px; /* Mobile header height */
  }
`;

const LoadingOverlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, ${graniteRockTheme.colors.primary.darkGreen} 0%, ${graniteRockTheme.colors.primary.mediumGreen} 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: ${graniteRockTheme.zIndex.modal};
  color: white;

  .loading-logo {
    font-size: 4rem;
    margin-bottom: ${graniteRockTheme.spacing[6]};
    animation: pulse 2s ease-in-out infinite;
  }

  .loading-title {
    font-family: ${graniteRockTheme.typography.fontFamilies.primary};
    font-size: ${graniteRockTheme.typography.fontSizes['3xl']};
    font-weight: ${graniteRockTheme.typography.fontWeights.black};
    margin-bottom: ${graniteRockTheme.spacing[4]};
  }

  .loading-subtitle {
    font-size: ${graniteRockTheme.typography.fontSizes.lg};
    opacity: 0.8;
    margin-bottom: ${graniteRockTheme.spacing[8]};
  }

  .loading-progress {
    width: 300px;
    height: 4px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 2px;
    overflow: hidden;
  }

  .loading-bar {
    height: 100%;
    background: linear-gradient(90deg, ${graniteRockTheme.colors.primary.orange} 0%, ${graniteRockTheme.colors.primary.lightOrange} 100%);
    border-radius: 2px;
    animation: loading 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
  }

  @keyframes loading {
    0% { width: 0%; }
    50% { width: 70%; }
    100% { width: 100%; }
  }
`;

const ErrorBoundary = styled.div`
  padding: ${graniteRockTheme.spacing[8]};
  text-align: center;
  background: white;
  margin: ${graniteRockTheme.spacing[6]};
  border-radius: ${graniteRockTheme.borderRadius['2xl']};
  box-shadow: ${graniteRockTheme.shadows.xl};
  border-left: 4px solid ${graniteRockTheme.colors.semantic.error};

  .error-icon {
    font-size: 4rem;
    margin-bottom: ${graniteRockTheme.spacing[4]};
  }

  .error-title {
    font-size: ${graniteRockTheme.typography.fontSizes['2xl']};
    font-weight: ${graniteRockTheme.typography.fontWeights.bold};
    color: ${graniteRockTheme.colors.semantic.error};
    margin-bottom: ${graniteRockTheme.spacing[4]};
  }

  .error-message {
    font-size: ${graniteRockTheme.typography.fontSizes.base};
    color: ${graniteRockTheme.colors.primary.darkGray};
    margin-bottom: ${graniteRockTheme.spacing[6]};
    line-height: ${graniteRockTheme.typography.lineHeights.relaxed};
  }

  .error-actions {
    display: flex;
    gap: ${graniteRockTheme.spacing[4]};
    justify-content: center;
  }
`;

const ErrorButton = styled(motion.button)`
  background: linear-gradient(135deg, ${graniteRockTheme.colors.primary.darkGreen} 0%, ${graniteRockTheme.colors.primary.mediumGreen} 100%);
  color: white;
  border: none;
  border-radius: ${graniteRockTheme.borderRadius.lg};
  padding: ${graniteRockTheme.spacing[3]} ${graniteRockTheme.spacing[6]};
  font-family: ${graniteRockTheme.typography.fontFamilies.primary};
  font-size: ${graniteRockTheme.typography.fontSizes.sm};
  font-weight: ${graniteRockTheme.typography.fontWeights.semibold};
  cursor: pointer;
  transition: all ${graniteRockTheme.animations.transitions.base};

  &:hover {
    transform: translateY(-2px);
    box-shadow: ${graniteRockTheme.shadows.lg};
  }

  &:active {
    transform: translateY(0);
  }
`;

// Component mapping for dynamic routing
const COMPONENT_MAP = {
  Dashboard,
  SalesJournal,
  DetailByTicket,
  OutOfBalance,
  Research1140,
  PipelineControl,
  TieoutManagement,
  PipelineHistory,
  Documentation,
  DebugTools,
};

interface AppProps {}

const App: React.FC<AppProps> = () => {
  const {
    activeTab,
    setActiveTab,
    outOfBalanceData,
    isLoading: storeLoading,
    error,
    refreshAllData
  } = useFinancialStore();

  const [isInitializing, setIsInitializing] = useState(true);
  const [hasError, setHasError] = useState(false);

  // Initialize application
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Simulate initialization time for smooth loading experience
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Initialize data
        await refreshAllData();

        setIsInitializing(false);
      } catch (error) {
        console.error('Failed to initialize application:', error);
        setHasError(true);
        setIsInitializing(false);
      }
    };

    initializeApp();
  }, [refreshAllData]);

  // Error boundary fallback
  const handleRetry = () => {
    setHasError(false);
    setIsInitializing(true);
    refreshAllData().then(() => {
      setIsInitializing(false);
    }).catch(() => {
      setHasError(true);
      setIsInitializing(false);
    });
  };

  const handleReload = () => {
    window.location.reload();
  };

  // Show loading screen during initialization
  if (isInitializing) {
    return (
      <ThemeProvider theme={graniteRockTheme}>
        <GlobalStyles />
        <AnimatePresence>
          <LoadingOverlay
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="loading-logo">🏗️</div>
            <div className="loading-title">GraniteRock</div>
            <div className="loading-subtitle">Sales Journal Application</div>
            <div className="loading-progress">
              <div className="loading-bar" />
            </div>
          </LoadingOverlay>
        </AnimatePresence>
      </ThemeProvider>
    );
  }

  // Show error boundary
  if (hasError) {
    return (
      <ThemeProvider theme={graniteRockTheme}>
        <GlobalStyles />
        <AppContainer>
          <ErrorBoundary>
            <div className="error-icon">⚠️</div>
            <div className="error-title">Application Error</div>
            <div className="error-message">
              Something went wrong while loading the GraniteRock Sales Journal application.
              Please try refreshing the page or contact your system administrator if the problem persists.
            </div>
            <div className="error-actions">
              <ErrorButton
                onClick={handleRetry}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                🔄 Retry
              </ErrorButton>
              <ErrorButton
                onClick={handleReload}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                ↻ Reload Page
              </ErrorButton>
            </div>
          </ErrorBoundary>
        </AppContainer>
      </ThemeProvider>
    );
  }

  // Get the active component
  const getActiveComponent = () => {
    const componentMap = {
      dashboard: Dashboard,
      journal: SalesJournal,
      details: DetailByTicket,
      balance: OutOfBalance,
      research: Research1140,
      pipeline: PipelineControl,
      tieout: TieoutManagement,
      history: PipelineHistory,
      documentation: Documentation,
      debug: DebugTools,
    };

    const Component = componentMap[activeTab as keyof typeof componentMap] || Dashboard;
    return <Component />;
  };

  return (
    <ThemeProvider theme={graniteRockTheme}>
      <GlobalStyles />
      <Router>
        <AppContainer>
          <Sidebar
            activeTab={activeTab}
            onTabChange={setActiveTab}
            outOfBalanceData={outOfBalanceData}
          />

          <MainContent
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.2 }}
              >
                {getActiveComponent()}
              </motion.div>
            </AnimatePresence>
          </MainContent>
        </AppContainer>
      </Router>
    </ThemeProvider>
  );
};

export default App;