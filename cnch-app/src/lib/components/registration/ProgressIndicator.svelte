<script lang="ts">
	import { Check } from 'lucide-svelte';
	import { cn } from '$lib/utils';

	let { currentStep = $bindable(1), steps = ['مرحله ۱', 'مرحله ۲', 'مرحله ۳'] } = $props();

	const totalSteps = $derived(steps.length);
	const progress = $derived(Math.min((currentStep / totalSteps) * 100, 100));
</script>

<div dir="rtl" class="w-full py-8">
	<!-- Progress Bar -->
	<div class="relative mb-8">
		<div class="h-2 w-full overflow-hidden rounded-full bg-gray-200">
			<div
				class="h-full bg-primary transition-all duration-500 ease-out"
				style="width: {progress}%"
			></div>
		</div>
	</div>

	<!-- Steps -->
	<div class="flex items-center justify-between">
		{#each steps as label, idx}
			{@const number = idx + 1}
			<div class="flex flex-1 flex-col items-center">
				<!-- Step Circle -->
				<div
					class={cn(
						'flex size-12 items-center justify-center rounded-full border-2 font-semibold transition-all duration-300',
						currentStep > number
							? 'border-primary bg-primary text-primary-foreground'
							: currentStep === number
								? 'border-primary bg-primary text-primary-foreground'
								: 'border-gray-300 bg-white text-gray-400'
					)}
				>
					{#if currentStep > number}
						<Check class="size-6" />
					{:else}
						<span class="text-sm">{number}</span>
					{/if}
				</div>

				<!-- Step Label -->
				<p
					class={cn(
						'mt-2 text-center text-sm font-medium transition-colors',
						currentStep >= number ? 'text-gray-900' : 'text-gray-400'
					)}
				>
					{label}
				</p>
			</div>

			<!-- Connector Line (except for last step) -->
			{#if number < totalSteps}
				<div class="relative -mt-8 flex-1">
					<div class="h-0.5 w-full bg-gray-200">
						<div
							class={cn(
								'h-full bg-primary transition-all duration-500',
								currentStep > number ? 'w-full' : 'w-0'
							)}
						></div>
					</div>
				</div>
			{/if}
		{/each}
	</div>
</div>
