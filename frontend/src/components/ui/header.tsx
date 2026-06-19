import React from 'react'
import Link from 'next/link'
import Input from '@/components/ui/input'

const Header = () => {
  return (
    <header>
        <div className='flex justify-between items-center p-4'>
            <div>
                <Link href="/">
                    <h1>Ucontext</h1>
                </Link>
            </div>
            <div>
                <Input />
            </div>
            <div>
                <Link href="/signin">
                    Sign In
                </Link>
            </div>
        </div>
    </header>
  )
}

export default Header