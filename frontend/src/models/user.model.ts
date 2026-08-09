import { adminDb } from './firebase.server';
import { FieldValue } from 'firebase-admin/firestore';

export interface UserData {
  uid: string;
  email?: string;
  name?: string;
  picture?: string;
  createdAt?: string | any; // 'any' allows FieldValue during write
  lastLoginAt?: string | any;
  currentPlan?: string;
  walletBalance?: number;
  scheduledPlan?: string | null;
}

export class UserModel {
  private static collection = 'users';

  /**
   * Upserts a user in Firestore. Should be called on sign in/up.
   */
  static async upsertUser(userData: UserData): Promise<void> {
    if (!process.env.FIREBASE_PRIVATE_KEY) {
      console.warn('Skipping Firestore upsert because FIREBASE_PRIVATE_KEY is not configured.');
      return;
    }

    try {
      const userRef = adminDb.collection(this.collection).doc(userData.uid);
      
      const updateData = {
        email: userData.email,
        name: userData.name,
        picture: userData.picture,
        lastLoginAt: FieldValue.serverTimestamp(),
      };

      // Remove undefined fields to avoid Firestore errors
      const cleanData = Object.fromEntries(
        Object.entries(updateData).filter(([_, v]) => v !== undefined)
      );

      const doc = await userRef.get();
      if (!doc.exists) {
        await userRef.set({
          ...cleanData,
          createdAt: FieldValue.serverTimestamp(),
          currentPlan: 'Free',
          walletBalance: 0,
          scheduledPlan: null,
        });
      } else {
        await userRef.set(cleanData, { merge: true });
      }
    } catch (error) {
      console.error('Error upserting user in Firestore:', error);
      throw new Error('Failed to save user data');
    }
  }

  /**
   * Updates billing specific fields for a user.
   */
  static async updateBilling(uid: string, data: { currentPlan?: string, walletBalance?: number, scheduledPlan?: string | null }): Promise<void> {
    const userRef = adminDb.collection(this.collection).doc(uid);
    await userRef.update(data);
  }

  /**
   * Fetches a user from Firestore by UID.
   */
  static async getUser(uid: string): Promise<UserData | null> {
    try {
      const doc = await adminDb.collection(this.collection).doc(uid).get();
      if (!doc.exists) {
        return null;
      }
      const data = doc.data();
      return { 
        uid, 
        ...data,
        createdAt: data?.createdAt?.toDate?.()?.toISOString() || null,
        lastLoginAt: data?.lastLoginAt?.toDate?.()?.toISOString() || null,
      } as UserData;
    } catch (error) {
      console.error('Error fetching user from Firestore:', error);
      return null;
    }
  }
}
