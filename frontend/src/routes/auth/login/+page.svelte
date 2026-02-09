<script>
	import { goto } from '$app/navigation';
	import { userStore } from '$lib/stores';
	import { signInWithGoogle, signInWithEmail } from '$lib/firebase';

	let email = '';
	let password = '';
	let isLoading = false;
	let errorMessage = '';
	let showPassword = false;

	async function handleGoogleSignIn() {
		isLoading = true;
		try {
			const result = await signInWithGoogle();
			if (result.user) {
				userStore.set(result.user);
				await goto('/dashboard');
			}
		} catch (error) {
			errorMessage = error.message;
		}
		isLoading = false;
	}

	async function handleEmailSignIn() {
		isLoading = true;
		errorMessage = '';

		if (!email || !password) {
			errorMessage = 'Please enter email and password';
			isLoading = false;
			return;
		}

		try {
			const result = await signInWithEmail(email, password);
			if (result.user) {
				userStore.set(result.user);
				const token = await result.user.getIdToken();
				localStorage.setItem('firebaseToken', token);
				await goto('/dashboard');
			}
		} catch (error) {
			errorMessage = error.message;
		}
		isLoading = false;
	}

	function togglePasswordVisibility() {
		showPassword = !showPassword;
	}
</script>

<svelte:head>
	<title>Login - Fashion Studio</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center px-4">
	<div class="w-full max-w-md">
		<div class="card">
			<h1 class="text-3xl font-bold text-gray-900 mb-8 text-center">Welcome to Studio</h1>

			{#if errorMessage}
				<div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
					<p class="text-red-700 text-sm">{errorMessage}</p>
				</div>
			{/if}

			<!-- Google Sign In -->
			<button
				on:click={handleGoogleSignIn}
				disabled={isLoading}
				class="w-full mb-4 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition disabled:opacity-50"
			>
				{#if isLoading}
					<span>Processing...</span>
				{:else}
					<span class="flex items-center justify-center gap-2">
						<svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
							<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
							<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
							<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
							<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
						</svg>
						Sign in with Google
					</span>
				{/if}
			</button>

			<div class="relative mb-6">
				<div class="absolute inset-0 flex items-center">
					<div class="w-full border-t border-gray-300"></div>
				</div>
				<div class="relative flex justify-center text-sm">
					<span class="px-2 bg-white text-gray-500">Or continue with email</span>
				</div>
			</div>

			<!-- Email Sign In -->
			<form on:submit|preventDefault={handleEmailSignIn} class="space-y-4">
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
					<div class="relative">
						<input
							type={showPassword ? 'text' : 'password'}
							id="password"
							bind:value={password}
							placeholder="••••••••"
							class="input-field"
							disabled={isLoading}
							required
						/>
						<button
							type="button"
							on:click={togglePasswordVisibility}
							class="absolute right-3 top-2 text-gray-500 hover:text-gray-700"
						>
							{showPassword ? '👁️‍🗨️' : '👁️'}
						</button>
					</div>
				</div>

				<button
					type="submit"
					disabled={isLoading}
					class="btn-primary w-full disabled:opacity-50"
				>
					{isLoading ? 'Signing in...' : 'Sign in with Email'}
				</button>
			</form>

			<p class="text-center text-sm text-gray-600 mt-6">
				Don't have an account? <a href="/register" class="text-amber-400 hover:text-amber-500 font-semibold">
					Sign up
				</a>
			</p>
		</div>

		<p class="text-center text-gray-400 text-sm mt-6">
			Or <a href="/create-shoot" class="text-amber-400 hover:text-amber-500">try free (3 images)</a> without logging in
		</p>
	</div>
</div>
