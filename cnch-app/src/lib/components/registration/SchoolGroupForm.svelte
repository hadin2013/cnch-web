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

	// Initialize with initialData without triggering infinite effect loops
	$effect(() => {
		if (initialData) {
			untrack(() => {
				$form = { ...$form, ...initialData };
			});
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
				<Building2 class="absolute right-3 top-3 h-4 w-4 text-gray-400" />
				<Input
					id="group_name"
					name="group_name"
					placeholder="مثال: دانشمندان جوان"
					bind:value={$form.group_name}
					class="pr-10 text-right"
				/>
			</div>
			{#if $errors.group_name}
				<p class="text-xs text-red-500">{$errors.group_name}</p>
			{/if}
		</div>

		<!-- Province & City -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
			<div class="space-y-2">
				<Label for="province" class="text-right">
					استان <span class="text-red-500">*</span>
				</Label>
				<Select.Root
					type="single"
					bind:value={$form.province}
				>
					<Select.Trigger class="w-full text-right">
						<span>{selectedProvince}</span>
					</Select.Trigger>
					<Select.Content class="max-h-60 overflow-y-auto">
						{#each iranProvinces as province}
							<Select.Item value={province} label={province} class="text-right">
								{province}
							</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>
				{#if $errors.province}
					<p class="text-xs text-red-500">{$errors.province}</p>
				{/if}
			</div>

			<div class="space-y-2">
				<Label for="city" class="text-right">
					شهر/شهرستان <span class="text-red-500">*</span>
				</Label>
				<div class="relative">
					<MapPin class="absolute right-3 top-3 h-4 w-4 text-gray-400" />
					<Input
						id="city"
						name="city"
						placeholder="مثال: تهران"
						bind:value={$form.city}
						class="pr-10 text-right"
					/>
				</div>
				{#if $errors.city}
					<p class="text-xs text-red-500">{$errors.city}</p>
				{/if}
			</div>
		</div>

		<!-- School Name -->
		<div class="space-y-2">
			<Label for="school_name" class="text-right">
				نام مدرسه <span class="text-red-500">*</span>
			</Label>
			<Input
				id="school_name"
				name="school_name"
				placeholder="مثال: دبیرستان شهید بهشتی"
				bind:value={$form.school_name}
				class="text-right"
			/>
			{#if $errors.school_name}
				<p class="text-xs text-red-500">{$errors.school_name}</p>
			{/if}
		</div>

		<!-- School Phone -->
		<div class="space-y-2">
			<Label for="school_phone" class="text-right">
				تلفن مدرسه <span class="text-red-500">*</span>
			</Label>
			<div class="relative">
				<Phone class="absolute right-3 top-3 h-4 w-4 text-gray-400" />
				<Input
					id="school_phone"
					name="school_phone"
					placeholder="مثال: 02112345678"
					bind:value={$form.school_phone}
					class="pr-10 text-right"
					dir="ltr"
				/>
			</div>
			{#if $errors.school_phone}
				<p class="text-xs text-red-500">{$errors.school_phone}</p>
			{/if}
		</div>

		<!-- Action Buttons -->
		<div class="flex items-center justify-between pt-4">
			<Button
				type="button"
				variant="outline"
				onclick={onBack}
			>
				مرحله قبل
			</Button>

			<Button
				type="button"
				onclick={handleNext}
			>
				مرحله بعد: اطلاعات دانش‌آموزان
			</Button>
		</div>
	</form>
</div>
