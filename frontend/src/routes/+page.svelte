<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { userStore, creditsStore } from '$lib/stores';

	let isLoading = true;

	onMount(async () => {
		// Check if user is already logged in
		const token = localStorage.getItem('firebaseToken');
		
		if (token) {
			// User is logged in, redirect to dashboard
			goto('/dashboard');
		} else {
			// Check anonymous trial status
			const trialStatus = localStorage.getItem('anonTrialStatus');
			if (!trialStatus) {
				// First time anonymous user, fetch trial status
				try {
					const response = await fetch('/api/anon/trial-status');
					if (response.ok) {
						const data = await response.json();
						localStorage.setItem('anonTrialStatus', JSON.stringify(data));
					}
				} catch (error) {
					console.error('Failed to fetch trial status:', error);
				}
			}
		}
		
		isLoading = false;
	});
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
	<!-- Navigation -->
	<nav class="bg-black bg-opacity-50 backdrop-blur-md sticky top-0 z-50">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between items-center h-16">
				<a href="/" class="text-2xl font-bold text-amber-400">✨ Studio</a>
				<div class="flex gap-4">
					<a href="/login" class="text-white hover:text-amber-400 transition">Login</a>
					<a href="/create-shoot" class="btn-primary text-sm">Create</a>
				</div>
			</div>
		</div>
	</nav>

	<!-- Hero Section -->
	<div class="relative overflow-hidden">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-24">
			<div class="text-center">
				<h1 class="text-5xl md:text-7xl font-bold text-white mb-6">
					AI Fashion Studio
				</h1>
				<p class="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
					Upload reference images. Get professional fashion photoshoots in seconds.
				</p>

				{#if !isLoading}
					<div class="flex flex-col sm:flex-row gap-4 justify-center">
						<a href="/create-shoot" class="btn-primary">
							Try Free (3 Images)
						</a>
						<a href="/login" class="btn-secondary">
							Login / Sign Up
						</a>
					</div>
				{/if}
			</div>

			<!-- Feature Cards -->
			<div class="mt-20 grid md:grid-cols-3 gap-8">
				<div class="card text-center">
					<div class="text-4xl mb-4">📸</div>
					<h3 class="text-xl font-bold text-gray-900 mb-2">Multiple References</h3>
					<p class="text-gray-600">Upload multiple angles and views for better results</p>
				</div>

				<div class="card text-center">
					<div class="text-4xl mb-4">🎨</div>
					<h3 class="text-xl font-bold text-gray-900 mb-2">Studio Quality</h3>
					<p class="text-gray-600">Professional lighting and composition instantly</p>
				</div>

				<div class="card text-center">
					<div class="text-4xl mb-4">⚡</div>
					<h3 class="text-xl font-bold text-gray-900 mb-2">Lightning Fast</h3>
					<p class="text-gray-600">Get your photoshoot in under 60 seconds</p>
				</div>
			</div>
		</div>
	</div>

	<!-- Footer -->
	<footer class="bg-black bg-opacity-50 text-center py-8 text-gray-400 mt-20">
		<p>&copy; 2026 Fashion Photoshoot Studio. All rights reserved.</p>
	</footer>
</div>
