import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Forum',
    description: 'Discuss topics and share knowledge with the community.',
};

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    return children;
}
