<script lang="ts">
	import { enhance } from '$app/forms';
	import type { SubmitFunction } from '@sveltejs/kit';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import * as Input from '$lib/components/ui/input';
	import { Badge } from '$lib/components/ui/badge';
	import * as Alert from '$lib/components/ui/alert';
	import {
		Users,
		Building2,
		Ticket,
		Search,
		ShieldCheck,
		CheckCircle2,
		AlertCircle,
		MapPin,
		Phone
	} from 'lucide-svelte';
	import type { AdminGroupRow, AdminUserRow, Ticket as TicketType } from '$lib/utils/api';

	let { data } = $props();
	let activeTab = $state<'users' | 'groups' | 'tickets'>('users');
	let actionNotice = $state<{ ok: boolean; text: string } | null>(null);
	const users = $derived(data.users as AdminUserRow[]);
	const groups = $derived(data.groups as AdminGroupRow[]);
	const tickets = $derived(data.tickets as TicketType[]);
	const openTickets = $derived(tickets.filter((item) => !item.resolved).length);
	const tabs = [
		{ id: 'users' as const, label: 'کاربران', icon: Users },
		{ id: 'groups' as const, label: 'گروه‌ها', icon: Building2 },
		{ id: 'tickets' as const, label: 'تیکت‌ها', icon: Ticket }
	];
	function actionEnhance(successText: string): SubmitFunction {
		return () =>
			async ({ result, update }) => {
				const error =
					result.type === 'failure' && typeof result.data?.error === 'string'
						? result.data.error
						: 'انجام عملیات ممکن نشد.';
				actionNotice =
					result.type === 'success' ? { ok: true, text: successText } : { ok: false, text: error };
				await update();
			};
	}
</script>

<svelte:head><title>پنل مدیریت - مسابقه ملی علوم اعصاب شناختی</title></svelte:head>

<div dir="rtl" class="min-h-screen bg-slate-50 py-10">
	<div class="mx-auto w-full max-w-7xl space-y-6 px-4 sm:px-6">
		<div
			class="flex flex-col gap-4 rounded-2xl bg-[#0D47A1] p-6 text-white shadow-lg md:flex-row md:items-center md:justify-between md:p-8"
		>
			<div>
				<p class="flex items-center gap-2 text-sm text-blue-100">
					<ShieldCheck class="size-4" /> دسترسی مدیر
				</p>
				<h1 class="mt-2 text-3xl font-bold">پنل مدیریت مسابقه</h1>
				<p class="mt-2 text-sm text-blue-100">
					مدیریت کاربران، گروه‌های ثبت‌نامی و درخواست‌های پشتیبانی
				</p>
			</div>
			<div class="grid grid-cols-3 gap-3 text-center">
				<div class="rounded-xl bg-white/10 px-4 py-3">
					<p class="text-2xl font-bold">{users.length}</p>
					<p class="text-xs text-blue-100">کاربر</p>
				</div>
				<div class="rounded-xl bg-white/10 px-4 py-3">
					<p class="text-2xl font-bold">{groups.length}</p>
					<p class="text-xs text-blue-100">گروه</p>
				</div>
				<div class="rounded-xl bg-white/10 px-4 py-3">
					<p class="text-2xl font-bold">{openTickets}</p>
					<p class="text-xs text-blue-100">تیکت باز</p>
				</div>
			</div>
		</div>

		{#if data.loadError}<Alert.Root class="border-red-200 bg-red-50 text-red-800"
				><AlertCircle class="size-4" /><Alert.Description>{data.loadError}</Alert.Description
				></Alert.Root
			>{/if}
		{#if actionNotice}<Alert.Root
				class={actionNotice.ok
					? 'border-emerald-200 bg-emerald-50 text-emerald-800'
					: 'border-red-200 bg-red-50 text-red-800'}
				>{#if actionNotice.ok}<CheckCircle2 class="size-4" />{:else}<AlertCircle
						class="size-4"
					/>{/if}<Alert.Description>{actionNotice.text}</Alert.Description></Alert.Root
			>{/if}

		<Card.Root>
			<Card.Header class="gap-4">
				<div class="flex flex-wrap gap-2">
					{#each tabs as tab}<button
							type="button"
							onclick={() => (activeTab = tab.id)}
							class={activeTab === tab.id
								? 'inline-flex items-center gap-2 rounded-lg bg-[#0D47A1] px-4 py-2 text-sm font-medium text-white'
								: 'inline-flex items-center gap-2 rounded-lg bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200'}
							><tab.icon class="size-4" />{tab.label}</button
						>{/each}
				</div>
				<form method="GET" class="flex flex-col gap-2 sm:flex-row">
					<div class="relative flex-1">
						<Search
							class="absolute top-1/2 right-3 size-4 -translate-y-1/2 text-slate-400"
						/><Input.Root
							name="q"
							value={data.filters.q}
							placeholder="جست‌وجوی نام، ایمیل، مدرسه یا شهر"
							class="pr-9"
						/>
					</div>
					<select name="role" class="h-9 rounded-md border bg-white px-3 text-sm"
						><option value="">همه نقش‌ها</option><option
							value="normal"
							selected={data.filters.role === 'normal'}>کاربر عادی</option
						><option value="mentor" selected={data.filters.role === 'mentor'}>منتور</option><option
							value="admin"
							selected={data.filters.role === 'admin'}>مدیر</option
						></select
					>
					<Button type="submit">جست‌وجو</Button>
				</form>
			</Card.Header>
			<Card.Content>
				{#if activeTab === 'users'}
					<div class="overflow-x-auto">
						<table class="w-full min-w-[760px] text-right text-sm">
							<thead
								><tr class="border-b text-slate-500"
									><th class="p-3">کاربر</th><th class="p-3">تماس</th><th class="p-3">کد ملی</th><th
										class="p-3">نوع</th
									><th class="p-3">نقش و عملیات</th></tr
								></thead
							><tbody
								>{#each users as item}<tr class="border-b last:border-0"
										><td class="p-3"
											><p class="font-medium">
												{`${item.first_name} ${item.last_name}`.trim() || item.username}
											</p>
											<p class="text-xs text-slate-500">#{item.id}</p></td
										><td class="p-3"
											><p dir="ltr" class="text-left">{item.email}</p>
											<p dir="ltr" class="text-left text-xs text-slate-500">
												{item.phone_number || '—'}
											</p></td
										><td class="p-3" dir="ltr">{item.national_id || '—'}</td><td class="p-3"
											>{#if item.is_student}<Badge variant="secondary">دانش‌آموز</Badge
												>{:else}<Badge variant="outline">مسئول / کاربر</Badge>{/if}</td
										><td class="p-3"
											><form
												method="POST"
												action="?/updateRole"
												use:enhance={actionEnhance('نقش کاربر به‌روزرسانی شد.')}
												class="flex items-center gap-2"
											>
												<input type="hidden" name="id" value={item.id} /><select
													name="role"
													class="h-9 rounded-md border bg-white px-2 text-sm"
													><option value="normal" selected={item.role === 'normal'}
														>کاربر عادی</option
													><option value="mentor" selected={item.role === 'mentor'}>منتور</option
													><option value="admin" selected={item.role === 'admin'}>مدیر</option
													></select
												><Button type="submit" size="sm" variant="outline">ذخیره</Button>
											</form></td
										></tr
									>{/each}</tbody
							>
						</table>
						{#if !users.length}<p class="py-12 text-center text-slate-500">
								کاربری با این فیلتر پیدا نشد.
							</p>{/if}
					</div>
				{:else if activeTab === 'groups'}
					<div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
						{#each groups as group}<div class="rounded-xl border p-4">
								<div class="flex items-start justify-between gap-3">
									<div>
										<h3 class="font-bold">{group.group_name}</h3>
										<p class="mt-1 text-sm text-slate-600">{group.school_name}</p>
									</div>
									<Badge variant="secondary">{group.student_count} دانش‌آموز</Badge>
								</div>
								<div class="mt-4 space-y-2 text-sm text-slate-600">
									<p class="flex items-center gap-2">
										<MapPin class="size-4" />{group.province}، {group.city}
									</p>
									<p class="flex items-center gap-2">
										<Phone class="size-4" /><span dir="ltr">{group.school_phone}</span>
									</p>
									<p>مسئول: {group.organizer_name || 'ثبت نشده'}</p>
								</div>
							</div>{/each}{#if !groups.length}<p
								class="py-12 text-center text-slate-500 md:col-span-2 xl:col-span-3"
							>
								گروهی پیدا نشد.
							</p>{/if}
					</div>
				{:else}
					<div class="space-y-4">
						{#each tickets as item}<div
								class={item.resolved
									? 'rounded-xl border bg-slate-50 p-4 opacity-75'
									: 'rounded-xl border border-amber-200 bg-amber-50/40 p-4'}
							>
								<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
									<div>
										<div class="flex items-center gap-2">
											<h3 class="font-semibold">{item.title}</h3>
											<Badge variant={item.resolved ? 'secondary' : 'outline'}
												>{item.resolved ? 'بسته' : 'باز'}</Badge
											>
										</div>
										<p class="mt-1 text-xs text-slate-500">{item.user_name}</p>
										<p class="mt-3 text-sm whitespace-pre-wrap text-slate-700">{item.message}</p>
									</div>
									<form
										method="POST"
										action="?/setTicketResolved"
										use:enhance={actionEnhance('وضعیت تیکت به‌روزرسانی شد.')}
									>
										<input type="hidden" name="id" value={item.id} /><input
											type="hidden"
											name="resolved"
											value={String(!item.resolved)}
										/><Button
											type="submit"
											size="sm"
											variant={item.resolved ? 'outline' : 'default'}
											>{item.resolved ? 'بازگشایی' : 'بستن تیکت'}</Button
										>
									</form>
								</div>
							</div>{/each}{#if !tickets.length}<p class="py-12 text-center text-slate-500">
								تیکتی ثبت نشده است.
							</p>{/if}
					</div>
				{/if}
			</Card.Content>
		</Card.Root>
	</div>
</div>
