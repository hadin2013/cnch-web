<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/logos/main.jpg';
	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import { navigating } from '$app/stores';

	let { children, data } = $props();

	const auth = $derived(data.auth);
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<html lang="fa" dir="rtl"></html>
</svelte:head>

{#if $navigating}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/20 backdrop-blur-sm">
		<div
			class="h-16 w-16 animate-spin rounded-full border-4 border-gray-300 border-t-primary"
		></div>
	</div>
{/if}

<div class="flex min-h-screen flex-col">
	<Header {auth} />
	<main class="flex-1">
		{@render children()}
	</main>
	<Footer />
</div>
