<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { zod4Client } from 'sveltekit-superforms/adapters';
	import { studentSchema } from '$lib/schemas/student.schema';
	import { grades, majors } from '$lib/types/registration.types';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Select from '$lib/components/ui/select';
	import * as Alert from '$lib/components/ui/alert';
	import * as Card from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { User, Phone, CreditCard, GraduationCap, Trash2, Plus } from 'lucide-svelte';
	import { untrack } from 'svelte';

	let { data, students = $bindable([]), onNext, onBack } = $props();

	const { form, errors, enhance, reset, validateForm } = untrack(() => superForm(data, {
		validators: zod4Client(studentSchema),
		resetForm: true,
		dataType: 'json'
	}));

	let selectedGrade = $derived(
		grades.find((f) => f === $form.grade) ?? 'پایه تحصیلی را انتخاب کنید'
	);
	let selectedMajor = $derived(
		majors.find((f) => f === $form.major) ?? 'رشته تحصیلی را انتخاب کنید'
	);

	async function addStudent() {
		const result = await validateForm({ update: true });
		if (result.valid) {
			students = [...students, $form];
			reset();
		}
	}

	function removeStudent(index: number) {
		students = students.filter((_, i) => i !== index);
	}

	function continueToNext() {
		if (students.length === 0) {
			alert('لطفاً حداقل یک دانش‌آموز اضافه کنید');
			return;
		}
		onNext?.();
	}
</script>

<div dir="rtl" class="w-full space-y-6">
	<div class="space-y-2">
		<h2 class="text-2xl font-bold text-gray-900">اطلاعات دانش‌آموزان</h2>
		<p class="text-sm text-gray-600">
			دانش‌آموزان گروه خود را اضافه کنید. می‌توانید چندین دانش‌آموز ثبت کنید.
		</p>
	</div>

	<!-- Added Students List -->
	{#if students.length > 0}
		<div class="space-y-3">
			<div class="flex items-center justify-between">
				<h3 class="font-semibold text-gray-900">
					دانش‌آموزان ثبت شده ({students.length})
				</h3>
			</div>
			<div class="grid gap-3 md:grid-cols-2">
				{#each students as student, index}
					<Card.Root class="overflow-hidden">
						<Card.Content class="p-4">
							<div class="flex items-start justify-between">
								<div class="space-y-1">
									<p class="font-semibold text-gray-900">
										{student.first_name}
										{student.last_name}
									</p>
									<div class="flex flex-wrap gap-2">
										<Badge variant="secondary">{student.grade}</Badge>
										<Badge variant="outline">{student.major}</Badge>
									</div>
									<p class="text-sm text-gray-600" dir="ltr">
										{student.phone_number}
									</p>
								</div>
								<Button
									variant="ghost"
									size="icon"
									onclick={() => removeStudent(index)}
									class="size-8 text-red-500 hover:bg-red-50 hover:text-red-600"
								>
									<Trash2 class="size-4" />
								</Button>
							</div>
						</Card.Content>
					</Card.Root>
				{/each}
			</div>
		</div>
	{/if}

	<!-- Add Student Form -->
	<Card.Root>
		<Card.Header>
			<Card.Title class="flex items-center gap-2">
				<Plus class="size-5" />
				فرم دانش‌آموز جدید
			</Card.Title>
		</Card.Header>
		<Card.Content>
			<form method="POST" use:enhance class="space-y-6">

				<!-- Name Fields -->
				<div class="grid gap-6 md:grid-cols-2">
					<div class="space-y-2">
						<Label for="first_name" class="text-right">
							نام <span class="text-red-500">*</span>
						</Label>
						<div class="relative">
							<User class="absolute top-3 right-3 size-5 text-gray-400" />
							<Input
								id="first_name"
								name="first_name"
								bind:value={$form.first_name}
								placeholder="نام دانش‌آموز"
								class="pr-10 text-right"
								aria-invalid={$errors.first_name ? 'true' : undefined}
							/>
						</div>
						{#if $errors.first_name}
							<p class="text-sm text-red-500">{$errors.first_name[0]}</p>
						{/if}
					</div>

					<div class="space-y-2">
						<Label for="last_name" class="text-right">
							نام خانوادگی <span class="text-red-500">*</span>
						</Label>
						<div class="relative">
							<User class="absolute top-3 right-3 size-5 text-gray-400" />
							<Input
								id="last_name"
								name="last_name"
								bind:value={$form.last_name}
								placeholder="نام خانوادگی"
								class="pr-10 text-right"
								aria-invalid={$errors.last_name ? 'true' : undefined}
							/>
						</div>
						{#if $errors.last_name}
							<p class="text-sm text-red-500">{$errors.last_name[0]}</p>
						{/if}
					</div>
				</div>

				<!-- National ID & Phone -->
				<div class="grid gap-6 md:grid-cols-2">
					<div class="space-y-2">
						<Label for="national_id" class="text-right">
							کد ملی <span class="text-red-500">*</span>
						</Label>
						<div class="relative">
							<CreditCard class="absolute top-3 right-3 size-5 text-gray-400" />
							<Input
								id="national_id"
								name="national_id"
								bind:value={$form.national_id}
								placeholder="1234567890"
								dir="ltr"
								class="pr-10 text-left"
								maxlength="10"
								aria-invalid={$errors.national_id ? 'true' : undefined}
							/>
						</div>
						{#if $errors.national_id}
							<p class="text-sm text-red-500">{$errors.national_id[0]}</p>
						{/if}
					</div>

					<div class="space-y-2">
						<Label for="phone_number" class="text-right">
							شماره موبایل <span class="text-red-500">*</span>
						</Label>
						<div class="relative">
							<Phone class="absolute top-3 right-3 size-5 text-gray-400" />
							<Input
								id="phone_number"
								name="phone_number"
								bind:value={$form.phone_number}
								placeholder="09123456789"
								dir="ltr"
								class="pr-10 text-left"
								maxlength="11"
								aria-invalid={$errors.phone_number ? 'true' : undefined}
							/>
						</div>
						{#if $errors.phone_number}
							<p class="text-sm text-red-500">{$errors.phone_number[0]}</p>
						{/if}
					</div>
				</div>

				<!-- Grade & Major -->
				<div class="grid gap-6 md:grid-cols-2">
					<div class="space-y-2">
						<Label for="grade" class="text-right">
							پایه تحصیلی <span class="text-red-500">*</span>
						</Label>
						<Select.Root name="grade" type="single" bind:value={$form.grade}>
							<Select.Trigger
								class="w-full text-right"
								aria-invalid={$errors.grade ? 'true' : undefined}
							>
								<GraduationCap class="ml-2 size-4" />
								{selectedGrade}
							</Select.Trigger>
							<Select.Portal>
								<Select.Content>
									<Select.Group>
										<Select.Label>پایه های تحصیلی</Select.Label>
										{#each grades as grade}
											<Select.Item value={grade}>{grade}</Select.Item>
										{/each}
									</Select.Group>
								</Select.Content>
							</Select.Portal>
						</Select.Root>
						<input type="hidden" name="grade" bind:value={$form.grade} />
						{#if $errors.grade}
							<p class="text-sm text-red-500">{$errors.grade[0]}</p>
						{/if}
					</div>

					<div class="space-y-2">
						<Label for="major" class="text-right">
							رشته تحصیلی <span class="text-red-500">*</span>
						</Label>
						<Select.Root name="major" type="single" bind:value={$form.major}>
							<Select.Trigger
								class="w-full text-right"
								aria-invalid={$errors.major ? 'true' : undefined}
							>
								<GraduationCap class="ml-2 size-4" />
								{selectedMajor}
							</Select.Trigger>
							<Select.Portal>
								<Select.Content>
									<Select.Group>
										<Select.Label>رشته ها</Select.Label>
										{#each majors as major}
											<Select.Item value={major}>{major}</Select.Item>
										{/each}
									</Select.Group>
								</Select.Content>
							</Select.Portal>
						</Select.Root>
						<input type="hidden" name="major" bind:value={$form.major} />
						{#if $errors.major}
							<p class="text-sm text-red-500">{$errors.major[0]}</p>
						{/if}
					</div>
				</div>

				<!-- Add Student Button -->
			<Button type="button" variant="outline" class="w-full" onclick={addStudent}>
					<Plus class="ml-2 size-4" />
					افزودن دانش‌آموز
				</Button>
			</form>
		</Card.Content>
	</Card.Root>

	<!-- Navigation Buttons -->
	<div class="flex justify-between pt-4">
		{#if onBack}
			<Button variant="outline" size="lg" onclick={onBack}>بازگشت</Button>
		{/if}
		<Button
			size="lg"
			onclick={continueToNext}
			disabled={students.length === 0}
			class="min-w-[200px]"
		>
			ادامه به تأیید نهایی
		</Button>
	</div>
</div>
