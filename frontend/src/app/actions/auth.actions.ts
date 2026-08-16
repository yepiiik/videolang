'use server';

import { adminDb } from "@/models/firebase.server";
import { sendEmail } from "@/lib/ses";

/**
 * Generates a 6 digit code, saves it to Firestore with a 15 min expiry, and emails it.
 */
export async function sendVerificationCode(email: string) {
  if (!email) throw new Error("Email is required");

  // 1. Generate 6 digit code
  const code = Math.floor(100000 + Math.random() * 900000).toString();
  
  // 2. Calculate expiration (15 mins from now)
  const expiresAt = new Date(Date.now() + 15 * 60000);

  // 3. Save to Firestore (using email as doc ID to overwrite previous codes for this email)
  await adminDb.collection("verification_codes").doc(email).set({
    code,
    expiresAt,
    verified: false,
    createdAt: new Date(),
  });

  // 4. Send via SES
  const subject = "Your uSearch Verification Code";
  const htmlBody = `
    <div style="font-family: sans-serif; max-w: 600px; margin: 0 auto;">
      <h2>Verify your email address</h2>
      <p>Your verification code for uSearch is:</p>
      <h1 style="font-size: 32px; letter-spacing: 4px; background: #f4f4f5; padding: 16px; border-radius: 8px; text-align: center;">
        ${code}
      </h1>
      <p>This code will expire in 15 minutes.</p>
    </div>
  `;

  await sendEmail({
    to: email,
    subject,
    htmlBody,
  });

  return { success: true };
}

/**
 * Verifies the code in Firestore. If correct, marks it as verified.
 */
export async function verifyAuthCode(email: string, code: string) {
  if (!email || !code) throw new Error("Email and code are required");

  const docRef = adminDb.collection("verification_codes").doc(email);
  const doc = await docRef.get();

  if (!doc.exists) {
    throw new Error("No verification code found for this email. Please request a new one.");
  }

  const data = doc.data()!;
  
  // Check expiration
  if (data.expiresAt.toDate() < new Date()) {
    throw new Error("Verification code has expired. Please request a new one.");
  }

  // Check code match
  if (data.code !== code) {
    throw new Error("Incorrect verification code.");
  }

  // Mark as verified so we can optionally check it later if we want strict server enforcement
  await docRef.update({
    verified: true,
  });

  return { success: true };
}
