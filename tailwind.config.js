/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./public/**/*.html",
    "./views/**/*.ejs"
  ],
  safelist: [
    'md:max-w-2xl',
    'md:max-w-4xl',
    'max-w-4xl',
    'md:w-[800px]'
  ],
  theme: {
    extend: {
      colors: {
        "background": "#ffffff",
        "on-primary-container": "#848484",
        "on-secondary-container": "#626267",
        "on-surface-variant": "#4c4546",
        "secondary-fixed": "#e3e2e7",
        "surface-tint": "#5e5e5e",
        "surface": "#ffffff",
        "inverse-on-surface": "#f3f0f2",
        "tertiary": "#000000",
        "surface-container-lowest": "#ffffff",
        "error": "#ba1a1a",
        "primary-fixed-dim": "#c6c6c6",
        "outline-variant": "#cfc4c5",
        "tertiary-container": "#1a1c1d",
        "on-primary": "#ffffff",
        "on-error": "#ffffff",
        "on-surface": "#1b1b1d",
        "on-secondary": "#ffffff",
        "on-background": "#1b1b1d",
        "primary-container": "#1b1b1b",
        "surface-bright": "#ffffff",
        "on-primary-fixed-variant": "#474747",
        "on-error-container": "#93000a",
        "surface-container-highest": "#e4e2e4",
        "surface-container-low": "#f6f3f5",
        "error-container": "#ffdad6",
        "on-primary-fixed": "#1b1b1b",
        "tertiary-fixed": "#e2e2e4",
        "inverse-surface": "#303032",
        "on-tertiary-fixed-variant": "#454749",
        "surface-container-high": "#eae7ea",
        "inverse-primary": "#c6c6c6",
        "on-secondary-fixed-variant": "#46464b",
        "on-tertiary": "#ffffff",
        "primary-fixed": "#e2e2e2",
        "secondary-fixed-dim": "#c7c6cb",
        "tertiary-fixed-dim": "#c6c6c8",
        "secondary": "#5e5e63",
        "outline": "#7e7576",
        "surface-container": "#f0edef",
        "primary": "#000000",
        "on-tertiary-fixed": "#1a1c1d",
        "surface-variant": "#e4e2e4",
        "secondary-container": "#e0dfe4",
        "surface-dim": "#dcd9dc",
        "on-tertiary-container": "#838486",
        "on-secondary-fixed": "#1a1b1f"
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      spacing: {
        "base": "8px",
        "margin-edge": "80px",
        "container-max": "1440px",
        "section-gap": "120px",
        "gutter": "32px"
      },
      fontFamily: {
        "inter": ["DM Sans", "sans-serif"],
        "sans": ["DM Sans", "sans-serif"],
        "display": ["DM Sans", "sans-serif"],
        "headline-md": ["DM Sans", "sans-serif"],
        "headline-lg": ["DM Sans", "sans-serif"],
        "display-xl": ["DM Sans", "sans-serif"],
        "body-lg": ["DM Sans", "sans-serif"],
        "body-md": ["DM Sans", "sans-serif"],
        "label-sm": ["DM Sans", "sans-serif"]
      },
      fontSize: {
        "headline-md": ["32px", { "lineHeight": "1.3", "letterSpacing": "0.01em", "fontWeight": "600" }],
        "headline-lg": ["48px", { "lineHeight": "1.2", "letterSpacing": "-0.01em", "fontWeight": "600" }],
        "display-xl": ["80px", { "lineHeight": "1.1", "letterSpacing": "-0.02em", "fontWeight": "700" }],
        "services-display-xl": ["clamp(2.5rem, 8vw, 5rem)", { "lineHeight": "1.1", "letterSpacing": "-0.02em", "fontWeight": "700" }],
        "detail-display-xl": ["clamp(2.5rem, 8vw, 8rem)", { "lineHeight": "1", "letterSpacing": "-0.04em", "fontWeight": "900" }],
        "body-lg": ["18px", { "lineHeight": "1.6", "letterSpacing": "0.01em", "fontWeight": "400" }],
        "body-md": ["16px", { "lineHeight": "1.6", "letterSpacing": "0.01em", "fontWeight": "400" }],
        "label-sm": ["12px", { "lineHeight": "1.2", "letterSpacing": "0.1em", "fontWeight": "600" }]
      }
    }
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/container-queries")
  ]
}
