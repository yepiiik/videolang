import React from 'react'

const Input = () => {
  return (
    <input
      type="text"
      placeholder="Search for videos, topics, or questions..."
      className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  )
}

export default Input