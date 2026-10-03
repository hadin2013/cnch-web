import { fail, redirect } from '@sveltejs/kit';
import { login, getProfile } from '$lib/utils/api';
import { setAuthSession } from '$lib/utils/auth';
import type { Actions } from './$types';

export const actions: Actions = {
    default: async ({ request, cookies }) => {
        const formData = await request.formData();
        const usernameInput = String(formData.get('username') || formData.get('email') || '').trim();
        const password = String(formData.get('password') || '');

        if (!usernameInput || !password) {
            return fail(400, { error: 'لطفاً کد ملی (یا ایمیل) و رمز عبور را وارد کنید.' });
        }

        try {
            const loginRes = await login(usernameInput, password);
            if (!loginRes || !loginRes.access) {
                return fail(401, { error: 'کد ملی یا رمز عبور اشتباه است.' });
            }
            const access = loginRes.access;
            const profile = await getProfile(access);
            const u = profile.user;

            setAuthSession(cookies, access, {
                id: u.id,
                email: u.email,
                name: `${u.first_name || ''} ${u.last_name || ''}`.trim() || u.username,
                role: u.role
            });

            throw redirect(303, '/profile');
        } catch (error) {
            if (error && typeof error === 'object' && 'status' in error) throw error;
            const message =
                error instanceof Error && error.message ? error.message : 'کد ملی یا رمز عبور نامعتبر است.';
            return fail(401, { error: message });
        }
    }
};
