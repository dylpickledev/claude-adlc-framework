import streamlit as st
import _snowflake
import requests
import json
from datetime import datetime, timedelta
import time
import pandas as pd
import logging
import sys
from typing import Dict, List, Optional, Tuple, Any, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('orchestra_app.log')
    ]
)
logger = logging.getLogger(__name__)

# PostgreSQL connection imports
try:
    import psycopg2
    import psycopg2.extras
    # Check if running in local development mode
    import os

    if os.path.exists('_snowflake.py'):
        POSTGRES_AVAILABLE = False  # Force mock mode for demo
        logger.info("Running in local demo mode - database disabled")
    else:
        POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    logger.warning("PostgreSQL not available - psycopg2 not installed")

# Optional Excel export
try:
    import xlsxwriter

    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    logger.warning("Excel export not available - xlsxwriter not installed")

# PDF export imports
try:
    import matplotlib.pyplot as plt
    import matplotlib.backends.backend_pdf as backend_pdf
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.patches as patches

    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("PDF export not available - matplotlib not installed")

# Page configuration will be set in main execution block

# 🚀 PREMIUM 2024/2025 PROFESSIONAL DASHBOARD
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* 🌟 PREMIUM 2024/2025 DESIGN SYSTEM */

/* 🚀 PREMIUM TYPOGRAPHY */
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: #1a1d29 !important;
    text-rendering: optimizeLegibility;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h1, .stMarkdown h1 {
    font-size: 3.2rem !important;
    font-weight: 900 !important;
    margin-bottom: 1.5rem !important;
}

h2, .stMarkdown h2 {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    margin: 2rem 0 1rem 0 !important;
}

h3, .stMarkdown h3 {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin: 1.5rem 0 0.75rem 0 !important;
}
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --glass-bg: rgba(255, 255, 255, 0.85);
    --glass-border: rgba(255, 255, 255, 0.2);
    --shadow-subtle: 0 4px 20px rgba(0, 0, 0, 0.08);
    --shadow-medium: 0 8px 40px rgba(0, 0, 0, 0.12);
    --shadow-strong: 0 16px 60px rgba(0, 0, 0, 0.15);
    --border-radius: 16px;
    --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-attachment: fixed;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #343a40;
    min-height: 100vh;
    position: relative;
}

/* ✨ Subtle Professional Texture */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
        linear-gradient(135deg, rgba(108, 117, 125, 0.02) 0%, transparent 50%),
        radial-gradient(circle at 30% 80%, rgba(0, 86, 179, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 70% 20%, rgba(108, 117, 125, 0.02) 0%, transparent 50%);
    z-index: -1;
}

/* 💼 MODERN & SLEEK SIDEBAR */
.css-1d391kg, [data-testid="stSidebar"] {
    background: #f0f2f6 !important;
    border-right: 1px solid rgba(108, 117, 125, 0.15) !important;
    box-shadow:
        0 2px 12px rgba(108, 117, 125, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    position: relative;
    overflow: hidden;
}

.css-1d391kg::before, [data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg,
        rgba(0, 86, 179, 0.02) 0%,
        rgba(108, 117, 125, 0.02) 50%,
        rgba(255, 255, 255, 0.1) 100%) !important;
    z-index: -1;
}

/* Force Modern & Sleek styling over default Streamlit styles */
.css-1d391kg, [data-testid="stSidebar"],
.css-1d391kg > div, [data-testid="stSidebar"] > div {
    background-color: #f0f2f6 !important;
    color: #212529 !important;
}

/* 💼 MODERN & SLEEK NAVIGATION */
.css-1d391kg .stRadio > label, [data-testid="stSidebar"] .stRadio > label {
    color: #212529 !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 14px 18px;
    border-radius: 8px;
    margin: 6px 12px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(108, 117, 125, 0.12);
    background: rgba(255, 255, 255, 0.8) !important;
    position: relative;
    overflow: hidden;
}

.css-1d391kg .stRadio > label::before, [data-testid="stSidebar"] .stRadio > label::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 86, 179, 0.08), transparent);
    transition: left 0.4s ease;
}

.css-1d391kg .stRadio > label:hover, [data-testid="stSidebar"] .stRadio > label:hover {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(0, 86, 179, 0.25);
    transform: translateY(-1px);
    color: #0056b3;
    box-shadow: 0 4px 12px rgba(108, 117, 125, 0.15);
}

.css-1d391kg .stRadio > label:hover::before, [data-testid="stSidebar"] .stRadio > label:hover::before {
    left: 100%;
}

.css-1d391kg .stRadio > label[data-checked="true"], [data-testid="stSidebar"] .stRadio > label[data-checked="true"] {
    background: linear-gradient(135deg, #0056b3, #6c757d);
    border-color: #0056b3;
    color: white;
    font-weight: 600;
    box-shadow:
        0 4px 15px rgba(0, 86, 179, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* 💼 Modern Sidebar Typography */
.css-1d391kg h3, [data-testid="stSidebar"] h3 {
    color: #212529 !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    margin-bottom: 14px;
    letter-spacing: 0.025em;
}

.css-1d391kg .stMarkdown, [data-testid="stSidebar"] .stMarkdown {
    color: #212529 !important;
}

/* Ensure all sidebar text is dark and visible */
.css-1d391kg, [data-testid="stSidebar"] {
    color: #212529 !important;
}

.css-1d391kg p, [data-testid="stSidebar"] p,
.css-1d391kg div, [data-testid="stSidebar"] div,
.css-1d391kg span, [data-testid="stSidebar"] span,
.css-1d391kg label, [data-testid="stSidebar"] label {
    color: #212529 !important;
}

/* 💼 MODERN SLEEK PIPELINE BUTTONS */
.css-1d391kg .stButton > button, [data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #0056b3, #6c757d);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 18px;
    font-weight: 600;
    font-size: 14px;
    width: 100%;
    margin: 6px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow:
        0 2px 8px rgba(0, 86, 179, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    position: relative;
    overflow: hidden;
}

.css-1d391kg .stButton > button::before, [data-testid="stSidebar"] .stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
    transition: left 0.5s ease;
}

.css-1d391kg .stButton > button:hover, [data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 4px 16px rgba(0, 86, 179, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, #0066cc, #5a6268);
}

.css-1d391kg .stButton > button:hover::before, [data-testid="stSidebar"] .stButton > button:hover::before {
    left: 100%;
}

/* 🌟 PREMIUM GLASSMORPHISM MAIN CONTAINER */
.main .block-container {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: var(--border-radius);
    border: 1px solid var(--glass-border);
    box-shadow: var(--shadow-medium);
    padding: 3rem;
    margin: 1.5rem auto;
    max-width: 1400px;
    position: relative;
    overflow: hidden;
    transition: var(--transition-smooth);
}

.main .block-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--primary-gradient);
    border-radius: var(--border-radius) var(--border-radius) 0 0;
}

.main .block-container:hover {
    box-shadow: var(--shadow-strong);
    transform: translateY(-2px);
}

/* 🚀 PREMIUM 2024/2025 BUTTON STYLING */
.stButton > button {
    background: var(--primary-gradient);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 16px 24px;
    font-weight: 600;
    font-size: 13px;
    transition: var(--transition-smooth);
    box-shadow: var(--shadow-subtle);
    position: relative;
    overflow: hidden;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    backdrop-filter: blur(10px);
}

/* Premium shimmer effect on hover */

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
    transition: left 0.5s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 4px 16px rgba(0, 86, 179, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, #0066cc, #5a6268);
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button[data-baseweb="button"][kind="primary"] {
    background: linear-gradient(135deg, #0056b3, #6c757d);
    border-color: #0056b3;
    color: white;
    box-shadow:
        0 2px 10px rgba(0, 86, 179, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.stButton > button[data-baseweb="button"][kind="primary"]:hover {
    background: linear-gradient(135deg, #0066cc, #5a6268);
    transform: translateY(-2px);
    box-shadow:
        0 4px 16px rgba(0, 86, 179, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* 💼 MODERN SLEEK METRIC CARDS */
div[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(108, 117, 125, 0.12);
    border-radius: 12px;
    padding: 20px;
    box-shadow:
        0 2px 8px rgba(108, 117, 125, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
    border-left: 3px solid #0056b3;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow:
        0 4px 16px rgba(108, 117, 125, 0.12),
        inset 0 1px 0 rgba(255, 255, 255, 1);
    border-color: rgba(0, 86, 179, 0.25);
}

/* Use default Streamlit data table styling */

/* 💼 MODERN EXPANDERS */
.streamlit-expanderHeader {
    background: rgba(240, 242, 246, 0.8);
    border: 1px solid rgba(108, 117, 125, 0.15);
    border-radius: 8px;
    font-weight: 500;
    color: #343a40;
    padding: 16px 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 6px rgba(108, 117, 125, 0.08);
}

.streamlit-expanderHeader:hover {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(0, 86, 179, 0.25);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(108, 117, 125, 0.12);
    color: #0056b3;
}

/* 💼 MODERN FORM ELEMENTS */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(108, 117, 125, 0.2);
    border-radius: 6px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: #343a40;
    font-weight: 400;
    padding: 10px 14px;
    box-shadow:
        0 1px 4px rgba(108, 117, 125, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #0056b3;
    background: rgba(255, 255, 255, 1);
    box-shadow:
        0 0 0 3px rgba(0, 86, 179, 0.1),
        0 2px 8px rgba(0, 86, 179, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 1);
    transform: translateY(-1px);
}

/* Modern Dropdown Styling */
.stSelectbox > div > div > div {
    background: rgba(255, 255, 255, 0.98);
    color: #212529;
    border: 1px solid rgba(108, 117, 125, 0.2);
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(108, 117, 125, 0.1);
}

/* Fix dropdown options visibility - comprehensive */
.stSelectbox > div > div > div > div {
    color: #212529 !important;
    background: white !important;
    font-weight: 400 !important;
}

.stSelectbox > div > div > div > div:hover {
    background: rgba(0, 86, 179, 0.1) !important;
    color: #212529 !important;
}

.stSelectbox > div > div > div[data-baseweb="select"] > div {
    color: #212529 !important;
}

/* Fix dropdown menu list items */
.stSelectbox div[role="listbox"] div {
    color: #212529 !important;
    background: white !important;
}

.stSelectbox div[role="listbox"] div:hover {
    background: rgba(0, 86, 179, 0.1) !important;
    color: #212529 !important;
}

/* Fix selected value display */
.stSelectbox > div > div > div[data-baseweb="select"] span {
    color: #212529 !important;
}

/* 💼 MODERN TYPOGRAPHY SYSTEM */
.stSelectbox label,
.stTextInput label,
.stNumberInput label,
.stRadio label,
.stCheckbox label {
    color: #343a40;
    font-weight: 500;
    font-size: 15px;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.01em;
    margin-bottom: 6px;
}

/* Modern Radio and Checkbox */
.stRadio > div {
    color: #343a40;
    font-weight: 400;
}

.stCheckbox > div {
    color: #343a40;
    font-weight: 400;
}

/* Professional Status Indicators */
.stAlert {
    border-radius: 8px;
    border-left: 4px solid;
    font-weight: 500;
    padding: 16px;
}

.stSuccess {
    border-left-color: #27AE60;
    background: #E8F8F5;
    color: #1B5E20;
}

.stError {
    border-left-color: #C0392B;
    background: #FDEDEC;
    color: #B71C1C;
}

.stWarning {
    border-left-color: #E67E22;
    background: #FEF9E7;
    color: #E65100;
}

.stInfo {
    border-left-color: #2980B9;
    background: #EBF3FD;
    color: #0D47A1;
}

/* 💼 MODERN SLEEK TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
    padding: 6px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(240, 242, 246, 0.8);
    border-radius: 8px;
    border: 1px solid rgba(108, 117, 125, 0.15);
    font-weight: 500;
    color: #343a40;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 12px 20px;
    box-shadow:
        0 2px 4px rgba(108, 117, 125, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(0, 86, 179, 0.25);
    transform: translateY(-1px);
    box-shadow:
        0 4px 8px rgba(108, 117, 125, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 1);
    color: #0056b3;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0056b3, #6c757d);
    color: white;
    border-color: #0056b3;
    box-shadow:
        0 3px 12px rgba(0, 86, 179, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
}

/* 💼 MODERN SPINNER STYLING */
.stSpinner > div {
    border-color: #6c757d;
    border-top-color: #0056b3;
}

.stSpinner {
    filter: drop-shadow(0 2px 4px rgba(108, 117, 125, 0.1));
}

/* 💼 MODERN PROFESSIONAL TYPOGRAPHY HIERARCHY */
h1, h2, h3, h4, h5, h6 {
    color: #343a40;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    line-height: 1.3;
    letter-spacing: -0.01em;
}

h1 {
    font-size: 36px;
    color: #343a40;
    font-weight: 700;
    margin-bottom: 20px;
}

h2 {
    font-size: 28px;
    color: #0056b3;
    font-weight: 600;
    margin-bottom: 18px;
}

h3 {
    font-size: 22px;
    color: #343a40;
    font-weight: 600;
    margin-bottom: 14px;
}

h4 {
    font-size: 18px;
    color: #6c757d;
    font-weight: 500;
    margin-bottom: 12px;
}

/* Modern Content Text */
.stMarkdown {
    line-height: 1.6;
    color: #343a40;
    font-family: 'Inter', sans-serif;
}

.stMarkdown p {
    color: #343a40;
    font-size: 15px;
    font-weight: 400;
    line-height: 1.6;
    margin-bottom: 14px;
}

.stMarkdown strong {
    color: #0056b3;
    font-weight: 600;
}

.stMarkdown em {
    color: #6c757d;
    font-style: italic;
}

/* Use default Streamlit data table styling */

/* Custom card hover effects */
.hover-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

/* Loading and Alert Animations */
@keyframes pulse {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: 0.8;
        transform: scale(1.02);
    }
}

.loading-indicator {
    animation: pulse 2s infinite;
}

/* Specific pulse for financial alerts */
@keyframes financial-alert-pulse {
    0%, 100% {
        border-color: #C0392B;
        box-shadow: 0 0 0 0 rgba(192, 57, 43, 0.7);
    }
    50% {
        border-color: #E74C3C;
        box-shadow: 0 0 0 4px rgba(192, 57, 43, 0.3);
    }
}
</style>
""", unsafe_allow_html=True)

# 🔥 ENHANCED DROPDOWN STYLING WITH VISIBILITY FIX
st.markdown("""
<style>
/* Enhanced selectbox with visibility fix */
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    border-radius: 8px !important;
}

/* CRITICAL DROPDOWN VISIBILITY FIX */
.stSelectbox [data-baseweb="popover"] {
    background: white !important;
    border: 1px solid #ddd !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
    z-index: 999999 !important;
}

.stSelectbox [data-baseweb="popover"] [role="option"] {
    background: white !important;
    color: #333 !important;
    padding: 8px 12px !important;
    border-bottom: 1px solid #f0f0f0 !important;
}

.stSelectbox [data-baseweb="popover"] [role="option"]:hover {
    background: #f5f5f5 !important;
    color: #000 !important;
}

/* CRITICAL SIDEBAR TEXT FIX - FORCE DARK COLOR */
section[data-testid="stSidebar"] *,
.css-1d391kg *,
div[data-testid="stSidebar"] *,
.css-1cypcdb *,
.css-17eq0hr * {
    color: #212529 !important;
}

/* CRITICAL NAVIGATION TEXT FIX */
section[data-testid="stSidebar"] .stRadio label,
.css-1d391kg .stRadio label,
div[data-testid="stSidebar"] .stRadio label,
.css-1cypcdb .stRadio label,
.css-17eq0hr .stRadio label,
section[data-testid="stSidebar"] .stRadio > label,
div[data-testid="stSidebar"] .stRadio > label {
    color: #212529 !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    background: rgba(255, 255, 255, 0.9) !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    margin: 4px 8px !important;
}

/* FORCE ALL RADIO BUTTON TEXT TO BE DARK */
section[data-testid="stSidebar"] .stRadio > div > label,
section[data-testid="stSidebar"] .stRadio div label,
section[data-testid="stSidebar"] .stRadio label span,
div[data-testid="stSidebar"] .stRadio > div > label,
div[data-testid="stSidebar"] .stRadio div label,
div[data-testid="stSidebar"] .stRadio label span {
    color: #212529 !important;
    font-weight: 600 !important;
    font-size: 11px !important;
}

/* ULTRA SPECIFIC INACTIVE TAB COLOR FIX */
section[data-testid="stSidebar"] .stRadio input:not(:checked) + label,
section[data-testid="stSidebar"] .stRadio input:not(:checked) ~ label,
section[data-testid="stSidebar"] .stRadio > div:not(.selected) label,
div[data-testid="stSidebar"] .stRadio input:not(:checked) + label,
div[data-testid="stSidebar"] .stRadio input:not(:checked) ~ label,
div[data-testid="stSidebar"] .stRadio > div:not(.selected) label,
.css-1d391kg .stRadio input:not(:checked) + label,
.css-1d391kg .stRadio input:not(:checked) ~ label,
.css-1cypcdb .stRadio input:not(:checked) + label,
.css-1cypcdb .stRadio input:not(:checked) ~ label {
    color: #343a40 !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

/* CATCH-ALL SIDEBAR TEXT COLOR */
section[data-testid="stSidebar"] label[data-testid],
section[data-testid="stSidebar"] label,
div[data-testid="stSidebar"] label[data-testid],
div[data-testid="stSidebar"] label {
    color: #343a40 !important;
}

/* CRITICAL BUTTON CONSISTENCY FIX */
.stButton button,
section[data-testid="stSidebar"] .stButton button,
.css-1d391kg .stButton button,
div[data-testid="stSidebar"] .stButton button,
button[kind="primary"],
button[kind="secondary"],
.main .stButton button {
    background: linear-gradient(135deg, #0056b3, #6c757d) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 18px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0, 86, 179, 0.2) !important;
}

.stButton button:hover,
section[data-testid="stSidebar"] .stButton button:hover,
.css-1d391kg .stButton button:hover,
div[data-testid="stSidebar"] .stButton button:hover,
button[kind="primary"]:hover,
button[kind="secondary"]:hover,
.main .stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(0, 86, 179, 0.3) !important;
    background: linear-gradient(135deg, #0066cc, #5a6268) !important;
}

/* CRITICAL SIDEBAR BACKGROUND FIX */
section[data-testid="stSidebar"],
.css-1d391kg,
div[data-testid="stSidebar"],
.css-1cypcdb,
.css-17eq0hr {
    background: #f0f2f6 !important;
}

/* FORCE APP BACKGROUND */
.stApp {
    background: #ffffff !important;
    color: #343a40 !important;
}

/* OVERRIDE ANY REMAINING LIGHT TEXT */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label,
.css-1d391kg p,
.css-1d391kg span,
.css-1d391kg div,
.css-1d391kg label {
    color: #212529 !important;
}

/* MAIN CONTENT AREA RADIO BUTTON TEXT FIX */
.main .stRadio label,
.main .stRadio > div > label,
.main .stRadio div label,
.main .stRadio span,
div[data-testid="column"] .stRadio label,
div[data-testid="column"] .stRadio > div > label,
div[data-testid="column"] .stRadio div label,
div[data-testid="column"] .stRadio span,
section[data-testid="stAppViewContainer"] .stRadio label,
section[data-testid="stAppViewContainer"] .stRadio > div > label,
section[data-testid="stAppViewContainer"] .stRadio div label,
section[data-testid="stAppViewContainer"] .stRadio span {
    color: #343a40 !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

/* UNIVERSAL RADIO BUTTON TEXT COLOR OVERRIDE */
.stRadio label,
.stRadio > div > label,
.stRadio div label,
.stRadio span {
    color: #343a40 !important;
    font-weight: 500 !important;
}

/* MAIN CONTENT AREA TEXT VISIBILITY FIX */
.main p,
.main span,
.main div,
.main label,
.main h1,
.main h2,
.main h3,
.main h4,
.main h5,
.main h6,
div[data-testid="column"] p,
div[data-testid="column"] span,
div[data-testid="column"] div,
div[data-testid="column"] label,
section[data-testid="stAppViewContainer"] p,
section[data-testid="stAppViewContainer"] span,
section[data-testid="stAppViewContainer"] div,
section[data-testid="stAppViewContainer"] label {
    color: #343a40 !important;
}

/* DROPDOWN AND INPUT LABELS IN MAIN CONTENT */
.main .stSelectbox label,
.main .stSelectbox > label,
.main .stTextInput label,
.main .stTextInput > label,
div[data-testid="column"] .stSelectbox label,
div[data-testid="column"] .stSelectbox > label,
div[data-testid="column"] .stTextInput label,
div[data-testid="column"] .stTextInput > label,
section[data-testid="stAppViewContainer"] .stSelectbox label,
section[data-testid="stAppViewContainer"] .stSelectbox > label,
section[data-testid="stAppViewContainer"] .stTextInput label,
section[data-testid="stAppViewContainer"] .stTextInput > label {
    color: #343a40 !important;
    font-weight: 600 !important;
}

/* UNIVERSAL TEXT COLOR OVERRIDE - CATCH ALL */
.stApp p,
.stApp span,
.stApp div:not([data-testid="stSidebar"]),
.stApp label:not([data-testid="stSidebar"] label) {
    color: #343a40 !important;
}

/* IMPROVED DROPDOWN STYLING - SELECTED VALUE VISIBLE */
.stSelectbox [data-baseweb="select"] {
    background: #ffffff !important;
    border: 1px solid #6c757d !important;
    border-radius: 6px !important;
    min-height: 40px !important;
}

.stSelectbox [data-baseweb="select"]:hover {
    border-color: #0056b3 !important;
    box-shadow: 0 2px 6px rgba(0, 86, 179, 0.1) !important;
}

/* CRITICAL: SELECTED VALUE VISIBILITY FIX */
.stSelectbox [data-baseweb="select"] input,
.stSelectbox [data-baseweb="select"] input + div,
.stSelectbox [data-baseweb="select"] span[data-baseweb="tag"],
.stSelectbox [data-baseweb="select"] .css-1wa3eu0-placeholder,
.stSelectbox [data-baseweb="select"] .css-1dimb5e-singleValue,
div[data-baseweb="select"] span {
    color: #212529 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    opacity: 1 !important;
    background: transparent !important;
}

/* DROPDOWN CONTAINER TEXT */
.stSelectbox [data-baseweb="select"] > div {
    color: #212529 !important;
    background: #ffffff !important;
    padding: 8px 12px !important;
}

/* DROPDOWN ARROW */
.stSelectbox [data-baseweb="select"] svg {
    color: #6c757d !important;
    width: 16px !important;
    height: 16px !important;
}

/* DROPDOWN MENU OPTIONS */
.stSelectbox [data-baseweb="select"] [role="listbox"] {
    border-radius: 6px !important;
    border: 1px solid #dee2e6 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

.stSelectbox [data-baseweb="select"] [role="option"] {
    color: #212529 !important;
    font-weight: 500 !important;
    padding: 10px 12px !important;
    background: #ffffff !important;
}

.stSelectbox [data-baseweb="select"] [role="option"]:hover {
    background: #f8f9fa !important;
    color: #0056b3 !important;
}
</style>
""", unsafe_allow_html=True)

# Constants
REFRESH_PIPELINE_ID = "c468dd21-7af0-4892-9f48-d8cdf24d9b7d"  # Original pipeline for refresh
FINAL_PIPELINE_ID = "daa39221-b30f-4b27-a8ee-a1b98ca28d0f"  # New pipeline for finalize
DB_TIMEOUT = 30
CACHE_TTL = 300
MAX_RETRIES = 3


def get_orchestra_token() -> Optional[str]:
    """Get Orchestra token from Snowflake secrets with error handling"""
    try:
        token = _snowflake.get_generic_secret_string('orchestra_token')
        if not token:
            raise ValueError("Orchestra token is empty")
        return token
    except Exception as e:
        logger.error(f"Failed to retrieve orchestra token: {str(e)}")
        st.error("Failed to retrieve authentication token. Please contact your administrator.")
        st.stop()
        return None


def get_db_connection():
    """Get database connection with proper error handling - Mock mode for demo"""
    # For local development/demo mode, skip actual database connection
    import os
    if os.path.exists('_snowflake.py'):  # Local development mode detected
        logger.info("Running in local demo mode - using mock data")
        return None

    try:
        host = 'postgres.grc-ops.com'
        port = '5432'
        database = 'fellowship_of_data'
        username = _snowflake.get_generic_secret_string('postgres_username')
        password = _snowflake.get_generic_secret_string('postgres_password')

        if not username or not password:
            raise ValueError("Database credentials are missing")

        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password,
            sslmode='require',
            connect_timeout=DB_TIMEOUT
        )

        with conn.cursor() as cursor:
            cursor.execute("SET statement_timeout = 30000")

        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise


def query_postgres(query: str, params: Optional[Dict] = None, max_retries: int = MAX_RETRIES) -> Optional[pd.DataFrame]:
    """Execute a query against PostgreSQL with retry logic and comprehensive error handling"""
    if not POSTGRES_AVAILABLE:
        st.error("Database connection not available. Please contact your administrator.")
        return None

    for attempt in range(max_retries):
        conn = None
        try:
            conn = get_db_connection()

            # Log query for debugging (without sensitive params)
            logger.info(f"Executing query attempt {attempt + 1}")

            df = pd.read_sql_query(query, conn, params=params)
            logger.info(f"Query successful, returned {len(df)} rows")
            return df

        except psycopg2.OperationalError as e:
            logger.error(f"Database operational error (attempt {attempt + 1}): {str(e)}")
            if attempt == max_retries - 1:
                st.error("Database connection failed. Please try again later.")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff

        except psycopg2.Error as e:
            logger.error(f"Database error: {str(e)}")
            st.error("Database query failed. Please check your filters and try again.")
            return None

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            st.error("An unexpected error occurred. Please contact support.")
            return None

        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass


@st.cache_data(ttl=600, show_spinner=False)  # 10 minutes cache, no spinner
def get_batch_id_options(batch_type: str, is_proof: str) -> Tuple[List[str], Optional[str]]:
    """Get distinct batch_id values based on batch_type and is_proof filters
    Returns tuple of (options_list, max_batch_id)"""
    if not POSTGRES_AVAILABLE:
        return (["All"], None)

    try:
        query = """
                SELECT DISTINCT batch_id
                FROM dbt_dev_accounting.rpt_r245t_apex_sales_journal_tieout_app_only
                WHERE batch_type = %(batch_type)s
                  AND is_proof = %(is_proof)s
                ORDER BY batch_id DESC LIMIT 100 \
                """

        params = {
            'batch_type': batch_type,
            'is_proof': is_proof
        }

        df = query_postgres(query, params)
        if df is not None and not df.empty:
            batch_ids = df['batch_id'].tolist()
            max_batch_id = batch_ids[0] if batch_ids else None  # First item is max due to DESC order
            return (["All"] + batch_ids, max_batch_id)
        else:
            return (["All"], None)
    except Exception as e:
        logger.error(f"Failed to get batch ID options: {str(e)}")
        return (["All"], None)


@st.cache_data(ttl=600, show_spinner=False)  # 10 minutes cache, no spinner
def get_invalid_account_options(batch_type: str, is_proof: str, batch_id: str) -> List[str]:
    """Get distinct invalid account (error) values for dropdown based on current filters"""
    if not POSTGRES_AVAILABLE:
        return ["All"]

    try:
        where_conditions = []
        params = {}

        # Add batch type filter
        where_conditions.append("batch_type = %(batch_type)s")
        params['batch_type'] = batch_type

        # Add is_proof filter
        where_conditions.append("is_proof = %(is_proof)s")
        params['is_proof'] = is_proof

        # Add batch_id filter if not "All"
        if batch_id and batch_id != 'All':
            where_conditions.append("batch_id = %(batch_id)s")
            params['batch_id'] = batch_id

        where_conditions.append("error IS NOT NULL")

        query = f"""
            SELECT DISTINCT error 
            FROM dbt_dev_accounting.dash_r245a_apex_sales_journal_review_summary 
            WHERE {' AND '.join(where_conditions)}
            ORDER BY error
            LIMIT 50
        """

        df = query_postgres(query, params)
        if df is not None and not df.empty:
            return ["All"] + df['error'].tolist()
        else:
            return ["All"]
    except Exception as e:
        logger.error(f"Failed to get invalid account options: {str(e)}")
        return ["All"]


@st.cache_data(ttl=600, show_spinner=False)  # 10 minutes cache, no spinner
def get_branch_id_options(batch_type: str) -> List[str]:
    """Get distinct branch_id values for dropdown with caching"""
    if not POSTGRES_AVAILABLE:
        return ["All"]

    try:
        where_conditions = []
        params = {}

        # Add batch type filter
        where_conditions.append("batch_type = %(batch_type)s")
        params['batch_type'] = batch_type

        where_conditions.append("branch_id IS NOT NULL AND branch_id != '' AND branch_id != 'null'")

        query = f"""
            SELECT DISTINCT branch_id 
            FROM dbt_dev_accounting.dash_r245a_apex_sales_journal_review_detail 
            WHERE {' AND '.join(where_conditions)}
            ORDER BY branch_id
            LIMIT 50
        """

        df = query_postgres(query, params)
        if df is not None and not df.empty:
            return ["All"] + df['branch_id'].tolist()
        else:
            return ["All"]
    except Exception as e:
        logger.error(f"Failed to get branch options: {str(e)}")
        return ["All"]


@st.cache_data(ttl=300, show_spinner=False)  # 5 minutes cache
def get_out_of_balance_total(batch_type: str, batch_id: str, is_proof: str) -> Tuple[float, str]:
    """Get the total amount from out of balance table and return (total, color)"""
    # Check if is_proof is 'N' - if so, return 0 and gray
    if is_proof == 'N':
        return (0.0, "gray")

    if not POSTGRES_AVAILABLE:
        return (0.0, "gray")

    try:
        # First, check if there's any data in the sales journal for these filters
        journal_check_conditions = []
        journal_params = {}

        # Add batch type filter
        journal_check_conditions.append("batch_type = %(batch_type)s")
        journal_params['batch_type'] = batch_type

        # Add is_proof filter
        journal_check_conditions.append("is_proof = %(is_proof)s")
        journal_params['is_proof'] = is_proof

        # Add batch_id filter if not "All"
        if batch_id and batch_id != 'All':
            journal_check_conditions.append("batch_id = %(batch_id)s")
            journal_params['batch_id'] = batch_id

        # Check if there's any journal data
        journal_check_query = f"""
            SELECT COUNT(*) as record_count
            FROM dbt_dev_accounting.dash_r245a_apex_sales_journal_review_summary
            WHERE {' AND '.join(journal_check_conditions)}
            LIMIT 1
        """

        journal_df = query_postgres(journal_check_query, journal_params)

        # If no journal data exists, return 0
        if journal_df is None or journal_df.empty or journal_df['record_count'].iloc[0] == 0:
            logger.info(
                f"No journal data found for filters: batch_type={batch_type}, is_proof={is_proof}, batch_id={batch_id}")
            return (0.0, "gray")

        # Now get the out of balance total
        where_conditions = []
        params = {}

        # Add batch type filter
        where_conditions.append("batch_type = %(batch_type)s")
        params['batch_type'] = batch_type

        # Add batch_id filter if not "All"
        if batch_id and batch_id != 'All':
            where_conditions.append("batch_id = %(batch_id)s")
            params['batch_id'] = batch_id

        query = f"""
            SELECT COALESCE(SUM(amount), 0) as total_amount
            FROM dbt_dev_accounting.dash_r245a_apex_sales_journal_review_out_of_balance
            WHERE {' AND '.join(where_conditions)}
        """

        df = query_postgres(query, params)  # Use default retries
        if df is not None and not df.empty:
            total = df['total_amount'].iloc[0]
            color = "red" if abs(total) > 0.02 else "green"
            return (total, color)
        else:
            return (0.0, "gray")
    except Exception as e:
        logger.error(f"Failed to get out of balance total: {str(e)}")
        return (0.0, "gray")


@st.cache_data(ttl=300, show_spinner=False)  # Increased TTL to 5 minutes, no spinner
def get_tieout_status_emoji() -> str:
    """Get emoji for tieout tab based on data status with caching"""
    if not POSTGRES_AVAILABLE:
        return "❓"

    try:
        # Optimized query - only check first 100 rows for performance
        query = "SELECT test FROM dbt_dev_accounting.rpt_r245t_apex_sales_journal_tieout_app_only LIMIT 100"
        data = query_postgres(query)  # Use default retries
        if data is not None and not data.empty:
            all_ties = (data['test'] == 'TIES').all()
            return "✅" if all_ties else "❌"
        else:
            return "❓"
    except Exception as e:
        logger.error(f"Failed to get tieout status: {str(e)}")
        return "❓"


def get_tieout_records_status_emoji() -> str:
    """Get emoji for tieout records tab based on DMS task status with caching"""
    if not POSTGRES_AVAILABLE:
        return "❓"

    try:
        # Check DMS task status
        query = "SELECT task_status FROM dbt_dev_utils.fact_aws_dms__status"
        data = query_postgres(query)
        if data is not None and not data.empty:
            all_change_processing = (data['task_status'] == 'CHANGE PROCESSING').all()
            return "✅" if all_change_processing else "❌"
        else:
            return "❓"
    except Exception as e:
        logger.error(f"Failed to get tieout records status: {str(e)}")
        return "❓"


def invalidate_out_of_balance_cache():
    """Helper function to invalidate the out of balance cache when filters change"""
    if 'out_of_balance_filters' in st.session_state:
        st.session_state['out_of_balance_filters'] = ""  # Force recalculation


# Initialize session state with validation
def initialize_session_state():
    """Initialize session state variables with defaults"""
    # Get the max batch_id for default batch_type and is_proof
    default_batch_type = 'CASH'
    default_is_proof = 'Y'
    batch_options, max_batch_id = get_batch_id_options(default_batch_type, default_is_proof)
    default_batch_id = max_batch_id if max_batch_id else 'All'

    defaults = {
        'pipeline_run_id': None,
        'pipeline_type': None,  # 'refresh' or 'final'
        'last_run_time': None,
        'pipeline_status': None,
        'run_details': None,
        'pending_refresh': False,  # Add this flag to track when we're expecting a refresh
        'active_tab_index': 0,
        'shared_batch_type': default_batch_type,
        'shared_is_proof': default_is_proof,
        'shared_batch_id': default_batch_id,  # Now defaults to max batch_id
        'shared_invalid_account': "All",  # Changed from checkboxes to single dropdown value
        'shared_accountcode': "",
        'detail_item_id': "",
        'detail_ticket_number': "",
        'detail_bol_other_ticket': "",
        'detail_branch_id': "All",
        'ticket_number_1140': "",
        'show_finalize_confirmation': False,
        'previous_batch_type': default_batch_type,
        'previous_is_proof': default_is_proof,
        'out_of_balance_total': 0.0,  # Cache the total
        'out_of_balance_color': "gray",  # Cache the color
        'out_of_balance_filters': f"{default_batch_type}_{default_batch_id}_{default_is_proof}",  # Track filter state
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()


def refresh_and_reset_filters():
    """Refresh cached data and reset filters to defaults with latest data"""
    try:
        # Get default values
        default_batch_type = 'CASH'
        default_is_proof = 'Y'

        # Clear any cached tieout emoji
        if 'tieout_emoji' in st.session_state:
            del st.session_state['tieout_emoji']
        if 'tieout_emoji_timestamp' in st.session_state:
            del st.session_state['tieout_emoji_timestamp']
        # Clear any cached tieout records emoji
        if 'tieout_records_emoji' in st.session_state:
            del st.session_state['tieout_records_emoji']
        if 'tieout_records_emoji_timestamp' in st.session_state:
            del st.session_state['tieout_records_emoji_timestamp']

        # Get fresh batch options (cache was cleared, so this will fetch new data)
        batch_options, max_batch_id = get_batch_id_options(default_batch_type, default_is_proof)
        default_batch_id = max_batch_id if max_batch_id else 'All'

        # Reset all filter values to defaults with fresh data
        st.session_state['shared_batch_type'] = default_batch_type
        st.session_state['shared_is_proof'] = default_is_proof
        st.session_state['shared_batch_id'] = default_batch_id
        st.session_state['shared_invalid_account'] = "All"
        st.session_state['shared_accountcode'] = ""
        st.session_state['detail_item_id'] = ""
        st.session_state['detail_ticket_number'] = ""
        st.session_state['detail_bol_other_ticket'] = ""
        st.session_state['detail_branch_id'] = "All"
        st.session_state['ticket_number_1140'] = ""
        st.session_state['previous_batch_type'] = default_batch_type
        st.session_state['previous_is_proof'] = default_is_proof

        # Clear out of balance cache
        st.session_state['out_of_balance_total'] = 0.0
        st.session_state['out_of_balance_color'] = "gray"
        st.session_state['out_of_balance_filters'] = f"{default_batch_type}_{default_batch_id}_{default_is_proof}"

        logger.info(f"Filters reset to defaults with fresh data. New batch_id: {default_batch_id}")

    except Exception as e:
        logger.error(f"Error resetting filters: {str(e)}")


def trigger_pipeline(pipeline_id: str, pipeline_type: str) -> Optional[Dict]:
    """Trigger an Orchestra pipeline with comprehensive error handling"""
    url = f"https://app.getorchestra.io/engine/public/pipelines/{pipeline_id}/start"

    bearer_token = get_orchestra_token()
    if not bearer_token:
        return None

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    try:
        logger.info(f"Triggering {pipeline_type} pipeline {pipeline_id}")
        response = requests.post(url, headers=headers, json={}, timeout=30)
        response.raise_for_status()
        result = response.json()
        logger.info(f"{pipeline_type} pipeline triggered successfully: {result.get('pipelineRunId')}")
        return result
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Please check your internet connection.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("Authentication failed. Please contact your administrator.")
        elif e.response.status_code == 403:
            st.error("Permission denied. You don't have access to trigger this pipeline.")
        else:
            st.error(f"Pipeline trigger failed with status {e.response.status_code}")
        logger.error(f"HTTP error triggering pipeline: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error triggering pipeline: {str(e)}")
        st.error("Failed to trigger pipeline. Please try again or contact support.")
        return None


def get_pipeline_status(pipeline_run_id: str) -> Optional[Dict]:
    """Get the status of a pipeline run with error handling"""
    url = "https://app.getorchestra.io/api/engine/public/pipeline_runs"

    bearer_token = get_orchestra_token()
    if not bearer_token:
        return None

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    params = {
        "pipeline_run_ids": pipeline_run_id
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if results:
            return results[0]
        else:
            logger.warning(f"No results found for pipeline run {pipeline_run_id}")
            return None

    except Exception as e:
        logger.error(f"Failed to get pipeline status: {str(e)}")
        st.error("Failed to get pipeline status. Please try again.")
        return None


def get_pipeline_history(pipeline_ids: List[str], limit: int = 10) -> Optional[List[Dict]]:
    """Get the last few runs of specific pipelines with error handling"""
    bearer_token = get_orchestra_token()
    if not bearer_token:
        return None

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    all_pipeline_runs = []
    page = 1
    max_pages = 10  # Prevent infinite loops

    try:
        while page <= max_pages:
            url = "https://app.getorchestra.io/api/engine/public/pipeline_runs"
            params = {
                "page": page,
                "per_page": 100
            }

            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            if not results:
                break

            # Filter for both pipeline IDs
            pipeline_runs = [run for run in results if run.get("pipelineId") in pipeline_ids]
            all_pipeline_runs.extend(pipeline_runs)

            # Stop if we have enough runs
            if len(all_pipeline_runs) >= limit * len(pipeline_ids):  # Get more runs since we have multiple pipelines
                break

            actual_page_size = data.get('pageSize', 50)
            if len(results) < actual_page_size:
                break

            page += 1

        all_pipeline_runs.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
        return all_pipeline_runs[:limit]

    except Exception as e:
        logger.error(f"Failed to get pipeline history: {str(e)}")
        st.error("Failed to load pipeline history.")
        return None


def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp for display in Pacific Time with proper DST handling"""
    if not timestamp_str:
        return "Unknown"
    try:
        # Parse UTC timestamp
        dt_utc = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

        # Determine if we're in DST (roughly March 2nd Sunday to November 1st Sunday)
        year = dt_utc.year
        month = dt_utc.month
        day = dt_utc.day

        # Simple DST check: March through October is definitely DST
        if 3 < month < 11:
            # Definitely DST
            hours_offset = 7
            tz_name = "PDT"
        elif month == 3:
            # March - DST starts 2nd Sunday
            second_sunday = 14 - datetime(year, 3, 1).weekday()
            if day >= second_sunday:
                hours_offset = 7
                tz_name = "PDT"
            else:
                hours_offset = 8
                tz_name = "PST"
        elif month == 11:
            # November - DST ends 1st Sunday
            first_sunday = 7 - datetime(year, 11, 1).weekday()
            if day < first_sunday:
                hours_offset = 7
                tz_name = "PDT"
            else:
                hours_offset = 8
                tz_name = "PST"
        else:
            # December through February
            hours_offset = 8
            tz_name = "PST"

        dt_pacific = dt_utc - timedelta(hours=hours_offset)
        return dt_pacific.strftime(f"%Y-%m-%d %H:%M:%S {tz_name}")

    except Exception as e:
        logger.error(f"Failed to format timestamp {timestamp_str}: {str(e)}")
        return timestamp_str


def get_shared_filter_values() -> Dict[str, Any]:
    """Get shared filter values from session state with validation"""
    try:
        batch_type = st.session_state.get('shared_batch_type', 'CASH')
        if batch_type not in ["CASH", "CREDIT", "INTRA"]:
            batch_type = 'CASH'

        is_proof = st.session_state.get('shared_is_proof', 'Y')
        if is_proof not in ['Y', 'N']:
            is_proof = 'Y'

        batch_id = st.session_state.get('shared_batch_id', 'All')
        invalid_account = st.session_state.get('shared_invalid_account', 'All')

        result = {
            'batch_type': batch_type,
            'is_proof': is_proof,
            'batch_id': batch_id,
            'invalid_account': invalid_account,  # Now a single dropdown value
            'accountcode_filter': st.session_state.get("shared_accountcode", ""),
            'item_id_filter': st.session_state.get("detail_item_id", ""),
            'ticket_number_filter': st.session_state.get("detail_ticket_number", ""),
            'bol_other_ticket_filter': st.session_state.get("detail_bol_other_ticket", ""),
            'branch_id_filter': st.session_state.get("detail_branch_id", "All"),
        }

        logger.info(
            f"Retrieved filters: batch_type={result['batch_type']}, is_proof={result['is_proof']}, batch_id={result['batch_id']}")
        return result

    except Exception as e:
        logger.error(f"Failed to get shared filter values: {str(e)}")
        # Return safe defaults
        return {
            'batch_type': 'CASH',
            'is_proof': 'Y',
            'batch_id': 'All',
            'invalid_account': 'All',
            'accountcode_filter': "",
            'item_id_filter': "",
            'ticket_number_filter': "",
            'bol_other_ticket_filter': "",
            'branch_id_filter': "All",
        }


def build_where_conditions_and_params(filters: Dict[str, Any], include_detail_filters: bool = False,
                                      table_name: str = None) -> Tuple[List[str], Dict[str, Any]]:
    """Build SQL WHERE conditions and parameters based on filters with validation"""
    where_conditions = []
    params = {}

    try:
        # Batch type filter with validation
        valid_batch_types = ["CASH", "CREDIT", "INTRA"]
        batch_type = filters.get('batch_type', 'CASH')
        if batch_type not in valid_batch_types:
            logger.warning(f"Invalid batch type: {batch_type}, using CASH")
            batch_type = "CASH"

        where_conditions.append("batch_type = %(batch_type)s")
        params['batch_type'] = batch_type

        # IS_PROOF filter - only add if NOT the out_of_balance table (it already has this in the view)
        is_proof = filters.get('is_proof', 'Y')
        if is_proof in ['Y', 'N'] and table_name != 'out_of_balance':
            where_conditions.append("is_proof = %(is_proof)s")
            params['is_proof'] = is_proof

        # Batch ID filter
        batch_id = filters.get('batch_id', 'All')
        if batch_id and batch_id != 'All':
            where_conditions.append("batch_id = %(batch_id)s")
            params['batch_id'] = batch_id

        # Account code filter with input sanitization
        accountcode_filter = filters.get('accountcode_filter', '')
        if accountcode_filter and str(accountcode_filter).strip():
            # Sanitize input to prevent SQL injection
            account_code = str(accountcode_filter).strip()[:50]  # Limit length
            if account_code:  # Only add if not empty after sanitization
                where_conditions.append("accountcode_adjusted ILIKE %(accountcode)s")
                params['accountcode'] = f"%{account_code}%"

        # Invalid account filter - now a single dropdown value
        invalid_account = filters.get('invalid_account', 'All')
        if invalid_account and invalid_account != 'All':
            where_conditions.append("error = %(invalid_account)s")
            params['invalid_account'] = invalid_account

        # Detail filters (only for specific tabs)
        if include_detail_filters:
            # Item ID filter
            item_id_filter = filters.get('item_id_filter', '')
            if item_id_filter and str(item_id_filter).strip():
                item_id = str(item_id_filter).strip()[:50]
                if item_id:
                    where_conditions.append("item_id ILIKE %(item_id)s")
                    params['item_id'] = f"%{item_id}%"

            # Ticket number filter
            ticket_number_filter = filters.get('ticket_number_filter', '')
            if ticket_number_filter and str(ticket_number_filter).strip():
                ticket_number = str(ticket_number_filter).strip()[:20]
                if ticket_number:
                    where_conditions.append("ticket_number::text ILIKE %(ticket_number)s")
                    params['ticket_number'] = f"%{ticket_number}%"

            # BOL other ticket filter
            bol_filter = filters.get('bol_other_ticket_filter', '')
            if bol_filter and str(bol_filter).strip():
                bol_ticket = str(bol_filter).strip()[:50]
                if bol_ticket:
                    where_conditions.append("bol_other_ticket_number ILIKE %(bol_other_ticket)s")
                    params['bol_other_ticket'] = f"%{bol_ticket}%"

            # Branch ID filter
            branch_id_filter = filters.get('branch_id_filter', 'All')
            if branch_id_filter and str(branch_id_filter).strip() and branch_id_filter != "All":
                branch_id = str(branch_id_filter).strip()[:10]
                if branch_id:
                    where_conditions.append("branch_id = %(branch_id)s")
                    params['branch_id'] = branch_id

        logger.info(f"Built {len(where_conditions)} WHERE conditions with {len(params)} parameters")
        return where_conditions, params

    except Exception as e:
        logger.error(f"Error building WHERE conditions: {str(e)}")
        # Return basic filter as fallback
        where_conditions = ["batch_type = %(batch_type)s"]
        params = {'batch_type': 'CASH'}
        st.warning("Using default filters due to an error processing your selections")
        return where_conditions, params


def safe_format_currency(value: Any) -> str:
    """Safely format currency values"""
    try:
        if pd.isna(value) or value is None:
            return "$0.00"
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return "$0.00"


def safe_format_number(value: Any) -> str:
    """Safely format numeric values"""
    try:
        if pd.isna(value) or value is None:
            return "0"
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return "0"


def safe_format_date(date_value: Any) -> str:
    """Safely format date values"""
    try:
        if pd.isna(date_value) or date_value is None:
            return ""
        return pd.to_datetime(date_value).strftime('%m/%d/%Y')
    except:
        return str(date_value) if date_value else ""


def create_pdf_report(journal_data: pd.DataFrame, filters: Dict[str, Any], total_qty: float,
                      total_amount: float) -> bytes:
    """Create a PDF report for Sales Journal data using matplotlib with all records and proper formatting"""
    if not PDF_AVAILABLE:
        raise ImportError("matplotlib is not available for PDF generation")

    import io
    buffer = io.BytesIO()

    try:
        # Set up matplotlib for better PDF rendering
        plt.style.use('default')

        with PdfPages(buffer) as pdf:
            if not journal_data.empty:
                # Prepare data for table
                table_data = []
                headers = ['Account Code', 'Batch Type', 'Invalid Account', 'Entry Qty', 'Amount']

                for _, row in journal_data.iterrows():
                    table_data.append([
                        str(row['accountcode_adjusted'])[:25],  # Allow longer account codes
                        str(row['batch_type']),
                        str(row['invalid_acount']),
                        f"{row['account_entry_qty']:,.2f}",
                        f"${row['amount']:,.2f}"
                    ])

                # Calculate rows per page (maximize use of page space)
                rows_per_page = 50  # Significantly increased to fill more of the page
                total_pages = (len(table_data) + rows_per_page - 1) // rows_per_page

                for page_num in range(total_pages):
                    # Create figure for each page - Portrait orientation 8.5" x 11"
                    fig = plt.figure(figsize=(8.5, 11))
                    fig.patch.set_facecolor('white')

                    # Title
                    fig.suptitle('Sales Journal by Account - R245A', fontsize=16, fontweight='bold', y=0.95)

                    # Only show metadata on first page
                    if page_num == 0:
                        # Add report metadata - moved further right
                        metadata_text = f"""Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S PST')}
Batch Type: {filters['batch_type']}
Proof: {filters['is_proof']}
Batch ID: {filters['batch_id']}
Account Code Filter: {filters['accountcode_filter'] if filters['accountcode_filter'] else 'None'}"""

                        # Summary metrics
                        summary_text = f"""Total Records: {len(journal_data):,}
Total Entry Qty: {total_qty:,.2f}
Total Amount: ${total_amount:,.2f}"""

                        # Move both boxes further right for better alignment
                        plt.figtext(0.20, 0.87, metadata_text, fontsize=9, ha='left', va='top',
                                    bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.7))

                        plt.figtext(0.60, 0.87, summary_text, fontsize=9, ha='left', va='top',
                                    bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.7))

                        table_top = 0.78
                    else:
                        table_top = 0.90  # Much higher position for subsequent pages without metadata

                    # Get data for this page
                    start_idx = page_num * rows_per_page
                    end_idx = min(start_idx + rows_per_page, len(table_data))
                    page_data = table_data[start_idx:end_idx]

                    # Create table subplot
                    ax = fig.add_subplot(111)
                    ax.axis('off')

                    if page_data:
                        # Calculate table height to use much more of the page - very aggressive use of space
                        if page_num == 0:
                            # First page has metadata, so less space available
                            table_height = min(0.72, len(page_data) * 0.014 + 0.05)
                        else:
                            # Subsequent pages can use more space
                            table_height = min(0.78, len(page_data) * 0.014 + 0.05)
                        table_bottom = table_top - table_height

                        table = ax.table(cellText=page_data,
                                         colLabels=headers,
                                         cellLoc='center',
                                         loc='center',
                                         bbox=[0.05, table_bottom, 0.90, table_height])

                        # Style the table
                        table.auto_set_font_size(False)
                        table.set_fontsize(7)  # Slightly smaller font to accommodate more rows
                        table.scale(1, 1.2)  # Reduced scaling for tighter fit

                        # Header styling
                        for i in range(len(headers)):
                            table[(0, i)].set_facecolor('#4472C4')
                            table[(0, i)].set_text_props(weight='bold', color='white')
                            table[(0, i)].set_height(0.04)  # Reduced header height

                        # Alternate row colors
                        for i in range(1, len(page_data) + 1):
                            for j in range(len(headers)):
                                if i % 2 == 0:
                                    table[(i, j)].set_facecolor('#F2F2F2')
                                else:
                                    table[(i, j)].set_facecolor('white')
                                table[(i, j)].set_height(0.03)  # Reduced row height to fit more

                    # Add page information and footer with better spacing
                    if total_pages > 1:
                        plt.figtext(0.5, 0.07, f"Page {page_num + 1} of {total_pages}", fontsize=10, ha='center',
                                    style='italic')
                        plt.figtext(0.5, 0.04, 'APEX Sales Journal Report', fontsize=9, ha='center', style='italic')
                    else:
                        plt.figtext(0.5, 0.05, 'APEX Sales Journal Report', fontsize=9, ha='center', style='italic')

                    # Save the page
                    pdf.savefig(fig, bbox_inches='tight', dpi=300)
                    plt.close(fig)

            else:
                # No data available - single page
                fig = plt.figure(figsize=(8.5, 11))
                fig.patch.set_facecolor('white')

                # Title
                fig.suptitle('Sales Journal by Account - R245A', fontsize=16, fontweight='bold', y=0.95)

                # Add report metadata
                metadata_text = f"""Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S PST')}
Batch Type: {filters['batch_type']}
Proof: {filters['is_proof']}
Batch ID: {filters['batch_id']}
Account Code Filter: {filters['accountcode_filter'] if filters['accountcode_filter'] else 'None'}"""

                summary_text = f"""Total Records: 0
Total Entry Qty: 0.00
Total Amount: $0.00"""

                # Move both boxes further right for better alignment (same as data pages)
                plt.figtext(0.20, 0.87, metadata_text, fontsize=9, ha='left', va='top',
                            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.7))

                plt.figtext(0.60, 0.87, summary_text, fontsize=9, ha='left', va='top',
                            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.7))

                # No data message
                ax = fig.add_subplot(111)
                ax.axis('off')
                ax.text(0.5, 0.5, 'No data available for the selected filters',
                        ha='center', va='center', fontsize=14,
                        bbox=dict(boxstyle="round,pad=1", facecolor='lightyellow'))

                # Add footer
                plt.figtext(0.5, 0.05, 'APEX Sales Journal Report',
                            fontsize=9, ha='center', style='italic')

                # Save the page
                pdf.savefig(fig, bbox_inches='tight', dpi=300)
                plt.close(fig)

        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        logger.error(f"Error creating PDF report: {str(e)}")
        plt.close('all')  # Clean up any open figures
        raise


def render_error_boundary(func, *args, **kwargs):
    """Wrapper function to catch and display errors gracefully"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in {func.__name__}: {str(e)}")
        st.error(f"An error occurred while loading this section. Please refresh the page or contact support.")
        st.exception(e)
        return None


def check_and_reset_batch_id_if_needed():
    """Check if batch_type or is_proof changed and reset batch_id if needed"""
    current_batch_type = st.session_state.get('shared_batch_type', 'CASH')
    current_is_proof = st.session_state.get('shared_is_proof', 'Y')
    previous_batch_type = st.session_state.get('previous_batch_type', 'CASH')
    previous_is_proof = st.session_state.get('previous_is_proof', 'Y')

    if current_batch_type != previous_batch_type or current_is_proof != previous_is_proof:
        # Get the new max batch_id for the new filters
        batch_options, max_batch_id = get_batch_id_options(current_batch_type, current_is_proof)
        st.session_state['shared_batch_id'] = max_batch_id if max_batch_id else 'All'
        st.session_state['previous_batch_type'] = current_batch_type
        st.session_state['previous_is_proof'] = current_is_proof
        logger.info(f"Reset batch_id to '{st.session_state['shared_batch_id']}' due to filter change")


def render_sales_journal_tab():
    """Render the Sales Journal tab with comprehensive error handling and PDF export"""
    st.header("📊 Sales Journal by Acct-R245A")
    st.markdown("**APEX UPGRADE TEST VERSION**")

    if not POSTGRES_AVAILABLE:
        st.info("🔧 **Demo Mode** - Displaying sample data (database not connected)")

        # Create mock data for demo purposes
        import random

        mock_data = []
        account_codes = ['1100-Cash', '1200-Receivables', '4000-Sales', '5000-COGS', '6000-Expenses']
        batch_types = ['CASH', 'CREDIT', 'INTRA']

        for i in range(15):
            mock_data.append({
                'accountcode_adjusted': random.choice(account_codes),
                'batch_type': random.choice(batch_types),
                'invalid_acount': 'N' if i < 12 else 'Y',  # Most entries are valid
                'account_entry_qty': random.randint(5, 50),
                'amount': round(random.uniform(1000, 50000), 2)
            })

        journal_data = pd.DataFrame(mock_data)

    else:
        try:
            # Check if we need to reset batch_id
            check_and_reset_batch_id_if_needed()

            filters = get_shared_filter_values()
            where_conditions, params = build_where_conditions_and_params(filters)

            base_query = """
                         SELECT accountcode_adjusted, \
                                batch_type, \
                                error                  as invalid_acount, \
                                SUM(account_entry_qty) AS account_entry_qty, \
                                SUM(amount)            AS amount
                         FROM dbt_dev_accounting.dash_r245a_apex_sales_journal_review_summary \
                         """

            if where_conditions:
                query = base_query + " WHERE " + " AND ".join(where_conditions)
            else:
                query = base_query

            # Modified ORDER BY clause
            query += " GROUP BY 1,2,3 ORDER BY error, accountcode_adjusted"

            with st.spinner("Loading sales journal data..."):
                journal_data = query_postgres(query, params)
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            journal_data = pd.DataFrame()

    # Common data processing for both mock and real data
    if journal_data is not None and not journal_data.empty:
        # Keep original data for PDF generation
        original_data = journal_data.copy()

        display_data = journal_data.copy()
        display_data['Amount'] = display_data['amount'].apply(safe_format_currency)
        display_data['Account Entry Qty'] = display_data['account_entry_qty'].apply(safe_format_number)

        display_data = display_data.rename(columns={
            'accountcode_adjusted': 'Accountcode Adjusted',
            'batch_type': 'Batch Type',
            'invalid_acount': 'Invalid Account'
        })

        display_columns = ['Accountcode Adjusted', 'Batch Type', 'Invalid Account', 'Account Entry Qty', 'Amount']
        display_data = display_data[display_columns]

        total_qty = journal_data['account_entry_qty'].sum()
        total_amount = journal_data['amount'].sum()
    else:
        original_data = pd.DataFrame()
        display_data = pd.DataFrame(
            columns=['Accountcode Adjusted', 'Batch Type', 'Invalid Account', 'Account Entry Qty', 'Amount'])
        total_qty = 0
        total_amount = 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Entry Qty", safe_format_number(total_qty))
    with col2:
        st.metric("Total Amount", safe_format_currency(total_amount))

    st.markdown("---")

    col_journal, col_filters = st.columns([3, 1])

    with col_journal:
        st.subheader("Journal Entries")
        st.dataframe(display_data, use_container_width=True, height=600, hide_index=True)

    # Get current filter values (for both mock and real modes)
    if POSTGRES_AVAILABLE:
        filters = get_shared_filter_values()
    else:
        # Mock filter values for demo
        filters = {
            'batch_type': 'CASH',
            'is_proof': 'Y',
            'batch_id': 'BATCH_001'
        }

    with col_filters:
        st.subheader("Filters")

        # Batch type at the top
        st.write("Batch Type:")
        batch_type_options = ["CASH", "CREDIT", "INTRA"]
        current_batch_type = filters['batch_type'] if filters['batch_type'] in batch_type_options else 'CASH'
        st.radio("Batch Type options:", batch_type_options,
                 index=batch_type_options.index(current_batch_type),
                 key="shared_batch_type_journal", label_visibility="collapsed",
                 on_change=lambda: (
                     st.session_state.update({"shared_batch_type": st.session_state.shared_batch_type_journal}),
                     invalidate_out_of_balance_cache()))

        # Proof filter
        st.write("Proof:")
        proof_options = ["Y", "N"]
        current_proof = filters['is_proof'] if filters['is_proof'] in proof_options else 'Y'
        st.radio("Proof options:", proof_options,
                 index=proof_options.index(current_proof),
                 key="shared_is_proof_journal", label_visibility="collapsed",
                 on_change=lambda: (
                     st.session_state.update({"shared_is_proof": st.session_state.shared_is_proof_journal}),
                     invalidate_out_of_balance_cache()))

        # Batch ID filter (simplified for demo mode)
        if POSTGRES_AVAILABLE:
            st.write("Batch ID:")
            batch_id_options, max_batch = get_batch_id_options(filters['batch_type'], filters['is_proof'])
            current_batch_id = filters['batch_id'] if filters['batch_id'] in batch_id_options else (
                max_batch if max_batch else "All")
            st.selectbox("Batch ID:", batch_id_options,
                         index=batch_id_options.index(current_batch_id) if current_batch_id in batch_id_options else 0,
                         key="shared_batch_id_journal", label_visibility="collapsed",
                         on_change=lambda: (
                             st.session_state.update({"shared_batch_id": st.session_state.shared_batch_id_journal}),
                             invalidate_out_of_balance_cache()))

            # Invalid Account dropdown (changed from checkboxes)
            st.write("Invalid Account:")
            invalid_account_options = get_invalid_account_options(filters['batch_type'], filters['is_proof'],
                                                                  filters['batch_id'])
            current_invalid_account = filters['invalid_account'] if filters[
                                                                        'invalid_account'] in invalid_account_options else "All"
            st.selectbox("Invalid Account:", invalid_account_options,
                         index=invalid_account_options.index(
                             current_invalid_account) if current_invalid_account in invalid_account_options else 0,
                         key="shared_invalid_account_journal", label_visibility="collapsed",
                         on_change=lambda: st.session_state.update(
                             {"shared_invalid_account": st.session_state.shared_invalid_account_journal}))
        else:
            # Demo mode - show simplified filters
            st.write("Batch ID:")
            st.selectbox("Batch ID:", ["BATCH_001", "BATCH_002", "All"],
                         index=0, key="demo_batch_id_journal", label_visibility="collapsed")

            st.write("Invalid Account:")
            st.selectbox("Invalid Account:", ["N", "Y", "All"],
                         index=0, key="demo_invalid_account_journal", label_visibility="collapsed")

        # Account Code input (common for both modes)
        st.write("Account Code:")
        if POSTGRES_AVAILABLE:
            account_code = st.text_input("Account Code Input", value=str(filters['accountcode_filter']),
                                         placeholder="Enter account code..", key="shared_accountcode_journal",
                                         label_visibility="collapsed",
                                         max_chars=50,
                                         on_change=lambda: st.session_state.update(
                                             {"shared_accountcode": st.session_state.shared_accountcode_journal}))
        else:
            account_code = st.text_input("Account Code Input", value="",
                                         placeholder="Enter account code..", key="demo_accountcode_journal",
                                         label_visibility="collapsed",
                                         max_chars=50)

    # Downloads section - moved outside filters column for better layout
    st.markdown("---")
    st.subheader("Downloads")

    col_download1, col_download2, col_download3 = st.columns([1, 1, 1])

    with col_download1:
        if not display_data.empty:
            csv_data = display_data.to_csv(index=False)
            st.download_button("📥 Download CSV", data=csv_data,
                               file_name=f"sales_journal_batch_{filters['batch_type']}_proof_{filters['is_proof']}.csv",
                               mime="text/csv", use_container_width=True)

    with col_download2:
        if EXCEL_AVAILABLE and not display_data.empty:
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                display_data.to_excel(writer, sheet_name='Sales Journal', index=False)
            excel_data = output.getvalue()

            st.download_button("📊 Download Excel", data=excel_data,
                               file_name=f"sales_journal_batch_{filters['batch_type']}_proof_{filters['is_proof']}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
        else:
            st.caption("Excel download not available")

    with col_download3:
        if PDF_AVAILABLE:
            try:
                if st.button("📄 Generate PDF", use_container_width=True):
                    with st.spinner("Generating PDF report..."):
                        pdf_data = create_pdf_report(original_data, filters, total_qty, total_amount)

                        st.download_button(
                            "📄 Download PDF Report",
                            data=pdf_data,
                            file_name=f"sales_journal_report_batch_{filters['batch_type']}_proof_{filters['is_proof']}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("PDF report generated successfully!")
            except Exception as e:
                st.error(f"Failed to generate PDF: {str(e)}")
        else:
            st.caption("PDF export not available")


def render_detail_by_ticket_tab():
    """Render the Detail by Ticket Date tab with comprehensive error handling"""
    st.header("📋 Detail by Ticket Date")
    st.markdown("**Detailed Ticket Transactions**")

    if not POSTGRES_AVAILABLE:
        st.error("Database connection not available. Please contact your administrator.")
        return

    try:
        # Check if we need to reset batch_id
        check_and_reset_batch_id_if_needed()

        filters = get_shared_filter_values()
        where_conditions, params = build_where_conditions_and_params(filters, include_detail_filters=True)

        base_query = """
                     SELECT accountcode_adjusted, \
                            customer, \
                            customer_job_number, \
                            branch_id, \
                            item_id, \
                            item_name, \
                            order_id, \
                            ticket_number, \
                            bol_other_ticket_number, \
                            other_bol_ref_number, \
                            sale_date, \
                            transaction_end_date, \
                            batch_type, \
                            error, \
                            sum(amount)                 AS amount, \
                            sum(account_entry_quantity) AS account_entry_quantity, \
                            sum(ticket_qty)             AS ticket_qty
                     FROM dbt_dev_accounting.dash_r245a_apex_sales_journal_review_detail \
                     """

        if where_conditions:
            query = base_query + " WHERE " + " AND ".join(where_conditions)
        else:
            query = base_query

        # Modified ORDER BY clause
        query += " GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14 ORDER BY error, accountcode_adjusted"

        with st.spinner("Loading detail data..."):
            detail_data = query_postgres(query, params)

        if detail_data is not None and not detail_data.empty:
            display_data = detail_data.copy()

            # Calculate totals before formatting
            total_amount = detail_data['amount'].sum()
            total_account_entry_qty = detail_data['account_entry_quantity'].sum()
            total_ticket_qty = detail_data['ticket_qty'].sum()
            total_records = len(detail_data)

            display_data['Amount'] = display_data['amount'].apply(safe_format_currency)
            display_data['Account Entry Qty'] = display_data['account_entry_quantity'].apply(safe_format_number)
            display_data['Ticket Qty'] = display_data['ticket_qty'].apply(safe_format_number)

            if 'sale_date' in display_data.columns:
                display_data['Sale Date'] = display_data['sale_date'].apply(safe_format_date)
                display_data = display_data.drop('sale_date', axis=1)

            display_data = display_data.rename(columns={
                'accountcode_adjusted': 'Accountcode Adjusted',
                'customer': 'Customer',
                'customer_job_number': 'Customer Job',
                'branch_id': 'Branch Id',
                'item_id': 'Item Id',
                'item_name': 'Item Name',
                'order_id': 'Order Id',
                'ticket_number': 'Ticket Number',
                'bol_other_ticket_number': 'Bol Other Ti..',
                'other_bol_ref_number': 'Other Bol R..'
            })

            display_columns = ['Accountcode Adjusted', 'Customer', 'Customer Job', 'Branch Id',
                               'Item Id', 'Item Name', 'Order Id', 'Ticket Number',
                               'Bol Other Ti..', 'Other Bol R..', 'Sale Date',
                               'Amount', 'Account Entry Qty', 'Ticket Qty']

            available_columns = [col for col in display_columns if col in display_data.columns]
            display_data = display_data[available_columns]
        else:
            display_data = pd.DataFrame(columns=['Accountcode Adjusted', 'Customer', 'Customer Job', 'Branch Id',
                                                 'Item Id', 'Item Name', 'Order Id', 'Ticket Number',
                                                 'Bol Other Ti..', 'Other Bol R..', 'Sale Date',
                                                 'Amount', 'Account Entry Qty', 'Ticket Qty'])
            total_amount = 0
            total_account_entry_qty = 0
            total_ticket_qty = 0
            total_records = 0

        # Display grand totals
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", f"{total_records:,}")
        with col2:
            st.metric("Total Amount", safe_format_currency(total_amount))
        with col3:
            st.metric("Total Account Entry Qty", safe_format_number(total_account_entry_qty))
        with col4:
            st.metric("Total Ticket Qty", safe_format_number(total_ticket_qty))

        st.markdown("---")

        col_detail, col_filters = st.columns([3, 1])

        with col_detail:
            st.subheader("Ticket Detail")
            st.dataframe(display_data, use_container_width=True, height=600, hide_index=True)

        with col_filters:
            st.subheader("Filters")

            st.markdown("**Shared Filters**")
            st.caption("Also used in Sales Journal tab")

            # Batch type at the top
            st.write("Batch Type:")
            batch_type_options = ["CASH", "CREDIT", "INTRA"]
            current_batch_type = filters['batch_type'] if filters['batch_type'] in batch_type_options else 'CASH'
            st.radio("Batch Type options:", batch_type_options,
                     index=batch_type_options.index(current_batch_type),
                     key="shared_batch_type_detail", label_visibility="collapsed",
                     on_change=lambda: (
                         st.session_state.update({"shared_batch_type": st.session_state.shared_batch_type_detail}),
                         invalidate_out_of_balance_cache()))

            # Proof filter
            st.write("Proof:")
            proof_options = ["Y", "N"]
            current_proof = filters['is_proof'] if filters['is_proof'] in proof_options else 'Y'
            st.radio("Proof options:", proof_options,
                     index=proof_options.index(current_proof),
                     key="shared_is_proof_detail", label_visibility="collapsed",
                     on_change=lambda: (
                         st.session_state.update({"shared_is_proof": st.session_state.shared_is_proof_detail}),
                         invalidate_out_of_balance_cache()))

            # Batch ID filter
            st.write("Batch ID:")
            batch_id_options, max_batch = get_batch_id_options(filters['batch_type'], filters['is_proof'])
            current_batch_id = filters['batch_id'] if filters['batch_id'] in batch_id_options else (
                max_batch if max_batch else "All")
            st.selectbox("Batch ID:", batch_id_options,
                         index=batch_id_options.index(current_batch_id) if current_batch_id in batch_id_options else 0,
                         key="shared_batch_id_detail", label_visibility="collapsed",
                         on_change=lambda: (
                             st.session_state.update({"shared_batch_id": st.session_state.shared_batch_id_detail}),
                             invalidate_out_of_balance_cache()))

            # Invalid Account dropdown (changed from checkboxes)
            st.write("Invalid Account:")
            invalid_account_options = get_invalid_account_options(filters['batch_type'], filters['is_proof'],
                                                                  filters['batch_id'])
            current_invalid_account = filters['invalid_account'] if filters[
                                                                        'invalid_account'] in invalid_account_options else "All"
            st.selectbox("Invalid Account:", invalid_account_options,
                         index=invalid_account_options.index(
                             current_invalid_account) if current_invalid_account in invalid_account_options else 0,
                         key="shared_invalid_account_detail", label_visibility="collapsed",
                         on_change=lambda: st.session_state.update(
                             {"shared_invalid_account": st.session_state.shared_invalid_account_detail}))

            st.text_input("Account Code:", value=str(filters['accountcode_filter']), placeholder="Enter account code..",
                          key="shared_accountcode_detail", max_chars=50,
                          on_change=lambda: st.session_state.update(
                              {"shared_accountcode": st.session_state.shared_accountcode_detail}))

            st.markdown("---")
            st.caption("Only for this tab")

            st.text_input("Item ID:", value=str(filters['item_id_filter']), placeholder="Enter item ID..",
                          key="detail_item_id", max_chars=50)
            st.text_input("Ticket Number:", value=str(filters['ticket_number_filter']),
                          placeholder="Enter ticket number..", key="detail_ticket_number", max_chars=20)
            st.text_input("BOL Other Ticket:", value=str(filters['bol_other_ticket_filter']),
                          placeholder="Enter BOL other ticket..", key="detail_bol_other_ticket", max_chars=50)

            branch_options = get_branch_id_options(filters['batch_type'])
            current_branch = filters['branch_id_filter'] if filters['branch_id_filter'] in branch_options else "All"
            st.selectbox("Branch ID:", branch_options, index=branch_options.index(current_branch),
                         key="detail_branch_id")

        # Downloads section - moved outside filters column for better layout
        st.markdown("---")
        st.subheader("Downloads")

        col_download1, col_download2 = st.columns([1, 1])

        with col_download1:
            if not display_data.empty:
                csv_data = display_data.to_csv(index=False)
                st.download_button("📥 Download CSV", data=csv_data,
                                   file_name=f"detail_by_ticket_batch_{filters['batch_type']}_proof_{filters['is_proof']}.csv",
                                   mime="text/csv", use_container_width=True)

        with col_download2:
            if EXCEL_AVAILABLE and not display_data.empty:
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    display_data.to_excel(writer, sheet_name='Detail by Ticket Date', index=False)
                excel_data = output.getvalue()

                st.download_button("📊 Download Excel", data=excel_data,
                                   file_name=f"detail_by_ticket_batch_{filters['batch_type']}_proof_{filters['is_proof']}.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)
            else:
                st.caption("Excel download not available")

    except Exception as e:
        logger.error(f"Error in render_detail_by_ticket_tab: {str(e)}")
        st.error("Failed to load detail data. Please try again or contact support.")
        st.exception(e)


def render_out_of_balance_ar_tab():
    """Render the Out of Balance tab with amount total in the tab name"""
    st.header("⚖️ Out of Balance")
    st.markdown("**Out of balance transactions**")

    if not POSTGRES_AVAILABLE:
        st.error("Database connection not available. Please contact your administrator.")
        return

    try:
        # Check if we need to reset batch_id
        check_and_reset_batch_id_if_needed()

        filters = get_shared_filter_values()
        # Pass table_name to indicate this is the out_of_balance table (to skip is_proof filter)
        where_conditions, params = build_where_conditions_and_params(filters, table_name='out_of_balance')

        base_query = """
                     SELECT ticket_unique_id, \
                            branch_id, \
                            ticket_number, \
                            ticket_item_no, \
                            item_id, \
                            item_name, \
                            customer_job_number, \
                            customer_name, \
                            accountcode_adjusted, \
                            account_entry_quantity, \
                            amount
                     FROM dbt_dev_accounting.dash_r245a_apex_sales_journal_review_out_of_balance \
                     """

        if where_conditions:
            query = base_query + " WHERE " + " AND ".join(where_conditions)
        else:
            query = base_query

        query += " ORDER BY ticket_unique_id, branch_id, ticket_number"

        with st.spinner("Loading out of balance data..."):
            out_of_balance_data = query_postgres(query, params)

        if out_of_balance_data is not None and not out_of_balance_data.empty:
            display_data = out_of_balance_data.copy()

            # Calculate totals before formatting
            total_qty = out_of_balance_data['account_entry_quantity'].sum()
            total_amount = out_of_balance_data['amount'].sum()
            record_count = len(out_of_balance_data)

            display_data['Amount'] = display_data['amount'].apply(safe_format_currency)
            display_data['Account Entry Qty'] = display_data['account_entry_quantity'].apply(safe_format_number)

            display_data = display_data.rename(columns={
                'ticket_unique_id': 'Ticket Unique ID',
                'branch_id': 'Branch ID',
                'ticket_number': 'Ticket Number',
                'ticket_item_no': 'Ticket Item No',
                'item_id': 'Item ID',
                'item_name': 'Item Name',
                'customer_job_number': 'Customer Job Number',
                'customer_name': 'Customer Name',
                'accountcode_adjusted': 'Accountcode Adjusted'
            })

            display_columns = ['Ticket Unique ID', 'Branch ID', 'Ticket Number', 'Ticket Item No', 'Item ID',
                               'Item Name', 'Customer Job Number', 'Customer Name', 'Accountcode Adjusted',
                               'Account Entry Qty', 'Amount']

            available_columns = [col for col in display_columns if col in display_data.columns]
            display_data = display_data[available_columns]
        else:
            display_data = pd.DataFrame(
                columns=['Ticket Unique ID', 'Branch ID', 'Ticket Number', 'Ticket Item No', 'Item ID',
                         'Item Name', 'Customer Job Number', 'Customer Name', 'Accountcode Adjusted',
                         'Account Entry Qty', 'Amount'])
            total_qty = 0
            total_amount = 0
            record_count = 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", f"{record_count:,}")
        with col2:
            st.metric("Total Entry Qty", safe_format_number(total_qty))
        with col3:
            st.metric("Total Amount", safe_format_currency(total_amount))

        st.markdown("---")

        col_data, col_filters = st.columns([3, 1])

        with col_data:
            st.subheader("Out of Balance Transactions")
            st.dataframe(display_data, use_container_width=True, height=600, hide_index=True)

        with col_filters:
            st.subheader("Global Filters")
            st.caption("Apply to all report tabs")

            # Batch type at the top
            st.write("Batch Type:")
            batch_type_options = ["CASH", "CREDIT", "INTRA"]
            current_batch_type = filters['batch_type'] if filters['batch_type'] in batch_type_options else 'CASH'
            st.radio("Batch Type options:", batch_type_options,
                     index=batch_type_options.index(current_batch_type),
                     key="shared_batch_type_ar", label_visibility="collapsed",
                     on_change=lambda: (
                         st.session_state.update({"shared_batch_type": st.session_state.shared_batch_type_ar}),
                         invalidate_out_of_balance_cache()))

            # Note about Proof filter
            st.info("ℹ️ This tab requires Proof mode to be 'Y'")

            # Batch ID filter
            st.write("Batch ID:")
            batch_id_options, max_batch = get_batch_id_options(filters['batch_type'], filters['is_proof'])
            current_batch_id = filters['batch_id'] if filters['batch_id'] in batch_id_options else (
                max_batch if max_batch else "All")
            st.selectbox("Batch ID:", batch_id_options,
                         index=batch_id_options.index(current_batch_id) if current_batch_id in batch_id_options else 0,
                         key="shared_batch_id_ar", label_visibility="collapsed",
                         on_change=lambda: (
                             st.session_state.update({"shared_batch_id": st.session_state.shared_batch_id_ar}),
                             invalidate_out_of_balance_cache()))

            # Invalid Account dropdown
            st.write("Invalid Account:")
            invalid_account_options = get_invalid_account_options(filters['batch_type'], filters['is_proof'],
                                                                  filters['batch_id'])
            current_invalid_account = filters['invalid_account'] if filters[
                                                                        'invalid_account'] in invalid_account_options else "All"
            st.selectbox("Invalid Account:", invalid_account_options,
                         index=invalid_account_options.index(
                             current_invalid_account) if current_invalid_account in invalid_account_options else 0,
                         key="shared_invalid_account_ar", label_visibility="collapsed",
                         on_change=lambda: st.session_state.update(
                             {"shared_invalid_account": st.session_state.shared_invalid_account_ar}))

            st.write("Account Code:")
            st.text_input("Account Code Input", value=str(filters['accountcode_filter']),
                          placeholder="Enter account code..",
                          key="shared_accountcode_ar", label_visibility="collapsed", max_chars=50,
                          on_change=lambda: st.session_state.update(
                              {"shared_accountcode": st.session_state.shared_accountcode_ar}))

        # Downloads section - moved outside filters column for better layout
        st.markdown("---")
        st.subheader("Downloads")

        col_download1, col_download2 = st.columns([1, 1])

        with col_download1:
            if not display_data.empty:
                csv_data = display_data.to_csv(index=False)
                st.download_button("📥 Download CSV", data=csv_data,
                                   file_name=f"out_of_balance_batch_{filters['batch_type']}.csv",
                                   mime="text/csv", use_container_width=True)

        with col_download2:
            if EXCEL_AVAILABLE and not display_data.empty:
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    display_data.to_excel(writer, sheet_name='Out of Balance', index=False)
                excel_data = output.getvalue()

                st.download_button("📊 Download Excel", data=excel_data,
                                   file_name=f"out_of_balance_batch_{filters['batch_type']}.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)
            else:
                st.caption("Excel download not available")

    except Exception as e:
        logger.error(f"Error in render_out_of_balance_ar_tab: {str(e)}")
        st.error("Failed to load out of balance data. Please try again or contact support.")
        st.exception(e)


def render_1140_research_tab():
    """Render the 1140 Research tab with comprehensive error handling"""
    st.header("🔍 1140 Research")
    st.markdown("**Research Object Account 1140 Transactions**")

    if not POSTGRES_AVAILABLE:
        st.error("Database connection not available. Please contact your administrator.")
        return

    try:
        # Check if we need to reset batch_id
        check_and_reset_batch_id_if_needed()

        filters = get_shared_filter_values()

        # Handle 1140-specific filters independently
        ticket_number_1140 = st.session_state.get("ticket_number_1140", "")

        # Build WHERE conditions using only the shared filters first
        where_conditions, params = build_where_conditions_and_params(filters)

        # Add 1140-specific ticket number filter directly
        if ticket_number_1140 and str(ticket_number_1140).strip():
            ticket_clean = str(ticket_number_1140).strip()[:20]
            where_conditions.append("ticket_number::text ILIKE %(ticket_number_1140)s")
            params['ticket_number_1140'] = f"%{ticket_clean}%"

        base_query = """
                     SELECT accountcode_adjusted, \
                            transaction_end_date, \
                            sale_date, \
                            ticket_number, \
                            amount
                     FROM dbt_dev_accounting.dash_r245a_apex_sales_journal_review_1140_research \
                     """

        if where_conditions:
            query = base_query + " WHERE " + " AND ".join(where_conditions)
        else:
            query = base_query

        query += " ORDER BY accountcode_adjusted, transaction_end_date, ticket_number"

        with st.spinner("Loading 1140 research data..."):
            research_data = query_postgres(query, params)

        if research_data is not None and not research_data.empty:
            display_data = research_data.copy()

            # Format amount column
            display_data['Amount'] = display_data['amount'].apply(safe_format_currency)

            # Format date columns
            if 'transaction_end_date' in display_data.columns:
                display_data['Transaction End Date'] = display_data['transaction_end_date'].apply(safe_format_date)
                display_data = display_data.drop('transaction_end_date', axis=1)

            if 'sale_date' in display_data.columns:
                display_data['Sale Date'] = display_data['sale_date'].apply(safe_format_date)
                display_data = display_data.drop('sale_date', axis=1)

            display_data = display_data.rename(columns={
                'accountcode_adjusted': 'Accountcode Adjusted',
                'ticket_number': 'Ticket Number'
            })

            display_columns = ['Accountcode Adjusted', 'Transaction End Date', 'Sale Date', 'Ticket Number', 'Amount']

            available_columns = [col for col in display_columns if col in display_data.columns]
            display_data = display_data[available_columns]

            total_amount = research_data['amount'].sum()
            record_count = len(research_data)
        else:
            display_data = pd.DataFrame(
                columns=['Accountcode Adjusted', 'Transaction End Date', 'Sale Date', 'Ticket Number', 'Amount'])
            total_amount = 0
            record_count = 0

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Records", f"{record_count:,}")
        with col2:
            st.metric("Total Amount", safe_format_currency(total_amount))

        st.markdown("---")

        col_data, col_filters = st.columns([3, 1])

        with col_data:
            st.subheader("1140 Research Transactions")
            st.dataframe(display_data, use_container_width=True, height=600, hide_index=True)

        with col_filters:
            st.subheader("Global Filters")
            st.caption("Apply to all report tabs")

            # Batch type at the top
            st.write("Batch Type:")
            batch_type_options = ["CASH", "CREDIT", "INTRA"]
            current_batch_type = filters['batch_type'] if filters['batch_type'] in batch_type_options else 'CASH'
            st.radio("Batch Type options:", batch_type_options,
                     index=batch_type_options.index(current_batch_type),
                     key="shared_batch_type_1140", label_visibility="collapsed",
                     on_change=lambda: (
                         st.session_state.update({"shared_batch_type": st.session_state.shared_batch_type_1140}),
                         invalidate_out_of_balance_cache()))

            # Proof filter
            st.write("Proof:")
            proof_options = ["Y", "N"]
            current_proof = filters['is_proof'] if filters['is_proof'] in proof_options else 'Y'
            st.radio("Proof options:", proof_options,
                     index=proof_options.index(current_proof),
                     key="shared_is_proof_1140", label_visibility="collapsed",
                     on_change=lambda: (
                         st.session_state.update({"shared_is_proof": st.session_state.shared_is_proof_1140}),
                         invalidate_out_of_balance_cache()))

            # Batch ID filter
            st.write("Batch ID:")
            batch_id_options, max_batch = get_batch_id_options(filters['batch_type'], filters['is_proof'])
            current_batch_id = filters['batch_id'] if filters['batch_id'] in batch_id_options else (
                max_batch if max_batch else "All")
            st.selectbox("Batch ID:", batch_id_options,
                         index=batch_id_options.index(current_batch_id) if current_batch_id in batch_id_options else 0,
                         key="shared_batch_id_1140", label_visibility="collapsed",
                         on_change=lambda: (
                             st.session_state.update({"shared_batch_id": st.session_state.shared_batch_id_1140}),
                             invalidate_out_of_balance_cache()))

            # Invalid Account dropdown (changed from checkboxes)
            st.write("Invalid Account:")
            invalid_account_options = get_invalid_account_options(filters['batch_type'], filters['is_proof'],
                                                                  filters['batch_id'])
            current_invalid_account = filters['invalid_account'] if filters[
                                                                        'invalid_account'] in invalid_account_options else "All"
            st.selectbox("Invalid Account:", invalid_account_options,
                         index=invalid_account_options.index(
                             current_invalid_account) if current_invalid_account in invalid_account_options else 0,
                         key="shared_invalid_account_1140", label_visibility="collapsed",
                         on_change=lambda: st.session_state.update(
                             {"shared_invalid_account": st.session_state.shared_invalid_account_1140}))

            st.write("Account Code:")
            st.text_input("Account Code Input", value=str(filters['accountcode_filter']),
                          placeholder="Enter account code..",
                          key="shared_accountcode_1140", label_visibility="collapsed", max_chars=50,
                          on_change=lambda: st.session_state.update(
                              {"shared_accountcode": st.session_state.shared_accountcode_1140}))

            st.markdown("---")
            st.caption("Only for this tab")

            # Get the current value for the text input
            current_ticket_1140 = st.session_state.get("ticket_number_1140", "")
            st.text_input("Ticket Number:", value=str(current_ticket_1140), placeholder="Enter ticket number..",
                          key="ticket_number_1140", max_chars=20)

        # Downloads section - moved outside filters column for better layout
        st.markdown("---")
        st.subheader("Downloads")

        col_download1, col_download2 = st.columns([1, 1])

        with col_download1:
            if not display_data.empty:
                csv_data = display_data.to_csv(index=False)
                st.download_button("📥 Download CSV", data=csv_data,
                                   file_name=f"1140_research_batch_{filters['batch_type']}_proof_{filters['is_proof']}.csv",
                                   mime="text/csv", use_container_width=True)

        with col_download2:
            if EXCEL_AVAILABLE and not display_data.empty:
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    display_data.to_excel(writer, sheet_name='1140 Research', index=False)
                excel_data = output.getvalue()

                st.download_button("📊 Download Excel", data=excel_data,
                                   file_name=f"1140_research_batch_{filters['batch_type']}_proof_{filters['is_proof']}.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)
            else:
                st.caption("Excel download not available")

    except Exception as e:
        logger.error(f"Error in render_1140_research_tab: {str(e)}")
        st.error("Failed to load 1140 research data. Please try again or contact support.")
        st.exception(e)


def render_tieout_tab():
    """Render the Tieout tab with batch reconciliation data"""
    st.header("✅ Tieout - Batch Reconciliation")
    st.markdown("**APEX vs Data Warehouse batch reconciliation**")

    if not POSTGRES_AVAILABLE:
        st.error("Database connection not available. Please contact your administrator.")
        return

    try:
        tieout_query = """
                       SELECT batch_id, \
                              export_date, \
                              batch_type, \
                              is_proof, \
                              qty_apex, \
                              qty_batman, \
                              ticket_amount_apex, \
                              ticket_amount_batman, \
                              count_apex, \
                              count_batman, \
                              test
                       FROM dbt_dev_accounting.rpt_r245t_apex_sales_journal_tieout_app_only
                       ORDER BY batch_id DESC, export_date \
                       """

        with st.spinner("Loading tieout data..."):
            tieout_data = query_postgres(tieout_query)

        if tieout_data is not None and not tieout_data.empty:
            all_ties = (tieout_data['test'] == 'TIES').all() if 'test' in tieout_data.columns else False
            emoji = "✅" if all_ties else "❌"
            status_text = "All batches tie out correctly" if all_ties else "Some batches do not tie out"
            status_color = "green" if all_ties else "red"

            st.markdown(f":{status_color}[{status_text}]")

            display_data = tieout_data.copy()

            numeric_columns = ['qty_apex', 'qty_batman', 'ticket_amount_apex', 'ticket_amount_batman', 'count_apex',
                               'count_batman']
            for col in numeric_columns:
                if col in display_data.columns:
                    display_data[col] = display_data[col].apply(safe_format_number)

            if 'export_date' in display_data.columns:
                display_data['export_date'] = display_data['export_date'].apply(safe_format_date)

            display_data = display_data.rename(columns={
                'batch_id': 'Batch ID',
                'export_date': 'Export Date',
                'batch_type': 'Batch Type',
                'is_proof': 'Is Proof',
                'qty_apex': 'Qty APEX',
                'qty_batman': 'Qty Data Warehouse',
                'ticket_amount_apex': 'Ticket Amount APEX',
                'ticket_amount_batman': 'Ticket Amount Data Warehouse',
                'count_apex': 'Count APEX',
                'count_batman': 'Count Data Warehouse',
                'test': 'Test Result'
            })

            total_batches = len(display_data)
            ties_count = (tieout_data['test'] == 'TIES').sum() if 'test' in tieout_data.columns else 0
            non_ties_count = total_batches - ties_count

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Batches", total_batches)
            with col2:
                st.metric("✅ Ties", ties_count)
            with col3:
                st.metric("❌ Does Not Tie", non_ties_count)
            with col4:
                tie_percentage = (ties_count / total_batches * 100) if total_batches > 0 else 0
                st.metric("Tie Rate", f"{tie_percentage:.1f}%")

            st.markdown("---")
            st.subheader("Batch Tieout Details")

            def highlight_test_results(val):
                if val == 'TIES':
                    return 'background-color: #d4edda; color: #155724; font-weight: bold'
                else:
                    return 'background-color: #f8d7da; color: #721c24; font-weight: bold'

            if 'Test Result' in display_data.columns:
                styled_df = display_data.style.applymap(highlight_test_results, subset=['Test Result'])
            else:
                styled_df = display_data

            st.dataframe(styled_df, use_container_width=True, height=600, hide_index=True)

            st.markdown("---")
            st.subheader("Downloads")

            col_download1, col_download2 = st.columns([1, 1])

            with col_download1:
                csv_data = display_data.to_csv(index=False)
                st.download_button("📥 Download CSV", data=csv_data,
                                   file_name=f"batch_tieout_{datetime.now().strftime('%Y%m%d')}.csv",
                                   mime="text/csv", use_container_width=True)

            with col_download2:
                if EXCEL_AVAILABLE:
                    import io
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        display_data.to_excel(writer, sheet_name='Batch Tieout', index=False)
                    excel_data = output.getvalue()

                    st.download_button("📊 Download Excel", data=excel_data,
                                       file_name=f"batch_tieout_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                       use_container_width=True)
                else:
                    st.caption("Excel download not available")
        else:
            st.warning("No tieout data found.")

    except Exception as e:
        logger.error(f"Error in render_tieout_tab: {str(e)}")
        st.error("Failed to load tieout data. Please try again or contact support.")
        st.exception(e)


def render_modern_sidebar():
    """Render modern sidebar with navigation menu and filters"""
    with st.sidebar:
        # Main Navigation - At the top
        st.markdown("### 📋 Navigation")

        # Navigation with new Documentation tab
        nav_options = [
            ("🏠 Dashboard", "dashboard"),
            ("📊 Sales Journal", "journal"),
            ("📋 Detail by Ticket", "details"),
            ("⚖️ Out of Balance", "balance"),
            ("🔍 1140 Research", "research"),
            ("🚀 Pipeline Control", "pipeline"),
            ("⚙️ Tieout Management", "tieout"),
            ("📈 Pipeline History", "history"),
            ("📖 Documentation", "documentation"),
            ("🔧 Debug Tools", "debug")
        ]

        nav_labels = [option[0] for option in nav_options]
        nav_values = [option[1] for option in nav_options]

        # Set default to Dashboard (index 0)
        current_index = st.session_state.get('active_tab_index', 0)
        if current_index >= len(nav_values):
            current_index = 0

        selected_nav = st.radio(
            "Select page:",
            nav_values,
            format_func=lambda x: nav_labels[nav_values.index(x)],
            index=current_index,
            label_visibility="collapsed"
        )

        # Update active tab index if navigation changed
        new_index = nav_values.index(selected_nav)
        if new_index != current_index:
            st.session_state.active_tab_index = new_index
            st.rerun()

        st.markdown("---")

        # Critical Financial Alert - Out of Balance Indicator (Always Visible)
        out_of_balance_total = st.session_state.get('out_of_balance_total', 0.0)
        current_is_proof = st.session_state.get('shared_is_proof', 'Y')

        if current_is_proof == 'Y' and abs(out_of_balance_total) > 0.02:
            # Show prominent out-of-balance alert
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #C0392B15, #C0392B05);
                       border: 2px solid #C0392B;
                       border-radius: 8px;
                       padding: 16px;
                       margin: 12px 0;
                       text-align: center;
                       animation: pulse 2s infinite;">
                <div style="color: #C0392B; font-weight: 700; font-size: 16px; margin-bottom: 4px;">
                    ⚠️ OUT OF BALANCE
                </div>
                <div style="color: #C0392B; font-weight: 600; font-size: 20px;">
                    {safe_format_currency(out_of_balance_total)}
                </div>
                <div style="color: #C0392B; font-size: 12px; font-weight: 500; margin-top: 4px;">
                    Requires Immediate Attention
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Pipeline Control Buttons - Always accessible
        st.markdown("### 🚀 Pipeline Control")

        # Determine if buttons should be enabled based on current pipeline status
        current_status = ""
        if st.session_state.pipeline_status:
            current_status = st.session_state.pipeline_status.get("runStatus", "").upper()

        # Buttons are disabled if a pipeline is currently running
        buttons_enabled = current_status not in ["RUNNING", "CREATED", "QUEUED"]

        # Show current status if pipeline is running
        if not buttons_enabled:
            st.warning(f"Pipeline is currently {current_status.lower()}. Please wait for completion.")

        # Initialize confirmation state if not exists
        if 'show_finalize_confirmation' not in st.session_state:
            st.session_state.show_finalize_confirmation = False

        # Initialize auto-refresh state if not exists
        if 'auto_refresh_active' not in st.session_state:
            st.session_state.auto_refresh_active = False
        if 'auto_refresh_start_time' not in st.session_state:
            st.session_state.auto_refresh_start_time = None

        # Auto-refresh mechanism - show status if active
        if st.session_state.auto_refresh_active:
            refresh_duration = int(
                time.time() - st.session_state.auto_refresh_start_time) if st.session_state.auto_refresh_start_time else 0

            # Enhanced status display with corporate color coding
            status_color = "#E67E22"  # Professional orange for in-progress
            if current_status == "SUCCEEDED":
                status_color = "#27AE60"  # Corporate green for success
                st.session_state.auto_refresh_active = False  # Stop auto-refresh on completion
            elif current_status in ["FAILED", "CANCELLED"]:
                status_color = "#C0392B"  # Corporate red for failure
                st.session_state.auto_refresh_active = False  # Stop auto-refresh on failure

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {status_color}15, {status_color}05);
                       border-left: 4px solid {status_color};
                       padding: 12px;
                       border-radius: 8px;
                       margin-bottom: 16px;">
                <div style="color: {status_color}; font-weight: 600; font-size: 14px;">
                    🔄 Auto-refresh Active ({refresh_duration}s)
                </div>
                <div style="color: #666; font-size: 12px; margin-top: 4px;">
                    Status: {current_status.title()} | Refreshing every 5 seconds
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Auto-refresh every 5 seconds while pipeline is running
            if current_status in ["RUNNING", "CREATED", "QUEUED"] and refresh_duration < 600:  # Max 10 minutes
                time.sleep(5)
                st.rerun()

        # Professional Pipeline Control Buttons
        sidebar_button_style = """
        <style>
        .sidebar .stButton > button {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 6px;
            padding: 12px 16px;
            font-weight: 500;
            width: 100%;
            margin: 4px 0;
            transition: all 0.2s ease;
            font-size: 14px;
        }
        .sidebar .stButton > button:hover {
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
        }
        .sidebar .stButton > button[kind="primary"] {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.4);
        }
        </style>
        """
        st.markdown(sidebar_button_style, unsafe_allow_html=True)

        if st.button("🔄 Refresh Sales Journal",
                     type="primary",
                     use_container_width=True,
                     disabled=not buttons_enabled,
                     key="sidebar_refresh"):
            # Import the trigger_pipeline function logic
            with st.spinner("Triggering refresh pipeline..."):
                result = trigger_pipeline(REFRESH_PIPELINE_ID, "refresh")

                if result:
                    st.session_state.pipeline_run_id = result.get("pipelineRunId")
                    st.session_state.pipeline_type = "refresh"

                    # Mark that we're expecting a refresh
                    st.session_state.pending_refresh = True

                    # Start auto-refresh mechanism
                    st.session_state.auto_refresh_active = True
                    st.session_state.auto_refresh_start_time = time.time()

                    now_utc = datetime.utcnow()
                    now_pst = now_utc - timedelta(hours=8)
                    st.session_state.last_run_time = now_pst.strftime("%Y-%m-%d %H:%M:%S PST")

                    st.success("🎉 Refresh pipeline triggered! Auto-refresh enabled.")

                    if st.session_state.pipeline_run_id:
                        status = get_pipeline_status(st.session_state.pipeline_run_id)
                        if status:
                            st.session_state.pipeline_status = status
                            st.session_state.run_details = status
                    st.rerun()

        # Finalize Sales Journal Button
        if st.button("✅ Finalize Sales Journal",
                     type="secondary",
                     use_container_width=True,
                     disabled=not buttons_enabled,
                     key="sidebar_finalize"):
            st.session_state.show_finalize_confirmation = True
            st.rerun()

        # Finalize confirmation dialog
        if st.session_state.show_finalize_confirmation:
            st.warning("⚠️ **Confirmation Required**")
            st.markdown("""
            **You are about to finalize the Sales Journal Reporting. This should only be done AFTER Refreshing Sales Journal and validating data.**

            This action will:
            - Process final sales journal entries in Snowflake Data Warehouse
            - Refresh R245_R304BU JDE Reconcilation Report
            - Refresh R1004 Sales Forecast Summary Report

            **Are you sure you want to proceed?**
            """)

            col_confirm1, col_confirm2 = st.columns(2)

            with col_confirm1:
                if st.button("✅ Yes, Finalize", type="primary", use_container_width=True,
                             key="sidebar_confirm_finalize"):
                    st.session_state.show_finalize_confirmation = False

                    with st.spinner("Triggering finalize pipeline..."):
                        result = trigger_pipeline(FINAL_PIPELINE_ID, "final")

                        if result:
                            st.session_state.pipeline_run_id = result.get("pipelineRunId")
                            st.session_state.pipeline_type = "final"

                            now_utc = datetime.utcnow()
                            now_pst = now_utc - timedelta(hours=8)
                            st.session_state.last_run_time = now_pst.strftime("%Y-%m-%d %H:%M:%S PST")

                            st.success("Finalize pipeline triggered successfully!")

                            if st.session_state.pipeline_run_id:
                                status = get_pipeline_status(st.session_state.pipeline_run_id)
                                if status:
                                    st.session_state.pipeline_status = status
                                    st.session_state.run_details = status
                    st.rerun()

            with col_confirm2:
                if st.button("❌ Cancel", use_container_width=True, key="sidebar_cancel_finalize"):
                    st.session_state.show_finalize_confirmation = False
                    st.rerun()


def render_documentation_tab():
    """Render comprehensive documentation for the Sales Journal application"""
    st.header("📖 Sales Journal Documentation")
    st.markdown("**Complete guide to using the APEX Sales Journal application**")

    # Table of Contents
    st.markdown("## 📋 Table of Contents")
    st.markdown("""
    - [Getting Started](#getting-started)
    - [Main Workflow](#main-workflow)
    - [Tab Reference](#tab-reference)
    - [Common Tasks](#common-tasks)
    - [Troubleshooting](#troubleshooting)
    """)

    st.markdown("---")

    # Getting Started
    st.markdown("## 🚀 Getting Started")
    st.markdown("""
    The Sales Journal application is your central hub for managing and monitoring APEX sales data reconciliation
    with the Data Warehouse. The application provides real-time insights into data pipelines, batch reconciliation,
    and transaction-level details.

    ### Quick Start
    1. **Start at Dashboard** - Get an overview of system status
    2. **Run Pipeline Refresh** - Update data using Pipeline Control
    3. **Review Data** - Use Sales Journal, Details, and Balance tabs
    4. **Monitor Tieouts** - Check batch reconciliation status
    """)

    st.markdown("---")

    # Main Workflow
    st.markdown("## 🎯 Main Workflow")
    st.markdown("""
    ### Daily Operations
    """)

    # Workflow steps
    workflow_col1, workflow_col2 = st.columns(2)

    with workflow_col1:
        st.markdown("""
        **1. Pipeline Control** 🚀
        - Run "Refresh Sales Journal" to update data
        - Monitor pipeline status and execution
        - Use "Finalize Sales Journal" when ready

        **2. Data Review** 📊
        - Check Sales Journal for aggregated entries
        - Review Detail by Ticket for transaction-level data
        - Identify issues in Out of Balance tab

        **3. Issue Resolution** 🔍
        - Use 1140 Research for account investigations
        - Monitor Tieout Management for reconciliation
        - Check Pipeline History for execution logs
        """)

    with workflow_col2:
        st.info("""
        **💡 Pro Tips**
        - Always refresh pipeline before data analysis
        - Check tieout status for data quality validation
        - Use filters to narrow down data views
        - Export data for offline analysis when needed
        """)

    st.markdown("---")

    # Tab Reference
    st.markdown("## 📑 Tab Reference")

    # Dashboard
    with st.expander("🏠 Dashboard - System Overview", expanded=True):
        st.markdown("""
        **Purpose**: Central hub with key metrics and quick actions

        **Key Features**:
        - Pipeline status indicators (Ready, Running, Failed)
        - Balance status with real-time amounts
        - Tieout status showing data reconciliation
        - DMS replication monitoring
        - Quick action buttons for common tasks
        - Recent pipeline activity log

        **When to Use**: Start here every session to check system health
        """)

    # Sales Journal
    with st.expander("📊 Sales Journal - Aggregated Data"):
        st.markdown("""
        **Purpose**: View aggregated journal entries by account and batch

        **Key Features**:
        - Batch Type, Batch ID, and Proof filters
        - Account-level summaries with debit/credit totals
        - Export to PDF and CSV functionality
        - Real-time balance calculations
        - Sortable columns for data analysis

        **When to Use**: Daily review of journal entries and account balances
        """)

    # Detail by Ticket
    with st.expander("📋 Detail by Ticket - Transaction Level"):
        st.markdown("""
        **Purpose**: Transaction-level data grouped by ticket date

        **Key Features**:
        - Detailed transaction records
        - Ticket-level grouping and analysis
        - Same filtering options as Sales Journal
        - Export capabilities for detailed analysis
        - Drill-down from journal-level to transaction-level

        **When to Use**: Investigating specific transactions or ticket-level issues
        """)

    # Out of Balance
    with st.expander("⚖️ Out of Balance - Discrepancy Detection"):
        st.markdown("""
        **Purpose**: Identify transactions that don't balance correctly

        **Key Features**:
        - Only available when Proof = 'Y'
        - Shows items where debits ≠ credits
        - Real-time balance calculations
        - Color-coded status (Green ≤ $0.02, Red > $0.02)
        - Filtered views for targeted analysis

        **When to Use**: Quality control and error identification before finalization
        """)

    # 1140 Research
    with st.expander("🔍 1140 Research - Account Investigation"):
        st.markdown("""
        **Purpose**: Specialized research for Object Account 1140 transactions

        **Key Features**:
        - Account-specific filtering and analysis
        - Transaction history and patterns
        - Research tools for account investigations
        - Export capabilities for documentation

        **When to Use**: Investigating specific account discrepancies or research requests
        """)

    # Pipeline Control
    with st.expander("🚀 Pipeline Control - Data Refresh Management"):
        st.markdown("""
        **Purpose**: Control and monitor data refresh workflows

        **Key Features**:
        - "Refresh Sales Journal" button (5-second refresh cycle)
        - "Finalize Sales Journal" button (15-second refresh, requires confirmation)
        - Real-time pipeline status monitoring
        - Buttons disabled during pipeline execution
        - Automatic filter refresh after successful completion

        **When to Use**: Beginning of each session and when fresh data is needed
        """)

    # Tieout Management
    with st.expander("🔄 Tieout Management - Data Reconciliation"):
        st.markdown("""
        **Purpose**: Monitor batch and record-level reconciliation between APEX and Data Warehouse

        **Key Features**:
        - Batch Tieout: Compare batch totals between systems
        - Record Troubleshooting: Monitor AWS DMS replication
        - Real-time status indicators
        - Automatic "green" status when all tieouts match
        - DMS monitoring and exception tracking

        **When to Use**: Data quality validation and replication monitoring
        """)

    st.markdown("---")

    # Common Tasks
    st.markdown("## 🛠️ Common Tasks")

    task_col1, task_col2 = st.columns(2)

    with task_col1:
        st.markdown("""
        **Daily Startup Routine**
        1. Open Dashboard tab
        2. Check pipeline and tieout status
        3. Go to Pipeline Control
        4. Run "Refresh Sales Journal"
        5. Wait for completion
        6. Review data in Sales Journal tab

        **Data Analysis Workflow**
        1. Start with Sales Journal (aggregated view)
        2. Use filters to narrow scope
        3. Export data if needed
        4. Drill down to Detail by Ticket for specifics
        5. Check Out of Balance for issues
        """)

    with task_col2:
        st.markdown("""
        **Error Investigation Process**
        1. Check Dashboard for system issues
        2. Review Out of Balance tab for discrepancies
        3. Use Detail by Ticket for transaction details
        4. Check Tieout Management for data sync issues
        5. Use 1140 Research for account-specific problems
        6. Review Pipeline History for execution issues

        **End-of-Period Finalization**
        1. Run Refresh Sales Journal
        2. Verify all tieouts are "green"
        3. Check Out of Balance shows $0.00 or ≤ $0.02
        4. Run "Finalize Sales Journal" (requires confirmation)
        5. Verify finalization completed successfully
        """)

    st.markdown("---")

    # Troubleshooting
    st.markdown("## 🔧 Troubleshooting")

    with st.expander("Common Issues and Solutions"):
        st.markdown("""
        **Pipeline Won't Start**
        - Check if another pipeline is currently running
        - Verify database connectivity in Debug tab
        - Wait for current execution to complete

        **No Data Showing**
        - Verify correct filters are selected
        - Check if pipeline refresh is needed
        - Confirm database connection is available

        **Tieouts Not "Green"**
        - Run pipeline refresh to update data
        - Check DMS replication status in Tieout Management
        - Review specific batch discrepancies

        **Out of Balance Issues**
        - Ensure Proof filter is set to 'Y'
        - Run fresh pipeline refresh
        - Review transaction details for specific discrepancies

        **Performance Issues**
        - Use filters to limit data scope
        - Check pipeline execution status
        - Consider running refresh during off-peak hours
        """)

    st.markdown("---")

    # Contact Information
    st.markdown("## 📞 Support")
    st.info("""
    **Need Help?**
    - Check the Debug tab for system diagnostics
    - Review Pipeline History for execution logs
    - Contact your system administrator for database issues
    - This is the APEX Upgrade Test Version - validate results against production
    """)


def render_dashboard_overview_tab():
    """Enhanced Dashboard Overview with modern visual hierarchy and improved UX"""

    # Professional Corporate Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1B365D 0%, #2E5984 100%);
                color: white;
                padding: 32px 24px;
                border-radius: 8px;
                margin-bottom: 32px;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                border-left: 4px solid #4A7BA7;">
        <h1 style="margin: 0; font-size: 28px; font-weight: 600; letter-spacing: -0.02em;">🏠 Sales Journal Dashboard</h1>
        <p style="margin: 12px 0 0 0; font-size: 16px; opacity: 0.9; font-weight: 400;">Professional financial reporting and pipeline management</p>
    </div>
    """, unsafe_allow_html=True)

    if not POSTGRES_AVAILABLE:
        st.error("Database connection not available. Please contact your administrator.")
        return

    # Professional Corporate Status Cards
    def render_enhanced_status_card(title, status, icon, color, description=""):
        """Render a professional financial status card"""
        return f"""
        <div style="background: white;
                   border: 1px solid #E5E7EB;
                   border-radius: 8px;
                   padding: 24px;
                   margin: 8px 0;
                   box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                   border-left: 4px solid {color};
                   transition: all 0.2s ease;
                   height: 140px;
                   display: flex;
                   flex-direction: column;
                   justify-content: space-between;">
            <div>
                <div style="color: #2C3E50; font-size: 14px; font-weight: 600; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.05em;">
                    {title}
                </div>
                <div style="color: {color}; font-size: 20px; font-weight: 600; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 18px;">{icon}</span>
                    <span>{status}</span>
                </div>
            </div>
            <div style="color: #7F8C8D; font-size: 12px; line-height: 1.4; font-weight: 400;">
                {description}
            </div>
        </div>
        """

    try:
        # Enhanced metrics row with F-Pattern layout
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Enhanced Pipeline Status Card
            current_status = ""
            if st.session_state.pipeline_status:
                current_status = st.session_state.pipeline_status.get("runStatus", "").upper()

            if current_status in ["RUNNING", "CREATED", "QUEUED"]:
                status_color = "#E67E22"
                status_text = "RUNNING"
                status_icon = "🔄"
                description = "Pipeline is currently processing"
            elif current_status == "SUCCEEDED":
                status_color = "#27AE60"
                status_text = "READY"
                status_icon = "✅"
                description = "System is ready for operations"
            elif current_status == "FAILED":
                status_color = "#C0392B"
                status_text = "FAILED"
                status_icon = "❌"
                description = "Pipeline requires attention"
            else:
                status_color = "#7F8C8D"
                status_text = "IDLE"
                status_icon = "⏸️"
                description = "No active pipeline operations"

            st.markdown(render_enhanced_status_card(
                "🚀 Pipeline Status",
                status_text,
                status_icon,
                status_color,
                description
            ), unsafe_allow_html=True)

        with col2:
            # Enhanced Balance Status Card
            current_batch_type = st.session_state.get('shared_batch_type', 'CASH')
            current_batch_id = st.session_state.get('shared_batch_id', 'All')
            current_is_proof = st.session_state.get('shared_is_proof', 'Y')

            out_of_balance_total = st.session_state.get('out_of_balance_total', 0.0)

            if current_is_proof == 'Y':
                if abs(out_of_balance_total) <= 0.02:
                    balance_color = "#27AE60"
                    balance_text = "IN BALANCE"
                    balance_icon = "✅"
                    balance_desc = f"Amount: {safe_format_currency(out_of_balance_total)}"
                else:
                    balance_color = "#C0392B"
                    balance_text = "OUT OF BALANCE"
                    balance_icon = "🔴"
                    balance_desc = f"Variance: {safe_format_currency(out_of_balance_total)}"
            else:
                balance_color = "#E67E22"
                balance_text = "PROOF REQUIRED"
                balance_icon = "⚠️"
                balance_desc = "Set proof to 'Y' to check balance"

            st.markdown(render_enhanced_status_card(
                "⚖️ Balance Status",
                balance_text,
                balance_icon,
                balance_color,
                balance_desc
            ), unsafe_allow_html=True)

        with col3:
            # Enhanced Tieout Status Card
            tieout_emoji = st.session_state.get('tieout_emoji', '❓')
            if tieout_emoji == '✅':
                tieout_color = "#27AE60"
                tieout_text = "MATCHED"
                tieout_icon = "✅"
                tieout_desc = "Tieout reconciliation successful"
            elif tieout_emoji == '❌':
                tieout_color = "#C0392B"
                tieout_text = "MISMATCHED"
                tieout_icon = "❌"
                tieout_desc = "Tieout requires investigation"
            else:
                tieout_color = "#7F8C8D"
                tieout_text = "CHECKING"
                tieout_icon = "❓"
                tieout_desc = "Tieout verification in progress"

            st.markdown(render_enhanced_status_card(
                "🔍 Tieout Status",
                tieout_text,
                tieout_icon,
                tieout_color,
                tieout_desc
            ), unsafe_allow_html=True)

        with col4:
            # Enhanced DMS Status Card
            with st.spinner("Checking DMS..."):
                dms_query = "SELECT task_status FROM dbt_dev_utils.fact_aws_dms__status LIMIT 1"
                dms_data = query_postgres(dms_query)

                if dms_data is not None and not dms_data.empty:
                    if (dms_data['task_status'] == 'CHANGE PROCESSING').all():
                        dms_color = "#27AE60"
                        dms_text = "PROCESSING"
                        dms_icon = "✅"
                        dms_desc = "Data replication active"
                    else:
                        dms_color = "#C0392B"
                        dms_text = "STOPPED"
                        dms_icon = "❌"
                        dms_desc = "Replication service inactive"
                else:
                    dms_color = "#E67E22"
                    dms_text = "UNKNOWN"
                    dms_icon = "❓"
                    dms_desc = "Unable to determine status"

            st.markdown(render_enhanced_status_card(
                "⚙️ DMS Status",
                dms_text,
                dms_icon,
                dms_color,
                dms_desc
            ), unsafe_allow_html=True)

        # Professional section divider
        st.markdown("""
        <div style="height: 1px; background: #E5E7EB; margin: 32px 0;"></div>
        """, unsafe_allow_html=True)

        # Enhanced Quick Actions section
        st.markdown("""
        <div style="background: #f8f9fa;
                   border-radius: 16px;
                   padding: 24px;
                   margin-bottom: 24px;
                   border: 1px solid #e9ecef;">
            <h3 style="color: #2c3e50; margin-bottom: 16px; font-size: 20px; font-weight: 600;">
                🎯 Quick Actions
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced action buttons with modern styling
        action_button_style = """
        <style>
        .action-button {
            background: white;
            border: 2px solid #e1e8ed;
            border-radius: 12px;
            padding: 16px;
            margin: 8px 0;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .action-button:hover {
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        }
        </style>
        """
        st.markdown(action_button_style, unsafe_allow_html=True)

        action_col1, action_col2, action_col3, action_col4 = st.columns(4)

        with action_col1:
            if st.button("🔄 Refresh Pipeline", type="primary", use_container_width=True, help="Go to Pipeline Control"):
                st.session_state.active_tab_index = 5  # Pipeline Control tab (new index)
                st.rerun()

        with action_col2:
            if st.button("📊 View Journal", use_container_width=True, help="View Sales Journal entries"):
                st.session_state.active_tab_index = 1  # Sales Journal tab
                st.rerun()

        with action_col3:
            if st.button("⚖️ Check Balance", use_container_width=True, help="Check out of balance items"):
                if current_is_proof == 'Y':
                    st.session_state.active_tab_index = 3  # Out of Balance tab
                    st.rerun()
                else:
                    st.warning("Set Proof to 'Y' first")

        with action_col4:
            if st.button("🔍 Tieout Status", use_container_width=True, help="View tieout management"):
                st.session_state.active_tab_index = 6  # Tieout Management tab
                st.rerun()

        # Professional section divider
        st.markdown("""
        <div style="height: 1px; background: #E5E7EB; margin: 32px 0;"></div>
        """, unsafe_allow_html=True)

        # Enhanced Recent Activity section
        st.markdown("""
        <div style="background: #f8f9fa;
                   border-radius: 16px;
                   padding: 24px;
                   margin-bottom: 16px;
                   border: 1px solid #e9ecef;">
            <h3 style="color: #2c3e50; margin-bottom: 16px; font-size: 20px; font-weight: 600;">
                📈 Recent Pipeline Activity
            </h3>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Loading recent activity..."):
            history_data = get_pipeline_history([REFRESH_PIPELINE_ID, FINAL_PIPELINE_ID], limit=5)

        if history_data and len(history_data) > 0:
            for i, run in enumerate(history_data[:3]):  # Show only last 3 runs
                # Enhanced activity cards
                start_time = format_timestamp(run.get("startedAt") or run.get("createdAt"))
                pipeline_id = run.get("pipelineId", "")
                status = run.get("runStatus", "Unknown")

                # Determine colors and icons
                if pipeline_id == REFRESH_PIPELINE_ID:
                    pipeline_icon = "🔄"
                    pipeline_name = "Refresh"
                elif pipeline_id == FINAL_PIPELINE_ID:
                    pipeline_icon = "✅"
                    pipeline_name = "Final"
                else:
                    pipeline_icon = "❓"
                    pipeline_name = "Unknown"

                if status == "SUCCEEDED":
                    status_color = "#2ECC71"
                    status_icon = "✅"
                elif status == "FAILED":
                    status_color = "#E74C3C"
                    status_icon = "❌"
                else:
                    status_color = "#FF6B35"
                    status_icon = "🔄"

                st.markdown(f"""
                <div style="background: white;
                           border: 1px solid #e1e8ed;
                           border-radius: 12px;
                           padding: 16px;
                           margin: 8px 0;
                           border-left: 4px solid {status_color};
                           box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 600; color: #2c3e50; font-size: 14px;">
                                {pipeline_icon} {pipeline_name} Pipeline
                            </div>
                            <div style="color: #7f8c8d; font-size: 12px; margin-top: 4px;">
                                {start_time}
                            </div>
                        </div>
                        <div style="display: flex; align-items: center;">
                            <div style="background: {status_color}15;
                                       color: {status_color};
                                       padding: 6px 12px;
                                       border-radius: 20px;
                                       font-size: 12px;
                                       font-weight: 600;">
                                {status_icon} {status.upper()}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #fff3cd;
                       border: 1px solid #ffeaa7;
                       border-radius: 12px;
                       padding: 16px;
                       text-align: center;
                       color: #856404;">
                <div style="font-size: 14px;">📋 No recent activity found</div>
                <div style="font-size: 12px; margin-top: 4px; opacity: 0.8;">
                    Pipeline activity will appear here after first run
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Dashboard-specific footer (removed system info section)
        footer_col1, footer_col2 = st.columns(2)

        with footer_col1:
            st.markdown("### 🎯 Main Workflow")
            st.markdown("""
            1. **🚀 Pipeline Control**: Run Refresh Sales Journal
            2. **📊 Sales Journal**: Review aggregated entries
            3. **📋 Detail by Ticket**: Transaction-level analysis
            4. **⚖️ Out of Balance**: Identify discrepancies
            5. **🔍 1140 Research**: Account investigation
            """)

        with footer_col2:
            st.markdown("### 🔧 Key Features")
            st.markdown("""
            - **📖 Documentation**: Complete user guide available
            - **🔍 Tieout Status**: Real-time "green" indicators
            - **📈 Export**: CSV downloads with timestamps
            - **🔄 Auto-refresh**: Status updates every 5 minutes
            - **⚡ Quick Actions**: One-click navigation buttons
            """)

        st.markdown("---")
        st.markdown("*💡 **Tip**: Check the Documentation tab for detailed instructions on using each feature.*")

    except Exception as e:
        logger.error(f"Error in render_dashboard_overview_tab: {str(e)}")
        st.error("Failed to load dashboard data. Please try again or contact support.")
        st.exception(e)


def render_consolidated_tieout_tab():
    """Render consolidated Tieout tab with sub-tabs for Batches and Records"""
    st.header("🔍 Tieout Management")
    st.markdown("**APEX vs Data Warehouse reconciliation and troubleshooting**")

    # Sub-tab navigation
    tieout_tab1, tieout_tab2 = st.tabs(["🔄 Batch Tieout", "🔍 Record Troubleshooting"])

    with tieout_tab1:
        st.markdown("### 🔄 Batch Reconciliation")
        st.markdown("Compare batch totals between APEX and Data Warehouse")

        if not POSTGRES_AVAILABLE:
            st.error("Database connection not available. Please contact your administrator.")
            return

        try:
            # Use the original working tieout query (no filters needed)
            tieout_query = """
                           SELECT batch_id, \
                                  export_date, \
                                  batch_type, \
                                  is_proof, \
                                  qty_apex, \
                                  qty_batman, \
                                  ticket_amount_apex, \
                                  ticket_amount_batman, \
                                  count_apex, \
                                  count_batman, \
                                  test
                           FROM dbt_dev_accounting.rpt_r245t_apex_sales_journal_tieout_app_only
                           ORDER BY batch_id DESC, export_date \
                           """

            with st.spinner("Loading tieout data..."):
                tieout_data = query_postgres(tieout_query)

            if tieout_data is not None and not tieout_data.empty:
                # Use the original working status logic
                all_ties = (tieout_data['test'] == 'TIES').all() if 'test' in tieout_data.columns else False
                emoji = "✅" if all_ties else "❌"
                status_text = "All batches tie out correctly" if all_ties else "Some batches do not tie out"
                status_color = "green" if all_ties else "red"

                st.markdown(f":{status_color}[{emoji} **{status_text}**]")

                # Use the original working data formatting
                display_data = tieout_data.copy()

                # Format numeric columns
                numeric_columns = ['qty_apex', 'qty_batman', 'ticket_amount_apex', 'ticket_amount_batman', 'count_apex',
                                   'count_batman']
                for col in numeric_columns:
                    if col in display_data.columns:
                        display_data[col] = display_data[col].apply(safe_format_number)

                # Format date columns
                if 'export_date' in display_data.columns:
                    display_data['export_date'] = display_data['export_date'].apply(safe_format_date)

                # Rename columns for display
                display_data = display_data.rename(columns={
                    'batch_id': 'Batch ID',
                    'export_date': 'Export Date',
                    'batch_type': 'Batch Type',
                    'is_proof': 'Is Proof',
                    'qty_apex': 'Qty APEX',
                    'qty_batman': 'Qty Data Warehouse',
                    'ticket_amount_apex': 'Ticket Amount APEX',
                    'ticket_amount_batman': 'Ticket Amount Data Warehouse',
                    'count_apex': 'Count APEX',
                    'count_batman': 'Count Data Warehouse',
                    'test': 'Status'
                })

                st.dataframe(
                    display_data,
                    use_container_width=True,
                    hide_index=True
                )

                # Export functionality
                if st.button("📊 Export Tieout Data", use_container_width=True):
                    csv_data = tieout_data.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv_data,
                        file_name=f"tieout_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                st.warning("No tieout data found.")

        except Exception as e:
            logger.error(f"Error in tieout batches section: {str(e)}")
            st.error("An unexpected error occurred. Please contact support.")

            # Show more helpful error info in an expander
            with st.expander("🔍 Error Details"):
                if "relation" in str(e).lower() or "table" in str(e).lower():
                    st.warning("The tieout table may not be available. Please check with your administrator.")
                else:
                    st.code(f"Error: {str(e)}")
                st.caption("Share this information with support if the issue persists.")

    with tieout_tab2:
        st.markdown("### 🔍 Record Replication Troubleshooting")
        st.markdown("Monitor AWS DMS replication and troubleshoot ticket record issues")

        if not POSTGRES_AVAILABLE:
            st.error("Database connection not available. Please contact your administrator.")
            return

        try:
            # Section 1: Tickets Count Comparison (Last 7 Days)
            st.subheader("📊 Tickets Count Comparison (Last 7 Days)")
            tickets_query = """
                            SELECT *
                            FROM dbt_dev_utils.fact_apex_ih__tickets_count_last7days
                            ORDER BY sale_date DESC \
                            """

            with st.spinner("Loading tickets count data..."):
                tickets_data = query_postgres(tickets_query)

            if tickets_data is not None and not tickets_data.empty:
                if 'sale_date' in tickets_data.columns:
                    tickets_data['sale_date'] = tickets_data['sale_date'].apply(safe_format_date)

                st.dataframe(tickets_data, use_container_width=True, hide_index=True)
            else:
                st.warning("No tickets count data found.")

            st.divider()

            # Section 2: DMS Task Status
            st.subheader("⚙️ DMS Replication Task Status")
            dms_status_query = """
                               SELECT *
                               FROM dbt_dev_utils.fact_aws_dms__status \
                               """

            with st.spinner("Loading DMS status data..."):
                dms_data = query_postgres(dms_status_query)

            if dms_data is not None and not dms_data.empty:
                all_change_processing = (dms_data[
                                             'task_status'] == 'CHANGE PROCESSING').all() if 'task_status' in dms_data.columns else False
                emoji = "✅" if all_change_processing else "❌"
                status_text = "All replication tasks are processing changes" if all_change_processing else "Some replication tasks are not processing changes"
                status_color = "green" if all_change_processing else "red"

                st.markdown(f":{status_color}[{emoji} {status_text}]")

                st.dataframe(dms_data, use_container_width=True, hide_index=True)
            else:
                st.warning("No DMS status data found.")

            st.divider()

            # Section 3: Quick Status Summary
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🚫 Suspended Tables")
                suspended_query = "SELECT COUNT(*) as count FROM dbt_dev_utils.fact_aws_dms__suspended_tables"
                suspended_count = query_postgres(suspended_query)

                if suspended_count is not None and not suspended_count.empty:
                    count = suspended_count['count'].iloc[0]
                    if count == 0:
                        st.success("✅ No suspended tables")
                    else:
                        st.error(f"⚠️ {count} suspended table(s)")
                else:
                    st.warning("❓ Cannot check suspended tables")

            with col2:
                st.subheader("❌ Apply Exceptions")
                exceptions_query = "SELECT COUNT(*) as count FROM dbt_dev_utils.fact_aws_dms__apply_exceptions"
                exceptions_count = query_postgres(exceptions_query)

                if exceptions_count is not None and not exceptions_count.empty:
                    count = exceptions_count['count'].iloc[0]
                    if count == 0:
                        st.success("✅ No apply exceptions")
                    else:
                        st.error(f"⚠️ {count} exception(s)")
                else:
                    st.warning("❓ Cannot check exceptions")

        except Exception as e:
            logger.error(f"Error in tieout records section: {str(e)}")
            st.error("Failed to load tieout records data. Please try again or contact support.")


def render_tieout_records_tab():
    """Render the Tieout Records tab for troubleshooting ticket record replication"""
    st.header("🔍 Tieout Records - Ticket Replication Troubleshooting")
    st.markdown("**Troubleshooting ticket record replication between APEX and Data Warehouse**")

    if not POSTGRES_AVAILABLE:
        st.error("Database connection not available. Please contact your administrator.")
        return

    try:

        # Section 1: Tickets Count Comparison (Last 7 Days)
        st.subheader("📊 Tickets Count Comparison (Last 7 Days)")
        tickets_query = """
                        SELECT *
                        FROM dbt_dev_utils.fact_apex_ih__tickets_count_last7days
                        ORDER BY sale_date DESC \
                        """

        with st.spinner("Loading tickets count data..."):
            tickets_data = query_postgres(tickets_query)

        if tickets_data is not None and not tickets_data.empty:
            # Format dates if present
            if 'sale_date' in tickets_data.columns:
                tickets_data['sale_date'] = tickets_data['sale_date'].apply(safe_format_date)

            st.dataframe(
                tickets_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No tickets count data found.")

        st.divider()

        # Section 2: DMS Task Status
        st.subheader("⚙️ DMS Replication Task Status")
        dms_status_query = """
                           SELECT *
                           FROM dbt_dev_utils.fact_aws_dms__status \
                           """

        with st.spinner("Loading DMS status data..."):
            dms_data = query_postgres(dms_status_query)

        if dms_data is not None and not dms_data.empty:
            # Check status and display status indicator
            all_change_processing = (dms_data[
                                         'task_status'] == 'CHANGE PROCESSING').all() if 'task_status' in dms_data.columns else False
            emoji = "✅" if all_change_processing else "❌"
            status_text = "All replication tasks are processing changes" if all_change_processing else "Some replication tasks are not processing changes"
            status_color = "green" if all_change_processing else "red"

            st.markdown(f":{status_color}[{emoji} {status_text}]")

            st.dataframe(
                dms_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No DMS status data found.")

        st.divider()

        # Section 3: Sync Log Last Record
        st.subheader("📝 Sync Log - Most Recent Records")
        sync_log_query = """
                         SELECT *
                         FROM dbt_dev_utils.fact_postgres__sync_log_lastrecord \
                         """

        with st.spinner("Loading sync log data..."):
            sync_log_data = query_postgres(sync_log_query)

        if sync_log_data is not None and not sync_log_data.empty:
            # Format timestamps if present
            timestamp_columns = ['last_sync_time', 'created_at', 'updated_at', 'timestamp']
            for col in timestamp_columns:
                if col in sync_log_data.columns:
                    sync_log_data[col] = sync_log_data[col].apply(safe_format_date)

            st.dataframe(
                sync_log_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No sync log data found.")

        st.divider()

        # Section 4: Suspended Tables (Should be empty)
        st.subheader("🚫 DMS Suspended Tables")
        st.caption("This table should typically be empty. Any records indicate replication issues.")

        suspended_query = """
                          SELECT *
                          FROM dbt_dev_utils.fact_aws_dms__suspended_tables \
                          """

        with st.spinner("Loading suspended tables data..."):
            suspended_data = query_postgres(suspended_query)

        if suspended_data is not None and not suspended_data.empty:
            st.error(f"⚠️ Found {len(suspended_data)} suspended table(s)!")
            st.dataframe(
                suspended_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ No suspended tables found (as expected)")

        st.divider()

        # Section 5: Apply Exceptions (Should be empty)
        st.subheader("❌ DMS Apply Exceptions")
        st.caption("This table should typically be empty. Any records indicate replication errors.")

        exceptions_query = """
                           SELECT *
                           FROM dbt_dev_utils.fact_aws_dms__apply_exceptions \
                           """

        with st.spinner("Loading apply exceptions data..."):
            exceptions_data = query_postgres(exceptions_query)

        if exceptions_data is not None and not exceptions_data.empty:
            st.error(f"⚠️ Found {len(exceptions_data)} apply exception(s)!")
            st.dataframe(
                exceptions_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ No apply exceptions found (as expected)")

    except Exception as e:
        logger.error(f"Error in render_tieout_records_tab: {str(e)}")
        st.error("Failed to load tieout records data. Please try again or contact support.")
        st.exception(e)


def render_pipeline_control_tab():
    """Render Pipeline Control tab with error handling - Updated with two buttons"""
    st.header("Pipeline Control")

    try:
        if st.session_state.last_run_time:
            current_pipeline_type = st.session_state.get('pipeline_type', 'unknown')
            st.info(f"Last run: {st.session_state.last_run_time} ({current_pipeline_type.title()} Pipeline)")

        # Determine if buttons should be enabled based on current pipeline status
        current_status = ""
        if st.session_state.pipeline_status:
            current_status = st.session_state.pipeline_status.get("runStatus", "").upper()

        # Buttons are disabled if a pipeline is currently running
        buttons_enabled = current_status not in ["RUNNING", "CREATED", "QUEUED"]

        # Show current status if pipeline is running
        if not buttons_enabled:
            st.warning(
                f"Pipeline is currently {current_status.lower()}. Please wait for completion before starting another run.")

        # Initialize confirmation state if not exists
        if 'show_finalize_confirmation' not in st.session_state:
            st.session_state.show_finalize_confirmation = False

        # Two buttons side by side
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Refresh Sales Journal",
                         type="primary",
                         use_container_width=True,
                         disabled=not buttons_enabled):
                with st.spinner("Triggering refresh pipeline..."):
                    result = trigger_pipeline(REFRESH_PIPELINE_ID, "refresh")

                    if result:
                        st.session_state.pipeline_run_id = result.get("pipelineRunId")
                        st.session_state.pipeline_type = "refresh"

                        # Mark that we're expecting a refresh
                        st.session_state.pending_refresh = True

                        now_utc = datetime.utcnow()
                        now_pst = now_utc - timedelta(hours=8)
                        st.session_state.last_run_time = now_pst.strftime("%Y-%m-%d %H:%M:%S PST")

                        st.success("Refresh pipeline triggered successfully!")
                        st.json(result)

                        if st.session_state.pipeline_run_id:
                            status = get_pipeline_status(st.session_state.pipeline_run_id)
                            if status:
                                st.session_state.pipeline_status = status
                                st.session_state.run_details = status

        with col2:
            if st.button("✅ Finalize Sales Journal",
                         type="secondary",
                         use_container_width=True,
                         disabled=not buttons_enabled):
                st.session_state.show_finalize_confirmation = True

        # Finalize confirmation dialog
        if st.session_state.show_finalize_confirmation:
            st.markdown("---")
            st.warning("⚠️ **Confirmation Required**")
            st.markdown("""
            **You are about to finalize the Sales Journal Reporting. This should only be done AFTER Refreshing Sales Journal and validating data.**

            This action will:
            - Process final sales journal entries in Snowflake Data Warehouse
            - Refresh R245_R304BU JDE Reconcilation Report
            - Refresh R1004 Sales Forecast Summary Report

            **Are you sure you want to proceed?**
            """)

            col_confirm1, col_confirm2, col_confirm3 = st.columns([1, 1, 1])

            with col_confirm1:
                if st.button("✅ Yes, Finalize", type="primary", use_container_width=True):
                    st.session_state.show_finalize_confirmation = False

                    with st.spinner("Triggering finalize pipeline..."):
                        result = trigger_pipeline(FINAL_PIPELINE_ID, "final")

                        if result:
                            st.session_state.pipeline_run_id = result.get("pipelineRunId")
                            st.session_state.pipeline_type = "final"

                            # Mark that we're expecting a refresh for final pipeline too
                            st.session_state.pending_refresh = True

                            now_utc = datetime.utcnow()
                            now_pst = now_utc - timedelta(hours=8)
                            st.session_state.last_run_time = now_pst.strftime("%Y-%m-%d %H:%M:%S PST")

                            st.success("Finalize pipeline triggered successfully!")
                            st.json(result)

                            if st.session_state.pipeline_run_id:
                                status = get_pipeline_status(st.session_state.pipeline_run_id)
                                if status:
                                    st.session_state.pipeline_status = status
                                    st.session_state.run_details = status
                    st.rerun()

            with col_confirm2:
                if st.button("❌ Cancel", type="secondary", use_container_width=True):
                    st.session_state.show_finalize_confirmation = False
                    st.rerun()

            with col_confirm3:
                st.empty()  # Spacer column

        st.markdown("---")
        st.header("Status Monitor")

        # Only show refresh status button if we're not in confirmation mode
        if not st.session_state.get('show_finalize_confirmation', False):
            if st.button("🔄 Refresh Status"):
                if st.session_state.pipeline_run_id:
                    status = get_pipeline_status(st.session_state.pipeline_run_id)
                    if status:
                        st.session_state.pipeline_status = status
                        st.session_state.run_details = status
                else:
                    st.warning("No active pipeline run to check")

        if st.session_state.pipeline_run_id:
            st.header("Current Run Status")

            col_status1, col_status2, col_status3 = st.columns(3)

            with col_status1:
                st.metric("Pipeline Run ID", st.session_state.pipeline_run_id)

            with col_status2:
                if st.session_state.pipeline_status:
                    status_value = st.session_state.pipeline_status.get("runStatus", "Unknown")
                    st.metric("Status", status_value)
                else:
                    st.metric("Status", "Loading...")

            with col_status3:
                pipeline_type = st.session_state.get('pipeline_type', 'unknown')
                st.metric("Pipeline Type", pipeline_type.title())

            if st.session_state.run_details:
                st.subheader("Run Details")

                detail_tab1, detail_tab2 = st.tabs(["Overview", "Raw Data"])

                with detail_tab1:
                    details = st.session_state.run_details

                    if "runStatus" in details:
                        status = details["runStatus"]
                        status_color = "green" if status == "SUCCEEDED" else "orange" if status in ["RUNNING",
                                                                                                    "CREATED"] else "red" if status == "FAILED" else "gray"
                        st.markdown(f"**Status:** :{status_color}[{status}]")

                    if "pipelineName" in details:
                        st.write(f"**Pipeline:** {details['pipelineName']}")

                    if "startedAt" in details:
                        st.write(f"**Start Time:** {format_timestamp(details['startedAt'])}")

                    if "completedAt" in details:
                        st.write(f"**End Time:** {format_timestamp(details['completedAt'])}")

                    if "message" in details:
                        st.write(f"**Message:** {details['message']}")

                    if "branch" in details:
                        st.write(f"**Branch:** {details['branch']}")

                    if "envName" in details:
                        st.write(f"**Environment:** {details['envName']}")

                with detail_tab2:
                    st.json(st.session_state.run_details)

            # Auto-refresh logic with different intervals based on pipeline type
            if st.session_state.pipeline_run_id:
                current_status = st.session_state.pipeline_status.get("runStatus",
                                                                      "").upper() if st.session_state.pipeline_status else ""
                pipeline_type = st.session_state.get('pipeline_type', 'refresh')

                # Only auto-refresh if pipeline is still running
                if current_status in ["RUNNING", "CREATED"]:
                    refresh_interval = 15 if pipeline_type == "final" else 5  # 15 seconds for final, 5 for refresh
                    with st.empty():
                        st.info(f"Auto-refreshing in {refresh_interval} seconds... ({pipeline_type.title()} Pipeline)")
                        time.sleep(refresh_interval)
                        # Get updated status
                        status = get_pipeline_status(st.session_state.pipeline_run_id)
                        if status:
                            st.session_state.pipeline_status = status
                            st.session_state.run_details = status
                        st.rerun()
                elif current_status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
                    # Check if we need to refresh caches and reset filters
                    if current_status == "SUCCEEDED" and st.session_state.get('pending_refresh', False):
                        # Clear the pending refresh flag
                        st.session_state.pending_refresh = False

                        # Clear all cached data
                        st.cache_data.clear()
                        if hasattr(st, 'cache_resource'):
                            st.cache_resource.clear()

                        # Reset filters to defaults with new data
                        refresh_and_reset_filters()

                        logger.info(
                            f"{pipeline_type.title()} pipeline completed successfully - caches cleared and filters reset")

                        st.success(
                            f"✅ {pipeline_type.title()} pipeline completed successfully! Filters have been refreshed with latest data.")

                        # Force a rerun to refresh the UI with new data
                        time.sleep(1)  # Brief pause to show the success message
                        st.rerun()
                    else:
                        # Show final status without refreshing
                        st.success(f"{pipeline_type.title()} pipeline completed with status: {current_status}")
                elif current_status:
                    st.info(f"{pipeline_type.title()} pipeline status: {current_status}")

        else:
            st.info("No active pipeline run. Trigger a pipeline to monitor its status.")

    except Exception as e:
        logger.error(f"Error in render_pipeline_control_tab: {str(e)}")
        st.error("Error in pipeline control. Please refresh the page.")
        st.exception(e)


def render_pipeline_history_tab():
    """Render the Pipeline History tab - Updated to show both pipelines"""
    st.header("📊 Recent Pipeline Runs")

    try:
        with st.spinner("Loading pipeline history..."):
            # Get history for both pipelines
            history_data = get_pipeline_history([REFRESH_PIPELINE_ID, FINAL_PIPELINE_ID], limit=15)

        if history_data and len(history_data) > 0:
            table_data = []
            for run in history_data:
                run_id = run.get("id", "N/A")[:8] + "..." if run.get("id") else "N/A"
                status = run.get("runStatus", "Unknown")
                start_time = format_timestamp(run.get("startedAt") or run.get("createdAt"))
                end_time = format_timestamp(run.get("completedAt"))

                # Determine pipeline type based on pipeline ID
                pipeline_id = run.get("pipelineId", "")
                if pipeline_id == REFRESH_PIPELINE_ID:
                    pipeline_type = "Refresh"
                elif pipeline_id == FINAL_PIPELINE_ID:
                    pipeline_type = "Final"
                else:
                    pipeline_type = "Unknown"

                duration = "N/A"
                if run.get("startedAt") and run.get("completedAt"):
                    try:
                        start_dt = datetime.fromisoformat(run["startedAt"].replace('Z', '+00:00'))
                        end_dt = datetime.fromisoformat(run["completedAt"].replace('Z', '+00:00'))
                        duration_seconds = (end_dt - start_dt).total_seconds()

                        if duration_seconds < 60:
                            duration = f"{int(duration_seconds)}s"
                        elif duration_seconds < 3600:
                            duration = f"{int(duration_seconds / 60)}m {int(duration_seconds % 60)}s"
                        else:
                            hours = int(duration_seconds / 3600)
                            minutes = int((duration_seconds % 3600) / 60)
                            duration = f"{hours}h {minutes}m"
                    except:
                        duration = "N/A"

                table_data.append({
                    "Pipeline": pipeline_type,  # New column first
                    "Run ID": run_id,
                    "Status": status,
                    "Started": start_time,
                    "Completed": end_time,
                    "Duration": duration,
                    "Message": run.get("message", "")[:50] + "..." if len(run.get("message", "")) > 50 else run.get(
                        "message", "")
                })

            df = pd.DataFrame(table_data)

            def style_status(val):
                val_upper = str(val).upper()
                if val_upper == 'SUCCEEDED':
                    return 'color: green; font-weight: bold'
                elif val_upper == 'FAILED':
                    return 'color: red; font-weight: bold'
                elif val_upper in ['RUNNING', 'CREATED']:
                    return 'color: orange; font-weight: bold'
                elif val_upper == 'WARNING':
                    return 'color: gold; font-weight: bold'
                elif val_upper in ['CANCELLED', 'CANCELLING']:
                    return 'color: gray; font-weight: bold'
                else:
                    return 'color: gray'

            def style_pipeline_type(val):
                if val == 'Refresh':
                    return 'background-color: #e3f2fd; color: #0d47a1; font-weight: bold'
                elif val == 'Final':
                    return 'background-color: #f3e5f5; color: #4a148c; font-weight: bold'
                else:
                    return 'color: gray'

            styled_df = df.style.applymap(style_status, subset=['Status']).applymap(style_pipeline_type,
                                                                                    subset=['Pipeline'])
            st.dataframe(styled_df, use_container_width=True, height=600, hide_index=True)

            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)

            refresh_runs = [r for r in table_data if r['Pipeline'] == 'Refresh']
            final_runs = [r for r in table_data if r['Pipeline'] == 'Final']

            with col1:
                st.metric("Total Runs", len(history_data))
            with col2:
                st.metric("Refresh Runs", len(refresh_runs))
            with col3:
                st.metric("Final Runs", len(final_runs))
            with col4:
                if st.button("🔄 Refresh History"):
                    st.rerun()

            st.caption(f"Showing last {len(history_data)} runs across both pipelines")
        else:
            st.info("No recent pipeline runs found.")
            if st.button("🔄 Refresh History"):
                st.rerun()

    except Exception as e:
        logger.error(f"Error in render_pipeline_history_tab: {str(e)}")
        st.error("Failed to load pipeline history. Please try again or contact support.")
        st.exception(e)


def render_debug_tab():
    """Render debug information tab (simplified for this example)"""
    st.header("🔧 Debug & Connection Information")
    st.markdown("**Troubleshooting tools for the Sales Journal reports**")

    try:
        st.info(f"**Refresh Pipeline ID:** `{REFRESH_PIPELINE_ID}`")
        st.info(f"**Final Pipeline ID:** `{FINAL_PIPELINE_ID}`")

        # Connection status
        st.subheader("Connection Status")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔌 Test Database"):
                try:
                    query = "SELECT 1 as test, NOW() as current_time"
                    result = query_postgres(query)
                    if result is not None and not result.empty:
                        st.success("✅ Database connection successful!")
                        st.write(f"Current database time: {result.iloc[0]['current_time']}")
                    else:
                        st.error("❌ Database connection failed")
                except Exception as e:
                    st.error(f"❌ Database connection failed: {str(e)}")

        with col2:
            if st.button("🔌 Test Orchestra API"):
                try:
                    token = get_orchestra_token()
                    if token:
                        st.success("✅ Orchestra token retrieved successfully!")
                        st.write(f"Token length: {len(token)} characters")
                    else:
                        st.error("❌ Failed to get Orchestra token")
                except Exception as e:
                    st.error(f"❌ Orchestra API test failed: {str(e)}")

        with col3:
            if st.button("🧹 Clear Cache"):
                st.cache_data.clear()
                if hasattr(st, 'cache_resource'):
                    st.cache_resource.clear()
                # Also clear the out of balance cache
                invalidate_out_of_balance_cache()
                st.success("✅ Cache cleared!")

        # System information
        st.subheader("System Information")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Package Availability:**")
            st.write(f"• PostgreSQL: {'✅ Available' if POSTGRES_AVAILABLE else '❌ Not Available'}")
            st.write(f"• Excel Export: {'✅ Available' if EXCEL_AVAILABLE else '❌ Not Available'}")
            st.write(f"• PDF Export: {'✅ Available' if PDF_AVAILABLE else '❌ Not Available'}")
            st.write(f"• Pandas Version: {pd.__version__}")

        with col2:
            st.write("**Configuration:**")
            st.write(f"• Database Timeout: {DB_TIMEOUT}s")
            st.write(f"• Cache TTL: {CACHE_TTL}s")
            st.write(f"• Max Retries: {MAX_RETRIES}")

        # Current filter state
        st.subheader("Current Filter State")
        filters = get_shared_filter_values()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"**Batch Type:** {filters['batch_type']}")
        with col2:
            st.write(f"**Proof:** {filters['is_proof']}")
        with col3:
            st.write(f"**Batch ID:** {filters['batch_id']}")
        with col4:
            st.write(f"**Account Code:** '{filters['accountcode_filter']}'")

        # Current Pipeline State
        st.subheader("Current Pipeline State")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"**Active Pipeline Type:** {st.session_state.get('pipeline_type', 'None')}")
        with col2:
            st.write(f"**Pipeline Run ID:** {st.session_state.get('pipeline_run_id', 'None')}")
        with col3:
            st.write(f"**Last Run Time:** {st.session_state.get('last_run_time', 'None')}")
        with col4:
            st.write(f"**Pending Refresh:** {st.session_state.get('pending_refresh', False)}")

    except Exception as e:
        logger.error(f"Error in render_debug_tab: {str(e)}")
        st.error("Error in debug tab. Please contact support.")
        st.exception(e)


# MAIN UI
def main():
    """Main application function with modern navigation"""
    try:

        # Render modern sidebar navigation
        render_modern_sidebar()

        # Update cached emoji values (less frequent updates for better performance)
        if 'tieout_emoji' not in st.session_state or st.session_state.get('tieout_emoji_timestamp',
                                                                          0) < time.time() - 300:
            tieout_emoji = get_tieout_status_emoji()
            st.session_state['tieout_emoji'] = tieout_emoji
            st.session_state['tieout_emoji_timestamp'] = time.time()

        if 'tieout_records_emoji' not in st.session_state or st.session_state.get('tieout_records_emoji_timestamp',
                                                                                  0) < time.time() - 300:
            tieout_records_emoji = get_tieout_records_status_emoji()
            st.session_state['tieout_records_emoji'] = tieout_records_emoji
            st.session_state['tieout_records_emoji_timestamp'] = time.time()

        # Update out of balance calculations
        current_batch_type = st.session_state.get('shared_batch_type', 'CASH')
        current_batch_id = st.session_state.get('shared_batch_id', 'All')
        current_is_proof = st.session_state.get('shared_is_proof', 'Y')
        current_filter_key = f"{current_batch_type}_{current_batch_id}_{current_is_proof}"

        if st.session_state.get('out_of_balance_filters') != current_filter_key:
            out_of_balance_total, out_of_balance_color = get_out_of_balance_total(
                current_batch_type, current_batch_id, current_is_proof
            )
            st.session_state['out_of_balance_total'] = out_of_balance_total
            st.session_state['out_of_balance_color'] = out_of_balance_color
            st.session_state['out_of_balance_filters'] = current_filter_key

        # Main content area - no more tab buttons, using sidebar navigation
        active_tab = st.session_state.get('active_tab_index', 0)

        # Route to the appropriate page based on sidebar selection
        # New mapping based on reorganized navigation:
        # 0=Dashboard, 1=Journal, 2=Details, 3=Balance, 4=Research, 5=Pipeline, 6=Tieout, 7=History, 8=Documentation, 9=Debug

        if active_tab == 0:  # Dashboard (new default)
            render_error_boundary(render_dashboard_overview_tab)
        elif active_tab == 1:  # Sales Journal
            render_error_boundary(render_sales_journal_tab)
        elif active_tab == 2:  # Detail by Ticket
            render_error_boundary(render_detail_by_ticket_tab)
        elif active_tab == 3:  # Out of Balance
            if current_is_proof == 'Y':
                render_error_boundary(render_out_of_balance_ar_tab)
            else:
                st.warning("⚖️ **Out of Balance Analysis Unavailable**")
                st.info(
                    "This feature is only available when **Proof** is set to **'Y'**. Please update the Data Filter in the sidebar.")
                st.markdown("---")
                st.markdown("### Why is this required?")
                st.markdown("- Out of balance calculations depend on proof journal entries")
                st.markdown("- Non-proof entries may contain preliminary or incomplete data")
                st.markdown("- Proof mode ensures data accuracy and consistency")
        elif active_tab == 4:  # 1140 Research
            render_error_boundary(render_1140_research_tab)
        elif active_tab == 5:  # Pipeline Control (moved after Research)
            render_error_boundary(render_pipeline_control_tab)
        elif active_tab == 6:  # Tieout Management
            render_error_boundary(render_consolidated_tieout_tab)
        elif active_tab == 7:  # Pipeline History
            render_error_boundary(render_pipeline_history_tab)
        elif active_tab == 8:  # Documentation
            render_error_boundary(render_documentation_tab)
        elif active_tab == 9:  # Debug
            render_error_boundary(render_debug_tab)
        else:
            st.error("Invalid page selected. Please use the sidebar navigation.")

        # Add custom CSS for better visual design
        st.markdown("""
        <style>
        /* Custom CSS for modern look */
        .main > div {
            padding-top: 1rem;
        }

        /* Enhance metric cards */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            padding: 1rem;
            border-radius: 10px;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Status indicators */
        .stSuccess {
            background-color: #d4edda;
            border-left: 4px solid #28a745;
            border-radius: 5px;
            padding: 0.5rem;
        }

        .stError {
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            border-radius: 5px;
            padding: 0.5rem;
        }

        .stWarning {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 5px;
            padding: 0.5rem;
        }

        /* Use default Streamlit dataframe styling */

        /* Better button styling */
        .stButton > button {
            border-radius: 20px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f8f9fa;
            border-right: 2px solid #e9ecef;
        }

        /* Header improvements */
        h1, h2, h3 {
            color: #2c3e50;
            font-weight: 600;
        }

        /* Container improvements */
        .block-container {
            padding-top: 2rem;
            max-width: 1200px;
        }
        </style>
        """, unsafe_allow_html=True)


    except ValueError as e:
        if "not in list" in str(e):
            logger.error(f"Filter value error in main application: {str(e)}")
            st.error("🔧 **Filter Configuration Issue**")
            st.warning("It looks like there's an unexpected filter value. This has been automatically corrected.")
            st.info("If this persists, please use the 'Refresh Data' button in the sidebar to reset all filters.")

            # Reset problematic filters to defaults
            st.session_state.shared_batch_type = 'CASH'
            st.session_state.shared_batch_id = 'All'
            st.session_state.shared_is_proof = 'Y'
            st.rerun()
        else:
            logger.error(f"ValueError in main application: {str(e)}")
            st.error("A configuration error occurred. Please refresh the page or contact support.")
            st.exception(e)
    except Exception as e:
        logger.error(f"Critical error in main application: {str(e)}")
        st.error("A critical error occurred. Please refresh the page or contact support.")

        # Add expandable error details for debugging
        with st.expander("🔍 Error Details (for troubleshooting)"):
            st.code(str(e))
            st.caption("Please share these details if contacting support")


if __name__ == "__main__":
    # Set page configuration for better layout (must be first)
    st.set_page_config(
        page_title="Sales Journal - APEX Upgrade Test",
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main()
