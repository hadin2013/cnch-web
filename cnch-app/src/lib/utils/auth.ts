import type { Cookies } from '@sveltejs/kit';
import { dev } from '$app/environment';

const TOKEN_COOKIE = 'cnch_token';
const USER_COOKIE = 'cnch_user';
// must stay >= backend ACCESS_TOKEN_LIFETIME (1h)
const MAX_AGE = 60 * 60;

export interface AuthUser {
	id: number;
	email: string;
	name: string;
	role: string;
}

export function getToken(cookies: Cookies): string | null {
	return cookies.get(TOKEN_COOKIE) ?? null;
}

export function getAuthUser(cookies: Cookies): AuthUser | null {
	const raw = cookies.get(USER_COOKIE);
	if (!raw) return null;
	try {
		return JSON.parse(raw) as AuthUser;
	} catch {
		return null;
	}
}

function cookieOptions() {
	return { path: '/', httpOnly: true, sameSite: 'lax' as const, secure: !dev, maxAge: MAX_AGE };
}

export function setAuthSession(cookies: Cookies, accessToken: string, user: AuthUser): void {
	cookies.set(TOKEN_COOKIE, accessToken, cookieOptions());
	cookies.set(USER_COOKIE, JSON.stringify(user), cookieOptions());
}

export function clearAuthSession(cookies: Cookies): void {
	cookies.delete(TOKEN_COOKIE, { path: '/' });
	cookies.delete(USER_COOKIE, { path: '/' });
}
