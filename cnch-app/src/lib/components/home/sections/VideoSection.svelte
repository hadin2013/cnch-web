<script>
	import { Card } from '$lib/components/ui/card';
	import { onMount } from 'svelte';

	let visible = $state(false);

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) visible = true;
				});
			},
			{ threshold: 0.3 }
		);

		const section = document.getElementById('video');
		if (section) observer.observe(section);

		// Inject Aparat embed script into its target div
		const container = document.getElementById('36641990935');
		if (container) {
			const script = document.createElement('script');
			script.type = 'text/javascript';
			script.src =
				'https://www.aparat.com/embed/mmtneqq?data[rnddiv]=36641990935&data[responsive]=yes&muted=false&titleShow=true';
			container.appendChild(script);
		}

		return () => observer.disconnect();
	});
</script>

<section class="bg-white py-16 md:py-24" id="video">
	<div class="container mx-auto px-4 sm:px-6 lg:px-8">
		<div
			class="mx-auto max-w-4xl transition-all duration-1000 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-8 opacity-0'}"
		>
			<Card class="overflow-hidden transition-shadow duration-300 hover:shadow-2xl">
				<div class="relative aspect-video bg-gray-900">
					<div id="36641990935" class="h-full w-full"></div>
				</div>
			</Card>
		</div>
	</div>
</section>
