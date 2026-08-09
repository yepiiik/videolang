import { NextRequest, NextResponse } from 'next/server';
import { AuthModel } from '@/models/auth.model';
import { adminAuth } from '@/models/firebase.server';
import { UserModel } from '@/models/user.model';

export async function POST(request: NextRequest) {
  try {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader?.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'Missing or invalid token' }, { status: 401 });
    }

    const idToken = authHeader.split('Bearer ')[1];
    
    // Decode token to get user info
    const decodedToken = await adminAuth.verifyIdToken(idToken);
    
    // Upsert user to Firestore
    await UserModel.upsertUser({
      uid: decodedToken.uid,
      email: decodedToken.email,
      name: decodedToken.name,
      picture: decodedToken.picture,
    });

    // Set session expiration to 5 days
    const expiresIn = 60 * 60 * 24 * 5 * 1000;
    
    // Create the session cookie via Firebase Admin
    const sessionCookie = await AuthModel.createSessionCookie(idToken, expiresIn);
    
    const response = NextResponse.json({ success: true }, { status: 200 });
    
    // Set cookie
    response.cookies.set('session', sessionCookie, {
      maxAge: expiresIn / 1000,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      path: '/',
    });

    return response;
  } catch (error: any) {
    console.error('Session creation error:', error);
    return NextResponse.json({ error: 'Unauthorized request' }, { status: 401 });
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const sessionCookie = request.cookies.get('session')?.value;
    
    if (sessionCookie) {
      // Verify and revoke token to force re-authentication on all devices
      const decodedClaims = await AuthModel.verifySession(sessionCookie);
      if (decodedClaims) {
        await AuthModel.revokeRefreshTokens(decodedClaims.uid);
      }
    }
    
    const response = NextResponse.json({ success: true }, { status: 200 });
    response.cookies.delete('session');
    
    return response;
  } catch (error) {
    console.error('Session deletion error:', error);
    // Even if it fails server-side (e.g. invalid cookie), delete it client-side
    const response = NextResponse.json({ success: true }, { status: 200 });
    response.cookies.delete('session');
    return response;
  }
}
