import { writable } from 'svelte/store';

export const userStore = writable(null);
export const creditsStore = writable(0);
export const loadingStore = writable(false);
