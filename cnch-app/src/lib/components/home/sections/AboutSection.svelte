<script>
	import { Card, CardContent } from '$lib/components/ui/card';
	import { Calendar, Layers, Users } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let visible = $state(false);
	let countersStarted = $state(false);

	const stats = [
		{
			icon: Calendar,
			value: 35,
			label: 'هفته مسابقه',
			suffix: '',
			color: 'text-blue-500',
			static: false
		},
		{
			icon: Layers,
			value: 4,
			label: 'فاز آموزشی',
			suffix: '',
			color: 'text-purple-500',
			static: false
		},
		{
			icon: Users,
			value: 27,
			label: 'دوره‌ی متوالی',
			suffix: '',
			color: 'text-orange-500',
			static: false
		}
	];

	let animatedValues = $state(stats.map(() => 0));

	function animateCounters() {
		if (countersStarted) return;
		countersStarted = true;

		stats.forEach((stat, index) => {
			const duration = 2000;
			const steps = 60;
			const increment = stat.value / steps;
			let current = 0;
			let step = 0;

			const interval = setInterval(() => {
				step++;
				current += increment;

				if (step >= steps) {
					animatedValues[index] = stat.value;
					clearInterval(interval);
				} else {
					animatedValues[index] = Math.floor(current);
				}
			}, duration / steps);
		});
	}

	onMount(() => {
		visible = true;

		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						animateCounters();
					}
				});
			},
			{ threshold: 0.2 }
		);

		const section = document.getElementById('about');
		if (section) observer.observe(section);

		return () => observer.disconnect();
	});

	const reducedMotion =
		typeof window !== 'undefined'
			? window.matchMedia('(prefers-reduced-motion: reduce)').matches
			: false;
</script>

<section class="bg-white py-16 md:py-24" id="about">
	<div class="container mx-auto px-4 sm:px-6 lg:px-8">
		<!-- Section Header -->
		<div
			class="mb-12 text-center transition-all duration-1000 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-8 opacity-0'}"
		>
			<h2 class="mb-4 text-3xl font-bold text-gray-900 md:text-4xl">درباره مسابقه</h2>
			<div class="mx-auto h-1 w-24 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"></div>
		</div>

		<!-- Content Grid -->
		<div class="grid gap-12 lg:grid-cols-2 lg:gap-16">
			<!-- Left: Description -->
			<div
				class="transition-all duration-1000 delay-200 {visible
					? 'translate-x-0 opacity-100'
					: 'translate-x-8 opacity-0'}"
			>
				<h3 class="mb-4 text-2xl font-bold text-gray-900">مسابقه ملی علوم اعصاب شناختی چیست؟</h3>
				<div class="space-y-4 text-gray-700 leading-relaxed">
					<p>
						مسابقه علوم اعصاب شناختی (CNCH) یک رویداد علمی ـ آموزشی برای دانش‌آموزان هفتم تا یازدهم است که با هدف ترویج تفکر پژوهش‌محور، آشنایی نظام‌مند با علوم اعصاب و پرورش استعدادهای برتر در حوزه شناخت و مغز طراحی شده است. این مسابقه تلاش می‌کند پلی میان آموزش مدرسه‌ای و پژوهش دانشگاهی ایجاد کند و دانش‌آموزان را با مفاهیم کلیدی نوروساینس، روش‌شناسی علمی و کاربردهای بین‌رشته‌ای آن آشنا سازد.
					</p>

					<p>
						مسابقه CNCH در دوره‌های پیشین با حمایت و همکاری <strong>ستاد توسعه علوم و فناوری‌های شناختی</strong> و <strong>سازمان ملی پرورش استعدادهای درخشان (سمپاد)</strong> برگزار شده و در حال حاضر با همکاری <strong>انجمن علوم اعصاب ایران</strong> به فعالیت خود ادامه می‌دهد. این همکاری‌ها نشان‌دهنده جایگاه علمی مسابقه و هم‌راستایی آن با سیاست‌های ملی توسعه علوم شناختی است.
					</p>

					<p>
						با توجه به رشد شتابان علوم اعصاب در سطح جهانی و نقش آن در حوزه‌هایی مانند سلامت روان، یادگیری، تصمیم‌گیری و فناوری‌های نوین، آشنایی زودهنگام دانش‌آموزان با این حوزه اهمیت راهبردی دارد. همچنین هم‌پوشانی روزافزون نوروساینس با هوش مصنوعی و شکل‌گیری حوزه <strong>NeuroAI</strong>، که از تعامل میان مدل‌های عصبی زیستی و الگوریتم‌های یادگیری ماشین شکل گرفته، جایگاه این دانش را در آینده علم و فناوری دوچندان کرده است. CNCH با تمرکز بر این تحولات، بستری برای تربیت نسل آینده پژوهشگران و نوآوران در علوم شناختی و NeuroAI فراهم می‌کند.
					</p>
				</div>
			</div>

			<!-- Right: Stats Cards -->
			<div class="grid grid-cols-3 content-start gap-4 self-start md:gap-6">
				{#each stats as stat, i}
					<Card
						class="group py-0 transition-all duration-500 {!reducedMotion
							? 'hover:-translate-y-2 hover:shadow-xl'
							: ''} {visible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
						style="transition-delay: {(i + 3) * 100}ms"
					>
						<CardContent class="p-6">
							<div class="mb-4 flex justify-center">
								<div
									class="rounded-full bg-gradient-to-br from-blue-50 to-purple-50 p-3 {!reducedMotion
										? 'group-hover:rotate-12'
										: ''} transition-transform duration-300"
								>
									<stat.icon class="h-8 w-8 {stat.color}" />
								</div>
							</div>

							<div class="text-center">
								<div class="mb-2 text-4xl font-bold text-gray-900" aria-live="polite">
								{animatedValues[i]}{stat.suffix}
								</div>
								<div class="text-sm font-medium text-gray-600">{stat.label}</div>
							</div>
						</CardContent>
					</Card>
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
