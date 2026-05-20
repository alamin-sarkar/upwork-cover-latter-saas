const ACCESS_COOKIE = "pc_access_token";
const REFRESH_COOKIE = "pc_refresh_token";

function readCookie(name: string): string | null {
  if (typeof document === "undefined") {
    return null;
  }

  const entry = document.cookie
    .split("; ")
    .find((item) => item.startsWith(`${name}=`));
  return entry ? decodeURIComponent(entry.split("=")[1] ?? "") : null;
}

function writeCookie(name: string, value: string, days = 14) {
  if (typeof document === "undefined") {
    return;
  }

  const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; path=/; expires=${expires}; SameSite=Lax`;
}

function clearCookie(name: string) {
  if (typeof document === "undefined") {
    return;
  }

  document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax`;
}

export function readSessionCookies() {
  return {
    accessToken: readCookie(ACCESS_COOKIE),
    refreshToken: readCookie(REFRESH_COOKIE),
  };
}

export function persistSessionCookies(accessToken: string, refreshToken: string) {
  writeCookie(ACCESS_COOKIE, accessToken);
  writeCookie(REFRESH_COOKIE, refreshToken);
}

export function clearSessionCookies() {
  clearCookie(ACCESS_COOKIE);
  clearCookie(REFRESH_COOKIE);
}

export const sessionCookieNames = {
  access: ACCESS_COOKIE,
  refresh: REFRESH_COOKIE,
};
