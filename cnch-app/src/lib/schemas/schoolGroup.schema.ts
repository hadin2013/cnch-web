import { z } from 'zod';

export const schoolGroupSchema = z.object({
	group_name: z
		.string()
		.min(2, 'نام گروه باید حداقل ۲ حرف باشد')
		.max(100, 'نام گروه نباید بیشتر از ۱۰۰ حرف باشد'),

	province: z
		.string()
		.min(2, 'استان را انتخاب کنید'),

	city: z
		.string()
		.min(2, 'شهر را انتخاب کنید'),

	school_name: z
		.string()
		.min(3, 'نام مدرسه باید حداقل ۳ حرف باشد')
		.max(200, 'نام مدرسه نباید بیشتر از ۲۰۰ حرف باشد'),

	school_phone: z
		.string()
		.min(1, 'شماره تلفن مدرسه الزامی است')
		.regex(/^0\d{10}$/, 'شماره تلفن باید ۱۱ رقم باشد و با ۰ شروع شود')
});

export type SchoolGroupSchema = typeof schoolGroupSchema;
export type SchoolGroup = z.infer<typeof schoolGroupSchema>;
