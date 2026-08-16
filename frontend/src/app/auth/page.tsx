"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight } from "lucide-react";
import Image from "next/image";
import { useAuthViewModel } from "@/viewmodels/useAuthViewModel";
import { sendVerificationCode, verifyAuthCode } from "@/app/actions/auth.actions";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [signUpStep, setSignUpStep] = useState(1);
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [customError, setCustomError] = useState<string | null>(null);
  const router = useRouter();
  const { signInWithGoogle, signInWithEmail, signUpWithEmail, isLoading: isLoadingAuth, error: authError } = useAuthViewModel();

  // Combine local errors with auth model errors
  const error = customError || authError;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setCustomError(null);
    
    try {
      if (isLogin) {
        await signInWithEmail(email, password);
        router.push("/profile");
      } else {
        if (signUpStep === 1) {
          await sendVerificationCode(email);
          setSignUpStep(2);
        } else if (signUpStep === 2) {
          await verifyAuthCode(email, code);
          setSignUpStep(3);
        } else if (signUpStep === 3) {
          await signUpWithEmail(email, password);
          router.push("/profile");
        }
      }
    } catch (err: any) {
      setCustomError(err.message || "An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-[calc(100vh-4rem)] items-center justify-center p-4">
      <div className="w-full max-w-md p-8 bg-card border rounded-3xl shadow-xl">
        <div className="flex flex-col items-center text-center space-y-4 mb-8">
          <div className="bg-primary/10 p-3 rounded-2xl mb-2">
            <Image src="/usearch.svg" alt="uSearch Logo" width={32} height={32} className="h-8 w-auto" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight">
            {isLogin ? "Welcome back" : "Create an account"}
          </h1>
          <p className="text-muted-foreground text-sm">
            {isLogin ? "Enter your credentials to access your dashboard" : "Get started with the fastest caption search API"}
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-500 text-sm text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {(isLogin || signUpStep === 1) && (
            <div className="space-y-2">
              <label className="text-sm font-semibold">Email</label>
              <input 
                type="email" 
                required 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={!isLogin && signUpStep !== 1}
                className="w-full px-4 py-3 bg-muted/50 border-2 border-transparent focus:border-primary focus:bg-background outline-none rounded-xl transition-all disabled:opacity-50"
                placeholder="name@example.com"
              />
            </div>
          )}

          {!isLogin && signUpStep === 2 && (
            <div className="space-y-2 animate-in fade-in slide-in-from-bottom-2">
              <label className="text-sm font-semibold">Verification Code</label>
              <p className="text-xs text-muted-foreground mb-2">We sent a 6-digit code to {email}</p>
              <input 
                type="text" 
                required 
                maxLength={6}
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full px-4 py-3 bg-muted/50 border-2 border-transparent focus:border-primary focus:bg-background outline-none rounded-xl transition-all tracking-[0.5em] font-mono text-center text-xl"
                placeholder="000000"
              />
            </div>
          )}

          {(isLogin || signUpStep === 3) && (
            <div className="space-y-2 animate-in fade-in slide-in-from-bottom-2">
              <div className="flex items-center justify-between">
                <label className="text-sm font-semibold">{isLogin ? "Password" : "Create Password"}</label>
                {isLogin && <a href="#" className="text-xs text-primary font-medium hover:underline">Forgot password?</a>}
              </div>
              <input 
                type="password" 
                required 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-muted/50 border-2 border-transparent focus:border-primary focus:bg-background outline-none rounded-xl transition-all"
                placeholder="••••••••"
              />
            </div>
          )}

          <button 
            type="submit"
            disabled={isLoading || isLoadingAuth}
            className="w-full flex items-center justify-center font-bold text-primary-foreground bg-foreground hover:bg-foreground/90 transition-all shadow-md py-3.5 mt-6 rounded-xl disabled:opacity-50"
          >
            {(isLoading || isLoadingAuth) ? (
              <div className="w-5 h-5 border-2 border-background/30 border-t-background rounded-full animate-spin" />
            ) : (
              <>
                {isLogin 
                  ? "Sign In" 
                  : signUpStep === 1 
                    ? "Continue with Email" 
                    : signUpStep === 2 
                      ? "Verify Code" 
                      : "Create Account"
                }
                <ArrowRight className="ml-2 w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-muted-foreground/20" />
          </div>
          <div className="relative flex justify-center text-xs uppercase font-bold">
            <span className="bg-card px-2 text-muted-foreground">Or continue with</span>
          </div>
        </div>

        <button 
          type="button"
          disabled={isLoadingAuth}
          onClick={async () => {
            await signInWithGoogle();
            if (!error) {
              router.push("/profile");
            }
          }}
          className="w-full flex items-center justify-center font-bold text-foreground bg-background hover:bg-muted border-2 border-muted transition-all shadow-sm py-3.5 rounded-xl disabled:opacity-50"
        >
          <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
          </svg>
          Google
        </button>

        <div className="mt-6 flex items-center justify-center space-x-2 text-sm text-muted-foreground">
          <span>{isLogin ? "Don't have an account?" : "Already have an account?"}</span>
          <button 
            onClick={() => {
              setIsLogin(!isLogin);
              setSignUpStep(1);
              setCustomError(null);
            }} 
            className="text-foreground font-bold hover:underline"
          >
            {isLogin ? "Sign Up" : "Sign In"}
          </button>
        </div>
      </div>
    </div>
  );
}
