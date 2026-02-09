<script>
	import { onMount } from 'svelte';
	import { getBackendUrl } from '$lib/api';

	let creditPackages = [];
	let isLoading = true;
	let selectedPackage = null;
	let paymentMethod = 'jazzcash';
	let phoneNumber = '';
	let isProcessing = false;
	let errorMessage = '';
	let successMessage = '';

	const PAYMENT_METHODS = [
		{ id: 'jazzcash', name: 'JazzCash' },
		{ id: 'easypaisa', name: 'EasyPaisa' }
	];

	onMount(async () => {
		try {
			const response = await fetch(`${getBackendUrl()}/api/credits/packages`);
			if (response.ok) {
				const data = await response.json();
				creditPackages = data.packages;
				selectedPackage = creditPackages[1]; // Default to featured package
			}
		} catch (error) {
			errorMessage = 'Failed to load credit packages';
		}
		isLoading = false;
	});

	async function handlePayment() {
		if (!phoneNumber) {
			errorMessage = 'Please enter your phone number';
			return;
		}

		isProcessing = true;
		errorMessage = '';
		successMessage = '';

		try {
			// In real implementation, redirect to payment gateway
			// For now, show mock payment flow
			successMessage = `Redirecting to ${paymentMethod.toUpperCase()} payment...`;
			
			// Simulate 2-second payment processing
			setTimeout(() => {
				successMessage = `Payment of PKR ${selectedPackage.priceInPkr} successful! ${selectedPackage.credits} credits added.`;
			}, 2000);
		} catch (error) {
			errorMessage = `Payment error: ${error.message}`;
		}

		isProcessing = false;
	}
</script>

<svelte:head>
	<title>Buy Credits - Fashion Studio</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
	<div class="max-w-4xl mx-auto">
		<div class="card">
			<h1 class="text-3xl font-bold text-gray-900 mb-2">Buy Credits</h1>
			<p class="text-gray-600 mb-8">Generate more professional photoshoots with credits</p>

			{#if errorMessage}
				<div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
					<p class="text-red-700">{errorMessage}</p>
				</div>
			{/if}

			{#if successMessage}
				<div class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
					<p class="text-green-700">{successMessage}</p>
				</div>
			{/if}

			{#if !isLoading && creditPackages.length > 0}
				<!-- Credit Packages -->
				<div class="mb-12">
					<h2 class="text-xl font-bold text-gray-900 mb-6">Select Package</h2>
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
						{#each creditPackages as package}
							<button
								on:click={() => (selectedPackage = package)}
								class={`p-6 border-2 rounded-lg transition ${
									selectedPackage?.id === package.id
										? 'border-amber-400 bg-amber-50'
										: 'border-gray-300 hover:border-amber-400'
								}`}
							>
								<div class="text-3xl font-bold text-gray-900 mb-2">
									{package.credits}
								</div>
								<p class="text-sm text-gray-600 mb-2">Credits</p>
								<p class="text-lg font-semibold text-amber-600">
									PKR {package.priceInPkr}
								</p>
								{#if package.featured}
									<p class="text-xs text-amber-600 font-semibold mt-2">POPULAR</p>
								{/if}
							</button>
						{/each}
					</div>
				</div>

				<!-- Selected Package Details -->
				{#if selectedPackage}
					<div class="bg-gray-50 p-6 rounded-lg mb-8">
						<h3 class="text-lg font-bold text-gray-900 mb-4">Order Summary</h3>
						<div class="flex justify-between items-center border-b border-gray-200 pb-4 mb-4">
							<span class="text-gray-600">{selectedPackage.credits} Credits</span>
							<span class="font-semibold text-gray-900">PKR {selectedPackage.priceInPkr}</span>
						</div>
						<div class="flex justify-between items-center">
							<span class="text-gray-600">Rate per credit</span>
							<span class="font-semibold text-gray-900">
								PKR {Math.round(selectedPackage.priceInPkr / selectedPackage.credits)}
							</span>
						</div>
					</div>
				{/if}

				<!-- Payment Method Selection -->
				<div class="mb-8">
					<h2 class="text-xl font-bold text-gray-900 mb-6">Payment Method</h2>
					<div class="space-y-3">
						{#each PAYMENT_METHODS as method}
							<label class="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50">
								<input
									type="radio"
									bind:group={paymentMethod}
									value={method.id}
									class="mr-3"
								/>
								<span class="font-medium text-gray-900">{method.name}</span>
							</label>
						{/each}
					</div>
				</div>

				<!-- Phone Number Input -->
				<div class="mb-8">
					<label class="block text-sm font-medium text-gray-700 mb-2">
						Phone Number
					</label>
					<input
						type="tel"
						bind:value={phoneNumber}
						placeholder="+92xxxxxxxxxx or 03xxxxxxxxxx"
						class="input-field"
						disabled={isProcessing}
					/>
					<p class="text-sm text-gray-600 mt-2">
						Your phone number for payment verification
					</p>
				</div>

				<!-- Payment Button -->
				<button
					on:click={handlePayment}
					disabled={!selectedPackage || !phoneNumber || isProcessing}
					class="btn-primary w-full disabled:opacity-50"
				>
					{isProcessing
						? 'Processing Payment...'
						: `Pay PKR ${selectedPackage?.priceInPkr || 0}`}
				</button>
			{:else}
				<div class="text-center py-12">
					<p class="text-gray-600">Loading credit packages...</p>
				</div>
			{/if}
		</div>
	</div>
</div>
