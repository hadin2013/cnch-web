<script>
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Trophy, Users, Briefcase, GraduationCap, Award, Rocket } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let visible = $state(false);

	const benefits = [
		{
			icon: Trophy,
			title: 'جایزه معتبر اهوازی',
			description: 'دریافت جایزه یادبود پزشک بزرگ ایرانی قرن چهارم برای تیم‌های برتر',
			color: 'from-yellow-500 to-orange-500'
		},
		{
			icon: Award,
			title: 'جوایز نقدی',
			description: 'جوایز نقدی ویژه برای رتبه‌های اول تا سوم مسابقه',
			color: 'from-green-500 to-emerald-500'
		},
		{
			icon: Users,
			title: 'عضویت در انجمن CNCH',
			description: 'دسترسی به شبکه فعالان علوم اعصاب و حمایت‌های بعدی',
			color: 'from-blue-500 to-cyan-500'
		},
		{
			icon: Rocket,
			title: 'مسیر جشنواره خوارزمی',
			description: 'تسهیل و حمایت برای ورود به جشنواره جوان خوارزمی',
			color: 'from-purple-500 to-pink-500'
		},
		{
			icon: Briefcase,
			title: 'کارآموزی و تولید محصول',
			description: 'فرصت کارآموزی در مراکز تحقیقاتی و کمک به تولید محصول',
			color: 'from-red-500 to-rose-500'
		},
		{
			icon: GraduationCap,
			title: 'رزومه دانشگاهی',
			description: 'ساخت رزومه قوی برای پذیرش در دانشگاه‌های برتر داخل و خارج',
			color: 'from-indigo-500 to-violet-500'
		}
	];

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						visible = true;
					}
				});
			},
			{ threshold: 0.1 }
		);

		const section = document.getElementById('prizes');
		if (section) observer.observe(section);

		return () => observer.disconnect();
	});

	const reducedMotion =
		typeof window !== 'undefined'
			? window.matchMedia('(prefers-reduced-motion: reduce)').matches
			: false;
</script>

<section class="bg-white py-16 md:py-24" id="prizes">
	<div class="container mx-auto px-4 sm:px-6 lg:px-8">
		<!-- Section Header -->
		<div class="mb-16 text-center">
			<div class="mb-6 flex justify-center">
				<div
					class="rounded-full bg-gradient-to-br from-yellow-100 to-orange-100 p-4 {!reducedMotion
						? 'animate-bounce'
						: ''}"
				>
					<Trophy class="h-12 w-12 text-orange-500" />
				</div>
			</div>
			<h2 class="mb-4 text-3xl font-bold text-gray-900 md:text-4xl">جوایز و حمایت‌ها</h2>
			<p class="mx-auto max-w-2xl text-lg text-gray-600">
				برگزیدگان این مسابقه از جوایز ارزشمند و حمایت‌های ویژه بهره‌مند خواهند شد
			</p>
			<div class="mx-auto mt-4 h-1 w-24 rounded-full bg-gradient-to-r from-yellow-500 to-orange-500">
			</div>
		</div>

		<!-- Benefits Grid -->
		<div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
			{#each benefits as benefit, i}
				<Card
					class="group overflow-hidden py-0 transition-all duration-500 {visible
						? 'translate-y-0 opacity-100'
						: 'translate-y-8 opacity-0'} {!reducedMotion
						? 'hover:-translate-y-2 hover:shadow-2xl'
						: ''}"
					style="transition-delay: {i * 100}ms"
				>
					<CardHeader class="relative overflow-hidden bg-gradient-to-br {benefit.color} p-6">
						<!-- Background Pattern -->
						<div
							class="absolute inset-0 opacity-10"
							style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 20px 20px;"
						></div>

						<div class="relative flex items-center gap-4">
							<div
								class="rounded-lg bg-white/20 p-3 backdrop-blur-sm {!reducedMotion
									? 'group-hover:rotate-12 group-hover:scale-110'
									: ''} transition-all duration-300"
							>
								<benefit.icon class="h-6 w-6 text-white" />
							</div>
							<CardTitle class="text-lg font-bold text-white">{benefit.title}</CardTitle>
						</div>
					</CardHeader>

					<CardContent class="p-6">
						<p class="leading-relaxed text-gray-700">{benefit.description}</p>
					</CardContent>

					<!-- Hover Effect Overlay -->
					{#if !reducedMotion}
						<div
							class="absolute inset-0 bg-gradient-to-br {benefit.color} opacity-0 transition-opacity duration-300 group-hover:opacity-5"
						></div>
					{/if}
				</Card>
			{/each}
		</div>

		<!-- Call to Action -->
		<div
			class="mt-12 text-center transition-all duration-700 delay-600 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-8 opacity-0'}"
		>
			<p class="text-lg font-medium text-gray-700">
				<span class="text-2xl">🎯</span>
				همین الان ثبت‌نام کنید و بخشی از این جامعه علمی شوید!
			</p>
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
