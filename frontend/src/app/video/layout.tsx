import { Metadata } from 'next';

export const metadata: Metadata = {
    title: 'Video',
    description: 'Detailed information about the video and its captions.',
};

export default function Layout({
    children,
}: {
    children: React.ReactNode;
}) {
    return children;
}
