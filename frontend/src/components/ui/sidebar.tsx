import React from 'react'
import Link from 'next/link'

const Sidebar = () => {
    return (
        <aside className='flex flex-col flex-1 max-w-48 p-4'>
            <nav>
                <ul>
                    <li><Link href="/">Home</Link></li>
                    <li><Link href="/forum">Forum</Link></li>
                    <li><Link href="/pricing">Pricing</Link></li>
                </ul>
            </nav>
        </aside>
    )
}

export default Sidebar