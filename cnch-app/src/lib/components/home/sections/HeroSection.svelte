<script>
	import { Button } from '$lib/components/ui/button';
	import { Calendar, Download } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import guidelinesPdf from '$lib/assets/cnch guidlines.pdf';

	// Countdown to registration deadline: ۱۵ اسفند (March 06, 2026)
	const deadline = new Date('2026-03-06T23:59:59');

	let timeLeft = $state({
		days: 0,
		hours: 0,
		minutes: 0,
		seconds: 0
	});

	let visible = $state(false);

	function updateCountdown() {
		const now = new Date();
		const difference = deadline.getTime() - now.getTime();

		if (difference > 0) {
			timeLeft = {
				days: Math.floor(difference / (1000 * 60 * 60 * 24)),
				hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
				minutes: Math.floor((difference / 1000 / 60) % 60),
				seconds: Math.floor((difference / 1000) % 60)
			};
		} else {
			timeLeft = { days: 0, hours: 0, minutes: 0, seconds: 0 };
		}
	}

	onMount(() => {
		visible = true;
		updateCountdown();
		const interval = setInterval(updateCountdown, 1000);
		return () => clearInterval(interval);
	});

	const reducedMotion =
		typeof window !== 'undefined'
			? window.matchMedia('(prefers-reduced-motion: reduce)').matches
			: false;
</script>

<section
	class="relative overflow-hidden bg-gradient-to-br from-[#0D47A1] via-[#1565C0] to-[#0D47A1] py-20 text-white md:py-32"
	id="hero"
>
	<!-- Animated background particles (disabled for reduced motion) -->
	{#if !reducedMotion}
		<div class="absolute inset-0 overflow-hidden opacity-30">
			<div class="stars-small"></div>
			<div class="stars-medium"></div>
			<div class="stars-large"></div>
		</div>
	{/if}

	<div class="container relative z-10 mx-auto px-4 sm:px-6 lg:px-8">
		<div
			class="mx-auto max-w-4xl text-center transition-all duration-1000 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-8 opacity-0'}"
		>
			<!-- Main Heading -->
			<h1 class="mb-6 text-4xl font-bold leading-tight md:text-5xl lg:text-6xl">
				بیست و هفتمین دوره<br />
				<span class="bg-gradient-to-r from-blue-200 to-white bg-clip-text text-transparent">
					مسابقات ملی علوم اعصاب شناختی
				</span>
			</h1>

			<!-- Subtitle -->
			<p class="mb-8 text-lg text-blue-100 md:text-xl">
				ویژه دانش‌آموزان هفتم تا یازدهم
			</p>

			<!-- Countdown Timer -->
			<div class="mb-10" role="timer" aria-label="زمان باقی‌مانده تا پایان ثبت‌نام">
				<div class="mb-4 flex items-center justify-center gap-2 text-sm text-blue-200">
					<Calendar class="h-4 w-4" />
					<span>زمان باقی‌مانده تا پایان ثبت‌نام</span>
				</div>
				<div class="flex justify-center gap-3 md:gap-6" dir="ltr">
					{#each [
						{ value: timeLeft.days, label: 'روز' },
						{ value: timeLeft.hours, label: 'ساعت' },
						{ value: timeLeft.minutes, label: 'دقیقه' },
						{ value: timeLeft.seconds, label: 'ثانیه' }
					] as unit, i}
						<div
							class="flex flex-col items-center transition-all duration-300 {!reducedMotion
								? 'hover:scale-110'
								: ''}"
							style="animation-delay: {i * 100}ms"
						>
							<div
								class="flex h-16 w-16 items-center justify-center rounded-lg bg-white/10 backdrop-blur-sm md:h-20 md:w-20 {!reducedMotion
									? 'animate-pulse'
									: ''}"
							>
								<span class="text-2xl font-bold md:text-3xl" aria-live="polite">
									{String(unit.value).padStart(2, '0')}
								</span>
							</div>
							<span class="mt-2 text-xs text-blue-200 md:text-sm">{unit.label}</span>
						</div>
					{/each}
				</div>
			</div>

			<!-- CTA Buttons -->
			<div class="flex flex-col items-center justify-center gap-4 sm:flex-row">
				<Button
					href="/register"
					size="lg"
					class="group w-full bg-white text-[#0D47A1] transition-all duration-300 hover:bg-blue-50 hover:shadow-2xl sm:w-auto {!reducedMotion
						? 'hover:scale-105 active:scale-95'
						: ''}"
				>
					<span class="font-bold">ثبت‌نام کنید</span>
					<svg
						class="mr-2 h-5 w-5 transition-transform {!reducedMotion
							? 'group-hover:-translate-x-1'
							: ''}"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M15 19l-7-7 7-7"
						/>
					</svg>
				</Button>

				<Button
					href={guidelinesPdf}
					download="CNCH-Guidelines.pdf"
					variant="outline"
					size="lg"
					class="group w-full border-2 border-white bg-transparent text-white transition-all duration-300 hover:bg-white hover:text-[#0D47A1] sm:w-auto {!reducedMotion
						? 'hover:scale-105 active:scale-95'
						: ''}"
				>
					<Download class="ml-2 h-5 w-5" />
					<span class="font-bold">دانلود دفترچه راهنما</span>
				</Button>
			</div>
		</div>
	</div>
</section>

<style>
	@keyframes twinkle {
		0%,
		100% {
			opacity: 0;
		}
		50% {
			opacity: 1;
		}
	}

	.stars-small,
	.stars-medium,
	.stars-large {
		position: absolute;
		width: 100%;
		height: 100%;
		background-image: radial-gradient(2px 2px at 20% 30%, white, transparent),
			radial-gradient(2px 2px at 60% 70%, white, transparent),
			radial-gradient(1px 1px at 50% 50%, white, transparent),
			radial-gradient(1px 1px at 80% 10%, white, transparent);
		background-size:
			200% 200%,
			300% 300%,
			250% 250%,
			280% 280%;
		background-repeat: repeat;
	}

	.stars-small {
		animation: twinkle 3s ease-in-out infinite;
	}

	.stars-medium {
		animation: twinkle 4s ease-in-out infinite;
		animation-delay: 1s;
	}

	.stars-large {
		animation: twinkle 5s ease-in-out infinite;
		animation-delay: 2s;
	}

	@media (prefers-reduced-motion: reduce) {
		.stars-small,
		.stars-medium,
		.stars-large {
			animation: none;
		}
	}
</style>
