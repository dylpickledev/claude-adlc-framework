// GraniteRock Design System - Premium Financial Application Theme
// Implementing colorblind-accessible design with corporate brand guidelines

export const graniteRockTheme = {
  colors: {
    // Primary GraniteRock palette
    primary: {
      darkGreen: '#003F2C',      // Navigation, headers, trust elements
      orange: '#D9792C',         // CTAs, alerts, important metrics
      mediumGreen: '#8EA449',    // Success states, positive trends
      black: '#000000',          // Primary text, data labels
      grayGreen: '#799D90',      // Secondary elements, borders
      lightOrange: '#F89953',    // Hover states, secondary CTAs
      lightGreen: '#B9D284',     // Background highlights, success indicators
      darkGray: '#58595B',       // Muted text, disabled states
      lightCyan: '#B6D8CC',      // Subtle backgrounds, card containers
    },

    // Extended palette for complex UI states
    extended: {
      darkRed: '#920009',        // Error states, critical alerts
      mediumGray: '#939598',     // Neutral elements
      brightRed: '#F50019',      // Urgent notifications
      yellowOrange: '#FCB523',   // Warning states
      cyan: '#54FFFE',          // Information highlights
      blue: '#3300FC',          // Links, informational elements
      magenta: '#F900FD',       // Special highlights
      peach: '#D77C6D',         // Soft accent
      lightPink: '#E4979A',     // Gentle highlights
      paleYellow: '#FBE79C',    // Background accents
      lightCyanAlt: '#B9FFFF',  // Alternative light backgrounds
      lightBlue: '#79A6DB',     // Secondary information
      lavender: '#D2A4BD',      // Subtle accents
      cyanBlue: '#37AECC',      // Active states
      darkGreenAlt: '#3D7921',  // Alternative success
      mutedGreenGray: '#A7A089', // Disabled states
      darkTeal: '#1F4F5C',      // Deep accent
      darkBlue: '#163562',      // Professional accent
      darkPurple: '#380E74',    // Premium accent
      veryLightCyan: '#A6E0EE', // Background wash
      lightGreenAlt: '#96C77F', // Alternative success
      lightGray: '#C9C8C7',     // Neutral backgrounds
      blueGray: '#4E818D',      // Professional neutral
      mediumBlue: '#4D82C4',    // Information
      purple: '#6947A6',        // Premium elements
    },

    // Semantic color mappings for financial applications
    semantic: {
      success: '#8EA449',        // Positive financial metrics
      warning: '#FCB523',        // Cautionary financial states
      error: '#920009',          // Financial errors, out of balance
      info: '#37AECC',           // Informational elements
      positive: '#8EA449',       // Profit, gains, positive variance
      negative: '#920009',       // Loss, negative variance
      neutral: '#58595B',        // Balanced, no change
      premium: '#6947A6',        // Premium features, VIP elements
    },

    // Accessibility-focused color combinations (colorblind-safe)
    accessible: {
      // Blue/orange combinations - universally accessible
      primaryAction: '#3300FC',    // Blue for primary actions
      secondaryAction: '#D9792C',  // Orange for secondary actions

      // High contrast combinations (4.5:1 minimum)
      textPrimary: '#000000',      // On light backgrounds
      textSecondary: '#58595B',    // Muted text
      textInverse: '#FFFFFF',      // On dark backgrounds

      // Background combinations
      backgroundLight: '#FFFFFF',   // Main background
      backgroundMedium: '#B6D8CC',  // Card backgrounds
      backgroundDark: '#003F2C',    // Header backgrounds

      // Interactive states
      focusRing: '#3300FC',        // Focus indicators
      hoverState: '#F89953',       // Hover overlays
      activeState: '#37AECC',      // Active/selected states
    }
  },

  typography: {
    // Modern font stack - Inter for interface, JetBrains Mono for data
    fontFamilies: {
      primary: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      secondary: "'Inter', system-ui, sans-serif",
      monospace: "'JetBrains Mono', 'Monaco', 'Menlo', monospace",
    },

    // Financial application typography scale
    fontSizes: {
      xs: '0.75rem',    // 12px - Helper text, captions
      sm: '0.875rem',   // 14px - Body text, labels
      base: '1rem',     // 16px - Primary body text
      lg: '1.125rem',   // 18px - Emphasized text
      xl: '1.25rem',    // 20px - Small headings
      '2xl': '1.5rem',  // 24px - Section headings
      '3xl': '1.875rem', // 30px - Page titles
      '4xl': '2.25rem', // 36px - Hero headings
      '5xl': '3rem',    // 48px - Display text
    },

    fontWeights: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
      black: 900,
    },

    lineHeights: {
      none: 1,
      tight: 1.25,
      snug: 1.375,
      normal: 1.5,
      relaxed: 1.625,
      loose: 2,
    },

    letterSpacing: {
      tighter: '-0.05em',
      tight: '-0.025em',
      normal: '0em',
      wide: '0.025em',
      wider: '0.05em',
      widest: '0.1em',
    },
  },

  spacing: {
    // 8-point grid system for consistent spacing
    px: '1px',
    0: '0',
    0.5: '0.125rem', // 2px
    1: '0.25rem',    // 4px
    1.5: '0.375rem', // 6px
    2: '0.5rem',     // 8px
    2.5: '0.625rem', // 10px
    3: '0.75rem',    // 12px
    3.5: '0.875rem', // 14px
    4: '1rem',       // 16px
    5: '1.25rem',    // 20px
    6: '1.5rem',     // 24px
    7: '1.75rem',    // 28px
    8: '2rem',       // 32px
    9: '2.25rem',    // 36px
    10: '2.5rem',    // 40px
    12: '3rem',      // 48px
    14: '3.5rem',    // 56px
    16: '4rem',      // 64px
    20: '5rem',      // 80px
    24: '6rem',      // 96px
    28: '7rem',      // 112px
    32: '8rem',      // 128px
  },

  borderRadius: {
    none: '0',
    sm: '0.125rem',   // 2px
    base: '0.25rem',  // 4px
    md: '0.375rem',   // 6px
    lg: '0.5rem',     // 8px
    xl: '0.75rem',    // 12px
    '2xl': '1rem',    // 16px
    '3xl': '1.5rem',  // 24px
    full: '9999px',
  },

  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    none: 'none',
  },

  // Component-specific styling patterns
  components: {
    card: {
      background: 'linear-gradient(135deg, #B6D8CC 0%, #FFFFFF 100%)',
      border: '1px solid #799D90',
      borderRadius: '0.75rem',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      padding: '1.5rem',
    },

    button: {
      primary: {
        background: 'linear-gradient(135deg, #D9792C 0%, #F89953 100%)',
        color: '#FFFFFF',
        borderRadius: '0.5rem',
        padding: '0.75rem 1.5rem',
        fontSize: '0.875rem',
        fontWeight: 600,
        transition: 'all 0.2s ease-in-out',
      },
      secondary: {
        background: 'transparent',
        color: '#003F2C',
        border: '1px solid #003F2C',
        borderRadius: '0.5rem',
        padding: '0.75rem 1.5rem',
        fontSize: '0.875rem',
        fontWeight: 600,
        transition: 'all 0.2s ease-in-out',
      },
    },

    input: {
      base: {
        background: '#FFFFFF',
        border: '1px solid #799D90',
        borderRadius: '0.375rem',
        padding: '0.75rem 1rem',
        fontSize: '0.875rem',
        color: '#000000',
        transition: 'border-color 0.2s ease-in-out',
      },
      focus: {
        borderColor: '#3300FC',
        outline: '2px solid rgba(51, 0, 252, 0.1)',
      },
    },

    metric: {
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: '#FFFFFF',
      borderRadius: '0.75rem',
      padding: '1.5rem',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    },
  },

  // Animation and transition presets
  animations: {
    transitions: {
      fast: '0.15s ease-in-out',
      base: '0.2s ease-in-out',
      slow: '0.3s ease-in-out',
    },

    easing: {
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    },
  },

  // Responsive breakpoints
  breakpoints: {
    sm: '640px',   // Small devices
    md: '768px',   // Medium devices
    lg: '1024px',  // Large devices
    xl: '1280px',  // Extra large devices
    '2xl': '1536px', // 2X large devices
  },

  // Z-index scale for layering
  zIndex: {
    hide: -1,
    auto: 'auto',
    base: 0,
    docked: 10,
    dropdown: 1000,
    sticky: 1100,
    banner: 1200,
    overlay: 1300,
    modal: 1400,
    popover: 1500,
    skipLink: 1600,
    toast: 1700,
    tooltip: 1800,
  },
} as const;

export type GraniteRockTheme = typeof graniteRockTheme;