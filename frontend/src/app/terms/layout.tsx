import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Terms of Service',
    description: 'Learn about our terms of service and how they affect your use of our platform.',
};

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    return children;
}
