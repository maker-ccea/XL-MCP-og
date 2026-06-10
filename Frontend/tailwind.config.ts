import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: ['./src/**/*.{vue,ts,tsx,html}', './index.html'],
  theme: {
    extend: {
      colors: {
        'on-primary-fixed-variant': '#474746',
        'on-primary-container': '#858383',
        'on-secondary-fixed-variant': '#474741',
        'tertiary-container': '#1c1b1a',
        'surface-container': '#eceef1',
        'primary-fixed-dim': '#c8c6c5',
        'on-secondary-container': '#63635c',
        'on-error': '#ffffff',
        'inverse-on-surface': '#eff1f4',
        'surface-variant': '#e0e3e6',
        'on-primary': '#ffffff',
        outline: '#747878',
        'on-tertiary-container': '#868382',
        'surface-container-highest': '#e0e3e6',
        'on-tertiary-fixed-variant': '#484645',
        'inverse-surface': '#2d3133',
        'surface-bright': '#f7f9fc',
        tertiary: '#000000',
        'surface-dim': '#d8dadd',
        'error-container': '#ffdad6',
        'on-tertiary': '#ffffff',
        secondary: '#5f5f58',
        'secondary-container': '#e2e0d7',
        background: '#f7f9fc',
        'on-primary-fixed': '#1c1b1b',
        'inverse-primary': '#c8c6c5',
        'on-surface': '#191c1e',
        primary: '#000000',
        'tertiary-fixed': '#e6e2df',
        'primary-container': '#1c1b1b',
        error: '#ba1a1a',
        'on-secondary': '#ffffff',
        'on-background': '#191c1e',
        'surface-container-high': '#e6e8eb',
        surface: '#f7f9fc',
        'surface-tint': '#5f5e5e',
        'secondary-fixed-dim': '#c8c6bf',
        'on-tertiary-fixed': '#1c1b1a',
        'surface-container-low': '#f2f4f7',
        'surface-container-lowest': '#ffffff',
        'on-error-container': '#93000a',
        'outline-variant': '#c4c7c7',
        'tertiary-fixed-dim': '#cac6c4',
        'on-secondary-fixed': '#1c1c17',
        'on-surface-variant': '#444748',
        'primary-fixed': '#e5e2e1',
        'secondary-fixed': '#e5e2da',
        'custom-border-light': '#d3d1c7',
        'custom-border-divider': '#f0ede8'
      },
      borderRadius: {
        DEFAULT: '0.125rem',
        lg: '0.25rem',
        xl: '0.5rem',
        full: '0.75rem'
      },
      spacing: {
        'margin-mobile': '20px',
        'container-max-width': '800px',
        'margin-desktop': '40px',
        unit: '8px',
        'card-padding': '16px',
        gutter: '16px'
      },
      fontFamily: {
        'card-body': ['Inter', 'sans-serif'],
        'label-caps': ['Inter', 'sans-serif'],
        'body-main': ['Inter', 'sans-serif'],
        'card-title': ['Inter', 'sans-serif'],
        'display-welcome': ['Inter', 'sans-serif'],
        headline: ['Inter', 'sans-serif'],
        display: ['Inter', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        label: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      fontSize: {
        'card-body': ['12px', { lineHeight: '1.5', letterSpacing: '0', fontWeight: '400' }],
        'label-caps': ['11px', { lineHeight: '1', letterSpacing: '0.05em', fontWeight: '600' }],
        'body-main': ['15px', { lineHeight: '1.6', letterSpacing: '0', fontWeight: '400' }],
        'card-title': ['13px', { lineHeight: '1.4', letterSpacing: '0.01em', fontWeight: '500' }],
        'display-welcome': ['28px', { lineHeight: '1.2', letterSpacing: '-0.02em', fontWeight: '400' }],
        'mono-small': ['10px', { lineHeight: '1', letterSpacing: '0', fontWeight: '500' }]
      }
    }
  },
  plugins: []
} satisfies Config
