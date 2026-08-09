import { adminAuth } from './firebase.server';

export interface UserSession {
  uid: string;
  email?: string;
  email_verified?: boolean;
}

export class AuthModel {
  /**
   * Verifies a Firebase session cookie and returns the user's decoded claims.
   * @param sessionCookie The session cookie string
   */
  static async verifySession(sessionCookie: string): Promise<UserSession | null> {
    try {
      const decodedClaims = await adminAuth.verifySessionCookie(sessionCookie, true);
      return {
        uid: decodedClaims.uid,
        email: decodedClaims.email,
        email_verified: decodedClaims.email_verified,
      };
    } catch (error) {
      console.error('Session verification failed:', error);
      return null;
    }
  }

  /**
   * Creates a session cookie from an ID token.
   * @param idToken The client-provided ID token
   * @param expiresIn Expiration time in milliseconds (e.g. 5 days)
   */
  static async createSessionCookie(idToken: string, expiresIn: number): Promise<string> {
    return await adminAuth.createSessionCookie(idToken, { expiresIn });
  }

  /**
   * Revokes all sessions for a specific user.
   * @param uid The user ID
   */
  static async revokeRefreshTokens(uid: string): Promise<void> {
    await adminAuth.revokeRefreshTokens(uid);
  }
}
