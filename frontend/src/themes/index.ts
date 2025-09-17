// Theme selector keyed off the build-time customer flag.
const CUSTOMER = import.meta.env.VITE_CUSTOMER ?? "";

export async function loadTheme(): Promise<void> {
  if (CUSTOMER === "harborlight") {
    await import("./harborlight.css");
  }
}
