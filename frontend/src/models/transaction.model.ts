import { adminDb } from './firebase.server';
import { FieldValue } from 'firebase-admin/firestore';

export interface TransactionData {
  id: string;
  amount: number | string; // Can be a number or formatted string like "+$20.00"
  description: string;
  method: string;
  status: string;
  date: string | any;
}

export class TransactionModel {
  /**
   * Records a new transaction for a user.
   */
  static async createTransaction(uid: string, data: Omit<TransactionData, 'id' | 'date'>): Promise<TransactionData> {
    const transactionsRef = adminDb.collection('users').doc(uid).collection('transactions');
    const newTxRef = transactionsRef.doc();
    
    const newTxData = {
      ...data,
      date: FieldValue.serverTimestamp(),
    };

    await newTxRef.set(newTxData);

    return {
      id: newTxRef.id,
      amount: data.amount,
      description: data.description,
      method: data.method,
      status: data.status,
      date: new Date().toISOString(),
    } as TransactionData;
  }

  /**
   * Fetches the transaction history for a given user.
   */
  static async getTransactions(uid: string): Promise<TransactionData[]> {
    const snapshot = await adminDb.collection('users').doc(uid).collection('transactions').orderBy('date', 'desc').get();
    
    return snapshot.docs.map(doc => {
      const data = doc.data();
      return {
        id: doc.id,
        ...data,
        date: data.date?.toDate?.()?.toISOString() || null,
      };
    }) as TransactionData[];
  }
}
