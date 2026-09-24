<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { zod4Client } from 'sveltekit-superforms/adapters';
	import { schoolGroupSchema } from '$lib/schemas/schoolGroup.schema';
	import { iranProvinces } from '$lib/types/registration.types';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Building2, MapPin, Phone } from 'lucide-svelte';
	import { untrack } from 'svelte';

	let { data, initialData, onNext, onBack } = $props();

	const { form, errors, enhance, validateForm } = untrack(() => superForm(data, {
		validators: zod4Client(schoolGroupSchema),
		resetForm: false,
		dataType: 'json'
	}));

	// Initialize with initialData if provided
	$effect(() => {
		if (initialData) {
			$form = { ...$form, ...initialData };
		}
	});

	let selectedProvince = $derived(iranProvinces.find((f) => f === $form.province) ?? 'استان را انتخاب کنید');

	async function handleNext() {
		const result = await validateForm({ update: true });
		if (result.valid) {
			onNext?.($form);
		}
	}
</script>

<div dir="rtl" class="w-full space-y-6">
	<div class="space-y-2">
		<h2 class="text-2xl font-bold text-gray-900">اطلاعات گروه مدرسه</h2>
		<p class="text-sm text-gray-600">
			لطفاً اطلاعات گروه و مدرسه خود را با دقت وارد کنید.
		</p>
	</div>

	<form method="POST" use:enhance class="space-y-6">
		<!-- Group Name -->
		<div class="space-y-2">
			<Label for="group_name" class="text-right">
				نام گروه <span class="text-red-500">*</span>
			</Label>
			<div class="relative">
				<Building2 class="absolute right-3 top-3 size-5 text-gray-400" />
				<Input
					id="group_name"
					name="group_name"
					bind:value={$form.group_name}
					placeholder="مثال: گروه نخبگان تهران"
					class="pr-10 text-right"
					aria-invalid={$errors.group_name ? 'true' : undefined}
				/>
			</div>
			{#if $errors.group_name}
				<p class="text-sm text-red-500">{$errors.group_name[0]}</p>
			{/if}
		</div>

		<!-- Province & City -->
		<div class="grid gap-6 md:grid-cols-2">
			<!-- Province -->
			<div class="space-y-2">
				<Label for="province" class="text-right">
					استان <span class="text-red-500">*</span>
				</Label>
				<Select.Root type="single" name="province" bind:value={$form.province}>
					<Select.Trigger class="w-full text-right" aria-invalid={$errors.province ? 'true' : undefined}>
						<MapPin class="ml-2 size-4" />
						{selectedProvince}
					</Select.Trigger>
					<Select.Portal>
						<Select.Content>
							<Select.Group>
								<Select.Label>استان ها</Select.Label>
								{#each iranProvinces as province}
									<Select.Item value={province}>{province}</Select.Item>
								{/each}
							</Select.Group>
						</Select.Content>
					</Select.Portal>
				</Select.Root>
				<input type="hidden" name="province" bind:value={$form.province} />
				{#if $errors.province}
					<p class="text-sm text-red-500">{$errors.province[0]}</p>
				{/if}
			</div>

			<!-- City -->
			<div class="space-y-2">
				<Label for="city" class="text-right">
					شهر <span class="text-red-500">*</span>
				</Label>
				<div class="relative">
					<MapPin class="absolute right-3 top-3 size-5 text-gray-400" />
					<Input
						id="city"
						name="city"
						bind:value={$form.city}
						placeholder="نام شهر"
						class="pr-10 text-right"
						aria-invalid={$errors.city ? 'true' : undefined}
					/>
				</div>
				{#if $errors.city}
					<p class="text-sm text-red-500">{$errors.city[0]}</p>
				{/if}
			</div>
		</div>

		<!-- School Name -->
		<div class="space-y-2">
			<Label for="school_name" class="text-right">
				نام مدرسه <span class="text-red-500">*</span>
			</Label>
			<div class="relative">
				<Building2 class="absolute right-3 top-3 size-5 text-gray-400" />
				<Input
					id="school_name"
					name="school_name"
					bind:value={$form.school_name}
					placeholder="مثال: دبیرستان نمونه فرزانگان"
					class="pr-10 text-right"
					aria-invalid={$errors.school_name ? 'true' : undefined}
				/>
			</div>
			{#if $errors.school_name}
				<p class="text-sm text-red-500">{$errors.school_name[0]}</p>
			{/if}
		</div>

		<!-- School Phone -->
		<div class="space-y-2">
			<Label for="school_phone" class="text-right">
				شماره تلفن مدرسه <span class="text-red-500">*</span>
			</Label>
			<div class="relative">
				<Phone class="absolute right-3 top-3 size-5 text-gray-400" />
				<Input
					id="school_phone"
					name="school_phone"
					bind:value={$form.school_phone}
					placeholder="02112345678"
					dir="ltr"
					class="pr-10 text-left"
					aria-invalid={$errors.school_phone ? 'true' : undefined}
				/>
			</div>
			{#if $errors.school_phone}
				<p class="text-sm text-red-500">{$errors.school_phone[0]}</p>
			{/if}
		</div>

		<!-- Actions -->
		<div class="flex justify-between gap-4 pt-4">
			{#if onBack}
				<Button type="button" variant="outline" onclick={onBack}>
					بازگشت
				</Button>
			{/if}
			<Button type="button" onclick={handleNext} class="mr-auto">
				مرحله بعد
			</Button>
		</div>
	</form>
</div>
