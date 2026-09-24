import { superValidate, message } from 'sveltekit-superforms';
import { zod4 } from 'sveltekit-superforms/adapters';
import { fail } from '@sveltejs/kit';
import { schoolGroupSchema } from '$lib/schemas/schoolGroup.schema';
import { studentSchema } from '$lib/schemas/student.schema';
import { createSchoolGroup, createStudent, signup, login } from '$lib/utils/api';
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
	// Step 1: create the organizer's account and start the auth session
	createAccount: async ({ request, cookies }) => {
		const formData = await request.formData();
		const data = {
			email: String(formData.get('email') || '')
				.trim()
				.toLowerCase(),
			password: String(formData.get('password') || ''),
			first_name: String(formData.get('first_name') || '').trim(),
			last_name: String(formData.get('last_name') || '').trim(),
			phone_number: String(formData.get('phone_number') || '').trim(),
			national_id: String(formData.get('national_id') || '').trim()
		};

		if (!data.email || !data.password) {
			return fail(400, { error: 'ایمیل و رمز عبور الزامی است.' });
		}

		try {
			const user = await signup(data);
			const { access } = await login(data.email, data.password);
			setAuthSession(cookies, access, {
				id: user.id,
				email: user.email,
				name: `${user.first_name} ${user.last_name}`.trim() || user.email,
				role: 'normal'
			});
			return { success: true };
		} catch (error) {
			const errorMessage =
				error instanceof Error && error.message ? error.message : 'خطا در ساخت حساب کاربری';
			return fail(500, { error: errorMessage });
		}
	},

	// Final step: create group + students (authenticated → group is linked to the organizer)
	submitRegistration: async ({ request, cookies }) => {
		const formData = await request.formData();
		const data = JSON.parse(formData.get('data') as string);
		const token = getToken(cookies);

		try {
			// Create school group
			const groupResponse = await createSchoolGroup(data.groupData, token);
			const groupId = groupResponse.id;

			// Create all students
			const studentPromises = data.students.map((student: any) =>
				createStudent(
					{
						...student,
						school_group: groupId
					},
					token
				)
			);

			await Promise.all(studentPromises);

			return { success: true, groupId };
		} catch (error) {
			const errorMessage =
				error instanceof Error && error.message ? error.message : 'خطا در ثبت اطلاعات';
			return fail(500, { error: errorMessage });
		}
	}
};
