import { fail, redirect } from '@sveltejs/kit';
import { login, getProfile } from '$lib/utils/api';
import { setAuthSession } from '$lib/utils/auth';
import type { Actions } from './$types';

export const actions: Actions = {
	default: async ({ request, cookies }) => {
		const formData = await request.formData();
		const email = String(formData.get('email') || '')
			.trim()
			.toLowerCase();
		const password = String(formData.get('password') || '');

		if (!email || !password) {
			return fail(400, { error: 'لطفاً ایمیل و رمز عبور را وارد کنید.' });
		}

		try {
			const { access } = await login(email, password);
			const profile = await getProfile(access);
			const u = profile.user;

			setAuthSession(cookies, access, {
				id: u.id,
				email: u.email,
				name: `${u.first_name} ${u.last_name}`.trim() || u.username,
				role: u.role
			});

			throw redirect(303, '/profile');
		} catch (error) {
			if (error && typeof error === 'object' && 'status' in error) throw error;
			const message =
				error instanceof Error && error.message ? error.message : 'خطا در ارتباط با سرور';
			return fail(401, { error: message });
		}
	}
};
