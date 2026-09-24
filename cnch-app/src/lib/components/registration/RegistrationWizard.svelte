<script lang="ts">
	import ProgressIndicator from './ProgressIndicator.svelte';
	import AccountStep from './AccountStep.svelte';
	import SchoolGroupForm from './SchoolGroupForm.svelte';
	import StudentForm from './StudentForm.svelte';
	import ConfirmationStep from './ConfirmationStep.svelte';
	import { goto } from '$app/navigation';
	import { untrack } from 'svelte';

	let { groupForm, studentForm, form = null, hasAccount = false } = $props();

	let accountReady = $state(untrack(() => hasAccount));
	let currentStep = $state(untrack(() => hasAccount) ? 2 : 1);
	let accountData = $state<any>(null);
	let groupData = $state<any>(null);
	let students = $state<any[]>([]);
	let isSuccess = $state(false);

	const stepLabels = ['مشخصات سرگروه', 'اطلاعات مدرسه', 'اطلاعات دانش‌آموزان', 'تأیید و ثبت'];
	const displayStep = $derived(currentStep);

	function handleAccountComplete(data: any) {
		accountData = data;
		accountReady = true;
		currentStep = 2;

		const leaderStudent = {
			first_name: data.first_name,
			last_name: data.last_name,
			national_id: data.national_id,
			phone_number: data.phone_number,
			grade: data.grade,
			major: data.major
		};

		if (students.length === 0) {
			students = [leaderStudent];
		} else {
			students[0] = leaderStudent;
		}
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
</script>

<div dir="rtl" class="mx-auto min-h-screen w-full max-w-4xl px-4 py-12">
	<div class="mb-8 text-center">
		<h1 class="mb-2 text-3xl font-bold text-gray-900 md:text-4xl">
			ثبت‌نام در مسابقه ملی علوم اعصاب شناختی
		</h1>
		<p class="text-gray-600">فرم ثبت‌نام گروهی دانش‌آموزان</p>
	</div>

	{#if !isSuccess}
		<ProgressIndicator currentStep={displayStep} steps={stepLabels} />
	{/if}

	<div class="mt-8 rounded-xl border border-gray-200 bg-white p-6 shadow-sm md:p-8">
		{#if currentStep === 1}
			<AccountStep initialData={accountData} onNext={handleAccountComplete} />
		{:else if currentStep === 2}
			<SchoolGroupForm
				data={groupForm}
				initialData={groupData}
				onNext={handleGroupFormComplete}
				onBack={() => { currentStep = 1; }}
			/>
		{:else if currentStep === 3}
			<StudentForm
				data={studentForm}
				bind:students
				onNext={handleNextToConfirmation}
				onBack={handleBackToGroup}
			/>
		{:else if currentStep === 4}
			<ConfirmationStep
				{accountData}
				{groupData}
				{students}
				onBack={handleBackToStudents}
				bind:isSuccess
			/>
		{/if}
	</div>
</div>
