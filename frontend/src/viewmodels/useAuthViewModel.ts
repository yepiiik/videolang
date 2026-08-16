import { useState, useEffect } from 'react';
import { 
  signInWithPopup, 
  GoogleAuthProvider, 
  signOut as firebaseSignOut,
  onAuthStateChanged,
  User,
  signInWithEmailAndPassword as firebaseSignInWithEmail,
  createUserWithEmailAndPassword as firebaseSignUpWithEmail,
  updateProfile
} from 'firebase/auth';
import { auth } from '@/models/firebase.client';

export function useAuthViewModel() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setIsLoading(false);
    });
    return () => unsubscribe();
  }, []);

  const establishServerSession = async (idToken: string) => {
    const res = await fetch('/api/auth/session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${idToken}`,
      },
    });

    if (!res.ok) {
      throw new Error('Failed to establish server session');
    }
  };

  const handleAuthAction = async (action: () => Promise<{ user: User }>) => {
    try {
      setIsLoading(true);
      setError(null);
      const userCredential = await action();
      const idToken = await userCredential.user.getIdToken(true);
      await establishServerSession(idToken);
    } catch (err: unknown) {
      console.error("Auth action failed", err);
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      await firebaseSignOut(auth);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const signInWithGoogle = () => {
    const provider = new GoogleAuthProvider();
    return handleAuthAction(() => signInWithPopup(auth, provider));
  };

  const signInWithEmail = (email: string, password: string) => {
    return handleAuthAction(() => firebaseSignInWithEmail(auth, email, password));
  };

  const signUpWithEmail = (email: string, password: string) => {
    return handleAuthAction(async () => {
      const cred = await firebaseSignUpWithEmail(auth, email, password);
      return cred;
    });
  };

  const signOut = async () => {
    try {
      setIsLoading(true);
      await firebaseSignOut(auth);
      
      // Clear session cookie on the server
      await fetch('/api/auth/session', { method: 'DELETE' });
    } catch (err: unknown) {
      console.error("Logout failed", err);
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    user,
    isLoading,
    error,
    signInWithGoogle,
    signInWithEmail,
    signUpWithEmail,
    signOut,
  };
}
