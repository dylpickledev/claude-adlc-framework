# 🏗️ GraniteRock Sales Journal - React Application

**Premium Financial Dashboard converted from Streamlit to React**
*Enterprise-grade financial reporting with modern architecture*

## 🌟 Overview

This React application is a comprehensive conversion of the GraniteRock Sales Journal from Streamlit to a modern, responsive, and highly performant React-based financial dashboard. Built with **TypeScript**, **Styled Components**, and **Zustand** state management, it provides enterprise-grade financial data visualization and reporting capabilities.

### ✨ Key Features

- **🎨 GraniteRock Brand Integration**: Full implementation of corporate design system with colorblind-accessible patterns
- **📊 Real-time Financial Data**: Live journal entries, balance monitoring, and pipeline status updates
- **⚖️ Out-of-Balance Detection**: Advanced financial reconciliation with automated alerts
- **📄 Multi-format Export**: PDF, Excel, and CSV export capabilities with customizable options
- **🔍 Advanced Filtering**: Dynamic data filtering with cached query optimization
- **🚀 Pipeline Management**: Real-time monitoring and control of data processing pipelines
- **♿ Accessibility First**: WCAG 2.1 AA compliance with comprehensive keyboard navigation
- **📱 Responsive Design**: Mobile-first approach with optimized tablet and desktop layouts

## 🏗️ Architecture

### **Modern React Patterns (2025)**
- **Hooks-first architecture** with custom financial logic hooks
- **Domain-centric organization** around financial business logic
- **Performance optimization** with memoization and virtualization
- **Type-safe development** with comprehensive TypeScript definitions

### **State Management Strategy**
- **Zustand**: Lightweight state management for UI state and business logic
- **TanStack Query**: Server state caching and real-time data synchronization
- **Local Storage**: Filter persistence and user preferences

### **Styling Architecture**
- **Styled Components**: Component-scoped styling with theme integration
- **Design System**: Comprehensive GraniteRock theme with consistent tokens
- **Responsive Breakpoints**: Mobile-first responsive design patterns
- **Animation Library**: Framer Motion for premium micro-interactions

## 🚀 Getting Started

### Prerequisites
- **Node.js** 18+ (LTS recommended)
- **npm** or **yarn** package manager
- **TypeScript** 5.0+
- Access to GraniteRock financial data APIs

### Installation

1. **Clone and Install Dependencies**
   ```bash
   cd react-app
   npm install
   ```

2. **Environment Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env.local

   # Configure API endpoints
   REACT_APP_API_BASE_URL=http://localhost:8000/api
   REACT_APP_ENVIRONMENT=development
   ```

3. **Development Server**
   ```bash
   npm run dev
   # Application available at http://localhost:3000
   ```

### Development Commands

```bash
# Development server with hot reload
npm run dev

# Production build
npm run build

# Type checking
npm run type-check

# Linting and code quality
npm run lint
npm run lint:fix

# Testing suite
npm run test
npm run test:watch
npm run test:coverage

# Preview production build
npm run preview
```

## 📁 Project Structure

```
src/
├── components/
│   ├── layout/
│   │   └── Sidebar.tsx           # Modern navigation with filters
│   ├── pages/
│   │   ├── Dashboard.tsx         # Executive overview
│   │   ├── SalesJournal.tsx      # Main financial data table
│   │   ├── DetailByTicket.tsx    # Transaction details
│   │   ├── OutOfBalance.tsx      # Balance reconciliation
│   │   ├── Research1140.tsx      # Account research
│   │   ├── PipelineControl.tsx   # Data pipeline management
│   │   ├── TieoutManagement.tsx  # Tieout processes
│   │   ├── PipelineHistory.tsx   # Execution history
│   │   ├── Documentation.tsx     # User guides
│   │   └── DebugTools.tsx        # Development utilities
│   └── shared/
│       ├── MetricCard.tsx        # Reusable metric displays
│       ├── DataTable.tsx         # Advanced financial tables
│       └── ExportButton.tsx      # Multi-format export
├── services/
│   └── api.ts                    # API layer with error handling
├── store/
│   └── financialStore.ts         # Zustand state management
├── theme/
│   └── graniterock.ts           # Complete design system
├── types/
│   └── financial.ts             # TypeScript definitions
├── utils/
│   └── formatters.ts            # Financial data formatting
└── App.tsx                      # Main application
```

## 🎨 Design System

### **GraniteRock Color Palette**

**Primary Colors**:
- `#003F2C` - Dark Green (Navigation, headers, trust elements)
- `#D9792C` - Orange (CTAs, alerts, important metrics)
- `#8EA449` - Medium Green (Success states, positive trends)
- `#000000` - Black (Text, data labels)
- `#799D90` - Gray-Green (Secondary elements, borders)

**Accessibility Features**:
- **WCAG 2.1 AA Compliance**: 4.5:1 minimum contrast ratios
- **Colorblind-Safe Patterns**: Blue/orange combinations with pattern/texture usage
- **Focus Management**: Visible focus indicators and logical tab order
- **Screen Reader Support**: Comprehensive ARIA labels and landmarks

### **Typography System**
- **Primary Font**: Inter (UI elements, headings, body text)
- **Monospace Font**: JetBrains Mono (Financial data, code, numbers)
- **Semantic Scale**: 12 font sizes with consistent line heights
- **Responsive Typography**: Fluid scaling across breakpoints

## 🔧 Key Components

### **Sales Journal Table**
- **Virtualized Rendering**: Handles 10,000+ rows efficiently
- **Advanced Sorting**: Multi-column sorting with persistent preferences
- **Real-time Filtering**: Instant search with debounced input
- **Export Integration**: PDF, Excel, CSV with formatting preservation

### **Financial Metrics Dashboard**
- **Live Data Updates**: WebSocket integration for real-time metrics
- **Interactive Charts**: Chart.js integration with financial-specific chart types
- **Responsive Cards**: Mobile-optimized metric displays
- **Trend Analysis**: Historical data comparison and variance calculation

### **Sidebar Navigation**
- **Dynamic Filtering**: Real-time filter updates with cache invalidation
- **Out-of-Balance Alerts**: Prominent financial discrepancy notifications
- **Quick Actions**: One-click access to critical functions
- **Status Indicators**: System health and tieout status monitoring

## 🌐 API Integration

### **Database Connections**
- **PostgreSQL**: Operational data store integration
- **Snowflake**: Analytics data warehouse queries
- **REST APIs**: Orchestra pipeline management
- **Real-time Updates**: WebSocket connections for live data

### **Caching Strategy**
- **Query Caching**: 5-minute TTL for financial data
- **Filter Options**: 10-minute TTL for dropdown data
- **Out-of-Balance**: 5-minute TTL with manual refresh
- **Tieout Status**: 30-second TTL for system monitoring

## 📊 Export Capabilities

### **PDF Reports**
- **Executive Summaries**: High-level financial metrics
- **Detailed Journal**: Complete transaction listings
- **Custom Branding**: GraniteRock corporate templates
- **Print Optimization**: Professional report layouts

### **Excel Workbooks**
- **Multi-sheet Reports**: Separate tabs for different data views
- **Formula Integration**: Dynamic calculations and pivot tables
- **Chart Embedding**: Visual data representations
- **Conditional Formatting**: Automated highlighting of critical data

### **CSV Data**
- **Raw Data Export**: Unformatted data for analysis
- **Custom Delimiters**: Configurable field separators
- **Encoding Options**: UTF-8 with BOM support
- **Large Dataset Handling**: Streaming export for performance

## 🔒 Security Features

### **Authentication & Authorization**
- **JWT Token Management**: Secure API authentication
- **Role-based Access**: Granular permission system
- **Session Management**: Automatic token refresh
- **CSRF Protection**: Cross-site request forgery prevention

### **Data Protection**
- **Input Sanitization**: XSS prevention with DOMPurify
- **SQL Injection Prevention**: Parameterized queries only
- **Secure Headers**: Content Security Policy implementation
- **HTTPS Enforcement**: SSL/TLS encrypted communications

## 🧪 Testing Strategy

### **Unit Tests (80%)**
- **Component Testing**: React Testing Library
- **Utility Functions**: Jest with comprehensive coverage
- **State Management**: Zustand store testing
- **API Layer**: Mock API responses and error handling

### **Integration Tests (15%)**
- **User Workflows**: Multi-component interactions
- **API Integration**: Real backend communication testing
- **State Persistence**: Local storage and cache testing
- **Navigation Flow**: Router and tab management

### **End-to-End Tests (5%)**
- **Critical Paths**: Complete financial workflows
- **Export Functions**: PDF, Excel, CSV generation
- **Real-time Updates**: WebSocket connection testing
- **Cross-browser**: Chrome, Firefox, Safari, Edge

## 🚀 Deployment

### **AWS Amplify Integration**
- **Automatic Deployments**: Git-based CI/CD pipeline
- **Environment Management**: Dev, staging, production configs
- **Global CDN**: CloudFront distribution with edge caching
- **SSL Certificates**: Automatic HTTPS with custom domains

### **Performance Optimization**
- **Code Splitting**: Dynamic imports for route-level splitting
- **Bundle Analysis**: Webpack bundle size optimization
- **Image Optimization**: WebP conversion with fallbacks
- **Caching Headers**: Aggressive caching for static assets

## 📈 Performance Metrics

### **Core Web Vitals Targets**
- **LCP (Largest Contentful Paint)**: < 2.5 seconds
- **FID (First Input Delay)**: < 100 milliseconds
- **CLS (Cumulative Layout Shift)**: < 0.1
- **TTI (Time to Interactive)**: < 3.5 seconds

### **Application-Specific Metrics**
- **Initial Load Time**: < 3 seconds for first page
- **Route Transitions**: < 500ms between pages
- **Data Table Rendering**: < 1 second for 1000+ rows
- **Export Generation**: < 10 seconds for large datasets

## 🐛 Development & Debugging

### **Debug Tools Page**
- **State Inspector**: Real-time Zustand store visualization
- **API Monitor**: Request/response logging with timing
- **Performance Profiler**: Component render tracking
- **Cache Inspector**: Query cache status and invalidation

### **Error Handling**
- **Error Boundaries**: Graceful component failure recovery
- **Global Error Handler**: Centralized error logging and reporting
- **User-Friendly Messages**: Clear error descriptions with actions
- **Automatic Retry**: Intelligent retry mechanisms for failed requests

## 🤝 Contributing

### **Development Standards**
- **TypeScript First**: Comprehensive type safety
- **ESLint Configuration**: Airbnb + React + TypeScript rules
- **Prettier Integration**: Consistent code formatting
- **Conventional Commits**: Standardized commit messages

### **Code Review Process**
1. Feature branch creation from `main`
2. Comprehensive testing (unit + integration)
3. Type safety validation
4. Performance impact assessment
5. Accessibility compliance check
6. Code review and approval
7. Merge with automated deployment

---

## 📞 Support & Documentation

**Internal Resources**:
- **Technical Documentation**: `/documentation` page in application
- **API Documentation**: Swagger/OpenAPI specifications
- **Design System**: Living style guide with component examples

**Contact Information**:
- **Development Team**: GraniteRock IT Department
- **Business Stakeholders**: Finance and Accounting Teams
- **System Administration**: Infrastructure and DevOps Teams

---

*Built with ❤️ for GraniteRock's Financial Operations Team*
*Modern React Architecture • Enterprise Security • Premium User Experience*