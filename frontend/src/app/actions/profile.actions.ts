'use server';

import { cookies } from 'next/headers';
import { AuthModel } from '@/models/auth.model';
import { UserModel } from '@/models/user.model';
import { ApiKeyModel } from '@/models/api-key.model';
import { TransactionModel } from '@/models/transaction.model';

async function getUid(): Promise<string> {
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get('session')?.value;
  if (!sessionCookie) throw new Error('Unauthorized');
  const session = await AuthModel.verifySession(sessionCookie);
  if (!session) throw new Error('Unauthorized');
  return session.uid;
}

export async function getProfileData() {
  const uid = await getUid();
  const [user, apiKeys, transactions] = await Promise.all([
    UserModel.getUser(uid),
    ApiKeyModel.getApiKeys(uid),
    TransactionModel.getTransactions(uid),
  ]);
  
  if (!user) throw new Error('User profile not found');
  
  return { user, apiKeys, transactions };
}

export async function generateApiKey(name: string) {
  const uid = await getUid();
  return await ApiKeyModel.createApiKey(uid, name);
}

export async function removeApiKey(keyId: string) {
  const uid = await getUid();
  await ApiKeyModel.deleteApiKey(uid, keyId);
}

export async function schedulePlan(newPlan: string, price: string, method: string) {
  const uid = await getUid();
  await UserModel.updateBilling(uid, {
    scheduledPlan: newPlan,
  });
  await TransactionModel.createTransaction(uid, {
    amount: price,
    description: `Subscription scheduled: ${newPlan}`,
    method,
    status: 'Pending',
  });
}

export async function applyScheduledPlan() {
  const uid = await getUid();
  const user = await UserModel.getUser(uid);
  if (!user || !user.scheduledPlan) return;

  await UserModel.updateBilling(uid, {
    currentPlan: user.scheduledPlan,
    scheduledPlan: null,
  });
  
  await TransactionModel.createTransaction(uid, {
    amount: '$0',
    description: `Applied scheduled plan: ${user.scheduledPlan}`,
    method: 'System',
    status: 'Completed',
  });
}

export async function depositFunds(amount: number, method: string) {
  const uid = await getUid();
  const user = await UserModel.getUser(uid);
  if (!user) throw new Error('User not found');

  const newBalance = (user.walletBalance || 0) + amount;
  await UserModel.updateBilling(uid, { walletBalance: newBalance });

  await TransactionModel.createTransaction(uid, {
    amount: `+$${amount}.00`,
    description: `Wallet Deposit`,
    method,
    status: 'Completed',
  });
}
