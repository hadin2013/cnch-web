<script lang="ts">
	import HeroSection from '$lib/components/home/sections/HeroSection.svelte';
	import AboutSection from '$lib/components/home/sections/AboutSection.svelte';
	import PartnersSection from '$lib/components/home/sections/PartnersSection.svelte';
	import VideoSection from '$lib/components/home/sections/VideoSection.svelte';
	import TimelineSection from '$lib/components/home/sections/TimelineSection.svelte';
	import PrizesSection from '$lib/components/home/sections/PrizesSection.svelte';
	import InfographicSection from '$lib/components/home/sections/InfographicSection.svelte';
	import FAQSection from '$lib/components/home/sections/FAQSection.svelte';
	import ContactSection from '$lib/components/home/sections/ContactSection.svelte';
	import CTASection from '$lib/components/home/sections/CTASection.svelte';
	import ProfessorsSection from '$lib/components/home/sections/ProfessorsSection.svelte';
	import { ArrowUp } from 'lucide-svelte';
	import mainLogo from '$lib/assets/logos/main.jpg';

	let showScrollTop = $state(false);

	$effect(() => {
		if (typeof window !== 'undefined') {
			const handleScroll = () => {
				showScrollTop = window.scrollY > 400;
			};

			window.addEventListener('scroll', handleScroll);
			return () => window.removeEventListener('scroll', handleScroll);
		}
	});

	function scrollToTop() {
		window.scrollTo({
			top: 0,
			behavior: 'smooth'
		});
	}

	const reducedMotion =
		typeof window !== 'undefined'
			? window.matchMedia('(prefers-reduced-motion: reduce)').matches
			: false;
</script>

<svelte:head>
	<title>مسابقات ملی علوم اعصاب شناختی - دوره ۲۷ | CNCH</title>
	<meta
		name="description"
		content="بیست و هفتمین دوره ملی علوم اعصاب شناختی. مسابقه پژوهشی-آموزشی ویژه دانش‌آموزان هفتم تا یازدهم با آموزش و راهنمایی منتورها. ثبت‌نام تا اسفند ۱۵."
	/>
	<meta
		name="keywords"
		content="علوم اعصاب شناختی, NeuroAI, مسابقه علمی, دانش آموزان, سمپاد, CNCH, علوم شناختی, مسابقه ملی"
	/>

	<!-- Open Graph / Facebook -->
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://www.CNCH.ir/" />
	<meta property="og:title" content="مسابقات ملی علوم اعصاب شناختی - دوره ۲۷" />
	<meta
		property="og:description"
		content="مسابقه پژوهشی-آموزشی ویژه دانش‌آموزان هشتم تا یازدهم. آموزش ، راهنمایی منتور و جوایز ویژه."
	/>
	<meta property="og:image" content={mainLogo} />
	<meta property="og:locale" content="fa_IR" />

	<!-- Twitter -->
	<meta property="twitter:card" content="summary_large_image" />
	<meta property="twitter:url" content="https://www.CNCH.ir/" />
	<meta property="twitter:title" content="مسابقات ملی علوم اعصاب شناختی - دوره ۲۷" />
	<meta
		property="twitter:description"
		content="مسابقه پژوهشی-آموزشی ویژه دانش‌آموزان هشتم تا یازدهم. آموزش ، راهنمایی منتور و جوایز ویژه."
	/>
	<meta property="twitter:image" content={mainLogo} />

	<!-- Canonical -->
	<link rel="canonical" href="https://www.CNCH.ir/" />
</svelte:head>

<!-- Homepage Sections -->
<HeroSection />
<AboutSection />
<PartnersSection />
<ProfessorsSection />
<VideoSection />
<TimelineSection />
<InfographicSection />
<PrizesSection />
<FAQSection />
<ContactSection />
<CTASection />

<!-- Scroll to Top Button -->
{#if showScrollTop}
	<button
		onclick={scrollToTop}
		class="fixed bottom-8 left-8 z-40 flex h-12 w-12 items-center justify-center rounded-full bg-[#0D47A1] text-white shadow-lg transition-all duration-300 {!reducedMotion
			? 'hover:scale-110 hover:shadow-2xl active:scale-95'
			: ''}"
		aria-label="بازگشت به بالا"
		style="animation: {!reducedMotion ? 'fadeInUp 0.3s ease-out' : 'none'};"
	>
		<ArrowUp class="h-6 w-6" />
	</button>
{/if}

<style>
	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		* {
			animation-duration: 0.01ms !important;
			animation-iteration-count: 1 !important;
			transition-duration: 0.01ms !important;
		}
	}
</style>
