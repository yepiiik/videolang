"use client";

import { useState } from "react";
import { Mail, MapPin, MessageSquare, ArrowRight } from "lucide-react";

export default function ContactPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSuccess(true);
      
      // Reset success state after a few seconds
      setTimeout(() => setIsSuccess(false), 5000);
    }, 1200);
  };

  return (
    <div className="flex flex-col min-h-[calc(100vh-4rem)]">
      {/* Hero Section */}
      <section className="bg-background pt-24 pb-12 px-6 md:px-12 text-center">
        <div className="max-w-3xl mx-auto space-y-6">
          <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary mb-4">
            <MessageSquare className="w-4 h-4 mr-2" />
            We&apos;re here to help
          </div>
          <h1 className="text-5xl md:text-7xl font-black tracking-tighter">Get in Touch</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Have questions about pricing, API access, or enterprise solutions? Send us a message and our team will get back to you within 24 hours.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section className="flex-1 px-6 md:px-12 pb-24">
        <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-24 items-start">
          
          {/* Contact Information */}
          <div className="space-y-12">
            <div>
              <h2 className="text-3xl font-extrabold mb-6">Contact Information</h2>
              <p className="text-muted-foreground mb-8 text-lg">
                Prefer to reach out directly? Use the information below to contact the right department.
              </p>
            </div>
            
            <div className="space-y-8">
              <div className="flex items-start space-x-4 p-6 rounded-2xl bg-muted/20 border transition-colors hover:bg-muted/40">
                <div className="bg-primary/10 p-3 rounded-xl">
                  <Mail className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h4 className="font-bold text-lg">Sales & Support</h4>
                  <p className="text-muted-foreground mt-1">hello@ucontext.com</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-4 p-6 rounded-2xl bg-muted/20 border transition-colors hover:bg-muted/40">
                <div className="bg-primary/10 p-3 rounded-xl">
                  <MapPin className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h4 className="font-bold text-lg">Headquarters</h4>
                  <p className="text-muted-foreground mt-1">
                    123 Innovation Drive<br />
                    San Francisco, CA 94103<br />
                    United States
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div className="bg-card border-2 rounded-3xl p-8 shadow-xl">
            {isSuccess ? (
              <div className="flex flex-col items-center justify-center text-center py-12 space-y-4 h-full min-h-[400px]">
                <div className="w-16 h-16 bg-green-500/20 text-green-500 rounded-full flex items-center justify-center mb-4 border-2 border-green-500">
                  <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold">Message Sent!</h3>
                <p className="text-muted-foreground">Thank you for reaching out. We will get back to you shortly.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                <h3 className="text-2xl font-bold mb-6">Send a Message</h3>
                
                <div className="space-y-2">
                  <label htmlFor="name" className="text-sm font-semibold">Full Name</label>
                  <input 
                    id="name"
                    type="text" 
                    required 
                    className="w-full px-4 py-3.5 bg-muted/50 border-2 border-transparent focus:border-primary focus:bg-background outline-none rounded-xl transition-all"
                    placeholder="John Doe"
                  />
                </div>
                
                <div className="space-y-2">
                  <label htmlFor="email" className="text-sm font-semibold">Email Address</label>
                  <input 
                    id="email"
                    type="email" 
                    required 
                    className="w-full px-4 py-3.5 bg-muted/50 border-2 border-transparent focus:border-primary focus:bg-background outline-none rounded-xl transition-all"
                    placeholder="name@example.com"
                  />
                </div>
                
                <div className="space-y-2">
                  <label htmlFor="message" className="text-sm font-semibold">Your Message</label>
                  <textarea 
                    id="message"
                    required 
                    rows={5}
                    className="w-full px-4 py-3.5 bg-muted/50 border-2 border-transparent focus:border-primary focus:bg-background outline-none rounded-xl transition-all resize-none"
                    placeholder="How can we help you?"
                  />
                </div>
                
                <button 
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full flex items-center justify-center font-bold text-primary-foreground bg-foreground hover:bg-foreground/90 transition-all shadow-md py-4 mt-4 rounded-xl disabled:opacity-50"
                >
                  {isSubmitting ? (
                    <div className="flex items-center space-x-2">
                      <div className="w-5 h-5 border-2 border-background/30 border-t-background rounded-full animate-spin" />
                      <span>Sending...</span>
                    </div>
                  ) : (
                    <>
                      Send Message
                      <ArrowRight className="ml-2 w-4 h-4" />
                    </>
                  )}
                </button>
              </form>
            )}
          </div>

        </div>
      </section>
    </div>
  );
}
