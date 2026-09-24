<script lang="ts">
	import { onMount } from 'svelte';

	let visible = $state(false);
	let sectionEl: HTMLElement | undefined;

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						visible = true;
						observer.disconnect();
					}
				});
			},
			{ threshold: 0.08 }
		);
		if (sectionEl) observer.observe(sectionEl);
		return () => observer.disconnect();
	});
</script>

<section
	id="infographic"
	bind:this={sectionEl}
	dir="rtl"
	class="relative overflow-hidden bg-gradient-to-b from-slate-50 to-white py-16 md:py-24"
>
	<!-- Decorative background blobs -->
	<div
		class="pointer-events-none absolute -right-32 -top-32 h-80 w-80 rounded-full bg-blue-100 opacity-40 blur-3xl"
	></div>
	<div
		class="pointer-events-none absolute -bottom-32 -left-32 h-80 w-80 rounded-full bg-purple-100 opacity-40 blur-3xl"
	></div>

	<div class="relative mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
		<!-- Section header -->
		<div
			class="mb-10 text-center transition-all duration-700 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-8 opacity-0'}"
		>
			<span
				class="mb-3 inline-block rounded-full bg-blue-100 px-4 py-1 text-sm font-semibold text-blue-700"
			>
				نقشه راه مسابقه
			</span>
			<h2 class="text-3xl font-extrabold text-gray-900 md:text-4xl">
				نقشه راه پژوهشگر آینده
			</h2>
			<p class="mx-auto mt-3 max-w-2xl text-base text-gray-500 md:text-lg">
				از ایده تا تأثیر؛ مسیر چهار فازی CNCH را در یک نگاه ببینید.
			</p>
		</div>

		<!-- Infographic image -->
		<div
			class="transition-all duration-1000 delay-200 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-12 opacity-0'}"
		>
			<a
				href="/infographic.jpg"
				target="_blank"
				rel="noopener noreferrer"
				aria-label="مشاهده اینفوگرافیک در اندازه کامل"
				class="group block overflow-hidden rounded-2xl shadow-2xl ring-1 ring-gray-200 transition-transform duration-300 hover:scale-[1.01] hover:shadow-3xl focus:outline-none focus:ring-4 focus:ring-blue-400"
			>
				<img
					src="/infographic.jpg"
					alt="اینفوگرافیک نقشه راه مسابقات ملی علوم اعصاب شناختی CNCH — چهار فاز مسابقه از آشنایی تا ارائه نتایج"
					class="w-full object-cover transition-opacity duration-300 group-hover:opacity-95"
					loading="lazy"
					decoding="async"
				/>
			</a>
			<p class="mt-3 text-center text-sm text-gray-400">
				برای مشاهده تمام‌صفحه کلیک کنید
			</p>
		</div>
	</div>
</section>
