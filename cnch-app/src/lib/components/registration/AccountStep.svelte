<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button } from '$lib/components/ui/button';
	import * as Input from '$lib/components/ui/input';
	import * as Label from '$lib/components/ui/label';
	import * as Alert from '$lib/components/ui/alert';
	import {
		UserRound,
		Mail,
		Lock,
		Phone,
		CreditCard,
		ArrowLeft,
		AlertCircle,
		LogIn
	} from 'lucide-svelte';

	let { form, onNext, onBack } = $props();

	let email = $state('');
	let password = $state('');
	let first_name = $state('');
	let last_name = $state('');
	let phone_number = $state('');
	let national_id = $state('');
	let isSubmitting = $state(false);
	let clientError = $state<string | null>(null);
</script>

<div dir="rtl" class="w-full space-y-6">
	<div class="space-y-2">
		<h2 class="text-2xl font-bold text-gray-900">ایجاد حساب کاربری</h2>
		<p class="text-sm text-gray-600">
			برای ثبت‌نام در مسابقه ابتدا یک حساب کاربری بسازید تا بتوانید پس از آن به پروفایل و اطلاعات
			ثبت‌نام خود دسترسی داشته باشید.
		</p>
	</div>

	<form
		method="POST"
		action="?/createAccount"
		use:enhance={() => {
			isSubmitting = true;
			clientError = null;
			return async ({ result }) => {
				isSubmitting = false;
				if (result.type === 'success') {
					onNext?.();
				} else if (result.type === 'failure') {
					const err = result.data as { error?: string } | undefined;
					clientError = err?.error || 'خطا در ساخت حساب کاربری';
				} else {
					clientError = 'خطا در ساخت حساب کاربری';
				}
			};
		}}
		class="space-y-6"
	>
		<div class="grid gap-6 md:grid-cols-2">
			<div class="space-y-2">
				<Label.Root for="first_name">نام</Label.Root>
				<div class="relative">
					<UserRound class="absolute top-1/2 right-3 size-5 -translate-y-1/2 text-gray-400" />
					<Input.Root
						id="first_name"
						name="first_name"
						bind:value={first_name}
						placeholder="مثال: علی"
						class="pr-10"
					/>
				</div>
			</div>
			<div class="space-y-2">
				<Label.Root for="last_name">نام خانوادگی</Label.Root>
				<div class="relative">
					<UserRound class="absolute top-1/2 right-3 size-5 -translate-y-1/2 text-gray-400" />
					<Input.Root
						id="last_name"
						name="last_name"
						bind:value={last_name}
						placeholder="مثال: احمدی"
						class="pr-10"
					/>
				</div>
			</div>
		</div>

		<div class="grid gap-6 md:grid-cols-2">
			<div class="space-y-2">
				<Label.Root for="email">
					ایمیل <span class="text-red-500">*</span>
				</Label.Root>
				<div class="relative">
					<Mail class="absolute top-1/2 right-3 size-5 -translate-y-1/2 text-gray-400" />
					<Input.Root
						id="email"
						name="email"
						type="email"
						bind:value={email}
						placeholder="you@example.com"
						dir="ltr"
						class="pr-10 text-left"
						required
					/>
				</div>
			</div>
			<div class="space-y-2">
				<Label.Root for="password">
					رمز عبور <span class="text-red-500">*</span>
				</Label.Root>
				<div class="relative">
					<Lock class="absolute top-1/2 right-3 size-5 -translate-y-1/2 text-gray-400" />
					<Input.Root
						id="password"
						name="password"
						type="password"
						bind:value={password}
						placeholder="دست‌کم ۶ کاراکتر"
						dir="ltr"
						class="pr-10 text-left"
						required
						minlength="6"
					/>
				</div>
			</div>
		</div>

		<div class="grid gap-6 md:grid-cols-2">
			<div class="space-y-2">
				<Label.Root for="phone_number">شماره تلفن همراه</Label.Root>
				<div class="relative">
					<Phone class="absolute top-1/2 right-3 size-5 -translate-y-1/2 text-gray-400" />
					<Input.Root
						id="phone_number"
						name="phone_number"
						bind:value={phone_number}
						placeholder="09123456789"
						dir="ltr"
						class="pr-10 text-left"
					/>
				</div>
			</div>
			<div class="space-y-2">
				<Label.Root for="national_id">کد ملی (اختیاری — برای مسئول گروه)</Label.Root>
				<div class="relative">
					<CreditCard class="absolute top-1/2 right-3 size-5 -translate-y-1/2 text-gray-400" />
					<Input.Root
						id="national_id"
						name="national_id"
						bind:value={national_id}
						placeholder="۱۰ رقم"
						dir="ltr"
						class="pr-10 text-left"
						maxlength="10"
					/>
				</div>
			</div>
		</div>

		{#if clientError || form?.error}
			<Alert.Root class="border-red-200 bg-red-50 text-red-800">
				<AlertCircle class="size-4" />
				<Alert.Description class="text-sm">{clientError || form.error}</Alert.Description>
			</Alert.Root>
		{/if}

		<div class="flex flex-col-reverse gap-3 pt-4 md:flex-row md:justify-between">
			{#if onBack}
				<Button type="button" variant="outline" onclick={onBack}>بازگشت</Button>
			{/if}
			<p class="hidden self-center text-sm text-gray-500 md:block">
				اگر قبلاً حساب دارید، می‌توانید با <a
					href="/login"
					class="font-medium text-primary underline">ورود</a
				> از این مرحله رد شوید.
			</p>
			<Button type="submit" class="md:mr-auto" disabled={isSubmitting}>
				{#if isSubmitting}
					در حال ساخت حساب...
				{:else}
					مرحله بعد
					<ArrowLeft class="size-4" />
				{/if}
			</Button>
		</div>
	</form>
</div>
