<script>
	import { v4 as uuidv4 } from 'uuid';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { userStore, creditsStore } from '$lib/stores';
	import { getBackendUrl } from '$lib/api';
	import UploadArea from '$lib/components/UploadArea.svelte';
	import GenerationLoading from '$lib/components/GenerationLoading.svelte';
	import ResultGallery from '$lib/components/ResultGallery.svelte';

	let isAuthenticated = false;
	let token = '';
	let uploadedImages = [];
	let articleType = '';
	let styleNotes = '';
	let imageSize = 'medium';
	let isGenerating = false;
	let generatedImages = [];
	let shootId = '';
	let currentStep = 'upload'; // upload, review, generating, results
	let errorMessage = '';
	let trialRemaining = 3;

	const ARTICLE_TYPES = [
		'Shirt',
		'Dress',
		'Pants',
		'Jacket',
		'Suit',
		'Skirt',
		'Sweater',
		'Coat'
	];

	const IMAGE_SIZES = [
		{ id: 'small', label: 'Small (512x512)', cost: '1' },
		{ id: 'medium', label: 'Medium (768x768)', cost: '1' },
		{ id: 'large', label: 'Large (1024x1024)', cost: '1' }
	];

	onMount(async () => {
		token = localStorage.getItem('firebaseToken');
		
		if (token) {
			isAuthenticated = true;
			// Fetch user credits
			try {
				const response = await fetch(`${getBackendUrl()}/api/user/credits?id_token=${token}`);
				if (response.ok) {
					const data = await response.json();
					creditsStore.set(data.credits);
				}
			} catch (error) {
				console.error('Failed to fetch credits:', error);
			}
		} else {
			// Check anonymous trial status
			try {
				const response = await fetch(`${getBackendUrl()}/api/anon/trial-status`);
				if (response.ok) {
					const data = await response.json();
					trialRemaining = data.remaining;
				}
			} catch (error) {
				console.error('Failed to fetch trial status:', error);
			}
		}
	});

	function handleImagesUploaded(event) {
		uploadedImages = event.detail;
		errorMessage = '';
	}

	async function handleGenerate() {
		errorMessage = '';

		if (uploadedImages.length === 0) {
			errorMessage = 'Please upload at least one image';
			return;
		}

		if (!articleType) {
			errorMessage = 'Please select an article type';
			return;
		}

		isGenerating = true;
		currentStep = 'generating';
		shootId = uuidv4();

		try {
			const payload = {
				articleType: articleType,
				styleNotes: styleNotes,
				imageSize: imageSize,
				uploadedImageUrls: uploadedImages,
				clientIp: 'client-ip'  // Will be overridden by server
			};

			if (token) {
				payload.idToken = token;
			}

			const response = await fetch(`${getBackendUrl()}/api/photoshoots/create`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload)
			});

			if (response.status === 402) {
				errorMessage = 'Insufficient credits. Please purchase more credits.';
				currentStep = 'upload';
				isGenerating = false;
				goto('/buy-credits');
				return;
			}

			if (!response.ok) {
				const error = await response.json();
				errorMessage = error.detail || 'Generation failed';
				currentStep = 'upload';
				isGenerating = false;
				return;
			}

			const result = await response.json();
			shootId = result.shoot_id;
			generatedImages = result.generatedImages;

			if (token) {
				creditsStore.set(result.creditsRemaining);
			} else {
				trialRemaining = result.creditsRemaining;
			}

			currentStep = 'results';
		} catch (error) {
			errorMessage = `Error: ${error.message}`;
			currentStep = 'upload';
		}

		isGenerating = false;
	}

	function handleReset() {
		uploadedImages = [];
		articleType = '';
		styleNotes = '';
		currentStep = 'upload';
		errorMessage = '';
	}

	function handleBackToDashboard() {
		if (isAuthenticated) {
			goto('/dashboard');
		} else {
			goto('/');
		}
	}
</script>

<svelte:head>
	<title>Create Photoshoot - Fashion Studio</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
	<div class="max-w-4xl mx-auto">
		{#if currentStep === 'upload' || currentStep === 'review'}
			<!-- Upload & Review Steps -->
			<div class="card">
				<div class="mb-8">
					<h1 class="text-3xl font-bold text-gray-900 mb-2">Create Photoshoot</h1>
					<p class="text-gray-600">
						{isAuthenticated
							? `You have ${$creditsStore} credits`
							: `Free trial: ${trialRemaining}/3 generations remaining`}
					</p>
				</div>

				{#if errorMessage}
					<div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
						<p class="text-red-700">{errorMessage}</p>
					</div>
				{/if}

				<!-- Step 1: Upload Images -->
				{#if currentStep === 'upload'}
					<div class="mb-8">
						<h2 class="text-xl font-bold text-gray-900 mb-4">Step 1: Upload Reference Images</h2>
						<UploadArea on:imagesUploaded={handleImagesUploaded} />
						<p class="text-sm text-gray-600 mt-4">
							Upload 1-5 reference images showing different angles of the article
						</p>
					</div>

					<!-- Article Type Selection -->
					<div class="mb-8">
						<h2 class="text-xl font-bold text-gray-900 mb-4">Step 2: Article Type</h2>
						<select bind:value={articleType} class="input-field">
							<option value="">Select article type...</option>
							{#each ARTICLE_TYPES as type}
								<option value={type}>{type}</option>
							{/each}
						</select>
					</div>

					<!-- Style Notes -->
					<div class="mb-8">
						<h2 class="text-xl font-bold text-gray-900 mb-4">Step 3: Style Notes (Optional)</h2>
						<textarea
							bind:value={styleNotes}
							placeholder="e.g., 'casual, vibrant colors, outdoor setting'"
							class="input-field h-20"
						/>
					</div>

					<!-- Image Size -->
					<div class="mb-8">
						<h2 class="text-xl font-bold text-gray-900 mb-4">Step 4: Output Size</h2>
						<div class="space-y-2">
							{#each IMAGE_SIZES as size}
								<label class="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50">
									<input type="radio" bind:group={imageSize} value={size.id} class="mr-3" />
									<span class="font-medium text-gray-900">{size.label}</span>
									<span class="ml-auto text-sm text-gray-600">{size.cost} credit</span>
								</label>
							{/each}
						</div>
					</div>

					<!-- Review Button -->
					<button
						on:click={() => (currentStep = 'review')}
						disabled={uploadedImages.length === 0 || !articleType}
						class="btn-primary w-full disabled:opacity-50"
					>
						Review & Generate
					</button>
				{/if}

				<!-- Step 2: Review -->
				{#if currentStep === 'review'}
					<div class="mb-8">
						<h2 class="text-xl font-bold text-gray-900 mb-4">Review Your Selection</h2>

						<div class="bg-gray-50 p-6 rounded-lg space-y-4">
							<div>
								<p class="text-sm text-gray-600">Article Type</p>
								<p class="text-lg font-semibold text-gray-900">{articleType}</p>
							</div>

							<div>
								<p class="text-sm text-gray-600">Style Notes</p>
								<p class="text-lg font-semibold text-gray-900">{styleNotes || '(none)'}</p>
							</div>

							<div>
								<p class="text-sm text-gray-600">Output Size</p>
								<p class="text-lg font-semibold text-gray-900">
									{IMAGE_SIZES.find((s) => s.id === imageSize)?.label}
								</p>
							</div>

							<div>
								<p class="text-sm text-gray-600">Reference Images</p>
								<div class="grid grid-cols-2 md:grid-cols-3 gap-4 mt-2">
									{#each uploadedImages as img}
										<img
											src={img}
											alt="reference"
											class="w-full h-32 object-cover rounded-lg"
										/>
									{/each}
								</div>
							</div>
						</div>
					</div>

					<div class="flex gap-4">
						<button
							on:click={() => (currentStep = 'upload')}
							class="btn-secondary flex-1"
						>
							Back
						</button>
						<button
							on:click={handleGenerate}
							class="btn-primary flex-1"
						>
							Generate Now
						</button>
					</div>
				{/if}
			</div>
		{/if}

		<!-- Generating State -->
		{#if currentStep === 'generating'}
			<GenerationLoading articleType={articleType} />
		{/if}

		<!-- Results State -->
		{#if currentStep === 'results'}
			<ResultGallery
				{generatedImages}
				{shootId}
				on:backToDashboard={handleBackToDashboard}
				on:createNew={handleReset}
			/>
		{/if}
	</div>
</div>
