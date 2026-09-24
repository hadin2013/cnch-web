export interface RegistrationState {
	currentStep: number;
	groupId: number | null;
	groupData: {
		group_name: string;
		province: string;
		city: string;
		school_name: string;
		school_phone: string;
	} | null;
	students: Array<{
		id?: number;
		first_name: string;
		last_name: string;
		national_id: string;
		phone_number: string;
		grade: string;
		major: string;
	}>;
}

export const iranProvinces = [
	'آذربایجان شرقی',
	'آذربایجان غربی',
	'اردبیل',
	'اصفهان',
	'البرز',
	'ایلام',
	'بوشهر',
	'تهران',
	'چهارمحال و بختیاری',
	'خراسان جنوبی',
	'خراسان رضوی',
	'خراسان شمالی',
	'خوزستان',
	'زنجان',
	'سمنان',
	'سیستان و بلوچستان',
	'فارس',
	'قزوین',
	'قم',
	'کردستان',
	'کرمان',
	'کرمانشاه',
	'کهگیلویه و بویراحمد',
	'گلستان',
	'گیلان',
	'لرستان',
	'مازندران',
	'مرکزی',
	'هرمزگان',
	'همدان',
	'یزد'
];

export const grades = ['هفتم', 'هشتم', 'نهم', 'دهم', 'یازدهم'];
export const majors = ['ریاضی', 'تجربی', 'انسانی', 'متوسطه اول'];
