<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Alert from '$lib/components/ui/alert';
	import * as Select from '$lib/components/ui/select/index.js';
	import { UserRound, Mail, Lock, Phone, CreditCard, ArrowLeft, AlertCircle, GraduationCap } from 'lucide-svelte';

	let { initialData = null, onNext } = $props();

	let email = $state(initialData?.email ?? '');
	let password = $state(initialData?.password ?? '');
	let first_name = $state(initialData?.first_name ?? '');
	let last_name = $state(initialData?.last_name ?? '');
	let phone_number = $state(initialData?.phone_number ?? '');
	let national_id = $state(initialData?.national_id ?? '');
	let grade = $state(initialData?.grade ?? '');
	let major = $state(initialData?.major ?? '');
	let clientError = $state<string | null>(null);

	const grades = ['هفتم', 'هشتم', 'نهم', 'دهم', 'یازدهم'];
	const majors = ['ریاضی', 'تجربی', 'انسانی', 'متوسطه اول'];

	function handleFormSubmit(e: Event) {
		e.preventDefault();
		clientError = null;

		if (!first_name.trim() || !last_name.trim()) {
			clientError = 'نام و نام خانوادگی سرگروه الزامی است.';
			return;
		}
		if (!national_id || national_id.length !== 10 || !/^\d{10}$/.test(national_id)) {
			clientError = 'کد ملی باید دقیقاً ۱۰ رقم باشد.';
			return;
		}
		if (!phone_number || !/^09\d{9}$/.test(phone_number)) {
			clientError = 'شماره موبایل باید ۱۱ رقم بوده و با ۰۹ شروع شود.';
			return;
		}
		if (!email.trim() || !email.includes('@')) {
			clientError = 'یک آدرس ایمیل معتبر وارد کنید.';
			return;
		}
		if (!password || password.length < 6) {
			clientError = 'رمز عبور باید حداقل ۶ کاراکتر باشد.';
			return;
		}
		if (!grade) {
			clientError = 'پایه تحصیلی سرگروه را انتخاب کنید.';
			return;
		}
		if (!major) {
			clientError = 'رشته تحصیلی سرگروه را انتخاب کنید.';
			return;
		}

		onNext?.({
			first_name: first_name.trim(),
			last_name: last_name.trim(),
			national_id: national_id.trim(),
			phone_number: phone_number.trim(),
			email: email.trim().toLowerCase(),
			password,
			grade,
			major
		});
	}
</script>

<div dir="rtl" class="w-full space-y-6">
	<div class="space-y-2">
		<h2 class="text-2xl font-bold text-gray-900">مشخصات سرگروه (ایجاد حساب)</h2>
		<p class="text-sm text-gray-600">
			سرگروه به عنوان سرپرست و اولین عضو دانش‌آموزی گروه مسابقه ثبت می‌شود.
		</p>
	</div>

	{#if clientError}
		<Alert.Root class="border-red-500 bg-red-50">
			<AlertCircle class="size-4 text-red-600" />
			<Alert.Description class="text-sm text-red-700">{clientError}</Alert.Description>
		</Alert.Root>
	{/if}

	<form onsubmit={handleFormSubmit} class="space-y-4">
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			<div class="space-y-2">
				<Label for="first_name">نام سرگروه *</Label>
				<div class="relative">
					<UserRound class="absolute right-3 top-3 h-4 w-4 text-gray-400" />
					<Input id="first_name" bind:value={first_name} placeholder="مثال: علی" class="pr-10" />
				</div>
			</div>
			<div class="space-y-2">
				<Label for="last_name">نام خانوادگی سرگروه *</Label>
				<Input id="last_name" bind:value={last_name} placeholder="مثال: محمدی" />
			</div>
		</div>

		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			<div class="space-y-2">
				<Label for="national_id">کد ملی سرگروه *</Label>
				<div class="relative">
					<CreditCard class="absolute right-3 top-3 h-4 w-4 text-gray-400" />
					<Input id="national_id" bind:value={national_id} maxlength={10} placeholder="۱۰ رقم" dir="ltr" class="pr-10" />
				</div>
			</div>
			<div class="space-y-2">
				<Label for="phone_number">شماره موبایل سرگروه *</Label>
				<div class="relative">
					<Phone class="absolute right-3 top-3 h-4 w-4 text-gray-400" />
					<Input id="phone_number" bind:value={phone_number} maxlength={11} placeholder="۰۹۱۲۳۴۵۶۷۸۹" dir="ltr" class="pr-10" />
				</div>
			</div>
		</div>

		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			<div class="space-y-2">
				<Label for="grade">پایه تحصیلی سرگروه *</Label>
				<Select.Root type="single" bind:value={grade}>
					<Select.Trigger class="w-full text-right">
						<span>{grade || 'پایه تحصیلی را انتخاب کنید'}</span>
					</Select.Trigger>
					<Select.Content>
						{#each grades as g}
							<Select.Item value={g} label={g}>{g}</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>
			</div>
			<div class="space-y-2">
				<Label for="major">رشته تحصیلی سرگروه *</Label>
				<Select.Root type="single" bind:value={major}>
					<Select.Trigger class="w-full text-right">
						<span>{major || 'رشته تحصیلی را انتخاب کنید'}</span>
					</Select.Trigger>
					<Select.Content>
						{#each majors as m}
							<Select.Item value={m} label={m}>{m}</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>
			</div>
		</div>

		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			<div class="space-y-2">
				<Label for="email">ایمیل ورود به سایت *</Label>
				<div class="relative">
					<Mail class="absolute right-3 top-3 h-4 w-4 text-gray-400" />
					<Input id="email" type="email" bind:value={email} placeholder="example@mail.com" dir="ltr" class="pr-10" />
				</div>
			</div>
			<div class="space-y-2">
				<Label for="password">رمز عبور حساب *</Label>
				<div class="relative">
					<Lock class="absolute right-3 top-3 h-4 w-4 text-gray-400" />
					<Input id="password" type="password" bind:value={password} placeholder="حداقل ۶ کاراکتر" dir="ltr" class="pr-10" />
				</div>
			</div>
		</div>

		<div class="flex justify-end pt-4">
			<Button type="submit">
				مرحله بعد: اطلاعات مدرسه
				<ArrowLeft class="mr-2 size-4" />
			</Button>
		</div>
	</form>
</div>
