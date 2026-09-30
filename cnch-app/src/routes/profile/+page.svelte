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
		ShieldCheck,
		BookOpen,
		FileCheck,
		Download,
		Video as VideoIcon,
		UploadCloud,
		CheckCircle
	} from 'lucide-svelte';
	import type { ApiUser, ProfileData, LearningContentItem, AssignmentItem } from '$lib/utils/api';
	import { untrack } from 'svelte';

	let { data } = $props();
	let profile = $derived(data.profile as ProfileData);
	let contents = $derived((data.contents || []) as LearningContentItem[]);
	let assignments = $derived((data.assignments || []) as AssignmentItem[]);
	let user = $derived(profile.user);

	let activeTab = $state<'profile' | 'content' | 'assignments'>('profile');
	let selectedAssignmentId = $state<number | null>(null);
	let isSubmittingAssignment = $state(false);

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

<svelte:head><title>پنل کاربری - مسابقه ملی علوم اعصاب شناختی</title></svelte:head>

<div dir="rtl" class="min-h-screen bg-slate-50 py-10 font-sans">
	<div class="mx-auto w-full max-w-6xl space-y-6 px-4 sm:px-6">
		{#if data.welcome}
			<Alert.Root class="border-emerald-200 bg-emerald-50 text-emerald-900">
				<CheckCircle2 class="size-5 text-emerald-600" />
				<Alert.Title>ثبت‌نام شما کامل شد</Alert.Title>
				<Alert.Description>اطلاعات گروه و دانش‌آموزان در پروفایل شما ثبت شده است.</Alert.Description>
			</Alert.Root>
		{/if}

		<!-- هدر مشخصات کاربری -->
		<section class="overflow-hidden rounded-2xl bg-gradient-to-l from-[#0D47A1] to-blue-700 p-6 text-white shadow-lg md:p-8">
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
					<Badge variant={roleVariant} class="border-white/20 bg-white/15 px-3 py-1 text-white">
						<ShieldCheck class="size-3.5" /> {roleLabel}
					</Badge>
					{#if user.role === 'admin'}
						<Button href="/admin" class="bg-white text-[#0D47A1] hover:bg-blue-50">پنل مدیریت</Button>
					{/if}
				</div>
			</div>
		</section>

		<!-- نوار انتخاب تب‌ها -->
		<div class="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-2">
			<button
				onclick={() => activeTab = 'profile'}
				class="flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition-all {activeTab === 'profile' ? 'bg-blue-700 text-white shadow-sm' : 'bg-white text-slate-700 hover:bg-slate-100 border'}"
			>
				<UserRound class="size-4" />
				مشخصات و تیم من
			</button>

			<button
				onclick={() => activeTab = 'content'}
				class="flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition-all {activeTab === 'content' ? 'bg-blue-700 text-white shadow-sm' : 'bg-white text-slate-700 hover:bg-slate-100 border'}"
			>
				<BookOpen class="size-4" />
				محتوای آموزشی
				{#if contents.length > 0}
					<span class="rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-900">{contents.length}</span>
				{/if}
			</button>

			<button
				onclick={() => activeTab = 'assignments'}
				class="flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition-all {activeTab === 'assignments' ? 'bg-blue-700 text-white shadow-sm' : 'bg-white text-slate-700 hover:bg-slate-100 border'}"
			>
				<FileCheck class="size-4" />
				تکالیف و پروژه‌ها
				{#if assignments.length > 0}
					<span class="rounded-full bg-emerald-100 px-2 py-0.5 text-xs text-emerald-900">{assignments.length}</span>
				{/if}
			</button>
		</div>

		<!-- تب ۱: مشخصات و تیم -->
		{#if activeTab === 'profile'}
			<div class="grid gap-6 lg:grid-cols-[1.35fr_0.65fr]">
				<div class="space-y-6">
					<Card.Root>
						<Card.Header>
							<Card.Title class="flex items-center gap-2"><UserRound class="size-5" /> اطلاعات حساب</Card.Title>
							<Card.Description>اطلاعات تماس و مشخصات فردی خود را به‌روز نگه دارید.</Card.Description>
						</Card.Header>
						<Card.Content>
							<form method="POST" action="?/updateProfile" use:enhance={() => {
								isSaving = true;
								profileNotice = null;
								return async ({ result, update }) => {
									isSaving = false;
									profileNotice = result.type === 'success' 
										? { ok: true, text: 'اطلاعات حساب با موفقیت ذخیره شد.' } 
										: { ok: false, text: resultMessage(result, 'ذخیره اطلاعات انجام نشد.') };
									await update();
								};
							}} class="space-y-5">
								<div class="grid gap-4 sm:grid-cols-2">
									<div class="space-y-2">
										<Label.Root for="first_name">نام</Label.Root>
										<Input.Root id="first_name" name="first_name" bind:value={first_name} />
									</div>
									<div class="space-y-2">
										<Label.Root for="last_name">نام خانوادگی</Label.Root>
										<Input.Root id="last_name" name="last_name" bind:value={last_name} />
									</div>
									<div class="space-y-2">
										<Label.Root for="email">ایمیل</Label.Root>
										<Input.Root id="email" name="email" type="email" dir="ltr" class="text-left" bind:value={email} required />
									</div>
									<div class="space-y-2">
										<Label.Root for="phone_number">شماره همراه</Label.Root>
										<Input.Root id="phone_number" name="phone_number" dir="ltr" class="text-left" bind:value={phone_number} />
									</div>
									<div class="space-y-2">
										<Label.Root for="date_of_birth">تاریخ تولد</Label.Root>
										<Input.Root id="date_of_birth" name="date_of_birth" type="date" dir="ltr" bind:value={date_of_birth} />
									</div>
									<div class="space-y-2">
										<Label.Root for="national_id">کد ملی</Label.Root>
										<Input.Root id="national_id" value={user.national_id || 'ثبت نشده'} disabled dir="ltr" class="text-left" />
									</div>
								</div>
								<div class="space-y-2">
									<Label.Root for="address">نشانی</Label.Root>
									<textarea id="address" name="address" bind:value={address} rows="3" class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm outline-none focus-visible:ring-2"></textarea>
								</div>
								{#if profileNotice}
									<Alert.Root class={profileNotice.ok ? 'border-emerald-200 bg-emerald-50 text-emerald-800' : 'border-red-200 bg-red-50 text-red-800'}>
										<AlertCircle class="size-4" />
										<Alert.Description>{profileNotice.text}</Alert.Description>
									</Alert.Root>
								{/if}
								<Button type="submit" disabled={isSaving}>{isSaving ? 'در حال ذخیره...' : 'ذخیره تغییرات'}</Button>
							</form>
						</Card.Content>
					</Card.Root>

					<Card.Root>
						<Card.Header>
							<Card.Title class="flex items-center gap-2"><Building2 class="size-5" /> ثبت‌نام مسابقه</Card.Title>
						</Card.Header>
						<Card.Content>
							{#if profile.group}
								<div class="space-y-5">
									<div class="grid gap-3 rounded-xl bg-blue-50 p-4 sm:grid-cols-2">
										<div><p class="text-xs text-slate-500">نام گروه</p><p class="font-semibold">{profile.group.group_name}</p></div>
										<div><p class="text-xs text-slate-500">مدرسه</p><p class="font-semibold">{profile.group.school_name}</p></div>
										<div class="flex items-center gap-2 text-sm"><MapPin class="size-4 text-blue-600" />{profile.group.province}، {profile.group.city}</div>
										<div class="flex items-center gap-2 text-sm"><Phone class="size-4 text-blue-600" /><span dir="ltr">{profile.group.school_phone}</span></div>
									</div>
									<div class="space-y-3">
										<div class="flex items-center justify-between">
											<h3 class="font-semibold">دانش‌آموزان گروه</h3>
											<Badge variant="secondary">{profile.group.students.length} نفر</Badge>
										</div>
										{#each profile.group.students as student}
											<div class="flex flex-col gap-2 rounded-lg border p-3 sm:flex-row sm:items-center sm:justify-between">
												<div class="flex items-center gap-3">
													<div class="flex size-9 items-center justify-center rounded-full bg-slate-100"><GraduationCap class="size-4" /></div>
													<div><p class="font-medium">{student.first_name} {student.last_name}</p><p class="text-xs text-slate-500" dir="ltr">{student.national_id}</p></div>
												</div>
												<div class="flex gap-2"><Badge variant="outline">{student.grade}</Badge><Badge variant="secondary">{student.major}</Badge></div>
											</div>
										{/each}
									</div>
								</div>
							{:else if profile.student}
								<div class="rounded-xl border bg-slate-50 p-5">
									<p class="font-semibold">{profile.student.first_name} {profile.student.last_name}</p>
									<p class="mt-2 text-sm text-slate-600">پایه {profile.student.grade}، رشته {profile.student.major}</p>
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
					<Card.Root>
						<Card.Header><Card.Title class="flex items-center gap-2"><KeyRound class="size-5" /> تغییر رمز عبور</Card.Title></Card.Header>
						<Card.Content>
							<form method="POST" action="?/changePassword" use:enhance={() => {
								isChangingPassword = true;
								passwordNotice = null;
								return async ({ result, update }) => {
									isChangingPassword = false;
									passwordNotice = result.type === 'success' 
										? { ok: true, text: 'رمز عبور تغییر کرد.' } 
										: { ok: false, text: resultMessage(result, 'تغییر رمز عبور انجام نشد.') };
									if (result.type === 'success') { old_password = ''; new_password = ''; }
									await update();
								};
							}} class="space-y-4">
								<div class="space-y-2">
									<Label.Root for="old_password">رمز فعلی</Label.Root>
									<Input.Root id="old_password" name="old_password" type="password" bind:value={old_password} required />
								</div>
								<div class="space-y-2">
									<Label.Root for="new_password">رمز جدید</Label.Root>
									<Input.Root id="new_password" name="new_password" type="password" minlength="6" bind:value={new_password} required />
								</div>
								{#if passwordNotice}<p class={passwordNotice.ok ? 'text-sm text-emerald-700' : 'text-sm text-red-700'}>{passwordNotice.text}</p>{/if}
								<Button type="submit" variant="outline" class="w-full" disabled={isChangingPassword}>تغییر رمز عبور</Button>
							</form>
						</Card.Content>
					</Card.Root>

					<Card.Root>
						<Card.Header><Card.Title class="flex items-center gap-2"><Ticket class="size-5" /> پشتیبانی</Card.Title></Card.Header>
						<Card.Content class="space-y-5">
							<form method="POST" action="?/createTicket" use:enhance={() => {
								isSendingTicket = true;
								ticketNotice = null;
								return async ({ result, update }) => {
									isSendingTicket = false;
									ticketNotice = result.type === 'success' ? { ok: true, text: 'پیام شما ارسال شد.' } : { ok: false, text: resultMessage(result, 'ارسال پیام انجام نشد.') };
									if (result.type === 'success') { ticketTitle = ''; ticketMessage = ''; }
									await update();
								};
							}} class="space-y-3">
								<Input.Root name="title" placeholder="عنوان پیام" bind:value={ticketTitle} required />
								<textarea name="message" placeholder="شرح سؤال یا مشکل" bind:value={ticketMessage} rows="4" class="w-full rounded-md border p-2 text-sm" required></textarea>
								{#if ticketNotice}<p class={ticketNotice.ok ? 'text-sm text-emerald-700' : 'text-sm text-red-700'}>{ticketNotice.text}</p>{/if}
								<Button type="submit" class="w-full" disabled={isSendingTicket}><Send class="size-4 ml-1" /> ارسال به پشتیبانی</Button>
							</form>
						</Card.Content>
					</Card.Root>
				</aside>
			</div>
		{/if}

		<!-- تب ۲: محتوای آموزشی (CONT) -->
		{#if activeTab === 'content'}
			<div class="space-y-6">
				{#if contents.length === 0}
					<div class="rounded-2xl border bg-white p-12 text-center text-slate-500">
						<BookOpen class="mx-auto size-12 text-slate-300 mb-3" />
						<p>در حال حاضر محتوای آموزشی فعالی برای شما ثبت نشده است.</p>
					</div>
				{:else}
					<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
						{#each contents as item}
							<div class="flex flex-col justify-between overflow-hidden rounded-2xl border bg-white shadow-sm transition hover:shadow-md">
								<div class="p-5">
									<div class="flex items-center justify-between">
										<Badge variant="secondary" class="gap-1">
											{#if item.content_type === 'video'}<VideoIcon class="size-3" /> ویدیو{/if}
											{#if item.content_type === 'document'}<Download class="size-3" /> جزوه / فایل{/if}
											{#if item.content_type === 'link'}لینک{/if}
										</Badge>
										{#if item.is_public}
											<span class="text-[11px] text-slate-400">عمومی</span>
										{:else}
											<span class="text-[11px] text-blue-600 font-medium">اختصاصی گروه شما</span>
										{/if}
									</div>
									<h3 class="mt-3 font-bold text-slate-900">{item.title}</h3>
									<p class="mt-2 text-xs leading-relaxed text-slate-600">{item.description || 'بدون توضیح'}</p>
								</div>
								<div class="border-t bg-slate-50 p-4">
									{#if item.file_url}
										<a href={item.file_url} target="_blank" download class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-700">
											<Download class="size-3.5" /> دانلود فایل
										</a>
									{:else if item.video_url}
										<a href={item.video_url} target="_blank" class="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-emerald-600 px-4 py-2 text-xs font-semibold text-white hover:bg-emerald-700">
											<VideoIcon class="size-3.5" /> مشاهده ویدیو
										</a>
									{/if}
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{/if}

		<!-- تب ۳: تکالیف و پروژه‌ها (ASSG) -->
		{#if activeTab === 'assignments'}
			<div class="space-y-6">
				{#if assignments.length === 0}
					<div class="rounded-2xl border bg-white p-12 text-center text-slate-500">
						<FileCheck class="mx-auto size-12 text-slate-300 mb-3" />
						<p>در حال حاضر هیچ تکلیفی برای گروه شما تعریف نشده است.</p>
					</div>
				{:else}
					<div class="grid gap-6 md:grid-cols-3">
						<div class="space-y-3">
							{#each assignments as assg}
								<button
									type="button"
									onclick={() => selectedAssignmentId = assg.id}
									class="w-full text-right rounded-xl border p-4 transition-all {(selectedAssignmentId ?? assignments[0]?.id) === assg.id ? 'border-blue-600 bg-blue-50/50 shadow-xs' : 'bg-white hover:border-slate-300'}"
								>
									<div class="flex items-center justify-between">
										<span class="font-bold text-slate-800 text-sm">{assg.title}</span>
										{#if assg.my_submission}
											<Badge class="bg-emerald-100 text-emerald-700">ارسال شده</Badge>
										{:else}
											<Badge variant="outline" class="text-amber-600 border-amber-300">در انتظار پاسخ</Badge>
										{/if}
									</div>
									<p class="mt-2 text-xs text-slate-500">بارم: {assg.max_score} نمره</p>
								</button>
							{/each}
						</div>

						<div class="md:col-span-2">
							{#each assignments.filter(a => a.id === (selectedAssignmentId ?? assignments[0]?.id)) as currentAssg}
								<Card.Root>
									<Card.Header>
										<Card.Title>{currentAssg.title}</Card.Title>
										<Card.Description class="pt-2 text-slate-700 leading-relaxed whitespace-pre-wrap">{currentAssg.description}</Card.Description>
										{#if currentAssg.attachment_url}
											<div class="pt-2">
												<a href={currentAssg.attachment_url} target="_blank" class="inline-flex items-center gap-1.5 text-xs text-blue-600 hover:underline">
													<Download class="size-3.5" /> دانلود فایل ضمیمه تکلیف
												</a>
											</div>
										{/if}
									</Card.Header>
									<Card.Content class="space-y-6">
										{#if currentAssg.my_submission}
											<div class="rounded-xl border border-emerald-200 bg-emerald-50/60 p-4">
												<div class="flex items-center gap-2 font-semibold text-emerald-900">
													<CheckCircle class="size-4 text-emerald-600" />
													وضعیت: {currentAssg.my_submission.status === 'graded' ? 'تصحیح شده' : 'ارسال شده (در انتظار بررسی)'}
												</div>
												{#if currentAssg.my_submission.score !== null}
													<p class="mt-2 text-sm text-emerald-950 font-bold">نمره کسب‌شده: {currentAssg.my_submission.score} از {currentAssg.max_score}</p>
												{/if}
												{#if currentAssg.my_submission.feedback}
													<div class="mt-3 rounded-lg bg-white p-3 text-xs border border-emerald-100 text-slate-700">
														<p class="font-bold text-slate-900 mb-1">بازخورد استاد/منتور:</p>
														{currentAssg.my_submission.feedback}
													</div>
												{/if}
												<div class="mt-3">
													<a href={currentAssg.my_submission.submission_file_url} target="_blank" class="text-xs text-emerald-800 underline">مشاهده یا دانلود فایل ارسال‌شده شما</a>
												</div>
											</div>
										{/if}

										<form
											method="POST"
											action="?/submitAssignment"
											enctype="multipart/form-data"
											use:enhance={() => {
												isSubmittingAssignment = true;
												return async ({ update }) => {
													isSubmittingAssignment = false;
													await update();
												};
											}}
											class="space-y-4 border-t pt-4"
										>
											<input type="hidden" name="assignment_id" value={currentAssg.id} />
											<div class="space-y-2">
												<Label.Root for="file">انتخاب فایل پاسخ (PDF، ZIP، Docx تا ۵۰ مگابایت):</Label.Root>
												<Input.Root id="file" name="file" type="file" required class="bg-white" />
											</div>
											<div class="space-y-2">
												<Label.Root for="comment">توضیح اختیاری:</Label.Root>
												<textarea id="comment" name="comment" rows="2" class="w-full rounded-md border p-2 text-sm"></textarea>
											</div>
											<Button type="submit" disabled={isSubmittingAssignment} class="gap-2">
												<UploadCloud class="size-4" />
												{isSubmittingAssignment ? 'در حال ارسال...' : (currentAssg.my_submission ? 'ارسال مجدد پاسخ' : 'ثبت و ارسال پاسخ')}
											</Button>
										</form>
									</Card.Content>
								</Card.Root>
							{/each}
						</div>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>