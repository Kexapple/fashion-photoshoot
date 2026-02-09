<script>
	import { createEventDispatcher } from 'svelte';

	export let generatedImages = [];
	export let shootId = '';

	const dispatch = createEventDispatcher();

	function handleDownload(imageUrl) {
		const link = document.createElement('a');
		link.href = imageUrl;
		link.download = `photoshoot-${shootId}-${Date.now()}.jpg`;
		link.click();
	}

	function handleCreateNew() {
		dispatch('createNew');
	}

	function handleBackToDashboard() {
		dispatch('backToDashboard');
	}
</script>

<div class="card">
	<div class="text-center mb-8">
		<div class="text-5xl mb-4">🎉</div>
		<h1 class="text-3xl font-bold text-gray-900 mb-2">Your Photoshoot is Ready!</h1>
		<p class="text-gray-600">Professional images generated in seconds</p>
	</div>

	<!-- Gallery -->
	<div class="mb-8">
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each generatedImages as image, index}
				<div class="group relative overflow-hidden rounded-lg bg-gray-100">
					<img
						src={image}
						alt="Generated image {index + 1}"
						class="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
					/>
					<div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-bg duration-300 flex items-center justify-center">
						<button
							on:click={() => handleDownload(image)}
							class="opacity-0 group-hover:opacity-100 px-4 py-2 bg-amber-400 text-gray-900 font-semibold rounded-lg transition"
						>
							⬇️ Download
						</button>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Actions -->
	<div class="flex flex-col sm:flex-row gap-4">
		<button
			on:click={handleCreateNew}
			class="btn-primary flex-1"
		>
			✨ Create Another
		</button>
		<button
			on:click={handleBackToDashboard}
			class="btn-secondary flex-1"
		>
			Back to Dashboard
		</button>
	</div>

	<p class="text-center text-sm text-gray-600 mt-6">
		Shoot ID: {shootId}
	</p>
</div>
