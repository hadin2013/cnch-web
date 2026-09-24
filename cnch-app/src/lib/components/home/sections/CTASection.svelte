<script>
	import { Button } from '$lib/components/ui/button';
	import { ArrowLeft, Calendar } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let visible = $state(false);

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						visible = true;
					}
				});
			},
			{ threshold: 0.3 }
		);

		const section = document.getElementById('cta');
		if (section) observer.observe(section);

		return () => observer.disconnect();
	});

	const reducedMotion =
		typeof window !== 'undefined'
			? window.matchMedia('(prefers-reduced-motion: reduce)').matches
			: false;
</script>

<section
	class="relative overflow-hidden bg-gradient-to-br from-[#0D47A1] via-[#1565C0] to-[#0D47A1] py-20 text-white md:py-28"
	id="cta"
>
	<!-- Animated Background -->
	{#if !reducedMotion}
		<div class="absolute inset-0 opacity-20">
			<div
				class="absolute h-96 w-96 -right-48 -top-48 rounded-full bg-white/10 blur-3xl"
				style="animation: float 8s ease-in-out infinite;"
			></div>
			<div
				class="absolute h-96 w-96 -left-48 -bottom-48 rounded-full bg-white/10 blur-3xl"
				style="animation: float 10s ease-in-out infinite reverse;"
			></div>
		</div>
	{/if}

	<div class="container relative z-10 mx-auto px-4 sm:px-6 lg:px-8">
		<div
			class="mx-auto max-w-3xl text-center transition-all duration-1000 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-8 opacity-0'}"
		>
			<!-- Icon -->
			<div class="mb-6 flex justify-center">
				<div
					class="rounded-full bg-white/10 p-4 backdrop-blur-sm {!reducedMotion
						? 'animate-bounce'
						: ''}"
				>
					<svg
						class="h-16 w-16 text-white"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M13 10V3L4 14h7v7l9-11h-7z"
						/>
					</svg>
				</div>
			</div>

			<!-- Heading -->
			<h2 class="mb-6 text-4xl font-bold leading-tight md:text-5xl lg:text-6xl">
				آماده‌اید برای شروع<br />
				<span class="bg-gradient-to-r from-blue-200 to-white bg-clip-text text-transparent">
					سفر علمی؟
				</span>
			</h2>

			<!-- Subtext -->
			<p class="mb-4 text-xl text-blue-100 md:text-2xl">
				به جمع هزاران دانش‌آموز علاقه‌مند به علوم شناختی بپیوندید
			</p>

			<!-- Deadline Notice -->
			<div
				class="mb-10 inline-flex items-center gap-2 rounded-full bg-white/10 px-6 py-3 backdrop-blur-sm"
			>
				<Calendar class="h-5 w-5 text-yellow-300" />
				<span class="font-semibold text-yellow-100">مهلت ثبت‌نام تا ۱۵ اسفند</span>
			</div>

			<!-- CTA Button -->
			<div class="flex flex-col items-center justify-center gap-4">
				<Button
					href="/register"
					size="lg"
					class="group h-14 w-full bg-white px-8 text-lg font-bold text-[#0D47A1] transition-all duration-300 hover:bg-blue-50 hover:shadow-2xl sm:w-auto {!reducedMotion
						? 'hover:scale-110 active:scale-95'
						: ''}"
				>
					<span>ثبت‌نام در مسابقه</span>
					<ArrowLeft
						class="mr-2 h-6 w-6 transition-transform {!reducedMotion
							? 'group-hover:-translate-x-2'
							: ''}"
					/>
				</Button>

				<p class="text-sm text-blue-200">
					✓ ثبت‌نام گروهی • ✓ آموزش کامل • ✓ راهنمایی منتور
				</p>
			</div>

			<!-- Trust Indicators -->
			<div
				class="mt-12 grid grid-cols-3 gap-8 border-t border-white/20 pt-12 transition-all duration-1000 delay-300 {visible
					? 'translate-y-0 opacity-100'
					: 'translate-y-8 opacity-0'}"
			>
				<div class="text-center">
					<div class="mb-2 text-3xl font-bold md:text-4xl">27</div>
					<div class="text-sm text-blue-200">دوره برگزاری</div>
				</div>
				<div class="text-center">
					<div class="mb-2 text-3xl font-bold md:text-4xl">4</div>
					<div class="text-sm text-blue-200">فاز آموزشی</div>
				</div>
				<div class="text-center">
					<div class="mb-2 text-3xl font-bold md:text-4xl">35</div>
					<div class="text-sm text-blue-200">هفته</div>
				</div>
			</div>
		</div>
	</div>
</section>

<style>
	@keyframes float {
		0%,
		100% {
			transform: translateY(0) translateX(0);
		}
		50% {
			transform: translateY(-20px) translateX(20px);
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
