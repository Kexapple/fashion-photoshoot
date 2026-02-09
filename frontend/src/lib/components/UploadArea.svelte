<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let fileDragActive = false;
	let imageFiles = [];
	let previewUrls = [];
	let isLoading = false;

	function handleDragOver(e) {
		e.preventDefault();
		fileDragActive = true;
	}

	function handleDragLeave() {
		fileDragActive = false;
	}

	function processFiles(files) {
		isLoading = true;
		const fileArray = Array.from(files);
		const validFiles = fileArray.filter((file) => file.type.startsWith('image/'));

		if (validFiles.length === 0) {
			alert('Please select valid image files');
			isLoading = false;
			return;
		}

		if (validFiles.length + previewUrls.length > 5) {
			alert('Maximum 5 images allowed');
			isLoading = false;
			return;
		}

		validFiles.forEach((file) => {
			const reader = new FileReader();
			reader.onload = (e) => {
				previewUrls = [...previewUrls, e.target.result];
				if (previewUrls.length === validFiles.length) {
					dispatch('imagesUploaded', previewUrls);
					isLoading = false;
				}
			};
			reader.readAsDataURL(file);
		});

		imageFiles = [...imageFiles, ...validFiles];
	}

	function handleDrop(e) {
		e.preventDefault();
		fileDragActive = false;
		processFiles(e.dataTransfer.files);
	}

	function handleFileSelect(e) {
		processFiles(e.target.files);
	}

	function removeImage(index) {
		previewUrls = previewUrls.filter((_, i) => i !== index);
		dispatch('imagesUploaded', previewUrls);
	}
</script>

<div
	class="border-2 border-dashed rounded-lg p-8 text-center transition"
	class:border-amber-400={fileDragActive}
	class:bg-amber-50={fileDragActive}
	class:border-gray-300={!fileDragActive}
	on:dragover={handleDragOver}
	on:dragleave={handleDragLeave}
	on:drop={handleDrop}
>
	<div class="mb-4">
		<div class="text-5xl mb-2">📸</div>
		<h3 class="text-lg font-bold text-gray-900">Drag & drop your images</h3>
		<p class="text-gray-600 text-sm">or click to browse</p>
	</div>

	<input
		type="file"
		multiple
		accept="image/*"
		on:change={handleFileSelect}
		class="hidden"
		id="fileInput"
		disabled={isLoading}
	/>

	<label for="fileInput" class="cursor-pointer">
		<button
			type="button"
			on:click={() => document.getElementById('fileInput').click()}
			class="btn-secondary"
			disabled={isLoading}
		>
			{isLoading ? 'Processing...' : 'Select Images'}
		</button>
	</label>

	<p class="text-xs text-gray-500 mt-4">
		Supported: JPEG, PNG, WebP (Max 5 images, 10MB each)
	</p>
</div>

<!-- Preview Section -->
{#if previewUrls.length > 0}
	<div class="mt-8">
		<h3 class="text-lg font-bold text-gray-900 mb-4">Selected Images ({previewUrls.length}/5)</h3>
		<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
			{#each previewUrls as preview, index}
				<div class="relative group">
					<img
						src={preview}
						alt="preview {index + 1}"
						class="w-full h-32 object-cover rounded-lg"
					/>
					<button
						type="button"
						on:click={() => removeImage(index)}
						class="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center opacity-0 group-hover:opacity-100 transition"
					>
						✕
					</button>
				</div>
			{/each}
		</div>
	</div>
{/if}
