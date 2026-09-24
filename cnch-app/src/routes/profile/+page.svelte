<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import * as Input from '$lib/components/ui/input';
	import * as Label from '$lib/components/ui/label';
	import { Badge } from '$lib/components/ui/badge';
	import * as Alert from '$lib/components/ui/alert';
	import * as Separator from '$lib/components/ui/separator';
	import {
		UserRound,
		Phone,
		Building2,
		MapPin,
		Users,
		CheckCircle2,
		AlertCircle,
		KeyRound,
		Calendar,
		GraduationCap,
		Ticket,
		Send,
		ShieldCheck
	} from 'lucide-svelte';
	import type { ApiUser, ProfileData } from '$lib/utils/api';
	import { untrack } from 'svelte';

	let { data } = $props();
	let profile = $derived(data.profile as ProfileData);
	let user = $derived(profile.user);
	const initialUser = untrack(() => data.profile.user as ApiUser);
	let first_name = $state(initialUser.first_name || '');
	let last_name = $state(initialUser.last_name || '');
	let email = $state(initialUser.email || '');
	let phone_number = $state(initialUser.phone_number || '');
	let date_of_birth = $state(
		initialUser.date_of_birth ? initialUser.date_of_birth.slice(0, 10) : ''
	);
	let address = $state(initialUser.address || '');
	let old_password = $state('');
	let new_password = $state('');
	let ticketTitle = $state('');
	let ticketMessage = $state('');
	let isSaving = $state(false);
	let isChangingPassword = $state(false);
	let isSendingTicket = $state(false);
	let profileNotice = $state<{ ok: boolean; text: string } | null>(null);
	let passwordNotice = $state<{ ok: boolean; text: string } | null>(null);
	let ticketNotice = $state<{ ok: boolean; text: string } | null>(null);

	const roleLabel = $derived(
		user.role === 'admin' ? 'مدیر' : user.role === 'mentor' ? 'منتور' : 'شرکت‌کننده'
	);
	const roleVariant = $derived(user.role === 'admin' ? 'default' : 'secondary');

	function resultMessage(
		result: { type: string; data?: Record<string, unknown> },
		fallback: string
	) {
		return typeof result.data?.error === 'string' ? result.data.error : fallback;
	}

	function formatDate(value: string) {
		return new Intl.DateTimeFormat('fa-IR', { dateStyle: 'medium' }).format(new Date(value));
	}
</script>

<svelte:head><title>پروفایل کاربری - مسابقه ملی علوم اعصاب شناختی</title></svelte:head>

<div dir="rtl" class="min-h-screen bg-slate-50 py-10">
	<div class="mx-auto w-full max-w-6xl space-y-6 px-4 sm:px-6">
		{#if data.welcome}
			<Alert.Root class="border-emerald-200 bg-emerald-50 text-emerald-900"
				><CheckCircle2 class="size-5 text-emerald-600" /><Alert.Title
					>ثبت‌نام شما کامل شد</Alert.Title
				><Alert.Description
					>اطلاعات گروه و دانش‌آموزان در پروفایل شما ثبت شده است.</Alert.Description
				></Alert.Root
			>
		{/if}

		<section
			class="overflow-hidden rounded-2xl bg-gradient-to-l from-[#0D47A1] to-blue-700 p-6 text-white shadow-lg md:p-8"
		>
			<div class="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
				<div class="flex items-center gap-4">
					<div class="flex size-16 shrink-0 items-center justify-center rounded-2xl bg-white/15">
						<UserRound class="size-8" />
					</div>
					<div>
						<p class="text-sm text-blue-100">پنل کاربری</p>
						<h1 class="mt-1 text-2xl font-bold md:text-3xl">
							{`${user.first_name} ${user.last_name}`.trim() || user.email}
						</h1>
						<p class="mt-1 text-sm text-blue-100" dir="ltr">{user.email}</p>
					</div>
				</div>
				<div class="flex flex-wrap gap-2">
					<Badge variant={roleVariant} class="border-white/20 bg-white/15 px-3 py-1 text-white"
						><ShieldCheck class="size-3.5" /> {roleLabel}</Badge
					>
					{#if user.role === 'admin'}<Button
							href="/admin"
							class="bg-white text-[#0D47A1] hover:bg-blue-50">پنل مدیریت</Button
						>{/if}
				</div>
			</div>
		</section>

		<div class="grid gap-6 lg:grid-cols-[1.35fr_0.65fr]">
			<div class="space-y-6">
				<Card.Root>
					<Card.Header
						><Card.Title class="flex items-center gap-2"
							><UserRound class="size-5" /> اطلاعات حساب</Card.Title
						><Card.Description>اطلاعات تماس و مشخصات فردی خود را به‌روز نگه دارید.</Card.Description
						></Card.Header
					>
					<Card.Content>
						<form
							method="POST"
							action="?/updateProfile"
							use:enhance={() => {
								isSaving = true;
								profileNotice = null;
								return async ({ result, update }) => {
									isSaving = false;
									profileNotice =
										result.type === 'success'
											? { ok: true, text: 'اطلاعات حساب با موفقیت ذخیره شد.' }
											: { ok: false, text: resultMessage(result, 'ذخیره اطلاعات انجام نشد.') };
									await update();
								};
							}}
							class="space-y-5"
						>
							<div class="grid gap-4 sm:grid-cols-2">
								<div class="space-y-2">
									<Label.Root for="first_name">نام</Label.Root><Input.Root
										id="first_name"
										name="first_name"
										bind:value={first_name}
									/>
								</div>
								<div class="space-y-2">
									<Label.Root for="last_name">نام خانوادگی</Label.Root><Input.Root
										id="last_name"
										name="last_name"
										bind:value={last_name}
									/>
								</div>
								<div class="space-y-2">
									<Label.Root for="email">ایمیل</Label.Root><Input.Root
										id="email"
										name="email"
										type="email"
										dir="ltr"
										class="text-left"
										bind:value={email}
										required
									/>
								</div>
								<div class="space-y-2">
									<Label.Root for="phone_number">شماره همراه</Label.Root><Input.Root
										id="phone_number"
										name="phone_number"
										dir="ltr"
										class="text-left"
										bind:value={phone_number}
									/>
								</div>
								<div class="space-y-2">
									<Label.Root for="date_of_birth">تاریخ تولد</Label.Root><Input.Root
										id="date_of_birth"
										name="date_of_birth"
										type="date"
										dir="ltr"
										bind:value={date_of_birth}
									/>
								</div>
								<div class="space-y-2">
									<Label.Root for="national_id">کد ملی</Label.Root><Input.Root
										id="national_id"
										value={user.national_id || 'ثبت نشده'}
										disabled
										dir="ltr"
										class="text-left"
									/>
								</div>
							</div>
							<div class="space-y-2">
								<Label.Root for="address">نشانی</Label.Root><textarea
									id="address"
									name="address"
									bind:value={address}
									rows="3"
									class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-xs outline-none focus-visible:ring-3 focus-visible:ring-ring/50"
								></textarea>
							</div>
							{#if profileNotice}<Alert.Root
									class={profileNotice.ok
										? 'border-emerald-200 bg-emerald-50 text-emerald-800'
										: 'border-red-200 bg-red-50 text-red-800'}
									><AlertCircle class="size-4" /><Alert.Description
										>{profileNotice.text}</Alert.Description
									></Alert.Root
								>{/if}
							<Button type="submit" disabled={isSaving}
								>{isSaving ? 'در حال ذخیره...' : 'ذخیره تغییرات'}</Button
							>
						</form>
					</Card.Content>
				</Card.Root>

				<Card.Root>
					<Card.Header
						><Card.Title class="flex items-center gap-2"
							><Building2 class="size-5" /> ثبت‌نام مسابقه</Card.Title
						></Card.Header
					>
					<Card.Content>
						{#if profile.group}
							<div class="space-y-5">
								<div class="grid gap-3 rounded-xl bg-blue-50 p-4 sm:grid-cols-2">
									<div>
										<p class="text-xs text-slate-500">نام گروه</p>
										<p class="font-semibold">{profile.group.group_name}</p>
									</div>
									<div>
										<p class="text-xs text-slate-500">مدرسه</p>
										<p class="font-semibold">{profile.group.school_name}</p>
									</div>
									<div class="flex items-center gap-2 text-sm">
										<MapPin class="size-4 text-blue-600" />
										{profile.group.province}، {profile.group.city}
									</div>
									<div class="flex items-center gap-2 text-sm">
										<Phone class="size-4 text-blue-600" /><span dir="ltr"
											>{profile.group.school_phone}</span
										>
									</div>
								</div>
								<div class="space-y-3">
									<div class="flex items-center justify-between">
										<h3 class="font-semibold">دانش‌آموزان گروه</h3>
										<Badge variant="secondary">{profile.group.students.length} نفر</Badge>
									</div>
									{#each profile.group.students as student}
										<div
											class="flex flex-col gap-2 rounded-lg border p-3 sm:flex-row sm:items-center sm:justify-between"
										>
											<div class="flex items-center gap-3">
												<div
													class="flex size-9 items-center justify-center rounded-full bg-slate-100"
												>
													<GraduationCap class="size-4" />
												</div>
												<div>
													<p class="font-medium">{student.first_name} {student.last_name}</p>
													<p class="text-xs text-slate-500" dir="ltr">{student.national_id}</p>
												</div>
											</div>
											<div class="flex gap-2">
												<Badge variant="outline">{student.grade}</Badge><Badge variant="secondary"
													>{student.major}</Badge
												>
											</div>
										</div>
									{/each}
								</div>
							</div>
						{:else if profile.student}
							<div class="rounded-xl border bg-slate-50 p-5">
								<p class="font-semibold">
									{profile.student.first_name}
									{profile.student.last_name}
								</p>
								<p class="mt-2 text-sm text-slate-600">
									پایه {profile.student.grade}، رشته {profile.student.major}
								</p>
							</div>
						{:else}
							<div class="py-8 text-center">
								<Users class="mx-auto size-10 text-slate-300" />
								<p class="mt-3 text-slate-600">هنوز گروهی برای این حساب ثبت نشده است.</p>
								<Button href="/register" class="mt-4">تکمیل ثبت‌نام مسابقه</Button>
							</div>
						{/if}
					</Card.Content>
				</Card.Root>
			</div>

			<aside class="space-y-6">
				<Card.Root
					><Card.Header
						><Card.Title class="flex items-center gap-2"
							><KeyRound class="size-5" /> تغییر رمز عبور</Card.Title
						></Card.Header
					><Card.Content>
						<form
							method="POST"
							action="?/changePassword"
							use:enhance={() => {
								isChangingPassword = true;
								passwordNotice = null;
								return async ({ result, update }) => {
									isChangingPassword = false;
									passwordNotice =
										result.type === 'success'
											? { ok: true, text: 'رمز عبور تغییر کرد.' }
											: { ok: false, text: resultMessage(result, 'تغییر رمز عبور انجام نشد.') };
									if (result.type === 'success') {
										old_password = '';
										new_password = '';
									}
									await update();
								};
							}}
							class="space-y-4"
						>
							<div class="space-y-2">
								<Label.Root for="old_password">رمز عبور فعلی</Label.Root><Input.Root
									id="old_password"
									name="old_password"
									type="password"
									bind:value={old_password}
									required
								/>
							</div>
							<div class="space-y-2">
								<Label.Root for="new_password">رمز عبور جدید</Label.Root><Input.Root
									id="new_password"
									name="new_password"
									type="password"
									minlength="6"
									bind:value={new_password}
									required
								/>
							</div>
							{#if passwordNotice}<p
									class={passwordNotice.ok ? 'text-sm text-emerald-700' : 'text-sm text-red-700'}
								>
									{passwordNotice.text}
								</p>{/if}<Button
								type="submit"
								variant="outline"
								class="w-full"
								disabled={isChangingPassword}
								>{isChangingPassword ? 'در حال تغییر...' : 'تغییر رمز عبور'}</Button
							>
						</form>
					</Card.Content></Card.Root
				>

				<Card.Root
					><Card.Header
						><Card.Title class="flex items-center gap-2"
							><Ticket class="size-5" /> پشتیبانی</Card.Title
						><Card.Description>سؤال یا مشکل خود را برای مدیران بفرستید.</Card.Description
						></Card.Header
					><Card.Content class="space-y-5">
						<form
							method="POST"
							action="?/createTicket"
							use:enhance={() => {
								isSendingTicket = true;
								ticketNotice = null;
								return async ({ result, update }) => {
									isSendingTicket = false;
									ticketNotice =
										result.type === 'success'
											? { ok: true, text: 'پیام شما ارسال شد.' }
											: { ok: false, text: resultMessage(result, 'ارسال پیام انجام نشد.') };
									if (result.type === 'success') {
										ticketTitle = '';
										ticketMessage = '';
									}
									await update();
								};
							}}
							class="space-y-3"
						>
							<Input.Root
								name="title"
								placeholder="عنوان پیام"
								bind:value={ticketTitle}
								required
							/><textarea
								name="message"
								placeholder="شرح سؤال یا مشکل"
								bind:value={ticketMessage}
								rows="4"
								required
								class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-xs outline-none focus-visible:ring-3 focus-visible:ring-ring/50"
							></textarea>
							{#if ticketNotice}<p
									class={ticketNotice.ok ? 'text-sm text-emerald-700' : 'text-sm text-red-700'}
								>
									{ticketNotice.text}
								</p>{/if}<Button type="submit" class="w-full" disabled={isSendingTicket}
								><Send class="size-4" />
								{isSendingTicket ? 'در حال ارسال...' : 'ارسال به پشتیبانی'}</Button
							>
						</form>
						{#if profile.tickets.length}<Separator.Root />
							<div class="space-y-3">
								<p class="text-sm font-semibold">پیام‌های قبلی</p>
								{#each profile.tickets as item}<div class="rounded-lg border p-3 text-sm">
										<div class="flex items-start justify-between gap-2">
											<p class="font-medium">{item.title}</p>
											<Badge variant={item.resolved ? 'secondary' : 'outline'}
												>{item.resolved ? 'پاسخ داده شده' : 'در انتظار'}</Badge
											>
										</div>
										<p class="mt-2 line-clamp-2 text-xs text-slate-600">{item.message}</p>
										<p class="mt-2 text-[11px] text-slate-400">
											<Calendar class="ml-1 inline size-3" />{formatDate(item.created_at)}
										</p>
									</div>{/each}
							</div>{/if}
					</Card.Content></Card.Root
				>
			</aside>
		</div>
	</div>
</div>
