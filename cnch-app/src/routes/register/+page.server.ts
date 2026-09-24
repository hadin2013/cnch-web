import { superValidate } from 'sveltekit-superforms';
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
	submitRegistration: async ({ request, cookies }) => {
		const formData = await request.formData();
		const data = JSON.parse(formData.get('data') as string);
		let token: string | null = null;

		try {
			// ۱. اگر اطلاعات اکانت در بسته ارسالی وجود دارد، مستقیماً حساب جدید ایجاد و لاگین می‌شود
			if (data.accountData) {
				const { grade, major, ...userPayload } = data.accountData;
				try {
					await signup(userPayload);
				} catch (signupErr: any) {
					console.log('Signup info:', signupErr?.message);
				}
				const { access } = await login(userPayload.email, userPayload.password);
				token = access;
				setAuthSession(cookies, access, {
					email: userPayload.email,
					name: `${userPayload.first_name} ${userPayload.last_name}`.trim() || userPayload.email,
					role: 'normal'
				});
			} else {
				token = getToken(cookies);
			}

			if (!token) {
				return fail(401, { error: 'شناسه دسترسی معتبر نیست. لطفاً مجدداً اقدام کنید.' });
			}

			// ۲. ایجاد گروه مدرسه
			const groupResponse = await createSchoolGroup(data.groupData, token);
			const groupId = groupResponse.id;

			// ۳. ایجاد اعضای دانش‌آموزی (سرگروه + بقیه اعضا)
			for (const student of data.students) {
				await createStudent(
					{
						...student,
						school_group: groupId
					},
					token
				);
			}

			return { success: true, groupId };
		} catch (error) {
			const errorMessage =
				error instanceof Error && error.message ? error.message : 'خطا در ثبت نهایی اطلاعات';
			return fail(500, { error: errorMessage });
		}
	}
};
