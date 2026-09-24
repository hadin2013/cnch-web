import { fail, redirect } from '@sveltejs/kit';
import { getAuthUser, getToken } from '$lib/utils/auth';
import {
	adminListGroups,
	adminListTickets,
	adminListUsers,
	adminSetTicketResolved,
	adminUpdateUser
} from '$lib/utils/api';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, url }) => {
	const token = getToken(cookies);
	const auth = getAuthUser(cookies);
	if (!token) throw redirect(303, '/login');
	if (auth?.role !== 'admin') throw redirect(303, '/profile');

	const q = url.searchParams.get('q')?.trim() || '';
	const role = url.searchParams.get('role')?.trim() || '';
	try {
		const [users, groups, tickets] = await Promise.all([
			adminListUsers(token, { q, role }),
			adminListGroups(token, q),
			adminListTickets(token)
		]);
		return { users, groups, tickets, filters: { q, role } };
	} catch (error) {
		return {
			users: [],
			groups: [],
			tickets: [],
			filters: { q, role },
			loadError: error instanceof Error ? error.message : 'دریافت اطلاعات مدیریت انجام نشد.'
		};
	}
};

export const actions: Actions = {
	updateRole: async ({ request, cookies }) => {
		const token = getToken(cookies);
		const auth = getAuthUser(cookies);
		if (!token) throw redirect(303, '/login');
		if (auth?.role !== 'admin') throw redirect(303, '/profile');

		const fd = await request.formData();
		const id = Number(fd.get('id'));
		const role = String(fd.get('role') || '');
		if (!Number.isInteger(id) || !['normal', 'mentor', 'admin'].includes(role)) {
			return fail(400, { error: 'اطلاعات کاربر نامعتبر است.' });
		}
		try {
			await adminUpdateUser(token, id, { role: role as 'normal' | 'mentor' | 'admin' });
			return { success: true };
		} catch (error) {
			return fail(400, { error: error instanceof Error ? error.message : 'تغییر نقش انجام نشد.' });
		}
	},

	setTicketResolved: async ({ request, cookies }) => {
		const token = getToken(cookies);
		const auth = getAuthUser(cookies);
		if (!token) throw redirect(303, '/login');
		if (auth?.role !== 'admin') throw redirect(303, '/profile');

		const fd = await request.formData();
		const id = Number(fd.get('id'));
		const resolved = String(fd.get('resolved')) === 'true';
		if (!Number.isInteger(id)) return fail(400, { error: 'شناسه تیکت نامعتبر است.' });
		try {
			await adminSetTicketResolved(token, id, resolved);
			return { success: true };
		} catch (error) {
			return fail(400, {
				error: error instanceof Error ? error.message : 'به‌روزرسانی تیکت انجام نشد.'
			});
		}
	}
};
