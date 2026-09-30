import { fail, redirect } from '@sveltejs/kit';
import { getToken, clearAuthSession, setAuthSession } from '$lib/utils/auth';
import { 
    getProfile, 
    updateProfile, 
    changePassword, 
    createTicket, 
    getLearningContents, 
    getAssignments, 
    submitAssignmentFile 
} from '$lib/utils/api';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, url }) => {
    const token = getToken(cookies);
    if (!token) throw redirect(303, '/login');

    try {
        const [profile, contents, assignments] = await Promise.all([
            getProfile(token),
            getLearningContents(token).catch(() => []),
            getAssignments(token).catch(() => [])
        ]);

        return {
            profile,
            contents,
            assignments,
            welcome: url.searchParams.get('welcome') === '1'
        };
    } catch {
        clearAuthSession(cookies);
        throw redirect(303, '/login');
    }
};

const clean = (v: FormDataEntryValue | null) => String(v ?? '').trim();

export const actions: Actions = {
    updateProfile: async ({ request, cookies }) => {
        const token = getToken(cookies);
        if (!token) throw redirect(303, '/login');

        const fd = await request.formData();
        const data = {
            first_name: clean(fd.get('first_name')),
            last_name: clean(fd.get('last_name')),
            email: clean(fd.get('email')).toLowerCase(),
            phone_number: clean(fd.get('phone_number')),
            date_of_birth: clean(fd.get('date_of_birth')) || null,
            address: clean(fd.get('address'))
        };

        try {
            const user = await updateProfile(token, data);
            setAuthSession(cookies, token, {
                id: user.id,
                email: user.email,
                name: `${user.first_name} ${user.last_name}`.trim() || user.username,
                role: user.role
            });
            return { success: true, user };
        } catch (error) {
            const msg = error instanceof Error && error.message ? error.message : 'خطا در ذخیره‌سازی اطلاعات';
            return fail(400, { error: msg });
        }
    },

    changePassword: async ({ request, cookies }) => {
        const token = getToken(cookies);
        if (!token) throw redirect(303, '/login');

        const fd = await request.formData();
        const old_password = clean(fd.get('old_password'));
        const new_password = clean(fd.get('new_password'));

        if (!old_password || !new_password) return fail(400, { error: 'هر دو فیلد الزامی است.' });
        if (new_password.length < 6) return fail(400, { error: 'رمز عبور جدید باید دست‌کم ۶ کاراکتر باشد.' });

        try {
            await changePassword(token, { old_password, new_password });
            return { success: true };
        } catch (error) {
            const msg = error instanceof Error && error.message ? error.message : 'خطا در تغییر رمز عبور';
            return fail(400, { error: msg });
        }
    },

    createTicket: async ({ request, cookies }) => {
        const token = getToken(cookies);
        if (!token) throw redirect(303, '/login');

        const fd = await request.formData();
        const title = clean(fd.get('title'));
        const message = clean(fd.get('message'));
        if (!title || !message) return fail(400, { error: 'عنوان و متن پیام الزامی است.' });

        try {
            const ticket = await createTicket(token, { title, message });
            return { success: true, ticket };
        } catch (error) {
            const msg = error instanceof Error && error.message ? error.message : 'خطا در ارسال پیام';
            return fail(400, { error: msg });
        }
    },

    submitAssignment: async ({ request, cookies }) => {
        const token = getToken(cookies);
        if (!token) throw redirect(303, '/login');

        const fd = await request.formData();
        const assignmentId = String(fd.get('assignment_id'));
        const file = fd.get('file');

        if (!file || !(file instanceof File) || file.size === 0) {
            return fail(400, { error: 'لطفاً فایل پاسخ را انتخاب کنید.' });
        }

        try {
            const uploadData = new FormData();
            uploadData.append('file', file);
            uploadData.append('comment', String(fd.get('comment') || ''));
            await submitAssignmentFile(token, assignmentId, uploadData);
            return { success: true, assignmentSubmitted: true };
        } catch (err: any) {
            return fail(400, { error: err.message || 'خطا در ارسال تکلیف' });
        }
    },

    logout: async ({ cookies }) => {
        clearAuthSession(cookies);
        throw redirect(303, '/');
    }
};