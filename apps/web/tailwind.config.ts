import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx,mdx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // PitchCraft "forest" theme — dark + Upwork green accent
        bg: {
          base: "#0b0f10",
          surface: "#10161a",
          elevated: "#152025",
        },
        ink: {
          primary: "#e6efe9",
          secondary: "#9aa8a3",
          muted: "#5f6e69",
        },
        accent: {
          DEFAULT: "#14a800",
          hover: "#1bb909",
          soft: "rgba(20, 168, 0, 0.12)",
        },
        border: {
          subtle: "#1f2a30",
          strong: "#2a3a42",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "ui-sans-serif", "system-ui"],
        mono: ["var(--font-mono)", "ui-monospace", "SFMono-Regular"],
      },
      borderRadius: {
        xl: "14px",
        "2xl": "18px",
      },
    },
  },
  plugins: [],
};

export default config;
