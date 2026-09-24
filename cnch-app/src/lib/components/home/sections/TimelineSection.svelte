<script>
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { BookOpen, GraduationCap, FlaskConical, Trophy, Flag } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let visiblePhases = $state([false, false, false, false]);
	let lineProgress = $state(0);

	const phases = [
		{
			number: 1,
			title: 'فاز آشنایی',
			period: 'مقدمات',
			icon: BookOpen,
			color: 'from-blue-500 to-blue-600',
			items: ['ثبت‌نام و تشکیل تیم', 'آموزش مقدماتی مفاهیم', 'آشنایی با ابزارها و روش‌ها']
		},
		{
			number: 2,
			title: 'فاز تخصصی',
			period: 'آموزش عمیق',
			icon: GraduationCap,
			color: 'from-purple-500 to-purple-600',
			items: [
				'عصب‌شناسی شناختی',
				'سایکوفیزیک و روش‌های آزمایشی',
				'آمار و تحلیل داده',
				'کارگاه‌های عملی'
			]
		},
		{
			number: 3,
			title: 'فاز پروژه',
			period: 'اجرای پژوهش',
			icon: FlaskConical,
			color: 'from-green-500 to-green-600',
			items: [
				'انتخاب سوال پژوهشی',
				'کار مستمر با منتور',
				'طراحی و اجرای آزمایش',
				'جمع‌آوری و تحلیل داده'
			]
		},
		{
			number: 4,
			title: 'فاز ارائه و داوری',
			period: 'نمایش نتایج',
			icon: Trophy,
			color: 'from-orange-500 to-orange-600',
			items: ['تهیه پوستر علمی', 'ارائه پروژه', 'جلسات داوری', 'اختتامیه و اهدای جوایز']
		}
	];

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						// Animate timeline line
						setTimeout(() => {
							const interval = setInterval(() => {
								lineProgress = Math.min(lineProgress + 2, 100);
								if (lineProgress >= 100) clearInterval(interval);
							}, 20);
						}, 300);

						// Animate phases one by one
						phases.forEach((_, index) => {
							setTimeout(() => {
								visiblePhases[index] = true;
							}, 500 + index * 300);
						});
					}
				});
			},
			{ threshold: 0.1 }
		);

		const section = document.getElementById('timeline');
		if (section) observer.observe(section);

		return () => observer.disconnect();
	});

	const reducedMotion =
		typeof window !== 'undefined'
			? window.matchMedia('(prefers-reduced-motion: reduce)').matches
			: false;
</script>

<section class="bg-gradient-to-b from-gray-50 to-white py-16 md:py-24" id="timeline">
	<div class="container mx-auto px-4 sm:px-6 lg:px-8">
		<!-- Section Header -->
		<div class="mb-16 text-center">
			<h2 class="mb-4 text-3xl font-bold text-gray-900 md:text-4xl">مسیر مسابقه</h2>
			<p class="mx-auto max-w-2xl text-lg text-gray-600">
				سفر ۴۷ هفته‌ای شما از آموزش تا ارائه پروژه نهایی
			</p>
			<div class="mx-auto mt-4 h-1 w-24 rounded-full bg-gradient-to-r from-blue-500 to-purple-500">
			</div>
		</div>

		<!-- Timeline -->
		<div class="relative mx-auto max-w-4xl">
			<!-- Vertical Line -->
			<div
				class="absolute right-1/2 top-0 hidden h-full w-1 translate-x-1/2 overflow-hidden rounded-full bg-gray-200 md:block"
				aria-hidden="true"
			>
				<div
					class="h-full w-full bg-gradient-to-b from-blue-500 via-purple-500 to-orange-500 transition-all duration-2000 ease-out"
					style="transform: translateY({100 - lineProgress}%)"
				></div>
			</div>

			<!-- Phases -->
			<div class="space-y-12">
				{#each phases as phase, index}
					<div
						class="relative transition-all duration-700 {visiblePhases[index]
							? 'translate-x-0 opacity-100'
							: index % 2 === 0
								? 'translate-x-16 opacity-0'
								: '-translate-x-16 opacity-0'}"
					>
					<div class="relative md:grid md:grid-cols-2 md:gap-16">
						<!-- Phase Card -->
						<div class="{index % 2 === 0 ? 'md:col-start-2' : 'md:col-start-1'}">
							<Card
								class="group overflow-hidden py-0 transition-all duration-300 {!reducedMotion
										? 'hover:-translate-y-1 hover:shadow-xl'
										: ''}"
								>
									<CardHeader class="bg-gradient-to-r {phase.color} p-6 text-white">
										<div class="flex items-center gap-4">
											<!-- Phase Icon -->
											<div
												class="rounded-full bg-white/20 p-3 backdrop-blur-sm {!reducedMotion
													? 'group-hover:rotate-12 group-hover:scale-110'
													: ''} transition-transform duration-300"
											>
												<phase.icon class="h-6 w-6" />
											</div>

											<div>
												<CardTitle class="text-xl font-bold">{phase.title}</CardTitle>
												<p class="text-sm text-white/80">{phase.period}</p>
											</div>
										</div>
									</CardHeader>

									<CardContent class="p-6">
										<ul class="space-y-3">
											{#each phase.items as item}
												<li class="flex items-start gap-3">
													<span
														class="mt-1 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-gradient-to-r {phase.color} text-xs text-white"
													>
														✓
													</span>
													<span class="text-gray-700">{item}</span>
												</li>
											{/each}
										</ul>
									</CardContent>
								</Card>
							</div>

							<!-- Timeline Dot (Desktop) -->
							<div
							class="absolute left-1/2 {index === phases.length-1 ? 'bottom' : 'top'}-0 hidden h-12 w-12 -translate-x-1/2 md:block"
								aria-hidden="true"
							>
								<div
									class="flex h-full w-full items-center justify-center rounded-full { index === phases.length-1 ? 'bg-gradient-to-r ' + phase.color : 'bg-white'} shadow-lg ring-4 ring-gray-200"

								>
								{#if index === phases.length-1}
									<Flag class="h-6 w-6 text-white" strokeWidth={2.5} />
								{:else}
									<div class="h-6 w-6 rounded-full bg-gradient-to-r {phase.color}"></div>
								{/if}
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</section>

<style>
	@media (prefers-reduced-motion: reduce) {
		* {
			animation-duration: 0.01ms !important;
			animation-iteration-count: 1 !important;
			transition-duration: 0.01ms !important;
		}
	}
</style>
