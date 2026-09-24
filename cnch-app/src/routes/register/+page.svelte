<script lang="ts">
	import RegistrationWizard from '$lib/components/registration/RegistrationWizard.svelte';

	let { data } = $props();
</script>

<svelte:head>
	<title>ثبت‌نام - مسابقه ملی علوم اعصاب شناختی</title>
	<meta
		name="description"
		content="فرم ثبت‌نام گروهی دانش‌آموزان در مسابقه ملی علوم اعصاب شناختی"
	/>
</svelte:head>

<RegistrationWizard {...data} hasAccount={!!(data as any).auth} />
