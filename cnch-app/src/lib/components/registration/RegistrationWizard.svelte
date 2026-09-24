<script lang="ts">
	import ProgressIndicator from './ProgressIndicator.svelte';
	import AccountStep from './AccountStep.svelte';
	import SchoolGroupForm from './SchoolGroupForm.svelte';
	import StudentForm from './StudentForm.svelte';
	import ConfirmationStep from './ConfirmationStep.svelte';
	import type { RegistrationState } from '$lib/types/registration.types';
	import { goto } from '$app/navigation';
	import { onMount, untrack } from 'svelte';

	let { groupForm, studentForm, form = null, hasAccount = false } = $props();

	// Registration state management with Svelte 5 runes
	// steps: 1 = account (only if no account yet), 2 = school group, 3 = students, 4 = confirm
	let accountReady = $state(untrack(() => hasAccount));
	let currentStep = $state(untrack(() => hasAccount) ? 2 : 1);
	let groupData = $state<any>(null);
	let students = $state<any[]>([]);
	let isSuccess = $state(false);
	let storageReady = $state(false);

	const stepLabels = $derived(
		accountReady
			? ['اطلاعات مدرسه', 'اطلاعات دانش‌آموزان', 'تأیید و ثبت']
			: ['حساب کاربری', 'اطلاعات مدرسه', 'اطلاعات دانش‌آموزان', 'تأیید و ثبت']
	);
	const displayStep = $derived(accountReady ? currentStep - 1 : currentStep);

	function handleAccountComplete() {
		accountReady = true;
		currentStep = 2;
	}

	function handleGroupFormComplete(data: any) {
		groupData = data;
		currentStep = 3;
	}

	function handleNextToConfirmation() {
		if (students.length > 0) {
			currentStep = 4;
		}
	}

	function handleBackToStudents() {
		currentStep = 3;
	}

	function handleBackToGroup() {
		currentStep = 2;
	}

	function handleBackFromAccount() {
		goto('/');
	}

	// Auto-save to localStorage
	$effect(() => {
		if (storageReady && !isSuccess) {
			const state: RegistrationState = {
				currentStep,
				groupId: null,
				groupData,
				students
			};
			localStorage.setItem('registration_state', JSON.stringify(state));
		}
	});

	// Restore first, then enable auto-save so the initial render cannot overwrite saved data.
	onMount(() => {
		const saved = localStorage.getItem('registration_state');
		if (saved) {
			try {
				const state: RegistrationState = JSON.parse(saved);
				if (accountReady && state.currentStep && state.currentStep >= 2)
					currentStep = state.currentStep;
				if (state.groupData) groupData = state.groupData;
				if (state.students) students = state.students;
			} catch (error) {
				console.error('Failed to restore registration state:', error);
			}
		}
		storageReady = true;
	});
</script>

<div dir="rtl" class="mx-auto min-h-screen w-full max-w-4xl px-4 py-12">
	<!-- Header -->
	<div class="mb-8 text-center">
		<h1 class="mb-2 text-3xl font-bold text-gray-900 md:text-4xl">
			ثبت‌نام در مسابقه ملی علوم اعصاب شناختی
		</h1>
		<p class="text-gray-600">فرم ثبت‌نام گروهی دانش‌آموزان</p>
	</div>

	<!-- Progress Indicator -->
	{#if !isSuccess}
		<ProgressIndicator currentStep={displayStep} steps={stepLabels} />
	{/if}

	<!-- Step Content -->
	<div class="mt-8">
		{#if currentStep === 1 && !accountReady}
			<AccountStep {form} onBack={handleBackFromAccount} onNext={handleAccountComplete} />
		{:else if currentStep === 2}
			<SchoolGroupForm
				data={groupForm}
				initialData={groupData}
				onNext={handleGroupFormComplete}
				onBack={handleBackFromAccount}
			/>
		{:else if currentStep === 3}
			<StudentForm
				data={studentForm}
				bind:students
				onNext={handleNextToConfirmation}
				onBack={handleBackToGroup}
			/>
		{:else if currentStep === 4}
			<ConfirmationStep {groupData} {students} onBack={handleBackToStudents} bind:isSuccess />
		{/if}
	</div>
</div>
