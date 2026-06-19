import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Pricing',
    description: 'View our pricing plans and choose the best option for your needs.',
};

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    return children;
}
