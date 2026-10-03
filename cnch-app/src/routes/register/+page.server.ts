import { superValidate } from 'sveltekit-superforms';
import { zod4 } from 'sveltekit-superforms/adapters';
import { fail } from '@sveltejs/kit';
import { schoolGroupSchema } from '$lib/schemas/schoolGroup.schema';
import { studentSchema } from '$lib/schemas/student.schema';
import { registerGroup } from '$lib/utils/api';
import { setAuthSession, getToken } from '$lib/utils/auth';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const groupForm = await superValidate(zod4(schoolGroupSchema as any));
	const studentForm = await superValidate(zod4(studentSchema as any));

	return {
		groupForm,
		studentForm
	};
};

export const actions: Actions = {
	submitRegistration: async ({ request, cookies }) => {
		const formData = await request.formData();
		const data = JSON.parse(formData.get('data') as string);
		const existingToken = getToken(cookies);

		try {
			const result = await registerGroup(data, existingToken);

			if (result.access && result.user) {
				setAuthSession(cookies, result.access, {
					id: result.user.id,
					email: result.user.email,
					name: `${result.user.first_name || ''} ${result.user.last_name || ''}`.trim() || result.user.username,
					role: result.user.role || 'normal'
				});
			}

			return { success: true, groupId: result.groupId };
		} catch (error) {
			const errorMessage =
				error instanceof Error && error.message ? error.message : 'خطا در ثبت نهایی اطلاعات';
			return fail(400, { error: errorMessage });
		}
	}
};
