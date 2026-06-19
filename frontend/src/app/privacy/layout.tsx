import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Privacy Policy',
    description: 'Learn about our privacy practices and how we protect your information.',
};

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    return children;
}
