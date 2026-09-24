import { z } from 'zod';

export const studentSchema = z.object({
	first_name: z
		.string()
		.min(2, 'نام باید حداقل ۲ حرف باشد')
		.max(50, 'نام نباید بیشتر از ۵۰ حرف باشد'),

	last_name: z
		.string()
		.min(2, 'نام خانوادگی باید حداقل ۲ حرف باشد')
		.max(50, 'نام خانوادگی نباید بیشتر از ۵۰ حرف باشد'),

	national_id: z
		.string()
		.length(10, 'کد ملی باید ۱۰ رقم باشد')
		.regex(/^\d{10}$/, 'کد ملی فقط باید شامل اعداد باشد'),

	phone_number: z
		.string()
		.min(1, 'شماره موبایل الزامی است')
		.regex(/^09\d{9}$/, 'شماره موبایل باید ۱۱ رقم و با ۰۹ شروع شود'),

	grade: z.enum(['هفتم', 'هشتم', 'نهم', 'دهم', 'یازدهم'], {
		error: 'پایه تحصیلی را انتخاب کنید'
	}),

	major: z.enum(['ریاضی', 'تجربی', 'انسانی', 'متوسطه اول'], {
		error: 'رشته تحصیلی را انتخاب کنید'
	})
});

export type StudentSchema = typeof studentSchema;
export type Student = z.infer<typeof studentSchema>;
