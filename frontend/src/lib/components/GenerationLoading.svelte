<script>
	export let articleType = '';
</script>

<div class="card text-center">
	<div class="mb-6">
		<div class="text-6xl mb-4 animate-pulse">✨</div>
		<h2 class="text-2xl font-bold text-gray-900 mb-2">Generating Your Photoshoot</h2>
		<p class="text-gray-600">
			Creating professional photos of your {articleType}...
		</p>
	</div>

	<div class="mb-8">
		<div class="max-w-md mx-auto">
			<!-- Loading Bar -->
			<div class="h-2 bg-gray-200 rounded-full overflow-hidden">
				<div class="h-full bg-gradient-to-r from-amber-400 to-amber-500 animate-pulse"></div>
			</div>
		</div>
	</div>

	<!-- Studio Lights Animation -->
	<div class="flex justify-center gap-4 mb-8">
		<div
			class="w-4 h-32 bg-gradient-to-b from-amber-300 to-transparent rounded-full opacity-50 animate-pulse"
			style="animation-delay: 0s"
		></div>
		<div
			class="w-4 h-32 bg-gradient-to-b from-amber-300 to-transparent rounded-full opacity-50 animate-pulse"
			style="animation-delay: 0.2s"
		></div>
		<div
			class="w-4 h-32 bg-gradient-to-b from-amber-300 to-transparent rounded-full opacity-50 animate-pulse"
			style="animation-delay: 0.4s"
		></div>
	</div>

	<p class="text-gray-600">This typically takes 30-40 seconds</p>
</div>
