import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0F0F0F",
        card: "#1A1A1A",
        f1red: "#E10600",
        compound: {
          soft: "#FF0000",
          medium: "#FFFF00",
          hard: "#FFFFFF",
          intermediate: "#00FF00",
          wet: "#00BFFF",
        },
      },
    },
  },
  plugins: [],
};
export default config;
