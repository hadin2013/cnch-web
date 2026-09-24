<script>
	import { onMount } from 'svelte';

	// ── Images ──────────────────────────────────────────────────────────────────
	import img_abbasian from '$lib/assets/professors/dr_abbasian.png';
	import img_arabzadeh from '$lib/assets/professors/ehsan_arabzadeh.jpg';
	import img_vaziri from '$lib/assets/professors/maryam_vaziri.jpg';
	import img_sarabi from '$lib/assets/professors/atieh_sarabi.jpg';
	import img_vahabi from '$lib/assets/professors/vahabi.jpg';
	import img_abolqasemi from '$lib/assets/professors/abolqasemi.jpg';
	import img_rajimehr from '$lib/assets/professors/reza_rajimehr.jpg';
	import img_fotouhi from '$lib/assets/professors/morteza_fotouhi.jpg';
	import img_sharif from '$lib/assets/professors/behrang_sharif.jpg';
	import img_golzar from '$lib/assets/professors/Golzar.jpg';
	import img_rezaei from '$lib/assets/professors/negin_rezaei.jpg';
	import img_khaliq from '$lib/assets/professors/Khaliq_Razavi.jpg';
	import img_ebrahimpour from '$lib/assets/professors/reza_ebrahimpour.jpg';
	import img_rafipoor from '$lib/assets/professors/hosein_rafipoor.jpg';
	import img_tara from '$lib/assets/professors/tara_qafari.jpg';
	import img_aryan from '$lib/assets/professors/aryan_zoroufi.jpg';
	import img_ayda from '$lib/assets/professors/ayda_miribrahimi.jpg';
	import img_erfan from '$lib/assets/professors/erfan_najafzadeh.jpg';
	import img_niloufar from '$lib/assets/professors/niloufar_hasani.jpg';
	import img_nima from '$lib/assets/professors/nima_moradi.jpg';
	import img_elnaz from '$lib/assets/professors/elnaz_karami.jpg';
	import img_mohsen from '$lib/assets/professors/mohsen_omrani.jpg';
	import img_hosein_j from '$lib/assets/professors/hosein_jafari.jpg';
	import img_roozbeh from '$lib/assets/professors/roozbeh_kiani.jpg';
	import img_saqar from '$lib/assets/professors/saqar_mirbaqeri.jpg';
	import img_joqatayi from '$lib/assets/professors/joqatayi.jpg';
	import img_ali_sh from '$lib/assets/professors/ali_shahbazi.jpg';
	import img_behzad from '$lib/assets/professors/behzad_nodoost.jpg';
	import img_shahab from '$lib/assets/professors/shahab_bakhtiari.jpg';

	// ── Data ────────────────────────────────────────────────────────────────────
	/** @type {{ name: string; affiliation: string; photo: string | null; badge?: string }[]} */
	const faculty = [
		{
			name: 'دکتر عبدالحسین عباسیان',
			affiliation: 'پژوهشگاه دانش‌های بنیادی (IPM)',
			photo: img_abbasian
		},
		{
			name: 'دکتر احسان عربزاده',
			affiliation: 'Australian National University',
			photo: img_arabzadeh
		},
		{
			name: 'دکتر مریم وزیری پاشکم',
			affiliation: 'University of Delaware',
			photo: img_vaziri
		},
		{
			name: 'دکتر عطیه سرابی',
			affiliation: 'پژوهشگاه دانش‌های بنیادی (IPM)',
			photo: img_sarabi
		},
		{
			name: 'دکتر عبدالحسین وهابی',
			affiliation: 'پژوهشگاه دانش‌های بنیادی (IPM)',
			photo: img_vahabi
		},
		{
			name: 'دکتر محمدرضا ابوالقاسمی',
			affiliation: 'پژوهشگاه دانش‌های بنیادی (IPM)',
			photo: img_abolqasemi
		},
		{
			name: 'دکتر رضا راجی مهر',
			affiliation: 'پژوهشگاه دانش‌های بنیادی (IPM)',
			photo: img_rajimehr
		},
		{
			name: 'دکتر مرتضی فتوحی',
			affiliation: 'دانشگاه صنعتی شریف',
			photo: img_fotouhi
		},
		{
			name: 'دکتر بهرنگ شریف',
			affiliation: 'ETH Zurich',
			photo: img_sharif
		},
		{
			name: 'دکتر اشکان گلزار',
			affiliation: 'McGill University',
			photo: img_golzar
		},
		{
			name: 'دکتر نگین رضایی',
			affiliation: 'Harvard University',
			photo: img_rezaei
		},
		{
			name: 'دکتر مهدی خلیق رضوی',
			affiliation: 'University of Cambridge',
			photo: img_khaliq
		},
		{
			name: 'دکتر رضا ابراهیم پور',
			affiliation: 'دانشگاه صنعتی شریف',
			photo: img_ebrahimpour
		},
		{
			name: 'دکتر حسین رفیع پور',
			affiliation: 'Post Doc – دانشگاه آکسفورد',
			photo: img_rafipoor,
			badge: 'Post Doc'
		},
		{
			name: 'دکتر تارا غفاری',
			affiliation: 'Post Doc – دانشگاه آکسفورد',
			photo: img_tara,
			badge: 'Post Doc'
		},
		{
			name: 'آرین ظروفی',
			affiliation: 'دانشجوی PhD – MIT',
			photo: img_aryan,
			badge: 'PhD'
		},
		{
			name: 'آیدا میرابراهیمی',
			affiliation: 'دانشجوی PhD – Carnegie Mellon',
			photo: img_ayda,
			badge: 'PhD'
		},
		{
			name: 'عرفان نجف زاده',
			affiliation: 'دانشجوی BSc – دانشگاه شهید بهشتی',
			photo: img_erfan,
			badge: 'BSc'
		},
		{ name: 'نیلوفر علی حسنی', affiliation: '', photo: img_niloufar },
		{ name: 'نیما مرادی', affiliation: '', photo: img_nima },
		{ name: 'دکتر الناز کرمی', affiliation: '', photo: img_elnaz },
		{ name: 'دکتر محسن عمرانی', affiliation: '', photo: img_mohsen },
		{ name: 'دکتر حسین جعفری', affiliation: '', photo: img_hosein_j },
		{ name: 'دکتر روزبه کیانی', affiliation: '', photo: img_roozbeh },
		{ name: 'دکتر ساغر میرباقری', affiliation: '', photo: img_saqar },
		{ name: 'دکتر شیما تالهی', affiliation: '', photo: null },
		{ name: 'دکتر محمد دماوندی', affiliation: '', photo: null },
		{ name: 'دکتر حسین استکی', affiliation: '', photo: null },
		{ name: 'دکتر محمد تقی جغتایی', affiliation: '', photo: img_joqatayi },
		{ name: 'دکتر علی شهبازی', affiliation: '', photo: img_ali_sh },
		{ name: 'دکتر بهزاد نوع‌دوست', affiliation: '', photo: img_behzad },
		{ name: 'دکتر شهاب بختیاری', affiliation: '', photo: img_shahab }
	];

	// ── Animation ───────────────────────────────────────────────────────────────
	let visible = $state(false);

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => entries.forEach((e) => { if (e.isIntersecting) visible = true; }),
			{ threshold: 0.05 }
		);
		const section = document.getElementById('professors');
		if (section) observer.observe(section);
		return () => observer.disconnect();
	});

	/**
	 * Returns initials from a Persian name for avatar fallback.
	 * @param {string} name
	 */
	function initials(name) {
		const parts = name.replace(/^دکتر\s*/u, '').trim().split(/\s+/);
		return parts
			.slice(0, 2)
			.map((p) => p[0])
			.join('');
	}
</script>

<!-- ════════════════════════════════════════════════════════════════════════
     Professors / Jury Section
     ════════════════════════════════════════════════════════════════════════ -->
<section
	id="professors"
	dir="rtl"
	class="relative overflow-hidden bg-gradient-to-b from-[#0a0f2e] via-[#0d1544] to-[#0a0f2e] py-24"
>
	<!-- Decorative blobs -->
	<div
		class="pointer-events-none absolute -right-32 top-0 h-[500px] w-[500px] rounded-full bg-[#1a237e]/20 blur-[120px]"
	></div>
	<div
		class="pointer-events-none absolute -left-32 bottom-0 h-[400px] w-[400px] rounded-full bg-[#0D47A1]/15 blur-[100px]"
	></div>

	<div class="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
		<!-- Section header -->
		<div
			class="mb-16 text-center transition-all duration-700 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-8 opacity-0'}"
		>
			<span
				class="mb-4 inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-900/30 px-4 py-1.5 text-sm font-medium text-blue-300"
			>
				<span class="h-1.5 w-1.5 animate-pulse rounded-full bg-blue-400"></span>
				هیئت علمی و داوران
			</span>
			<h2 class="mt-4 text-4xl font-bold text-white md:text-5xl">
				اساتید و
				<span class="bg-gradient-to-l from-blue-400 to-cyan-300 bg-clip-text text-transparent">
					داوران
				</span>
			</h2>
			<p class="mx-auto mt-4 max-w-2xl text-lg leading-relaxed text-blue-200/70">
				برترین متخصصان علوم اعصاب شناختی از دانشگاه‌های معتبر جهانی در کنار شما هستند
			</p>
			<div class="mx-auto mt-6 h-1 w-20 rounded-full bg-gradient-to-l from-blue-500 to-cyan-400"></div>
		</div>

		<!-- ── Faculty grid ───────────────────────────────────────────────────── -->
		<div
			class="grid grid-cols-2 gap-5 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6"
		>
			{#each faculty as professor, i}
				<div
					class="group flex flex-col items-center gap-3 rounded-2xl border border-white/5 bg-white/5 p-4
					       backdrop-blur-sm transition-all duration-500 hover:-translate-y-1 hover:border-blue-500/30
					       hover:bg-white/10 hover:shadow-lg hover:shadow-blue-900/30
					       {visible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}"
					style="transition-delay: {Math.min(i * 50, 600)}ms;"
				>
					<!-- Avatar -->
					<div class="relative">
						<div
							class="h-20 w-20 overflow-hidden rounded-full ring-2 ring-blue-500/30 transition-all duration-300 group-hover:ring-blue-400/60 group-hover:ring-offset-2 group-hover:ring-offset-[#0d1544] sm:h-24 sm:w-24"
						>
							{#if professor.photo}
								<img
									src={professor.photo}
									alt={professor.name}
									class="h-full w-full object-cover object-top"
									loading="lazy"
								/>
							{:else}
								<div
									class="flex h-full w-full items-center justify-center bg-gradient-to-br from-blue-700 to-blue-900 text-xl font-bold text-white"
								>
									{initials(professor.name)}
								</div>
							{/if}
						</div>
						{#if professor.badge}
							<span
								class="absolute -bottom-1 -left-1 rounded-full bg-gradient-to-r from-blue-600 to-cyan-500 px-1.5 py-0.5 text-[10px] font-bold text-white shadow"
							>
								{professor.badge}
							</span>
						{/if}
					</div>

					<!-- Name & affiliation -->
					<div class="text-center">
						<p class="text-sm font-semibold leading-snug text-white">{professor.name}</p>
						<p class="mt-1 text-[11px] leading-tight text-blue-300/70">{professor.affiliation}</p>
					</div>
				</div>
			{/each}
		</div>

	</div>
</section>
