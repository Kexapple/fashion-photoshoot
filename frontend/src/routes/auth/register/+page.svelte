<script>
	import { goto } from '$app/navigation';
	import { userStore } from '$lib/stores';
	import { signUpWithEmail } from '$lib/firebase';

	let email = '';
	let password = '';
	let displayName = '';
	let isLoading = false;
	let errorMessage = '';

	async function handleSignUp() {
		isLoading = true;
		errorMessage = '';

		if (!email || !password || !displayName) {
			errorMessage = 'Please fill in all fields';
			isLoading = false;
			return;
		}

		if (password.length < 6) {
			errorMessage = 'Password must be at least 6 characters';
			isLoading = false;
			return;
		}

		try {
			const result = await signUpWithEmail(email, password, displayName);
			if (result.user) {
				userStore.set(result.user);
				const token = await result.user.getIdToken();
				localStorage.setItem('firebaseToken', token);
				
				// Register user in backend (to get first-login bonus)
				const response = await fetch('/api/auth/register', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({
						idToken: token,
						email: result.user.email,
						displayName: result.user.displayName || displayName
					})
				});

				if (response.ok) {
					await goto('/dashboard');
				} else {
					errorMessage = 'Failed to register user profile';
				}
			}
		} catch (error) {
			errorMessage = error.message;
		}
		isLoading = false;
	}
</script>

<svelte:head>
	<title>Sign Up - Fashion Studio</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center px-4">
	<div class="w-full max-w-md">
		<div class="card">
			<h1 class="text-3xl font-bold text-gray-900 mb-8 text-center">Create Account</h1>

			{#if errorMessage}
				<div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
					<p class="text-red-700 text-sm">{errorMessage}</p>
				</div>
			{/if}

			<form on:submit|preventDefault={handleSignUp} class="space-y-4">
				<div>
					<label for="displayName" class="block text-sm font-medium text-gray-700 mb-1">
						Display Name
					</label>
					<input
						type="text"
						id="displayName"
						bind:value={displayName}
						placeholder="John Doe"
						class="input-field"
						disabled={isLoading}
						required
					/>
				</div>

				<div>
					<label for="email" class="block text-sm font-medium text-gray-700 mb-1">
						Email
					</label>
					<input
						type="email"
						id="email"
						bind:value={email}
						placeholder="you@example.com"
						class="input-field"
						disabled={isLoading}
						required
					/>
				</div>

				<div>
					<label for="password" class="block text-sm font-medium text-gray-700 mb-1">
						Password
					</label>
					<input
						type="password"
						id="password"
						bind:value={password}
						placeholder="••••••••"
						class="input-field"
						disabled={isLoading}
						required
					/>
					<p class="text-xs text-gray-500 mt-1">At least 6 characters</p>
				</div>

				<button
					type="submit"
					disabled={isLoading}
					class="btn-primary w-full disabled:opacity-50"
				>
					{isLoading ? 'Creating account...' : 'Create Account'}
				</button>
			</form>

			<p class="text-center text-sm text-gray-600 mt-6">
				Already have an account? <a href="/auth/login" class="text-amber-400 hover:text-amber-500 font-semibold">
					Sign in
				</a>
			</p>
		</div>
	</div>
</div>
