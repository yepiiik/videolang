'use server';

import { sendEmail } from "@/lib/ses";

export async function submitContactForm(name: string, email: string, message: string) {
  const contactInbox = process.env.AWS_SES_CONTACT_INBOX;
  
  if (!contactInbox) {
    console.error("AWS_SES_CONTACT_INBOX is not configured");
    throw new Error("Server configuration error. Contact support.");
  }

  const subject = `New Contact Form Submission from ${name}`;
  const htmlBody = `
    <h2>New Message from uSearch Contact Form</h2>
    <p><strong>Name:</strong> ${name}</p>
    <p><strong>Email:</strong> ${email}</p>
    <br/>
    <p><strong>Message:</strong></p>
    <p>${message.replace(/\n/g, '<br/>')}</p>
  `;

  await sendEmail({
    to: contactInbox,
    subject,
    htmlBody,
  });
}
