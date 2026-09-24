<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import * as Alert from '$lib/components/ui/alert';
	import { Badge } from '$lib/components/ui/badge';
	import { Separator } from '$lib/components/ui/separator';
	import {
		CheckCircle2,
		Building2,
		MapPin,
		Phone,
		Users,
		User,
		CreditCard,
		GraduationCap,
		ArrowRight
	} from 'lucide-svelte';

	let { groupData, students, onBack, isSuccess = $bindable(false) } = $props();

	let isSubmitting = $state(false);
	let errorMessage = $state<string | null>(null);
</script>

<div dir="rtl" class="w-full space-y-6">
	{#if isSuccess}
		<!-- Success Message -->
		<Alert.Root class="border-green-500 bg-green-50">
			<CheckCircle2 class="size-5 text-green-600" />
			<Alert.Title class="text-green-900">ثبت‌نام با موفقیت انجام شد!</Alert.Title>
			<Alert.Description class="text-green-800">
				اطلاعات گروه و دانش‌آموزان شما با موفقیت ثبت گردید.
			</Alert.Description>
		</Alert.Root>

		<Card.Root>
			<Card.Content class="p-8 text-center">
				<div
					class="mx-auto mb-4 flex size-16 items-center justify-center rounded-full bg-green-100"
				>
					<CheckCircle2 class="size-8 text-green-600" />
				</div>
				<h3 class="mb-2 text-xl font-bold text-gray-900">ثبت‌نام کامل شد</h3>
				<p class="mb-6 text-gray-600">
					از شرکت شما در مسابقه دانش‌آموزی علوم اعصاب شناختی متشکریم. حال می‌توانید به پنل پروفایل
					خود بروید و اطلاعات گروه و دانش‌آموزان را ببینید.
				</p>
				<Button
					onclick={() => (window.location.href = '/profile?welcome=1')}
					size="lg"
					class="bg-green-600 hover:bg-green-700"
				>
					<ArrowRight class="size-5" />
					رفتن به پروفایل
				</Button>
			</Card.Content>
		</Card.Root>
	{:else}
		<div class="space-y-2">
			<h2 class="text-2xl font-bold text-gray-900">تأیید و ثبت نهایی</h2>
			<p class="text-sm text-gray-600">
				لطفاً اطلاعات وارد شده را بررسی کرده و در صورت صحت، ثبت نهایی را تأیید کنید.
			</p>
		</div>

		<!-- School Group Information -->
		<Card.Root>
			<Card.Header>
				<Card.Title class="flex items-center gap-2">
					<Building2 class="size-5" />
					اطلاعات گروه مدرسه
				</Card.Title>
			</Card.Header>
			<Card.Content class="space-y-4">
				<div class="grid gap-4 md:grid-cols-2">
					<div class="space-y-1">
						<p class="text-sm font-medium text-gray-500">نام گروه</p>
						<p class="font-semibold text-gray-900">{groupData.group_name}</p>
					</div>
					<div class="space-y-1">
						<p class="text-sm font-medium text-gray-500">نام مدرسه</p>
						<p class="font-semibold text-gray-900">{groupData.school_name}</p>
					</div>
					<div class="space-y-1">
						<p class="text-sm font-medium text-gray-500">استان</p>
						<div class="flex items-center gap-2">
							<MapPin class="size-4 text-gray-400" />
							<p class="text-gray-900">{groupData.province}</p>
						</div>
					</div>
					<div class="space-y-1">
						<p class="text-sm font-medium text-gray-500">شهر</p>
						<div class="flex items-center gap-2">
							<MapPin class="size-4 text-gray-400" />
							<p class="text-gray-900">{groupData.city}</p>
						</div>
					</div>
					<div class="space-y-1 md:col-span-2">
						<p class="text-sm font-medium text-gray-500">شماره تلفن مدرسه</p>
						<div class="flex items-center gap-2">
							<Phone class="size-4 text-gray-400" />
							<p class="text-gray-900" dir="ltr">{groupData.school_phone}</p>
						</div>
					</div>
				</div>
			</Card.Content>
		</Card.Root>

		<!-- Students Information -->
		<Card.Root>
			<Card.Header>
				<Card.Title class="flex items-center justify-between">
					<div class="flex items-center gap-2">
						<Users class="size-5" />
						دانش‌آموزان ثبت‌نام شده
					</div>
					<Badge variant="secondary">{students.length} نفر</Badge>
				</Card.Title>
			</Card.Header>
			<Card.Content class="space-y-3">
				{#each students as student, index}
					<div class="rounded-lg border bg-gray-50 p-4">
						<div class="mb-3 flex items-center justify-between">
							<div class="flex items-center gap-2">
								<div
									class="flex size-8 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground"
								>
									{index + 1}
								</div>
								<h4 class="font-semibold text-gray-900">
									{student.first_name}
									{student.last_name}
								</h4>
							</div>
							<div class="flex gap-2">
								<Badge variant="secondary">{student.grade}</Badge>
								<Badge variant="outline">{student.major}</Badge>
							</div>
						</div>
						<Separator class="my-3" />
						<div class="grid gap-3 md:grid-cols-2">
							<div class="flex items-center gap-2 text-sm">
								<CreditCard class="size-4 text-gray-400" />
								<span class="text-gray-500">کد ملی:</span>
								<span class="font-medium" dir="ltr">{student.national_id}</span>
							</div>
							<div class="flex items-center gap-2 text-sm">
								<Phone class="size-4 text-gray-400" />
								<span class="text-gray-500">موبایل:</span>
								<span class="font-medium" dir="ltr">{student.phone_number}</span>
							</div>
						</div>
					</div>
				{/each}
			</Card.Content>
		</Card.Root>

		<!-- Summary Alert -->
		<Alert.Root>
			<Alert.Title>خلاصه ثبت‌نام</Alert.Title>
			<Alert.Description>
				شما در حال ثبت‌نام گروه
				<strong>{groupData.group_name}</strong>
				با
				<strong>{students.length} دانش‌آموز</strong>
				هستید. با تأیید، اطلاعات شما ثبت نهایی می‌شود.
			</Alert.Description>
		</Alert.Root>

		<!-- Submit Form -->
		<form
			method="POST"
			action="?/submitRegistration"
			use:enhance={() => {
				isSubmitting = true;
				errorMessage = null;

				return async ({ result, update }) => {
					isSubmitting = false;

					if (result.type === 'success') {
						isSuccess = true;
						if (typeof window !== 'undefined') {
							localStorage.removeItem('registration_state');
						}
					} else if (result.type === 'failure') {
						errorMessage = (result.data as any)?.error || 'خطا در ثبت اطلاعات';
					}

					await update();
				};
			}}
		>
			<input type="hidden" name="data" value={JSON.stringify({ groupData, students })} />

			<div class="flex justify-between pt-4">
				<Button type="button" variant="outline" size="lg" onclick={onBack} disabled={isSubmitting}>
					بازگشت به مرحله قبل
				</Button>
				<Button
					type="submit"
					size="lg"
					disabled={isSubmitting}
					class="min-w-[200px] bg-green-600 hover:bg-green-700"
				>
					{#if isSubmitting}
						<span class="animate-pulse">در حال ثبت نهایی...</span>
					{:else}
						<CheckCircle2 class="ml-2 size-5" />
						تأیید و ثبت نهایی
					{/if}
				</Button>
			</div>

			{#if errorMessage}
				<!-- Error Message -->
				<div class="mt-4 rounded-lg border border-red-200 bg-red-50 p-4 dark:bg-red-950" dir="rtl">
					<div class="flex w-full items-start gap-4">
						<div class="flex size-10 shrink-0 items-center justify-center rounded-full bg-red-100">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="size-5 text-red-600"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
									clip-rule="evenodd"
								/>
							</svg>
						</div>
						<div class="min-w-0 flex-1 space-y-1">
							<h5 class="block text-base font-semibold text-red-900 dark:text-red-100">
								خطا در ثبت‌نام
							</h5>
							<p class="block text-sm text-red-800 dark:text-red-200">{errorMessage}</p>
						</div>
					</div>
				</div>
			{/if}
		</form>
	{/if}
</div>
