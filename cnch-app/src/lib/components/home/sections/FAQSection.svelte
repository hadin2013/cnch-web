<script>
	import {
		Accordion,
		AccordionContent,
		AccordionItem,
		AccordionTrigger
	} from '$lib/components/ui/accordion';
	import { HelpCircle } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let visible = $state(false);

	const faqs = [
		{
			question: 'آیا دانش‌آموزان برای شرکت در این مسابقه نیاز به پیش‌زمینه علمی خاصی دارند؟',
			answer:
				'خیر. فاز اول و دوم مسابقه دقیقاً برای همین طراحی شده که دانش‌آموزان با هر سطحی از دانش (اما با علاقه و کنجکاوی زیاد) وارد شوند و آموزش‌های لازم را از اساتید برتر دریافت کنند.'
		},
		{
			question: 'این مسابقه چه کمکی به آینده تحصیلی دانش آموزان می‌کند؟',
			answer:
				'این مسابقه مهارت‌هایی مانند تفکر انتقادی، تحلیل علمی، درک مفاهیم زیستی-شناختی و آشنایی با حوزه‌های نوین علمی را تقویت می‌کند؛ مهارت‌هایی که در مسیر تحصیلی و شغلی آینده بسیار ارزشمند هستند.'
		},
		{
			question: 'مسابقه حضوری است یا آنلاین؟',
			answer:
				'تمامی مراحل مسابقه به صورت آنلاین برگزار می شود تا دانش آموزان سراسر کشور بتوانند دسترسی لازم به منابع را داشته باشند. تنها مرحله حضوری مسابقه، مرحله نهایی و اهدای جوائز به گروه های برگزیده است که محل برگزاری آن متعاقبا اعلام خواهد شد.'
		},
		{
			question: 'نقش منتورها در این مسابقه چیست؟',
			answer:
				'هر تیم در مراحل اصلی مسابقه تحت نظر یک منتور (راهنما) قرار می‌گیرد. منتورها به دانش‌آموزان کمک می‌کنند تا سوال پژوهشی خود را دقیق کنند، به داده‌های واقعی دسترسی داشته باشند و در نهایت یک پروژه‌ی علمی استاندارد ارائه دهند.'
		},
		{
			question: 'جوایز و حمایت‌های مسابقه شامل چه مواردی است؟',
			answer:
				'علاوه بر جوایز نقدی برای تیم‌های برتر، برگزیدگان جایزه معتبر "اهوازی" (یادبود پزشک بزرگ ایرانی قرن چهارم) را دریافت می‌کنند. همچنین: عضویت در انجمن CNCH برای حمایت‌های بعدی، تسهیل مسیر ورود به جشنواره جوان خوارزمی، کمک به تولید محصول، کارآموزی و رزومه‌سازی برای دانشگاه.'
		},
		{
			question: 'آیا دانش‌آموزان مدارس غیرسمپاد هم می‌توانند شرکت کنند؟',
			answer:
				'بله. طبق شرح وظایف تیم مسابقات علوم اعصاب شناختی، تمرکز بر جذب تمامی دانش‌آموزان مستعد (اعم از سمپادی و غیرسمپادی) است تا عدالت آموزشی در حوزه علوم شناختی برقرار شود.'
		},
		{
			question: 'هزینه راه اندازی یک پروژه علمی در این مسابقه چگونه است؟',
			answer:
			'هزینه‌های احتمالی فاز عملی (مثل خرید قطعات یا ابزار خاص) بر عهده تیم دانش‌آموزی است. مدارس (به‌ویژه سمپاد) معمولاً در تامین فضا و تجهیزات به دانش‌آموزان کمک می‌کنند. همچنین ما روش‌های اجرای پروژه با کمترین هزینه (با استفاده از داده‌های باز) را به شما آموزش می‌دهیم.'
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

		const section = document.getElementById('faq');
		if (section) observer.observe(section);

		return () => observer.disconnect();
	});

	const reducedMotion =
		typeof window !== 'undefined'
			? window.matchMedia('(prefers-reduced-motion: reduce)').matches
			: false;
</script>

<section class="bg-gradient-to-b from-gray-50 to-white py-16 md:py-24" id="faq">
	<div class="container mx-auto px-4 sm:px-6 lg:px-8">
		<!-- Section Header -->
		<div class="mb-12 text-center">
			<div class="mb-6 flex justify-center">
				<div class="rounded-full bg-gradient-to-br from-blue-100 to-purple-100 p-4">
					<HelpCircle class="h-12 w-12 text-blue-600" />
				</div>
			</div>
			<h2 class="mb-4 text-3xl font-bold text-gray-900 md:text-4xl">سوالات متداول</h2>
			<p class="mx-auto max-w-2xl text-lg text-gray-600">
				پاسخ به پرسش‌های رایج درباره مسابقه ملی علوم اعصاب شناختی
			</p>
			<div class="mx-auto mt-4 h-1 w-24 rounded-full bg-gradient-to-r from-blue-500 to-purple-500">
			</div>
		</div>

		<!-- FAQ Accordion -->
		<div
			class="mx-auto max-w-3xl transition-all duration-700 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-8 opacity-0'}"
		>
			<Accordion type="single" collapsible class="space-y-4">
				{#each faqs as faq, i}
					<AccordionItem
						value="item-{i}"
						class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm transition-all duration-300 {!reducedMotion
							? 'hover:shadow-md'
							: ''}"
						style="transition-delay: {i * 50}ms"
					>
						<AccordionTrigger
							class="px-6 py-4 text-right font-semibold text-gray-900 transition-colors hover:bg-gray-50 hover:text-blue-600 [&[data-state=open]]:bg-blue-50 [&[data-state=open]]:text-blue-600"
						>
							<div class="flex items-start gap-3">
								<span
									class="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-100 text-sm font-bold text-blue-600"
								>
									{i + 1}
								</span>
								<span class="text-right leading-relaxed">{faq.question}</span>
							</div>
						</AccordionTrigger>
						<AccordionContent class="bg-gray-50 px-6 py-4 text-gray-700 leading-relaxed">
							<div class="mr-9">
								{faq.answer}
							</div>
						</AccordionContent>
					</AccordionItem>
				{/each}
			</Accordion>
		</div>

		<!-- Contact CTA -->
		<div
			class="mt-12 text-center transition-all duration-700 delay-400 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-8 opacity-0'}"
		>
			<p class="text-gray-600">
				سوال دیگری دارید؟
				<a
					href="https://t.me/Blogishadmin"
					target="_blank"
					rel="noopener noreferrer"
					class="font-semibold text-blue-600 underline transition-colors hover:text-blue-700"
				>
					با ما تماس بگیرید
				</a>
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
