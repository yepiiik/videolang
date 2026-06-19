import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Sign In',
    description: 'Access your account to view and manage your profile information.',
};

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    return children;
}
