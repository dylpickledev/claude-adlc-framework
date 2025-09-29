import 'styled-components';

declare module 'styled-components' {
  export interface DefaultTheme {
    colors: {
      primary: {
        darkGreen: string;
        mediumGreen: string;
        lightGreen: string;
        orange: string;
        lightOrange: string;
        black: string;
        darkGray: string;
        mediumGray: string;
        lightGray: string;
        grayGreen: string;
        lightCyan: string;
      };
      semantic: {
        success: string;
        warning: string;
        error: string;
        info: string;
      };
      accessible: {
        focusRing: string;
        highContrast: string;
      };
    };
    typography: {
      fontFamilies: {
        primary: string;
        monospace: string;
      };
      fontSizes: {
        xs: string;
        sm: string;
        base: string;
        lg: string;
        xl: string;
        '2xl': string;
        '3xl': string;
        '4xl': string;
      };
      fontWeights: {
        normal: number;
        medium: number;
        semibold: number;
        bold: number;
        black: number;
      };
      lineHeights: {
        tight: string;
        normal: string;
        relaxed: string;
        loose: string;
      };
      letterSpacing: {
        tight: string;
        normal: string;
        wide: string;
      };
    };
    spacing: string[];
    borderRadius: {
      sm: string;
      md: string;
      lg: string;
      xl: string;
      '2xl': string;
      full: string;
    };
    shadows: {
      sm: string;
      md: string;
      lg: string;
      xl: string;
      '2xl': string;
    };
    breakpoints: {
      sm: string;
      md: string;
      lg: string;
      xl: string;
      '2xl': string;
    };
    zIndex: {
      dropdown: number;
      sticky: number;
      fixed: number;
      modal: number;
      popover: number;
      tooltip: number;
    };
    animations: {
      transitions: {
        base: string;
        fast: string;
        slow: string;
      };
      durations: {
        fast: string;
        base: string;
        slow: string;
      };
    };
  }
}