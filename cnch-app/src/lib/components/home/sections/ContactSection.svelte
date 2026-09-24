<script>
	import { onMount } from 'svelte';
	import { Mail, Phone, Instagram, Linkedin, AtSign } from 'lucide-svelte';

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
			{ threshold: 0.1 }
		);

		const section = document.getElementById('contact');
		if (section) observer.observe(section);

		return () => observer.disconnect();
	});

	const reducedMotion =
		typeof window !== 'undefined'
			? window.matchMedia('(prefers-reduced-motion: reduce)').matches
			: false;

	const socialContacts = [
		{
			id: 'telegram-channel',
			label: 'کانال تلگرام',
			value: '@cnchchannel',
			href: 'https://t.me/cnchchannel',
			colorClass: 'from-sky-400 to-cyan-500',
			bgClass: 'bg-sky-500/10 hover:bg-sky-500/20 border-sky-500/20 hover:border-sky-400/50',
			textClass: 'text-sky-400',
			brand: 'telegram'
		},
		{
			id: 'telegram-support',
			label: 'پشتیبانی تلگرام',
			value: '@blogishadmin',
			href: 'https://t.me/blogishadmin',
			colorClass: 'from-sky-400 to-cyan-500',
			bgClass: 'bg-sky-500/10 hover:bg-sky-500/20 border-sky-500/20 hover:border-sky-400/50',
			textClass: 'text-sky-400',
			brand: 'telegram'
		},
		{
			id: 'bale-channel',
			label: 'کانال بله',
			value: 'cnchchannel',
			href: 'https://ble.ir/cnchchannel',
			colorClass: 'from-emerald-400 to-teal-500',
			bgClass:
				'bg-emerald-500/10 hover:bg-emerald-500/20 border-emerald-500/20 hover:border-emerald-400/50',
			textClass: 'text-emerald-400',
			brand: 'bale'
		},
		{
			id: 'bale-support',
			label: 'پشتیبانی بله',
			value: 'cnch_support',
			href: 'https://ble.ir/cnch_support',
			colorClass: 'from-emerald-400 to-teal-500',
			bgClass:
				'bg-emerald-500/10 hover:bg-emerald-500/20 border-emerald-500/20 hover:border-emerald-400/50',
			textClass: 'text-emerald-400',
			brand: 'bale'
		},
		{
			id: 'instagram',
			label: 'اینستاگرام',
			value: 'cnch.official',
			href: 'https://instagram.com/cnch.official',
			colorClass: 'from-pink-500 to-purple-600',
			bgClass: 'bg-pink-500/10 hover:bg-pink-500/20 border-pink-500/20 hover:border-pink-400/50',
			textClass: 'text-pink-400',
			brand: 'instagram'
		},
		{
			id: 'linkedin',
			label: 'لینکدین',
			value: 'neuroscience-competition',
			href: 'https://linkedin.com/company/neuroscience-competition',
			colorClass: 'from-blue-500 to-blue-700',
			bgClass:
				'bg-blue-600/10 hover:bg-blue-600/20 border-blue-600/20 hover:border-blue-500/50',
			textClass: 'text-blue-400',
			brand: 'linkedin'
		},
		{
			id: 'aparat',
			label: 'آپارات',
			value: 'cnch',
			href: 'https://aparat.com/cnch',
			colorClass: 'from-red-500 to-orange-500',
			bgClass: 'bg-red-500/10 hover:bg-red-500/20 border-red-500/20 hover:border-red-400/50',
			textClass: 'text-red-400',
			brand: 'aparat'
		},
        {
			id: 'email',
			label: 'ایمیل گوگل',
			value: 'cnch1401@gmail.com',
			href: 'mailto:cnch1401@gmail.com',
			colorClass: 'from-amber-400 to-orange-500',
			bgClass:
				'bg-amber-500/10 hover:bg-amber-500/20 border-amber-500/20 hover:border-amber-400/50',
			textClass: 'text-amber-400',
			brand: 'gmail'
		}
	];

	const directContacts = [
		{
			id: 'phone',
			label: 'تماس تلفنی / پیامک',
			value: '۰۹۰۰۵۸۶۵۹۳۵',
			href: 'tel:09005865935',
			colorClass: 'from-violet-500 to-purple-600',
			bgClass:
				'bg-violet-500/10 hover:bg-violet-500/20 border-violet-500/20 hover:border-violet-400/50',
			textClass: 'text-violet-400',
			brand: 'phone'
		},
		{
			id: 'email-support',
			label: 'ایمیل پشتیبانی',
			value: 'support@cnch.ir',
			href: 'mailto:support@cnch.ir',
			colorClass: 'from-teal-400 to-cyan-600',
			bgClass:
				'bg-teal-500/10 hover:bg-teal-500/20 border-teal-500/20 hover:border-teal-400/50',
			textClass: 'text-teal-400',
			brand: 'email'
		}
	];
</script>

<section
	class="relative overflow-hidden bg-gradient-to-b from-[#0a1628] to-[#0D1B2A] py-20 text-white md:py-28"
	id="contact"
>
	<!-- Background decoration blobs -->
	{#if !reducedMotion}
		<div class="pointer-events-none absolute inset-0 overflow-hidden">
			<div
				class="absolute -right-64 -top-64 h-[500px] w-[500px] rounded-full bg-blue-900/20 blur-3xl"
				style="animation: float 12s ease-in-out infinite;"
			></div>
			<div
				class="absolute -bottom-64 -left-64 h-[500px] w-[500px] rounded-full bg-indigo-900/20 blur-3xl"
				style="animation: float 15s ease-in-out infinite reverse;"
			></div>
		</div>
	{/if}

	<div class="container relative z-10 mx-auto px-4 sm:px-6 lg:px-8">
		<!-- Section Header -->
		<div
			class="mb-14 text-center transition-all duration-700 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-6 opacity-0'}"
		>
			<div class="mb-4 flex justify-center">
				<span
					class="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-1.5 text-sm font-medium text-blue-300"
				>
					<!-- Live pulse dot -->
					<span class="relative flex h-2 w-2">
						<span
							class="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-75"
						></span>
						<span class="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
					</span>
					ارتباط با ما
				</span>
			</div>
			<h2 class="mb-4 text-3xl font-bold text-white md:text-4xl lg:text-5xl">
				تماس با
				<span class="bg-gradient-to-l from-blue-300 to-cyan-300 bg-clip-text text-transparent">
					دبیرخانه CNCH
				</span>
			</h2>
			<p class="mx-auto max-w-2xl text-base text-slate-400 md:text-lg">
				از طریق شبکه‌های اجتماعی یا اطلاعات تماس زیر با ما در ارتباط باشید. آماده پاسخگویی به
				سوالات شما هستیم.
			</p>
		</div>

		<!-- Social Contacts Grid -->
		<div class="mb-6 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
			{#each socialContacts as contact, i (contact.id)}
				<a
					href={contact.href}
					target="_blank"
					rel="noopener noreferrer"
					class="group relative overflow-hidden rounded-2xl border p-5 backdrop-blur-sm {contact.bgClass} {!reducedMotion
						? 'hover:-translate-y-1 hover:shadow-lg'
						: ''}"
					style="transition: transform 0.4s ease, opacity 0.4s ease, background-color 0.3s ease, border-color 0.3s ease; opacity: {visible
						? 1
						: 0}; transform: translateY({visible ? 0 : 24}px); transition-delay: {reducedMotion
						? '0ms'
						: `${i * 60}ms`};"
				>
					<!-- Colored brand icon -->
					<div
						class="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br {contact.colorClass} shadow-lg {!reducedMotion
							? 'transition-transform duration-300 group-hover:scale-110'
							: ''}"
					>
						{#if contact.brand === 'telegram'}
							<svg class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="currentColor">
								<path
									d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.782-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"
								/>
							</svg>
						{:else if contact.brand === 'bale'}
							<svg class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="currentColor">
								<path
									d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"
								/>
							</svg>
						{:else if contact.brand === 'instagram'}
							<Instagram class="h-6 w-6 text-white" />
						{:else if contact.brand === 'linkedin'}
							<Linkedin class="h-6 w-6 text-white" />
                        {:else if contact.brand === 'gmail'}
                            <AtSign class="h-6 w-6 text-white" />
						{:else if contact.brand === 'aparat'}
							<svg class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="currentColor">
								<path
									d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-1.5 14.5v-9l7 4.5-7 4.5z"
								/>
							</svg>
						{/if}
					</div>

					<p class="mb-1 text-xs font-medium text-slate-400">{contact.label}</p>
					<p class="truncate text-sm font-semibold {contact.textClass}">{contact.value}</p>

					<!-- Hover arrow indicator -->
					<div
						class="absolute bottom-4 left-4 opacity-0 transition-opacity duration-300 {!reducedMotion
							? 'group-hover:opacity-100'
							: ''}"
					>
						<svg
							class="h-4 w-4 {contact.textClass} rotate-180"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M17 8l4 4m0 0l-4 4m4-4H3"
							/>
						</svg>
					</div>
				</a>
			{/each}
		</div>

		<!-- Direct Contact Cards (Phone + Email) — full-width featured rows -->
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
			{#each directContacts as contact, i (contact.id)}
				<a
					href={contact.href}
					class="group flex items-center gap-5 overflow-hidden rounded-2xl border p-6 backdrop-blur-sm {contact.bgClass} {!reducedMotion
						? 'hover:-translate-y-1 hover:shadow-lg'
						: ''}"
					style="transition: transform 0.4s ease, opacity 0.4s ease, background-color 0.3s ease, border-color 0.3s ease; opacity: {visible
						? 1
						: 0}; transform: translateY({visible ? 0 : 24}px); transition-delay: {reducedMotion
						? '0ms'
						: `${(socialContacts.length + i) * 60}ms`};"
				>
					<!-- Icon -->
					<div
						class="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br {contact.colorClass} shadow-lg {!reducedMotion
							? 'transition-transform duration-300 group-hover:scale-110'
							: ''}"
					>
						{#if contact.brand === 'phone'}
							<Phone class="h-7 w-7 text-white" />
						{:else}
							<Mail class="h-7 w-7 text-white" />
						{/if}
					</div>

					<div class="min-w-0 flex-1">
						<p class="mb-1 text-sm font-medium text-slate-400">{contact.label}</p>
						<p
							dir={contact.brand === 'email' ? 'ltr' : 'rtl'}
							class="truncate text-base font-bold tracking-wide {contact.textClass}"
						>
							{contact.value}
						</p>
					</div>

					<!-- Arrow -->
					<svg
						class="h-5 w-5 shrink-0 rotate-180 text-slate-600 transition-colors duration-300 {!reducedMotion
							? 'group-hover:text-slate-400'
							: ''}"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M17 8l4 4m0 0l-4 4m4-4H3"
						/>
					</svg>
				</a>
			{/each}
		</div>
	</div>
</section>

<style>
	@keyframes float {
		0%,
		100% {
			transform: translateY(0px) scale(1);
		}
		50% {
			transform: translateY(-30px) scale(1.05);
		}
	}
</style>
