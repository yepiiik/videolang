import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Profile',
    description: 'View and manage your profile information.',
};

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    return children;
}
