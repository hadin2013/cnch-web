<script>
	import { Card, CardContent } from '$lib/components/ui/card';
	import { onMount } from 'svelte';
	import neurosAssocLogo from '$lib/assets/logos/neuroscience_association.png';
	import iumsLogo from '$lib/assets/logos/iums.png';
	import ipmLogo from '$lib/assets/logos/ipm.png';
	import utLogo from '$lib/assets/logos/ut.png';
	import sbmuLogo from '$lib/assets/logos/sbmu.png';

	let visible = $state(false);

	const partners = [
		{
			name: 'انجمن علوم اعصاب ایران',
			description: 'انجمن علمی تخصصی علوم اعصاب کشور',
			logo: neurosAssocLogo,
			altLogo: 'Neuroscience Association of Iran'
		},
		{
			name: 'دانشگاه علوم پزشکی ایران',
			description: 'دانشگاه علوم پزشکی و خدمات بهداشتی درمانی ایران',
			logo: iumsLogo,
			altLogo: 'Iran University of Medical Sciences'
		},
		{
			name: 'پژوهشگاه دانش‌های بنیادی',
			description: 'موسسه تحقیقات در علوم پایه (IPM)',
			logo: ipmLogo,
			altLogo: 'Institute for Research in Fundamental Sciences (IPM)'
		},
		{
			name: 'دانشگاه تهران',
			description: 'بزرگترین و معتبرترین دانشگاه ایران',
			logo: utLogo,
			altLogo: 'University of Tehran'
		},
		{
			name: 'دانشگاه علوم پزشکی شهید بهشتی',
			description: 'دانشگاه علوم پزشکی و خدمات بهداشتی درمانی شهید بهشتی',
			logo: sbmuLogo,
			altLogo: 'Shahid Beheshti University of Medical Sciences'
		}
	];

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) visible = true;
				});
			},
			{ threshold: 0.1 }
		);

		const section = document.getElementById('partners');
		if (section) observer.observe(section);

		return () => observer.disconnect();
	});
</script>

<section class="bg-gray-50 py-12 md:py-16" id="partners">
	<div class="container mx-auto px-4 sm:px-6 lg:px-8">
		<div class="mb-10 text-center">
			<h2 class="mb-3 text-2xl font-bold text-gray-900 md:text-3xl">همکاران و حامیان</h2>
			<div class="mx-auto h-1 w-16 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"></div>
		</div>

		<div class="flex flex-wrap justify-center gap-6">
			{#each partners as partner, i}
				<Card
					class="w-full max-w-xs transition-all duration-500 {visible
						? 'translate-y-0 opacity-100'
						: 'translate-y-6 opacity-0'}"
					style="transition-delay: {i * 100}ms"
				>
					<CardContent class="flex flex-col items-center gap-3 p-6 text-center">
						<div
							class="flex h-32 w-32 items-center justify-center rounded-full bg-gradient-to-br from-blue-100 to-purple-100 text-sm font-bold text-blue-700"
						>
							<img
								src={partner.logo}
								alt={partner.altLogo}
							/>
						</div>
						<p class="font-semibold text-gray-900">{partner.name}</p>
						<p class="text-sm text-gray-500">{partner.description}</p>
					</CardContent>
				</Card>
			{/each}
		</div>
	</div>
</section>
