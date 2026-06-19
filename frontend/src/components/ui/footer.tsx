import React from 'react'
import Link from 'next/link'

const Footer = () => {
  return (
    <footer>
        <div className='flex justify-between items-center p-4'>
            <div>
                <p>&copy; {new Date().getFullYear()} Ucontext. All rights reserved.</p>
            </div>
            <nav>
                <ul>
                    <li>
                        <Link href="/terms">Terms of Service</Link>
                    </li>
                    <li>
                        <Link href="/privacy">Privacy Policy</Link>
                    </li>
                </ul>
            </nav>
        </div>
    </footer>
  )
}

export default Footer