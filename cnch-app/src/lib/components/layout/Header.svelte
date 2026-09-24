<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Menu, X, LayoutDashboard, UserRound, LogOut, ShieldCheck } from 'lucide-svelte';
	import mainLogo from '$lib/assets/logos/main.jpg';
	import type { AuthUser } from '$lib/utils/auth';

	let { auth = null }: { auth?: AuthUser | null } = $props();

	let mobileMenuOpen = $state(false);
	let scrolled = $state(false);

	const isAdmin = $derived(!!auth && auth.role === 'admin');

	$effect(() => {
		const handleScroll = () => {
			scrolled = window.scrollY > 20;
		};

		if (typeof window !== 'undefined') {
			window.addEventListener('scroll', handleScroll);
			return () => window.removeEventListener('scroll', handleScroll);
		}
	});

	const navLinks = [
		{ href: '/#about', label: 'درباره مسابقه' },
		{ href: '/#professors', label: 'اساتید و داوران' },
		{ href: '/#timeline', label: 'مسیر مسابقه' },
		{ href: '/#prizes', label: 'جوایز' },
		{ href: '/#faq', label: 'سوالات متداول' },
		{ href: '/#contact', label: 'تماس با ما' }
	];

	function closeMenu() {
		mobileMenuOpen = false;
	}
</script>

<header
	class="sticky top-0 z-50 w-full transition-all duration-300 {scrolled
		? 'shadow-lg'
		: ''} bg-[#0D47A1]"
>
	<div class="container mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex h-20 items-center justify-between">
			<!-- Logo Section (Right side in RTL) -->
			<a href="/" class="flex items-center gap-3 transition-opacity hover:opacity-90">
				<img src={mainLogo} alt="CNCH Logo" class="h-12 w-auto object-contain" />
				<h1 class="text-lg font-bold text-white md:text-xl">مسابقات ملی علوم اعصاب شناختی</h1>
			</a>

			<!-- Desktop Navigation (Center) -->
			<nav class="hidden md:block">
				<ul class="flex items-center gap-8">
					{#each navLinks as link}
						<li>
							<a
								href={link.href}
								class="text-sm font-medium text-white transition-colors hover:text-blue-100"
							>
								{link.label}
							</a>
						</li>
					{/each}
				</ul>
			</nav>

			<!-- Auth / CTA (Left side in RTL) -->
			<div class="flex items-center gap-3">
				{#if auth}
					<span class="hidden items-center gap-2 text-sm font-medium text-blue-100 lg:flex">
						<UserRound class="size-4" />
						{auth.name || auth.email}
					</span>
					<Button
						href="/profile"
						variant="ghost"
						class="hidden text-white hover:bg-blue-800 hover:text-white md:inline-flex"
					>
						<LayoutDashboard class="size-4" />
						پروفایل
					</Button>
					{#if isAdmin}
						<Button
							href="/admin"
							variant="ghost"
							class="hidden text-white hover:bg-blue-800 hover:text-white md:inline-flex"
						>
							<ShieldCheck class="size-4" />
							مدیریت
						</Button>
					{/if}
					<form action="/profile?/logout" method="POST" class="hidden md:block">
						<button
							type="submit"
							class="inline-flex items-center gap-2 rounded-md p-2 text-sm text-blue-100 transition-colors hover:bg-blue-800 hover:text-white"
						>
							<LogOut class="size-4" />
							خروج
						</button>
					</form>
				{:else}
					<Button
						href="/login"
						variant="ghost"
						class="hidden text-white hover:bg-blue-800 hover:text-white md:inline-flex"
					>
						ورود
					</Button>
					<Button
						href="/register"
						class="hidden bg-white text-[#0D47A1] hover:bg-blue-50 md:inline-flex"
					>
						ثبت‌نام مسابقه
					</Button>
				{/if}

				<!-- Mobile Menu Toggle -->
				<button
					onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
					class="inline-flex items-center justify-center rounded-md p-2 text-white hover:bg-blue-800 md:hidden"
					aria-label="Toggle menu"
				>
					{#if mobileMenuOpen}
						<X class="h-6 w-6" />
					{:else}
						<Menu class="h-6 w-6" />
					{/if}
				</button>
			</div>
		</div>
	</div>

	<!-- Mobile Menu -->
	{#if mobileMenuOpen}
		<div class="border-t border-blue-600 md:hidden">
			<nav class="container mx-auto space-y-1 bg-[#0D47A1] px-4 pt-2 pb-4">
				{#each navLinks as link}
					<a
						href={link.href}
						onclick={closeMenu}
						class="block rounded-lg px-4 py-3 text-base font-medium text-white hover:bg-blue-800"
					>
						{link.label}
					</a>
				{/each}
				<div class="space-y-2 pt-4">
					{#if auth}
						<p class="px-4 pb-1 text-sm text-blue-100">ورود با: {auth.name || auth.email}</p>
						<Button href="/profile" class="w-full bg-white text-[#0D47A1] hover:bg-blue-50">
							پروفایل
						</Button>
						{#if isAdmin}
							<Button href="/admin" class="w-full text-white hover:bg-blue-800">پنل مدیریت</Button>
						{/if}
						<form action="/profile?/logout" method="POST">
							<button
								type="submit"
								class="w-full rounded-md px-4 py-3 text-center text-base font-medium text-blue-100 hover:bg-blue-800"
							>
								خروج
							</button>
						</form>
					{:else}
						<Button href="/login" class="w-full text-white hover:bg-blue-800">ورود</Button>
						<Button href="/register" class="w-full bg-white text-[#0D47A1] hover:bg-blue-50">
							ثبت‌نام مسابقه
						</Button>
					{/if}
				</div>
			</nav>
		</div>
	{/if}
</header>
