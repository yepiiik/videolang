import { adminDb } from './firebase.server';
import { FieldValue } from 'firebase-admin/firestore';

export interface ApiKeyData {
  id: string;
  name: string;
  key: string;
  createdAt: string | any;
  lastUsedAt: string | any;
}

export class ApiKeyModel {
  /**
   * Generates a new API key for a user and saves it to Firestore.
   */
  static async createApiKey(uid: string, name: string): Promise<ApiKeyData> {
    const apiKeysRef = adminDb.collection('users').doc(uid).collection('apiKeys');
    
    // Generate a random key string
    const rawSecret = `sk_live_${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`;
    
    const newKeyRef = apiKeysRef.doc();
    const newKeyData = {
      name,
      key: rawSecret,
      createdAt: FieldValue.serverTimestamp(),
      lastUsedAt: null,
    };

    await newKeyRef.set(newKeyData);

    return {
      id: newKeyRef.id,
      name,
      key: rawSecret,
      createdAt: new Date().toISOString(),
      lastUsedAt: null,
    } as ApiKeyData;
  }

  /**
   * Fetches all API keys for a given user.
   */
  static async getApiKeys(uid: string): Promise<ApiKeyData[]> {
    const snapshot = await adminDb.collection('users').doc(uid).collection('apiKeys').orderBy('createdAt', 'desc').get();
    
    return snapshot.docs.map(doc => {
      const data = doc.data();
      return {
        id: doc.id,
        ...data,
        createdAt: data.createdAt?.toDate?.()?.toISOString() || null,
        lastUsedAt: data.lastUsedAt?.toDate?.()?.toISOString() || null,
      };
    }) as ApiKeyData[];
  }

  /**
   * Deletes a specific API key.
   */
  static async deleteApiKey(uid: string, keyId: string): Promise<void> {
    await adminDb.collection('users').doc(uid).collection('apiKeys').doc(keyId).delete();
  }
}
