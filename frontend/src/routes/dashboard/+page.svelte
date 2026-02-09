<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { creditsStore } from '$lib/stores';
	import { getBackendUrl } from '$lib/api';

	let user = null;
	let credits = 0;
	let photoshoots = [];
	let isLoading = true;
	let token = '';

	onMount(async () => {
		token = localStorage.getItem('firebaseToken');

		if (!token) {
			goto('/auth/login');
			return;
		}

		// Fetch user profile
		try {
			const response = await fetch(`${getBackendUrl()}/api/auth/user/profile?id_token=${token}`);
			if (response.ok) {
				user = await response.json();
				credits = user.credits;
				creditsStore.set(credits);
			} else {
				goto('/auth/login');
			}
		} catch (error) {
			console.error('Failed to fetch profile:', error);
		}

		isLoading = false;
	});

	function handleLogout() {
		localStorage.removeItem('firebaseToken');
		goto('/');
	}

	function handleCreateNew() {
		goto('/create-shoot');
	}

	function handleBuyCredits() {
		goto('/buy-credits');
	}
</script>

<svelte:head>
	<title>Dashboard - Fashion Studio</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
	<div class="max-w-6xl mx-auto">
		{#if !isLoading && user}
			<!-- Header -->
			<div class="flex justify-between items-center mb-12">
				<div>
					<h1 class="text-4xl font-bold text-white mb-2">Welcome, {user.displayName}!</h1>
					<p class="text-gray-400">Your fashion photoshoot studio</p>
				</div>
				<button
					on:click={handleLogout}
					class="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
				>
					Logout
				</button>
			</div>

			<!-- Credits Card -->
			<div class="bg-gradient-to-r from-amber-400 to-amber-500 rounded-lg p-8 mb-12 text-gray-900">
				<div class="flex justify-between items-center">
					<div>
						<p class="text-sm font-semibold opacity-80">Available Credits</p>
						<p class="text-5xl font-bold">{credits}</p>
					</div>
					<button
						on:click={handleBuyCredits}
						class="px-6 py-3 bg-gray-900 hover:bg-black text-white font-semibold rounded-lg transition"
					>
						+ Buy Credits
					</button>
				</div>
			</div>

			<!-- Create New Button -->
			<button
				on:click={handleCreateNew}
				class="w-full mb-12 py-8 border-2 border-dashed border-gray-500 rounded-lg hover:border-amber-400 hover:bg-gray-800 transition flex flex-col items-center justify-center"
			>
				<div class="text-5xl mb-4">✨</div>
				<h2 class="text-2xl font-bold text-white">Create New Photoshoot</h2>
				<p class="text-gray-400 mt-2">Upload images and generate professional photoshoots</p>
			</button>

			<!-- Recent Photoshoots -->
			<div>
				<h2 class="text-2xl font-bold text-white mb-6">Your Photoshoots</h2>
				{#if photoshoots.length === 0}
					<div class="text-center py-12">
						<p class="text-gray-400 text-lg">No photoshoots yet. Create your first one!</p>
					</div>
				{:else}
					<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
						{#each photoshoots as shoot}
							<div class="bg-white rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition">
								<img
									src={shoot.generatedImages?.[0] || 'https://via.placeholder.com/300x300'}
									alt={shoot.articleType}
									class="w-full h-48 object-cover"
								/>
								<div class="p-4">
									<h3 class="font-bold text-gray-900">{shoot.articleType}</h3>
									<p class="text-sm text-gray-600">{new Date(shoot.createdAt).toLocaleDateString()}</p>
									<p class="text-sm text-amber-600 font-semibold">
										{shoot.generatedImages?.length || 0} images
									</p>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		{:else}
			<div class="text-center py-12">
				<p class="text-white text-lg">Loading dashboard...</p>
			</div>
		{/if}
	</div>
</div>
