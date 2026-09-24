<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import * as Input from '$lib/components/ui/input';
	import * as Label from '$lib/components/ui/label';
	import * as Alert from '$lib/components/ui/alert';
	import { Mail, Lock, LogIn, AlertCircle } from 'lucide-svelte';

	let { form } = $props();

	let isSubmitting = $state(false);
</script>

<svelte:head>
	<title>ورود - مسابقه ملی علوم اعصاب شناختی</title>
</svelte:head>

<div dir="rtl" class="mx-auto flex min-h-[70vh] w-full max-w-md items-center px-4 py-12">
	<Card.Root class="w-full">
		<Card.Header>
			<Card.Title class="text-xl">ورود به حساب کاربری</Card.Title>
			<Card.Description class="text-sm">
				برای دسترسی به پروفایل و اطلاعات ثبت‌نام خود وارد شوید.
			</Card.Description>
		</Card.Header>
		<Card.Content>
			<form
				method="POST"
				action="?/default"
				use:enhance={() => {
					isSubmitting = true;
					return async ({ update }) => {
						isSubmitting = false;
						await update();
					};
				}}
				class="space-y-4"
			>
				<div class="space-y-2">
					<Label.Root for="email">ایمیل</Label.Root>
					<div class="relative">
						<Mail class="absolute top-1/2 right-3 size-4 -translate-y-1/2 text-gray-400" />
						<Input.Root
							id="email"
							name="email"
							type="email"
							placeholder="you@example.com"
							dir="ltr"
							class="pr-10"
							required
						/>
					</div>
				</div>

				<div class="space-y-2">
					<Label.Root for="password">رمز عبور</Label.Root>
					<div class="relative">
						<Lock class="absolute top-1/2 right-3 size-4 -translate-y-1/2 text-gray-400" />
						<Input.Root
							id="password"
							name="password"
							type="password"
							placeholder="••••••••"
							dir="ltr"
							class="pr-10"
							required
						/>
					</div>
				</div>

				{#if form?.error}
					<Alert.Root class="border-red-200 bg-red-50 text-red-800">
						<AlertCircle class="size-4" />
						<Alert.Description class="text-sm">{form.error}</Alert.Description>
					</Alert.Root>
				{/if}

				<Button type="submit" class="w-full" disabled={isSubmitting}>
					{#if isSubmitting}
						در حال ورود...
					{:else}
						<LogIn class="size-4" />
						ورود
					{/if}
				</Button>

				<p class="text-center text-sm text-gray-600">
					حساب کاربری ندارید؟
					<a href="/register" class="font-medium text-primary underline underline-offset-4">
						ثبت‌نام برای مسابقه
					</a>
				</p>
			</form>
		</Card.Content>
	</Card.Root>
</div>
