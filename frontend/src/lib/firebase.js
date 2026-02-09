import { initializeApp } from 'firebase/app';
import {
	getAuth,
	signInWithPopup,
	GoogleAuthProvider,
	createUserWithEmailAndPassword,
	signInWithEmailAndPassword,
	updateProfile,
	signOut
} from 'firebase/auth';

// Firebase configuration
const firebaseConfig = {
	apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
	authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
	projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
	storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
	messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
	appId: import.meta.env.VITE_FIREBASE_APP_ID
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export async function signInWithGoogle() {
	const provider = new GoogleAuthProvider();
	try {
		const result = await signInWithPopup(auth, provider);
		const token = await result.user.getIdToken();
		localStorage.setItem('firebaseToken', token);
		return result;
	} catch (error) {
		throw new Error(error.message);
	}
}

export async function signUpWithEmail(email, password, displayName) {
	try {
		const result = await createUserWithEmailAndPassword(auth, email, password);
		await updateProfile(result.user, { displayName });
		const token = await result.user.getIdToken();
		localStorage.setItem('firebaseToken', token);
		return result;
	} catch (error) {
		throw new Error(error.message);
	}
}

export async function signInWithEmail(email, password) {
	try {
		const result = await signInWithEmailAndPassword(auth, email, password);
		const token = await result.user.getIdToken();
		localStorage.setItem('firebaseToken', token);
		return result;
	} catch (error) {
		throw new Error(error.message);
	}
}

export async function logout() {
	try {
		await signOut(auth);
		localStorage.removeItem('firebaseToken');
	} catch (error) {
		throw new Error(error.message);
	}
}

export function getCurrentUser() {
	return auth.currentUser;
}
