<script>
	import { Phone, Mail, Globe } from 'lucide-svelte';
	import { Separator } from '$lib/components/ui/separator';
	import mainLogo from '$lib/assets/logos/main.jpg';
	import altLogo from '$lib/assets/logos/alt.png';
	import neuroscienceLogo from '$lib/assets/logos/neuroscience_association.png';
	import guidelinesPdf from '$lib/assets/cnch guidlines.pdf';

	const quickLinks = [
		{ href: '#about', label: 'راهنمای مسابقه' },
		{ href: '#faq', label: 'سوالات متداول' },
		{ href: '#contact', label: 'تماس با ما' },
		{ href: '/register', label: 'ثبت‌نام' }
	];

	const contactInfo = [
		{ icon: Phone, text: '۰۹۰۰۵۸۶۵۹۳۵', href: 'tel:+989005865935' },
		{ icon: Mail, text: '@Blogishadmin', href: 'https://t.me/Blogishadmin' },
		{ icon: Globe, text: 'www.CNCH.ir', href: 'https://www.CNCH.ir' },
		{ icon: Globe, text: 'www.insorg.ir', href: 'https://www.insorg.ir' }
	];
</script>

<footer class="bg-[#0D47A1] text-white">
	<div class="container mx-auto px-4 py-12 sm:px-6 lg:px-8">
		<!-- Main Footer Content -->
		<div class="grid gap-8 md:grid-cols-3">
			<!-- About Section -->
			<div>
				<h3 class="mb-4 text-lg font-bold">درباره CNCH</h3>
				<p class="mb-4 text-sm leading-relaxed text-blue-100">
					بیست و هفتمین دوره مسابقات ملی علوم اعصاب شناختی، ویژه دانش‌آموزان هشتم تا یازدهم. مسابقه‌ای
					برای ورود به دنیای NeuroAI با آموزش و راهنمایی منتورها.
				</p>
				<a
					href={guidelinesPdf}
					download="CNCH-Guidelines.pdf"
					class="inline-flex items-center text-sm font-medium text-white underline hover:text-blue-100"
				>
					دانلود دفترچه راهنما
				</a>
			</div>

			<!-- Quick Links -->
			<div>
				<h3 class="mb-4 text-lg font-bold">دسترسی سریع</h3>
				<ul class="space-y-2">
					{#each quickLinks as link}
						<li>
							<a
								href={link.href}
								class="text-sm text-blue-100 transition-colors hover:text-white"
							>
								{link.label}
							</a>
						</li>
					{/each}
				</ul>
			</div>

			<!-- Contact Info -->
			<div>
				<h3 class="mb-4 text-lg font-bold">ارتباط با ما</h3>
				<ul class="space-y-3">
					{#each contactInfo as item}
						<li class="flex items-center gap-3">
							<svelte:component this={item.icon} class="h-4 w-4 text-blue-200" />
							<a
								href={item.href}
								target="_blank"
								rel="noopener noreferrer"
								class="text-sm text-blue-100 transition-colors hover:text-white"
							>
								{item.text}
							</a>
						</li>
					{/each}
				</ul>
			</div>
		</div>

		<Separator class="my-8 bg-blue-600" />

		<!-- Organizers Logos -->
		<div class="mb-8">
			<h3 class="mb-6 text-center text-sm font-semibold text-blue-200">برگزارکنندگان</h3>
			<div class="flex flex-wrap items-center justify-center gap-8">
				<img
					src={mainLogo}
					alt="CNCH"
					class="h-16 w-auto object-contain opacity-80 grayscale transition-all hover:opacity-100 hover:grayscale-0"
				/>
				<img
					src={altLogo}
					alt="Partner Organization"
					class="h-16 w-auto object-contain opacity-80 grayscale transition-all hover:opacity-100 hover:grayscale-0"
				/>
				<img
					src={neuroscienceLogo}
					alt="Neuroscience Association"
					class="h-16 w-auto object-contain opacity-80 grayscale transition-all hover:opacity-100 hover:grayscale-0"
				/>
			</div>
		</div>

		<Separator class="my-6 bg-blue-600" />

		<!-- Trust Seals -->
		<div class="mb-6 flex flex-wrap items-center justify-center gap-4">
			<a
				referrerpolicy="origin"
				target="_blank"
				href="https://trustseal.enamad.ir/?id=710290&Code=JeSWyWkDIyd6SwlJavHc8fvjvJGkmb1A"
			>
				<img
					referrerpolicy="origin"
					src="https://trustseal.enamad.ir/logo.aspx?id=710290&Code=JeSWyWkDIyd6SwlJavHc8fvjvJGkmb1A"
					alt="نماد اعتماد الکترونیکی"
					style="cursor:pointer"
					{...{ code: 'JeSWyWkDIyd6SwlJavHc8fvjvJGkmb1A' }}
					class="h-20 w-auto"
				/>
			</a>
		</div>

		<Separator class="my-6 bg-blue-600" />

		<!-- Copyright -->
		<div class="text-center text-sm text-blue-200">
			<p>© ۱۴۰۴ انجمن علوم اعصاب شناختی ایران | تمامی حقوق محفوظ است</p>
		</div>
	</div>
</footer>
