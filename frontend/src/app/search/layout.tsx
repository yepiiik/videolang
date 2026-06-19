import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Search Results',
    description: 'View search results and find the information you need.',
};

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    return children;
}
